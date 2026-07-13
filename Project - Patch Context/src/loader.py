import json
from pathlib import Path
from langchain_core.documents import Document

DATA_DIR = Path("data")


def load_json(filename):
    path = DATA_DIR / filename

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_commit_documents():
    commits = load_json("commits.json")

    documents = []

    for commit in commits:
        text = f"""
Commit Message:
{commit['message']}

Author:
{commit['author']}

Date:
{commit['date']}
"""

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "type": "commit",
                    "sha": commit["sha"],
                    "author": commit["author"],
                    "date": commit["date"],
                },
            )
        )

    return documents


def load_pr_documents():
    prs = load_json("prs.json")

    documents = []

    for pr in prs:
        text = f"""
Pull Request Title:
{pr['title']}

Description:
{pr['body']}

Author:
{pr['author']}

State:
{pr['state']}
"""

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "type": "pr",
                    "number": pr["number"],
                    "author": pr["author"],
                    "state": pr["state"],
                },
            )
        )

    return documents


def load_issue_documents():
    issues = load_json("issues.json")

    documents = []

    for issue in issues:
        text = f"""
Issue Title:
{issue['title']}

Description:
{issue['body']}

Author:
{issue['author']}

State:
{issue['state']}
"""

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "type": "issue",
                    "number": issue["number"],
                    "author": issue["author"],
                    "state": issue["state"],
                },
            )
        )

    return documents


def load_all_documents():
    documents = []

    documents.extend(load_commit_documents())
    documents.extend(load_pr_documents())
    documents.extend(load_issue_documents())

    return documents


if __name__ == "__main__":
    docs = load_all_documents()

    print(f"Total Documents: {len(docs)}")

    print("\nFirst Document:\n")
    print(docs[0])