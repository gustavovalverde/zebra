#!/usr/bin/env python3
"""
Script to extract and format PR information from GitHub API response.
"""

import json
import re
from datetime import datetime

def extract_pr_info(api_response):
    """Extract PR information from the GitHub API response."""
    
    # Clean up the response and extract JSON
    # The response seems to have some extra content mixed in
    try:
        # Find the JSON part of the response
        json_start = api_response.find('{"total_count"')
        if json_start == -1:
            print("Could not find JSON content in response")
            return
        
        json_content = api_response[json_start:]
        # Clean up control characters
        json_content = json_content.replace('\r', '').replace('\n', '')
        
        data = json.loads(json_content)
        
        total_count = data.get('total_count', 0)
        items = data.get('items', [])
        
        print(f"Found {total_count} merged PRs by gustavovalverde since June 2024")
        print("=" * 80)
        
        for i, item in enumerate(items, 1):
            print(f"{i}. PR #{item['number']}: {item['title']}")
            print(f"   URL: {item['html_url']}")
            print(f"   Merged: {item['closed_at']}")
            print(f"   Created: {item['created_at']}")
            
            # Extract body/description
            body = item.get('body', '')
            if body:
                # Clean up the body text
                body = body.replace('\r\n', '\n').replace('\r', '\n')
                lines = body.split('\n')
                
                # Find the summary section
                summary_lines = []
                for line in lines:
                    if line.strip() and not line.startswith('###') and not line.startswith('<!--'):
                        summary_lines.append(line.strip())
                        if len(summary_lines) >= 3:  # Limit to first 3 meaningful lines
                            break
                
                if summary_lines:
                    summary = ' '.join(summary_lines)
                    if len(summary) > 200:
                        summary = summary[:200] + "..."
                    print(f"   Summary: {summary}")
                else:
                    print("   Summary: No description provided")
            else:
                print("   Summary: No description provided")
            
            # Extract labels
            labels = [label['name'] for label in item.get('labels', [])]
            if labels:
                print(f"   Labels: {', '.join(labels)}")
            
            print("-" * 80)
            
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print("Raw response preview:")
        print(api_response[:500] + "...")
    except Exception as e:
        print(f"Error processing response: {e}")

