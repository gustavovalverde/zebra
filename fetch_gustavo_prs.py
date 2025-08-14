#!/usr/bin/env python3
"""
Script to fetch merged PRs by gustavovalverde in ZcashFoundation/zebra repository since June 2024.
"""

import requests
import json
from datetime import datetime, timezone
import sys

def fetch_merged_prs():
    """Fetch merged PRs by gustavovalverde since June 2024."""
    
    # GitHub API endpoint for ZcashFoundation/zebra repository
    base_url = "https://api.github.com"
    repo = "ZcashFoundation/zebra"
    
    # Set up headers for GitHub API
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Zebra-PR-Fetcher'
    }
    
    # Note: GitHub API has rate limits for unauthenticated requests
    # For production use, you might want to add authentication
    
    # Calculate date for June 1, 2024
    june_2024 = datetime(2024, 6, 1, tzinfo=timezone.utc).isoformat()
    
    # Search query for merged PRs by gustavovalverde since June 2024
    search_query = f'repo:{repo} author:gustavovalverde is:pr is:merged merged:>={june_2024}'
    
    print(f"Searching for merged PRs by gustavovalverde since {june_2024}")
    print(f"Search query: {search_query}")
    print("-" * 80)
    
    # Use GitHub Search API
    search_url = f"{base_url}/search/issues"
    params = {
        'q': search_query,
        'sort': 'created',
        'order': 'desc',
        'per_page': 100  # Maximum per page
    }
    
    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        total_count = data.get('total_count', 0)
        prs = data.get('items', [])
        
        print(f"Found {total_count} merged PRs by gustavovalverde since June 2024")
        print()
        
        if not prs:
            print("No PRs found matching the criteria.")
            return
        
        # Process each PR
        for i, pr in enumerate(prs, 1):
            print(f"{i}. PR #{pr['number']}: {pr['title']}")
            print(f"   URL: {pr['html_url']}")
            print(f"   Merged: {pr['closed_at']}")
            print(f"   Created: {pr['created_at']}")
            
            # Get PR details to extract description and changes
            pr_url = f"{base_url}/repos/{repo}/pulls/{pr['number']}"
            pr_response = requests.get(pr_url, headers=headers)
            
            if pr_response.status_code == 200:
                pr_details = pr_response.json()
                body = pr_details.get('body', '')
                
                if body:
                    # Extract first few lines of description
                    lines = body.split('\n')
                    summary = '\n'.join(lines[:5])  # First 5 lines
                    if len(lines) > 5:
                        summary += '\n...'
                    print(f"   Summary: {summary}")
                else:
                    print("   Summary: No description provided")
                
                # Get commit count and changed files
                commits_url = f"{pr_url}/commits"
                commits_response = requests.get(commits_url, headers=headers)
                if commits_response.status_code == 200:
                    commits_data = commits_response.json()
                    commit_count = len(commits_data)
                    print(f"   Commits: {commit_count}")
                
                files_url = f"{pr_url}/files"
                files_response = requests.get(files_url, headers=headers)
                if files_response.status_code == 200:
                    files_data = files_response.json()
                    changed_files = len(files_data)
                    additions = sum(f.get('additions', 0) for f in files_data)
                    deletions = sum(f.get('deletions', 0) for f in files_data)
                    print(f"   Changed files: {changed_files}")
                    print(f"   Additions: +{additions}, Deletions: -{deletions}")
            
            print("-" * 80)
            
            # Respect GitHub API rate limits
            if i % 10 == 0:
                print("Pausing to respect rate limits...")
                import time
                time.sleep(1)
        
        # Also try to get PRs from the regular PRs endpoint as backup
        print("\n" + "="*80)
        print("Alternative method: Fetching from PRs endpoint...")
        print("="*80)
        
        prs_url = f"{base_url}/repos/{repo}/pulls"
        params = {
            'state': 'closed',
            'sort': 'updated',
            'direction': 'desc',
            'per_page': 100
        }
        
        response = requests.get(prs_url, headers=headers, params=params)
        if response.status_code == 200:
            all_prs = response.json()
            gustavo_prs = []
            
            for pr in all_prs:
                if (pr.get('user', {}).get('login') == 'gustavovalverde' and 
                    pr.get('merged_at') and 
                    pr.get('merged_at') >= june_2024):
                    gustavo_prs.append(pr)
            
            if gustavo_prs:
                print(f"\nFound {len(gustavo_prs)} merged PRs by gustavovalverde since June 2024:")
                for pr in gustavo_prs:
                    print(f"- #{pr['number']}: {pr['title']} - {pr['html_url']}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_merged_prs()