import os
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
import info
import localSave
import submitOnline


def build_menu():
    """Main, minimal menu: check user, save local, submit/push, utilities, exit."""
    return inquirer.select(
        message="What would you like to do?",
        choices=[
            Choice("save_local", name="Save changes locally (commit)"),
            Choice("push_remote", name="Submit / Push changes to remote"),
            Choice("check_user", name="Check Git user info"),

            Choice("utilities", name="Utilities / other actions"),
            Choice("exit", name="Exit"),
        ],
    ).execute()


def build_utilities_menu():
    """Smaller utilities submenu for less-frequent actions."""
    return inquirer.select(
        message="Utilities - choose an action:",
        choices=[
            Choice("check_repo", name="Check repo info"),
            Choice("set_user", name="Set global Git user"),
            Choice("set_remote", name="Set remote repository"),
            Choice("back", name="Back to main menu"),
        ],
    ).execute()


def main():
    print("""
-------------------------------------------
 Welcome to Update File Info — 
helps you check/set Git user info, save changes locally, and push to remote.
 Choose an action from the menu below .\n
            Debre Berhan University 2025
-------------------------------------------
""")

    choice = build_menu()

    if choice == 'check_user':
        user = info.get_global_user()
        if user:
            print(f"Great — your Git global user is configured:\n  Name : {user[0]}\n  Email: {user[1]}\n\nYou're all set to make commits that identify you correctly.")
        else:
            print("It looks like your global Git username and/or email are not configured. This information is used to identify you in commits.")
            set_now = inquirer.confirm(message="Would you like to set them now?", default=True).execute()
            if set_now:
                success = info.set_global_user()
                if success:
                    print('\nThanks! Your global Git user info was updated.')
                else:
                    print('\nSorry — I could not update your Git config. Try running `git config --global user.name "Your Name"` manually.')
    elif choice == 'set_user':
        success = info.set_global_user()
        if success:
            print('\nThanks! Your global Git user info was updated.')
        else:
            print('\nUnable to set global Git user info. Please ensure Git is installed and you have permission to update global config.')
    elif choice == 'check_repo':
        repo_info = info.get_repo_info()
        if repo_info:
            print(f"Repository information:\n  Remote URL   : {repo_info[0]}\n  Current branch: {repo_info[1]}\n\nNice — your repository looks correctly configured.")
        else:
            print("I couldn't find a Git repository here or Git isn't available. Try running 'git status' to check the folder.")
    elif choice == 'set_remote':
        url = inquirer.text(message='Enter the remote repository URL (e.g., git@github.com:you/repo.git):').execute()
        if url:
            is_set = info.add_remote(url)
            if is_set:
                print('\nRemote repository added. You can now push your changes to this remote.')
            else:
                print('\nFailed to add remote. Make sure the URL is valid and you have network access.')
    elif choice == 'save_local':
        repo_path = os.path.abspath('.')
        commit_message = inquirer.text(message="Enter commit message:", default="Update").execute()
        success, message = localSave.save_changes(repo_path, commit_message)
        print('\n' + message)
    elif choice == 'push_remote':
        repo_path = os.path.abspath('.')
        submitOnline.push_changes(repo_path)
    elif choice == 'exit':
        print('\nGoodbye — happy coding!')


def run_loop():
    """Run the main interactive loop until the user chooses to exit."""
    print("""
-------------------------------------------
 Welcome to Update File Info — 
 helps you check/set Git user info, save changes locally, and push to remote.
 Choose an action from the menu below .\n
          Debre Berhan University 2025
-------------------------------------------
""")

    try:
        while True:
            choice = build_menu()

            if choice == 'check_user':
                user = info.get_global_user()
                if user:
                    print(f"Great — your Git global user is configured:\n  Name : {user[0]}\n  Email: {user[1]}\n\nYou're all set to make commits that identify you correctly.")
                else:
                    print("It looks like your global Git username and/or email are not configured. This information is used to identify you in commits.")
                    set_now = inquirer.confirm(message="Would you like to set them now?", default=True).execute()
                    if set_now:
                        success = info.set_global_user()
                        if success:
                            print('\nThanks! Your global Git user info was updated.')
                        else:
                            print('\nSorry — I could not update your Git config. Try running `git config --global user.name "Your Name"` manually.')

            elif choice == 'save_local':
                repo_path = os.path.abspath('.')
                commit_message = inquirer.text(message="Enter commit message:", default="Update").execute()
                success, message = localSave.save_changes(repo_path, commit_message)
                print('\n' + message)

            elif choice == 'push_remote':
                repo_path = os.path.abspath('.')
                submitOnline.push_changes(repo_path)

            elif choice == 'utilities':
                util_choice = build_utilities_menu()
                if util_choice == 'check_repo':
                    repo_info = info.get_repo_info()
                    if repo_info:
                        print(f"Repository information:\n  Remote URL   : {repo_info[0]}\n  Current branch: {repo_info[1]}\n\nNice — your repository looks correctly configured.")
                    else:
                        print("I couldn't find a Git repository here or Git isn't available. Try running 'git status' to check the folder.")
                elif util_choice == 'set_user':
                    success = info.set_global_user()
                    if success:
                        print('\nThanks! Your global Git user info was updated.')
                    else:
                        print('\nUnable to set global Git user info. Please ensure Git is installed and you have permission to update global config.')
                elif util_choice == 'set_remote':
                    url = inquirer.text(message='Enter the remote repository URL (e.g., git@github.com:you/repo.git):').execute()
                    if url:
                        is_set = info.add_remote(url)
                        if is_set:
                            print('\nRemote repository added. You can now push your changes to this remote.')
                        else:
                            print('\nFailed to add remote. Make sure the URL is valid and you have network access.')
                # if 'back' just loop again

            elif choice == 'exit':
                print('\nGoodbye — happy coding!')
                break

            else:
                # fallback - shouldn't happen but keep loop safe
                print('\nUnknown choice — returning to main menu.')

    except KeyboardInterrupt:
        print('\nInterrupted — exiting. Goodbye!')
 


if __name__ == '__main__':
    run_loop()