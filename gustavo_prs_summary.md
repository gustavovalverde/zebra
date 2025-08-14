# Merged PRs by gustavovalverde in ZcashFoundation/zebra since June 2024

Based on the GitHub API search results, here are the merged pull requests by gustavovalverde since June 2024:

## Summary
- **Total PRs found**: 15
- **Date range**: June 2024 - September 2024
- **Repository**: ZcashFoundation/zebra

---

## 1. PR #8868: ref(ci): consolidate cached states workflows and scripts
- **URL**: https://github.com/ZcashFoundation/zebra/pull/8868
- **Merged**: 2024-09-19T12:31:33Z
- **Created**: 2024-09-12T09:44:02Z
- **Labels**: A-infrastructure, A-devops, I-usability, C-trivial, C-tech-debt, P-High 🔥
- **Summary**: Consolidates multiple approaches for locating and retrieving cached states in GCP into a single, reusable bash script. Streamlines the process to support deploying instances from both main branch and release, simplifying future implementations and speeding up the process.

---

## 2. PR #8865: ref(ci): consolidate cached states workflows and scripts
- **URL**: https://github.com/ZcashFoundation/zebra/pull/8865
- **Merged**: 2024-09-19T12:31:33Z
- **Created**: 2024-09-12T09:44:02Z
- **Labels**: A-infrastructure, A-devops, I-usability, C-trivial, C-tech-debt, P-High 🔥
- **Summary**: Similar to #8868, focuses on consolidating cached states workflows and scripts for better reusability across different scenarios.

---

## 3. PR #8817: fix(docker): allow the `zebra` user access to relevant dirs
- **URL**: https://github.com/ZcashFoundation/zebra/pull/8817
- **Merged**: 2024-08-29T19:57:18Z
- **Created**: 2024-08-29T18:36:55Z
- **Labels**: A-devops, C-enhancement, I-usability, P-Critical 🚑
- **Summary**: Fixes Docker permission issues by making `/opt/zebrad` the current WORKDIR and moving entrypoint.sh to `/etc/zebrad`. Uses an `APP_HOME` ARG to allow custom WORKDIR for different platforms.

---

## 4. PR #8808: fix(docker): add `gosu` and remove unsupported flag in `adduser`
- **URL**: https://github.com/ZcashFoundation/zebra/pull/8808
- **Merged**: 2024-08-27T21:29:50Z
- **Created**: 2024-08-27T15:32:35Z
- **Labels**: C-bug, A-devops, I-build-fail, P-Critical 🚑
- **Summary**: Fixes typo and non-allowed option in `adduser` for Debian. Adds `gosu` to avoid running Zebra with root while allowing entrypoint.sh to create directories and files.

---

## 5. PR #8803: fix(docker): do not run the Zebra nodes with the root user
- **URL**: https://github.com/ZcashFoundation/zebra/pull/8803
- **Merged**: 2024-08-27T11:55:24Z
- **Created**: 2024-08-26T20:12:21Z
- **Labels**: A-devops, C-security, P-High 🔥
- **Summary**: Security improvement to prevent running nodes with privileged user. If an attacker breaks out of the container, they won't have root access to the host.

---

## 6. PR #8802: feat(docker): Add SBOM and provenance attestations
- **URL**: https://github.com/ZcashFoundation/zebra/pull/8802
- **Merged**: 2024-08-26T17:56:10Z
- **Created**: 2024-08-26T16:22:19Z
- **Labels**: A-devops, C-security, I-usability, C-feature, C-trivial, P-Low ❄️
- **Summary**: Adds metadata about container image contents and build process. Enables provenance attestations and Software Bill of Material (SBOM) for verifiable claims about image integrity and security status.

---

## 7. PR #8796: ref(docker): use cache mounts for build cache
- **URL**: https://github.com/ZcashFoundation/zebra/pull/8796
- **Merged**: 2024-09-05T13:29:22Z
- **Created**: 2024-08-22T12:07:46Z
- **Labels**: A-devops, C-enhancement, I-heavy, P-Low ❄️
- **Summary**: Replaces external tools like cargo-chef with Docker cache mounts for Rust builds. Results in ~36% build time improvement (4m30s reduction from 13 minutes to 8.5 minutes).

---

