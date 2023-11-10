import os
import subprocess
import requests
import json

from dotenv import load_dotenv
load_dotenv()

def stage_all_changes():
    """Stage all changes in the repository."""
    subprocess.run(['git', 'add', '.'])

def get_git_diffs():
    """Get diffs of staged changes in the repository."""
    stage_all_changes()  # Ensure all changes are staged
    diff_output = subprocess.check_output(['git', 'diff', '--cached']).decode()
    return diff_output

def generate_commit_message(diffs):
    """Generate a commit message using GPT-4."""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_api_key}'
    }

    commit_guideline = """
        Short (72 chars or less) summary

        - Bullet points are okay, too.
        - Typically a hyphen or asterisk is used for the bullet, followed by a
        single space. Use a hanging indent.
    """

    data = {
        "model": "gpt-4-1106-preview",
        "messages": [
            {"role": "system", "content": f"You are an assistant that suggests commit messages based on code changes.\n{commit_guideline}"},
            {"role": "user", "content": f"Here are some changes:\n\n{diffs}\n\nCan you suggest a good commit message? make sure to follow the guideline, do not provide anything more."}
        ]
    }

    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers=headers,
        data=json.dumps(data)
    )

    response_json = response.json()
    latest_message = response_json['choices'][0]['message']['content']
    return latest_message.strip()

def main():
    diffs = get_git_diffs()
    if not diffs:
        print("No changes to commit.")
        return

    print("Detected changes:")
    print(diffs)

    suggested_message = generate_commit_message(diffs)
    print("\nSuggested commit message:")
    print(suggested_message)

    user_decision = input("Do you want to modify this suggestion? (yes/no): ").strip().lower()
    if user_decision == 'yes':
        custom_message = input("Enter your commit message: ").strip()
        commit_message = custom_message or suggested_message
    else:
        commit_message = suggested_message

    # Committing the changes
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', commit_message])
    print("Changes committed to master branch.")

    # Pushing the changes to the remote master branch
    subprocess.run(['git', 'push', 'origin', 'master'])
    print("Changes pushed to the remote master branch.")

if __name__ == "__main__":
    main()
