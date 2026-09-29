import os
import sys
from dotenv import load_dotenv
from github import Github
from agent import evaluate_diff

load_dotenv()

def run_sentinel_on_pr(target_repo_full_name: str, pr_number: int):
    # Connect to GitHub using robot token
    gh = Github(os.getenv("GITHUB_TOKEN"))
    repo = gh.get_repo(target_repo_full_name)
    pr = repo.get_pull(pr_number)

    # Download code changes inside the PR
    diff_data = ""
    for file in pr.get_files():
        diff_data += f"\nFile: {file.filename}\nPatch:\n{file.patch}\n"

    # Evaluate code using agent.py
    report = evaluate_diff(code_diff=diff_data, repo_name=repo.name)

    if report["risk_score"] == "HIGH":
        badge = "🛑 **HIGH RISK DETECTED (MERGE BLOCKED)**"
    elif report["risk_score"] == "MEDIUM":
        badge = "⚠️ **WARNING (LEGAL REVIEW REQUIRED)**"
    else:
        badge = "✅ **PASSED (APPROVED LICENSE)**"

    comment_markdown = (
        f"## 🛡️ IP Poisoning Sentinel Audit Report\n\n"
        f"**Target Repository:** `{target_repo_full_name}`\n"
        f"**Status:** {badge}\n"
        f"**Detected License:** `{report['license_detected']}`\n\n"
        f"### Legal Risk Assessment\n{report['reason']}\n\n"
        f"### Action Required\n{report['recommendation']}\n\n"
        f"*Powered by Hindsight Persistent Memory Layer*"
    )

    # Post comment on target PR
    pr.create_issue_comment(comment_markdown)

    # Set GitHub merge status (Green check or Red X)
    state = "failure" if report["risk_score"] == "HIGH" else "success"
    latest_commit = list(pr.get_commits())[-1]
    latest_commit.create_status(
        state=state,
        description=f"IP Sentinel Risk: {report['risk_score']}",
        context="IP-Sentinel/License-Check"
    )
    print(f"Status '{state}' posted to PR #{pr_number} on {target_repo_full_name}")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        run_sentinel_on_pr(sys.argv[1], int(sys.argv[2]))
    else:
        print("Usage: python run_check.py <target_owner/target_repo> <pr_number>")
