from github import Github
from config import GITHUB_TOKEN
import json
import os


github = Github(GITHUB_TOKEN)

repo = github.get_repo("fastapi/fastapi")

print(f"Connected to: {repo.full_name}")


os.makedirs("data", exist_ok=True)



commits = []

for commit in repo.get_commits()[:10]:
    commits.append({
        "sha": commit.sha,
        "author": commit.commit.author.name,
        "message": commit.commit.message,
        "date": str(commit.commit.author.date)
    })

print(f"Downloaded {len(commits)} commits")


with open("data/commits.json", "w", encoding="utf-8") as f:
    json.dump(commits, f, indent=4)

print("Saved commits.json")


prs = []

for pr in repo.get_pulls(state="all")[:10]:
    prs.append({
        "number": pr.number,
        "title": pr.title,
        "author": pr.user.login if pr.user else "Unknown",
        "state": pr.state,
        "created_at": str(pr.created_at),
        "body": pr.body if pr.body else ""
    })

print(f"Downloaded {len(prs)} PRs")

with open("data/prs.json", "w", encoding="utf-8") as f:
    json.dump(prs, f, indent=4)

print("Saved prs.json")



issues = []

for issue in repo.get_issues(state="all"):

   
    if issue.pull_request:
        continue

    issues.append({
        "number": issue.number,
        "title": issue.title,
        "author": issue.user.login if issue.user else "Unknown",
        "state": issue.state,
        "created_at": str(issue.created_at),
        "body": issue.body if issue.body else ""
    })

    # Only download first 10 issues for testing
    if len(issues) == 10:
        break

print(f"Downloaded {len(issues)} issues")

with open("data/issues.json", "w", encoding="utf-8") as f:
    json.dump(issues, f, indent=4)

print("Saved issues.json")