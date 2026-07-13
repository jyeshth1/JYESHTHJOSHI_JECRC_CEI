import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
REPO = "fastapi/fastapi"
BASE_URL = f"https://api.github.com/repos/{REPO}"

def fetch_commits(limit=200):
    commits_data = []
    page = 1
    while len(commits_data) < limit:
        url = f"{BASE_URL}/commits?per_page=100&page={page}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Error fetching commits: {response.text}")
            break
        data = response.json()
        if not data:
            break
        for item in data:
            commits_data.append({
                "type": "commit",
                "id": item["sha"],
                "url": item["html_url"],
                "content": item["commit"]["message"],
                "author": item["commit"]["author"]["name"] if item["commit"]["author"] else "Unknown",
                "date": item["commit"]["author"]["date"] if item["commit"]["author"] else "Unknown"
            })
            if len(commits_data) >= limit:
                break
        page += 1
    return commits_data

def fetch_issues_and_prs(limit=300):
    issues_data = []
    page = 1
    while len(issues_data) < limit:
        url = f"{BASE_URL}/issues?state=all&per_page=100&page={page}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Error fetching issues: {response.text}")
            break
        data = response.json()
        if not data:
            break
        for item in data:
            is_pr = "pull_request" in item
            
            # We combine title and body for the content search
            title = item.get("title", "")
            body = item.get("body", "") or ""
            full_content = f"Title: {title}\n\nDescription:\n{body}"
            
            issues_data.append({
                "type": "pull_request" if is_pr else "issue",
                "id": str(item["number"]),
                "url": item["html_url"],
                "title": title,
                "content": full_content,
                "author": item["user"]["login"] if item.get("user") else "Unknown",
                "date": item["created_at"],
                "state": item["state"]
            })
            if len(issues_data) >= limit:
                break
        page += 1
    return issues_data

def main():
    print("Fetching FastAPI data...")
    commits = fetch_commits(limit=500)
    print(f"Fetched {len(commits)} commits.")
    
    issues_prs = fetch_issues_and_prs(limit=500)
    print(f"Fetched {len(issues_prs)} issues and PRs.")
    
    all_data = commits + issues_prs
    
    with open("fastapi_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(all_data)} items to fastapi_data.json")

if __name__ == "__main__":
    main()
