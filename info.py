import subprocess


def get_global_user():
    """Return (username, email) from global git config, or False if not set."""
    try:
        currentUser = subprocess.run(["git", "config", "--global", "user.name"], check=True, stdout=subprocess.PIPE, text=True)
        currentEmail = subprocess.run(["git", "config", "--global", "user.email"], check=True, stdout=subprocess.PIPE, text=True)
        if currentUser.stdout.strip() != "" and currentEmail.stdout.strip() != "":
            return currentUser.stdout.strip(), currentEmail.stdout.strip()
        else:
            return False
    except subprocess.CalledProcessError:
        return False


def get_repo_info():
    """Return (remote_url, current_branch) for the repo, or False if not a repo."""
    try:
        repo_url = subprocess.run(["git", "config", "--get", "remote.origin.url"], check=True, stdout=subprocess.PIPE, text=True)
        branch_name = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], check=True, stdout=subprocess.PIPE, text=True)
        return repo_url.stdout.strip(), branch_name.stdout.strip()
    except subprocess.CalledProcessError:
        return False


def add_remote(url):
    """Add a remote named 'origin' with the given URL."""
    try:
        subprocess.run(["git", "remote", "add", "origin", url], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def test_remote_auth(repo):
    """Test whether the given remote URL is accessible (auth check)."""
    try:
        result = subprocess.run([
            "git", "ls-remote", repo
        ], capture_output=True, text=True)
        if result.returncode == 0:
            return True
        elif result.stderr and "Authentication failed" in result.stderr:
            return False
        else:
            # Print helpful hint to user and return False
            print("Unable to contact the remote. Git output:\n", result.stderr)
            return False
    except Exception as e:
        print("Error while testing remote authentication:", e)
        return False


def set_global_user():
    """Prompt for and set global git username/email."""
    username = input("Please enter your full name for Git commits (e.g., Estifanos Abebaw): ").strip()
    email = input("Please enter your email address for Git commits (e.g., estif@dbu.edu.et): ").strip()
    try:
        subprocess.run(["git", "config", "--global", "user.name", username], check=True)
        subprocess.run(["git", "config", "--global", "user.email", email], check=True)
        return True
    except subprocess.CalledProcessError:
        print("Failed to set global Git user info. Make sure Git is installed and you have permission to change the global config.")
        return False


if __name__ == "__main__":
    set_global_user()
    input()

# Backwards-compatible aliases (keep old names for scripts that might call them)
has_user = get_global_user
check_repo_info = get_repo_info
set_remote_repo = add_remote
test_git_github_auth = test_remote_auth
set_git_user_config = set_global_user

