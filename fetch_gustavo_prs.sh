#!/bin/bash

# Script to fetch merged PRs by gustavovalverde in ZcashFoundation/zebra repository since June 2024

echo "Fetching merged PRs by gustavovalverde since June 2024..."
echo "Repository: ZcashFoundation/zebra"
echo "=" * 80

# GitHub API endpoint
API_BASE="https://api.github.com"
REPO="ZcashFoundation/zebra"

# Headers for GitHub API
HEADERS="-H 'Accept: application/vnd.github.v3+json' -H 'User-Agent: Zebra-PR-Fetcher'"

echo "Method 1: Using GitHub Search API"
echo "-" * 40

# Search for merged PRs by gustavovalverde since June 2024
SEARCH_QUERY="repo:ZcashFoundation/zebra author:gustavovalverde is:pr is:merged merged:>=2024-06-01"
SEARCH_URL="$API_BASE/search/issues?q=$(echo "$SEARCH_QUERY" | sed 's/ /%20/g')&sort=created&order=desc&per_page=100"

echo "Search query: $SEARCH_QUERY"
echo "Search URL: $SEARCH_URL"
echo

# Make the search request
echo "Fetching search results..."
SEARCH_RESPONSE=$(curl -s $HEADERS "$SEARCH_URL")

# Check if we got a valid response
if echo "$SEARCH_RESPONSE" | grep -q "total_count"; then
    TOTAL_COUNT=$(echo "$SEARCH_RESPONSE" | grep -o '"total_count":[0-9]*' | cut -d: -f2)
    echo "Found $TOTAL_COUNT merged PRs by gustavovalverde since June 2024"
    echo
    
    # Extract PR numbers and titles
    echo "$SEARCH_RESPONSE" | grep -o '"number":[0-9]*' | cut -d: -f2 | while read -r pr_number; do
        echo "Processing PR #$pr_number..."
        
        # Get PR details
        PR_URL="$API_BASE/repos/$REPO/pulls/$pr_number"
        PR_RESPONSE=$(curl -s $HEADERS "$PR_URL")
        
        if echo "$PR_RESPONSE" | grep -q '"title"'; then
            TITLE=$(echo "$PR_RESPONSE" | grep -o '"title":"[^"]*"' | cut -d'"' -f4)
            HTML_URL=$(echo "$PR_RESPONSE" | grep -o '"html_url":"[^"]*"' | cut -d'"' -f4)
            MERGED_AT=$(echo "$PR_RESPONSE" | grep -o '"merged_at":"[^"]*"' | cut -d'"' -f4)
            BODY=$(echo "$PR_RESPONSE" | grep -o '"body":"[^"]*"' | cut -d'"' -f4)
            
            echo "PR #$pr_number: $TITLE"
            echo "  URL: $HTML_URL"
            echo "  Merged: $MERGED_AT"
            
            if [ -n "$BODY" ]; then
                echo "  Summary: $BODY" | head -c 200
                if [ ${#BODY} -gt 200 ]; then
                    echo "..."
                else
                    echo
                fi
            else
                echo "  Summary: No description provided"
            fi
            
            # Get commit count
            COMMITS_URL="$PR_URL/commits"
            COMMITS_RESPONSE=$(curl -s $HEADERS "$COMMITS_URL")
            COMMIT_COUNT=$(echo "$COMMITS_RESPONSE" | grep -o '^\[.*\]$' | wc -l)
            echo "  Commits: $COMMIT_COUNT"
            
            # Get file changes
            FILES_URL="$PR_URL/files"
            FILES_RESPONSE=$(curl -s $HEADERS "$FILES_URL")
            CHANGED_FILES=$(echo "$FILES_RESPONSE" | grep -o '^\[.*\]$' | wc -l)
            
            ADDITIONS=$(echo "$FILES_RESPONSE" | grep -o '"additions":[0-9]*' | cut -d: -f2 | awk '{sum+=$1} END {print sum+0}')
            DELETIONS=$(echo "$FILES_RESPONSE" | grep -o '"deletions":[0-9]*' | cut -d: -f2 | awk '{sum+=$1} END {print sum+0}')
            
            echo "  Changed files: $CHANGED_FILES"
            echo "  Additions: +$ADDITIONS, Deletions: -$DELETIONS"
            echo "-" * 80
        fi
        
        # Small delay to respect rate limits
        sleep 1
    done
else
    echo "Error: Could not fetch search results"
    echo "Response: $SEARCH_RESPONSE"
fi

echo
echo "Method 2: Using PRs endpoint as backup"
echo "-" * 40

# Alternative method: get all closed PRs and filter
PRS_URL="$API_BASE/repos/$REPO/pulls?state=closed&sort=updated&direction=desc&per_page=100"
echo "Fetching from: $PRS_URL"

PRS_RESPONSE=$(curl -s $HEADERS "$PRS_URL")

if echo "$PRS_RESPONSE" | grep -q '"number"'; then
    echo "Successfully fetched PRs list"
    
    # Extract PRs by gustavovalverde that were merged since June
    echo "$PRS_RESPONSE" | grep -A 20 '"user"' | grep -B 20 -A 20 '"login":"gustavovalverde"' | grep -o '"number":[0-9]*' | cut -d: -f2 | while read -r pr_num; do
        echo "Found PR #$pr_num by gustavovalverde"
    done
else
    echo "Error: Could not fetch PRs list"
    echo "Response: $PRS_RESPONSE"
fi

echo
echo "Script completed."