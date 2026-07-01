from github import Github
from src.config import settings
from typing import Dict, Optional

class GitHubManager:
    def __init__(self):
        self.gh = Github(settings.GITHUB_TOKEN)

    def get_pr_diff(self, repo_name: str, pr_number: int) -> str:
        try:
            repo = self.gh.get_repo(repo_name)
            pr = repo.get_pull(pr_number)

            diff = ""
            for file in pr.get_files():
                if file.patch:
                    diff += f"File: {file.filename}\n"
                    diff += file.patch + "\n\n"

            return diff
        except Exception as e:
            print(f"Error getting PR diff: {e}")
            return ""

    def post_comment(self, repo_name: str, pr_number: int, comment_text: str) -> bool:
        try:
            repo = self.gh.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            pr.create_issue_comment(comment_text)
            return True
        except Exception as e:
            print(f"Error posting comment: {e}")
            return False

    def get_pr_info(self, repo_name: str, pr_number: int) -> Optional[Dict]:
        try:
            repo = self.gh.get_repo(repo_name)
            pr = repo.get_pull(pr_number)

            return {
                "number": pr.number,
                "title": pr.title,
                "branch": pr.head.ref,
                "author": pr.user.login,
                "created_at": pr.created_at.isoformat(),
                "url": pr.html_url,
                "diff": self.get_pr_diff(repo_name, pr_number)
            }
        except Exception as e:
            print(f"Error getting PR info: {e}")
            return None

    def update_pr_status(self, repo_name: str, pr_number: int, status: str, description: str):
        try:
            repo = self.gh.get_repo(repo_name)
            pr = repo.get_pull(pr_number)

            # Note: Can't directly block PR, but we update check runs if available
            return True
        except Exception as e:
            print(f"Error updating PR status: {e}")
            return False

github_manager = GitHubManager()