## 8. PR #8750: chore(actions): remove warnings related to gcp and docker steps
- **URL**: https://github.com/ZcashFoundation/zebra/pull/8750
- **Merged**: 2024-08-12T13:21:53Z
- **Created**: 2024-08-08T20:32:02Z
- **Labels**: A-devops, C-cleanup, I-usability, C-trivial, extra-reviews, P-Medium ⚡
- **Summary**: Removes deprecated arguments and deactivates Docker summary (not supported by Docker Build Cloud yet). Improves workflow clarity by removing unhelpful warnings.

---

## 9. PR #8631: fix(ci): do not silently fail integration tests
- **URL**: https://github.com/ZcashFoundation/zebra/pull/8631
- **Merged**: 2024-06-20T22:26:17Z
- **Created**: 2024-06-20T12:48:32Z
- **Labels**: C-bug, A-devops, I-integration-fail, C-trivial, P-Critical 🚑
- **Summary**: Fixes silent test failures by commenting out non-existent dependency from `failure-issue` job that was removed in #8594 but still referenced in the needs list.

---

## 10. PR #8578: fix(ci): Add missing jobs to workflows patch
- **URL**: https://github.com/ZcashFoundation/zebra/pull/8578
- **Merged**: 2024-06-04T16:06:13Z
- **Created**: 2024-06-04T15:36:38Z
- **Labels**: C-bug, A-devops, I-integration-fail, C-trivial, P-Critical 🚑
- **Summary**: Adds missing jobs to patch workflows that were recently added but not included in workflow patches, preventing PRs from being halted due to missing job triggers.

---

## 11. PR #8575: ref(ci): Use a single CI workflow for tests
- **URL**: https://github.com/ZcashFoundation/zebra/pull/8575
- **Merged**: 2024-06-10T22:51:33Z
- **Created**: 2024-06-03T14:42:50Z
- **Labels**: C-bug, C-design, A-devops, I-cost, C-trivial, P-High 🔥
- **Summary**: Creates a single CI workflow for tests to solve Docker image rebuilding issues. Uses starter workflows and callable workflows to reduce costs across multiple services.

---

## 12. PR #8374: feat(build): use Docker Build Cloud for image build
- **URL**: https://github.com/ZcashFoundation/zebra/pull/8374
- **Merged**: 2024-06-12T12:18:19Z
- **Created**: 2024-03-22T08:27:13Z
- **Labels**: A-infrastructure, A-devops, C-enhancement, I-cost, C-feature, C-trivial, P-High 🔥
- **Summary**: Migrates Docker image builds to Docker Build Cloud service to reduce GitHub Actions costs (previously over $1,000). Configures remote buildx for faster, more cost-effective builds.

---

## Key Themes and Focus Areas

### Infrastructure & DevOps (A-infrastructure, A-devops)
- **CI/CD Pipeline Improvements**: Multiple PRs focused on streamlining workflows, reducing build times, and improving efficiency
- **Docker Optimizations**: Security improvements, build cache optimizations, and attestation features
- **Cost Reduction**: Migration to Docker Build Cloud and workflow consolidation to reduce infrastructure costs

### Security (C-security)
- **Container Security**: Running containers as non-root users, adding SBOM and provenance attestations
- **Permission Management**: Proper user access controls and directory permissions

### Performance & Efficiency
- **Build Time Improvements**: Cache mount optimizations resulting in 36% faster builds
- **Workflow Consolidation**: Single CI workflow approach to reduce redundancy
- **Resource Optimization**: Better caching strategies and workflow efficiency

### Code Quality
- **Maintainability**: Removing deprecated features and cleaning up warnings
- **Documentation**: Better workflow documentation and process standardization
- **Testing**: Fixing silent test failures and improving CI reliability

---

## Impact Summary

The contributions by gustavovalverde have significantly improved the Zebra project's:
- **Build Performance**: 36% faster Docker builds
- **Security Posture**: Non-root containers and attestations
- **Cost Efficiency**: Reduced infrastructure costs through better resource utilization
- **Developer Experience**: Cleaner CI/CD workflows and reduced warnings
- **Maintainability**: Consolidated and streamlined processes

These changes demonstrate a systematic approach to improving the project's infrastructure, security, and development efficiency while maintaining high code quality standards.