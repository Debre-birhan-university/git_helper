import subprocess
import os
import git_utils


def push_changes(repo_path, remote_name: str = "origin"):
    """Push current branch to remote. Prints status and returns None."""
    if not git_utils.is_git_installed():
        print("Git doesn't seem to be installed. Please install Git and try again: https://git-scm.com/downloads")
        return

    if not git_utils.is_git_repo(repo_path):
        print(f"This folder doesn't look like a Git repository yet. Please commit your changes locally first (Save changes locally).")
        return

    branch = git_utils.get_branch(repo_path)
    if not branch:
        print("Could not determine the current branch. Are you in a Git repository?")
        return

    try:
        # push and set upstream if needed
        subprocess.run(["git", "push", "-u", remote_name, branch], check=True, cwd=repo_path)
        print("Success — your changes have been pushed to the remote repository.")
    except subprocess.CalledProcessError as e:
        print(f"Push failed: .\nCheck that the remote exists, your network connection is active, and your credentials are set up (SSH keys or credential helper).")


if __name__ == "__main__":
    repo_path = os.path.abspath('.')
    push_changes(repo_path)
    input()

# Backwards-compatible name
run_git_commands = push_changes
