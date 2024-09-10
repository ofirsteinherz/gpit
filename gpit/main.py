from .git_commands import check_for_unpushed_commits, get_git_diffs, stage_changes, commit_changes, push_changes
from .openai_integration import generate_commit_message, format_commit_message_from_json
from .cli_utilities import edit_message_in_editor, print_warnings

def main():
    print("\n🔍 Checking for unpushed commits...")
    unpushed_commits = check_for_unpushed_commits()

    if unpushed_commits:
        print("\n========================================")
        print("🚧 There are unpushed commits:\n")
        print(unpushed_commits)
        user_decision = input("\n🚀 Do you want to push these commits? (yes/no): ").strip().lower()

        if user_decision == 'yes':
            push_changes()
            print("\n✅ Unpushed commits have been pushed to the remote main branch.")
        else:
            print("\n🔄 Skipping push. Proceeding to check for local changes.")
    elif unpushed_commits is None:
        print("\n⚠️ Skipping push. Could not check for unpushed commits due to an error.")
    
    # Continue with the rest of the script
    print("\n🔍 Checking for local changes...")
    diffs = get_git_diffs()
    if not diffs:
        print("\n✨ No changes to commit. Your repository is up to date!")
        return

    print("\n========================================")
    print("📝 Detected changes:\n")
    print(diffs)

    show_warnings = True

    while True:
        suggested_message_json = generate_commit_message(diffs)
        suggested_message = format_commit_message_from_json(suggested_message_json)

        # Print warnings only on the first run or when a new message is not generated
        if show_warnings or not suggested_message_json.get("warnings", []):
            print("\n========================================")
            print("\n🚨 Warnings:")
            warnings = suggested_message_json.get("warnings", [])
            print_warnings(warnings)
            show_warnings = False

        print("\n========================================")
        print("📬 Suggested commit message:")
        print(suggested_message)

        print("\n👇 Choose an action:")
        user_decision = input("1️⃣ Use the current commit message\n"
                              "2️⃣ Generate a new commit message\n"
                              "3️⃣ Edit the current commit message\n"
                              "Your choice (1/2/3): ").strip()

        if user_decision == '1':
            commit_message = suggested_message
            break
        elif user_decision == '2':
            continue
        elif user_decision == '3':
            commit_message = edit_message_in_editor(suggested_message)
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

    stage_changes()
    commit_changes(commit_message)
    print("🎉 Changes committed to the main branch.\n")

    push_changes()
    print("🌍 Changes pushed to the remote main branch.")

if __name__ == "__main__":
    main()