# git_helper

Small collection of Python helper scripts to manage Git user/config, save changes locally (commit), and push to remote.

This repository contains lightweight CLI tools intended to be run from the project folder. The core idea was to consolidate common git helpers into a single module and keep the scripts simple and easy to use.

## Files of interest

- `git_utils.py` — Shared Git helper functions used by the other scripts (install check, repo detection, create .gitignore, run git commands, get current branch).
- `localSave.py` — Stage and commit local changes. If the folder is not a git repo it initializes one and writes a `.gitignore`.
- `submitOnline.py` — Push the current branch to the configured remote (defaults to `origin`) and sets upstream when first pushing.
- `info.py` — Query/set global git user info, read remote URL and current branch, test remote auth via `git ls-remote`.
- `main.py` — Simple interactive menu (uses InquirerPy) to call the above flows.

## Prerequisites

 - (Optional) `PyInquirer` package for `main.py` interactive menu. If you don't have it installed you can still run the individual scripts.

To install `PyInquirer`:

```powershell
pip install PyInquirer
```


Run the interactive menu:

```powershell
# from the project directory
python main.py
```

Save changes locally (commit):

```powershell
python localSave.py
# or call the function via the interactive menu
```

Push current branch to remote:

```powershell
python submitOnline.py
# or use the main menu 'submit to remote'
```

Get/set git user info:

```powershell
python info.py
# When run directly it launches the set-user interactive prompt
```


## Behavior notes and recommendations

- `localSave` will initialize a git repository if none exists and will add a `.gitignore` containing `*.exe` by default. Change `git_utils.create_git_ignore` if you want different patterns.
- `submitOnline` pushes the current branch and uses `-u origin <branch>` on the first push so future `git push` works without arguments.
- `info` interacts with global git config (user.name, user.email). These calls use `git config --global`.
- Authentication for `git push` depends on the user's git setup (SSH keys, credential manager, personal access token for HTTPS). The scripts do not attempt to handle credentials.

## Troubleshooting

- If `git` is not found: ensure Git is installed and available on PATH. On Windows, you may need to restart your shell after installing Git.
- If pushes fail due to authentication: configure SSH keys or use a credential helper / PAT for HTTPS.
- If `main.py` fails with import errors for `InquirerPy`, install the dependency or run the scripts directly.

## Next steps (suggested improvements)

- Add unit tests for `git_utils` with subprocess mocking.
- Add basic logging instead of printing for clearer diagnostics.
- Add optional arguments for remote/branch selection in `submitOnline`.
- Add linting (ruff/flake8) and type checks (mypy) for improved code quality.

## License

This repository is provided as-is. No license file included by default.