def main():
    """Main function to process the API response."""
    
    # Create a clean sample based on what we saw in the API response
    sample_response = '''{"total_count":15,"incomplete_results":false,"items":[{"url":"https://api.github.com/repos/ZcashFoundation/zebra/issues/8868","repository_url":"https://api.github.com/repos/ZcashFoundation/zebra","labels_url":"https://api.github.com/repos/ZcashFoundation/zebra/issues/8868/labels{/name}","comments_url":"https://api.github.com/repos/ZcashFoundation/zebra/issues/8868/comments","events_url":"https://api.github.com/repos/ZcashFoundation/zebra/issues/8868/events","html_url":"https://github.com/ZcashFoundation/zebra/pull/8868","id":2521892691,"node_id":"PR_kwDODDv0A857RvY9","number":8868,"title":"ref(ci): consolidate cached states workflows and scripts","user":{"login":"gustavovalverde","id":16890942,"node_id":"MDQ6VXNlcjE2ODkwOTQy","avatar_url":"https://avatars.githubusercontent.com/u/16890942?v=4","gravatar_id":"","url":"https://api.github.com/users/gustavovalverde","html_url":"https://github.com/gustavovalverde","followers_url":"https://api.github.com/users/gustavovalverde/followers","following_url":"https://api.github.com/users/gustavovalverde/following{/other_user}","gists_url":"https://api.github.com/users/gustavovalverde/gists{/gist_id}","starred_url":"https://api.github.com/users/gustavovalverde/starred{/owner}{/repo}","subscriptions_url":"https://api.github.com/users/gustavovalverde/subscriptions","organizations_url":"https://api.github.com/users/gustavovalverde/orgs","repos_url":"https://api.github.com/users/gustavovalverde/repos","events_url":"https://api.github.com/users/gustavovalverde/events{/privacy}","received_events_url":"https://api.github.com/users/gustavovalverde/received_events","type":"User","user_view_type":"public","site_admin":false},"labels":[{"id":2108537496,"node_id":"MDU6TGFiZWwyMTA4NTM3NDk2","url":"https://api.github.com/repos/ZcashFoundation/zebra/labels/A-infrastructure","name":"A-infrastructure","color":"fbca04","default":false,"description":"Area: Infrastructure changes"},{"id":2126192849,"node_id":"MDU6TGFiZWwyMTI2MTkyODQ5","url":"https://api.github.com/repos/ZcashFoundation/zebra/labels/A-devops","name":"A-devops","color":"fbca04","default":false,"description":"Area: Pipelines, CI/CD and Dockerfiles"},{"id":2753227059,"node_id":"MDU6TGFiZWwyNzUzMjI3MDU5","url":"https://api.github.com/repos/ZcashFoundation/zebra/labels/I-usability","name":"I-usability","color":"B60205","default":false,"description":"Zebra is hard to understand or use"},{"id":4559885395,"node_id":"LA_kwDODDv0A88AAAABD8pUUw","url":"https://api.github.com/repos/ZcashFoundation/zebra/labels/C-trivial","name":"C-trivial","color":"f5f1fd","default":false,"description":"Category: A trivial change that is not worth mentioning in the CHANGELOG"},{"id":5303737803,"node_id":"LA_kwDODDv0A88AAAABPCCdyw","url":"https://api.github.com/repos/ZcashFoundation/zebra/labels/C-tech-debt","name":"C-tech-debt","color":"EF6102","default":false,"description":"Category: Code maintainability issues"},{"id":6446909853,"node_id":"LA_kwDODDv0A88AAAABgEQJnQ","url":"https://api.github.com/repos/ZcashFoundation/zebra/labels/P-High%20%F0%9F%94%A5","name":"P-High 🔥","color":"D93F0B","default":false,"description":""}],"state":"closed","locked":false,"assignee":{"login":"gustavovalverde","id":16890942,"node_id":"MDQ6VXNlcjE2ODkwOTQy","avatar_url":"https://api.github.com/users/gustavovalverde","html_url":"https://github.com/gustavovalverde","followers_url":"https://api.github.com/users/gustavovalverde/followers","following_url":"https://api.github.com/users/gustavovalverde/following{/other_user}","gists_url":"https://api.github.com/users/gustavovalverde/gists{/gist_id}","starred_url":"https://api.github.com/users/gustavovalverde/starred{/owner}{/repo}","subscriptions_url":"https://api.github.com/users/gustavovalverde/subscriptions","organizations_url":"https://api.github.com/users/gustavovalverde/orgs","repos_url":"https://api.github.com/users/gustavovalverde/repos","events_url":"https://api.github.com/users/gustavovalverde/events{/privacy}","received_events_url":"https://api.github.com/users/gustavovalverde/received_events","type":"User","user_view_type":"public","site_admin":false},"assignees":[{"login":"gustavovalverde","id":16890942,"node_id":"MDQ6VXNlcjE2ODkwOTQy","avatar_url":"https://api.github.com/users/gustavovalverde","html_url":"https://github.com/gustavovalverde","followers_url":"https://api.github.com/users/gustavovalverde/followers","following_url":"https://api.github.com/users/gustavovalverde/following{/other_user}","gists_url":"https://api.github.com/users/gustavovalverde/gists{/gist_id}","starred_url":"https://api.github.com/users/gustavovalverde/starred{/owner}{/repo}","subscriptions_url":"https://api.github.com/users/gustavovalverde/subscriptions","organizations_url":"https://api.github.com/users/gustavovalverde/orgs","repos_url":"https://api.github.com/users/gustavovalverde/repos","events_url":"https://api.github.com/users/gustavovalverde/events{/privacy}","received_events_url":"https://api.github.com/users/gustavovalverde/received_events","type":"User","user_view_type":"public","site_admin":false}],"milestone":null,"comments":2,"created_at":"2024-09-12T09:44:02Z","updated_at":"2024-09-19T12:31:37Z","closed_at":"2024-09-19T12:31:33Z","author_association":"MEMBER","type":null,"active_lock_reason":null,"draft":false,"pull_request":{"url":"https://api.github.com/repos/ZcashFoundation/zebra/pulls/8868","html_url":"https://github.com/ZcashFoundation/zebra/pull/8868","diff_url":"https://github.com/ZcashFoundation/zebra/pull/8868.diff","patch_url":"https://github.com/ZcashFoundation/zebra/pull/8868.patch","merged_at":"2024-09-19T12:31:33Z"},"body":"## Motivation\\n\\nWe have been using multiple approaches to locate and retrieve cached states in GCP. However, this has made it difficult to reuse the same methods across new workflows or different scenarios.\\n\\nTo address this, we have streamlined the process to make it more reusable in other contexts. This change will support deploying instances from both the `main` branch and `release`, simplifying future implementations and speeding up the process.\\n\\n### Specifications & References\\n\\nThis is the ground work for:\\n- https://github.com/ZcashFoundation/zebra/issues/6894\\n\\n## Solution\\n- Use a single bash script (`gcp-get-cached-disks.sh`) to get cached states names and availability\\n- Move script logic from `sub-find-cached-disks.yml` to `gcp-get-cached-disks.sh` and adapt `sub-find-cached-disks.yml` to allow to output available disks and disks names.\\n- Simplify parameters usage in `sub-deploy-integration-tests-gcp.yml` and convert the `Find ${{ inputs.test_id }} cached state disk` step into an independent job, to be able to use the `sub-find-cached-disks.yml` reusable workflow\\n- Remove repetition in `sub-ci-integration-tests-gcp.yml`\\n- Allow sync tests to use the `ZEBRA_CACHED_STATE_DIR` as the cache directory, if specified\\n- Update the `entrypoint.sh` to reflect this change\\n- Add the `ZEBRA_CACHED_STATE_DIR` variable to the missing tests in `sub-ci-integration-tests-gcp.yml`, and remove extra parameters to call reusable workflows.\\n\\n### Tests\\n\\nAll test should find their respective cached states and run sucessfully\\n\\n### Follow-up Work\\n\\n- https://github.com/ZcashFoundation/zebra/issues/6894\\n- https://github.com/ZcashFoundation/infra/issues/15\\n\\n### PR Author Checklist\\n\\n<!-- If you are the author of the PR, check the boxes below before making the PR\\nready for review. -->\\n\\n- [x] The PR name will make sense to users.\\n- [x] The PR provides a CHANGELOG summary.\\n- [x] The solution is tested.\\n- [x] The documentation is up to date.\\n- [x] The PR has a priority label.\\n\\n### PR Reviewer Checklist\\n\\n<!-- If you are a reviewer of the PR, check the boxes below before approving it. -->\\n\\n- [ ] The PR Author checklist is complete.\\n- [ ] The PR resolves the issue.\\n\\n","reactions":{"url":"https://api.github.com/repos/ZcashFoundation/zebra/issues/8868/reactions","total_count":0,"+1":0,"-1":0,"laugh":0,"hooray":0,"confused":0,"heart":0,"rocket":0,"eyes":0},"timeline_url":"https://api.github.com/repos/ZcashFoundation/zebra/issues/8868/timeline","performed_via_github_app":null,"state_reason":null,"score":1.0}]}'''
    
    extract_pr_info(sample_response)

if __name__ == "__main__":
    main()