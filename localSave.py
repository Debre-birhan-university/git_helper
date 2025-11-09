import subprocess
import os
import git_utils
from typing import Tuple


def is_there_change(repo_path: str) -> Tuple[bool, str]:
    """Return (has_changes, message).

    Uses `git status --porcelain` to detect staged/unstaged changes. The message
    is a short human-friendly explanation (not raw traceback).
    """
    try:
        res = git_utils.run_git(["status", "--porcelain"], repo_path, check=True, capture_output=True, text=True)
        out = (res.stdout or "").strip()
        if not out:
            return False, "No changes detected. Nothing to commit."

        # summarize changes (count and first few file paths)
        lines = out.splitlines()
        count = len(lines)
        sample = ", ".join([l[3:] if len(l) > 3 else l for l in lines[:5]])
        more = "..." if count > 5 else ""
        return True, f"{count} changed file(s): {sample}{more}"

    except subprocess.CalledProcessError:
        return False, "Unable to determine repository status. Try running 'git status' in this folder."


def save_changes(repo_path: str, commit_message: str = "Update") -> Tuple[bool, str]:
    """Stage and commit changes locally. Returns (success: bool, message: str).

    This function performs a few validations and returns clear, short messages
    suitable for showing to end users.
    """
    if not git_utils.is_git_installed():
        return False, "Git is not installed. Please install Git: https://git-scm.com/downloads"

    if not git_utils.is_git_repo(repo_path):
        # Inform user and create a minimal repo if desired
        msg = f"The folder '{repo_path}' is not a Git repository. Initializing a new repository."
        try:
            git_utils.create_git_ignore(repo_path)
            git_utils.run_git(["init"], repo_path)
        except subprocess.CalledProcessError as e:
            return False, "Failed to initialize a Git repository. Try running 'git init' manually."

    # Check whether there are changes to commit
    has_changes, status_msg = is_there_change(repo_path)
    if not has_changes:
        return False, status_msg

    try:
        git_utils.run_git(["add", "."], repo_path)
        # run commit capturing output so we can return a friendly error message
        git_utils.run_git(["commit", "-m", commit_message], repo_path, capture_output=True, text=True)
        return True, "Saved locally — changes committed."

    except subprocess.CalledProcessError as e:
        # Try to extract stderr/stdout if available for a more precise message
        err = getattr(e, 'stderr', None) or getattr(e, 'output', None) or str(e)
        # keep message short and actionable
        return False, f"Commit failed: . may be there is no new change on your files ."


if __name__ == "__main__":
    repo_path = os.path.abspath('.')
    ok, message = save_changes(repo_path)
    print(message)


# Backwards-compatible name
run_git_commands = save_changes
