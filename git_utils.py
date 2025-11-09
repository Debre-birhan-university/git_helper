import subprocess
import os
from typing import Optional

def is_git_installed() -> bool:
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def is_git_repo(repo_path: str) -> bool:
    # fast-path: .git folder exists
    if os.path.isdir(os.path.join(repo_path, ".git")):
        return True

    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=repo_path
        )
        return result.stdout.strip() == "true"
    except subprocess.CalledProcessError:
        return False


def create_git_ignore(repo_path: str, patterns: Optional[list] = None) -> None:
    if patterns is None:
        patterns = ["*.exe"]
    path = os.path.join(repo_path, ".gitignore")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(patterns))


def run_git(args: list, repo_path: str, check: bool = True, capture_output: bool = False, text: bool = True):
    """Run a git command in repo_path. args should NOT include the leading 'git'."""
    return subprocess.run(["git"] + args, check=check, cwd=repo_path, capture_output=capture_output, text=text)


def get_current_branch(repo_path: str) -> Optional[str]:
    try:
        res = run_git(["rev-parse", "--abbrev-ref", "HEAD"], repo_path, check=True, capture_output=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError:
        return None

# alias with clearer name
def get_branch(repo_path: str) -> Optional[str]:
    return get_current_branch(repo_path)
