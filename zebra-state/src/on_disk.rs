//! The primary implementation of the `zebra_state::Service` built upon sled
use super::{Request, Response};
use crate::Config;
use futures::prelude::*;
use std::sync::Arc;
use std::{
    error,
    future::Future,
    pin::Pin,
    task::{Context, Poll},
};
use tower::{buffer::Buffer, Service};
use zebra_chain::serialization::{ZcashDeserialize, ZcashSerialize};
use zebra_chain::{
    block::{Block, BlockHeaderHash},
    types::BlockHeight,
};

#[derive(Clone)]
struct SledState {
    storage: sled::Db,
}

impl SledState {
    pub(crate) fn new(config: &Config) -> Self {
        let config = config.sled_config();

        Self {
            storage: config.open().unwrap(),
        }
    }

    pub(super) fn insert(
        &mut self,
        block: impl Into<Arc<Block>>,
    ) -> Result<BlockHeaderHash, Error> {
        let block = block.into();
        let hash: BlockHeaderHash = block.as_ref().into();
        let height = block.coinbase_height().unwrap();

        let height_map = self.storage.open_tree(b"height_map")?;
        let by_hash = self.storage.open_tree(b"by_hash")?;

        let mut bytes = Vec::new();
        block.zcash_serialize(&mut bytes)?;

        // TODO(jlusby): make this transactional
        height_map.insert(&height.0.to_be_bytes(), &hash.0)?;
        by_hash.insert(&hash.0, bytes)?;

        Ok(hash)
    }

    pub(super) fn get(&self, hash: BlockHeaderHash) -> Result<Option<Arc<Block>>, Error> {
        let by_hash = self.storage.open_tree(b"by_hash")?;
        let key = &hash.0;
        let value = by_hash.get(key)?;

        if let Some(bytes) = value {
            let bytes = bytes.as_ref();
            let block = ZcashDeserialize::zcash_deserialize(bytes)?;
            Ok(Some(block))
        } else {
            Ok(None)
        }
    }

    pub(super) fn get_main_chain_at(
        &self,
        height: BlockHeight,
    ) -> Result<Option<BlockHeaderHash>, Error> {
        let height_map = self.storage.open_tree(b"height_map")?;
        let key = height.0.to_be_bytes();
        let value = height_map.get(key)?;

        if let Some(bytes) = value {
            let bytes = bytes.as_ref();
            let hash = ZcashDeserialize::zcash_deserialize(bytes)?;
            Ok(Some(hash))
        } else {
            Ok(None)
        }
    }

    pub(super) fn get_tip(&self) -> Result<Option<Arc<Block>>, Error> {
        let tree = self.storage.open_tree(b"height_map")?;
        let last_entry = tree.iter().values().next_back();

        match last_entry {
            Some(Ok(bytes)) => Ok(Some(ZcashDeserialize::zcash_deserialize(bytes.as_ref())?)),
            Some(Err(e)) => Err(e)?,
            None => Ok(None),
        }
    }

    fn contains(&self, hash: &BlockHeaderHash) -> Result<bool, Error> {
        let by_hash = self.storage.open_tree(b"by_hash")?;
        let key = &hash.0;

        Ok(by_hash.contains_key(key)?)
    }
}

impl Default for SledState {
    fn default() -> Self {
        let config = crate::Config::default();
        Self::new(&config)
    }
}

impl Service<Request> for SledState {
    type Response = Response;
    type Error = Error;
    type Future =
        Pin<Box<dyn Future<Output = Result<Self::Response, Self::Error>> + Send + 'static>>;

    fn poll_ready(&mut self, _: &mut Context<'_>) -> Poll<Result<(), Self::Error>> {
        Poll::Ready(Ok(()))
    }

    fn call(&mut self, req: Request) -> Self::Future {
        match req {
            Request::AddBlock { block } => {
                let mut storage = self.clone();

                async move { storage.insert(block).map(|hash| Response::Added { hash }) }.boxed()
            }
            Request::GetBlock { hash } => {
                let storage = self.clone();
                async move {
                    storage
                        .get(hash)?
                        .map(|block| Response::Block { block })
                        .ok_or_else(|| "block could not be found".into())
                }
                .boxed()
            }
            Request::GetTip => {
                let storage = self.clone();
                async move {
                    storage
                        .get_tip()?
                        .map(|block| block.as_ref().into())
                        .map(|hash| Response::Tip { hash })
                        .ok_or_else(|| "zebra-state contains no blocks".into())
                }
                .boxed()
            }
            Request::GetDepth { hash } => {
                let storage = self.clone();

                async move {
                    if !storage.contains(&hash)? {
                        return Ok(Response::Depth(None));
                    }

                    let block = storage
                        .get(hash)?
                        .expect("block must be present if contains returned true");
                    let tip = storage
                        .get_tip()?
                        .expect("storage must have a tip if it contains the previous block");

                    let depth =
                        tip.coinbase_height().unwrap().0 - block.coinbase_height().unwrap().0;

                    Ok(Response::Depth(Some(depth)))
                }
                .boxed()
            }
            Request::GetBlockLocator { genesis } => {
                let storage = self.clone();

                async move {
                    let tip = match storage.get_tip()? {
                        Some(tip) => tip,
                        None => {
                            return Ok(Response::BlockLocator {
                                block_locator: vec![genesis],
                            })
                        }
                    };

                    let tip_height = tip
                        .coinbase_height()
                        .expect("tip of the current chain will have a coinbase height");

                    let heights = crate::block_locator_heights(tip_height);

                    let block_locator = heights
                        .map(|height| {
                            storage.get_main_chain_at(height).map(|hash| {
                                hash.expect("there should be no holes in the current chain")
                            })
                        })
                        .collect::<Result<_, _>>()?;

                    Ok(Response::BlockLocator { block_locator })
                }
                .boxed()
            }
        }
    }
}

/// An alternate repr for `BlockHeight` that implements `AsRef<[u8]>` for usage
/// with sled
struct BytesHeight(u32, [u8; 4]);

impl From<BlockHeight> for BytesHeight {
    fn from(height: BlockHeight) -> Self {
        let bytes = height.0.to_be_bytes();
        Self(height.0, bytes)
    }
}

impl AsRef<[u8]> for BytesHeight {
    fn as_ref(&self) -> &[u8] {
        &self.1[..]
    }
}

/// Return's a type that implement's the `zebra_state::Service` using `sled`
pub fn init(
    config: Config,
) -> impl Service<
    Request,
    Response = Response,
    Error = Error,
    Future = impl Future<Output = Result<Response, Error>>,
> + Send
       + Clone
       + 'static {
    Buffer::new(SledState::new(&config), 1)
}

type Error = Box<dyn error::Error + Send + Sync + 'static>;
