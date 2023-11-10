import os
import subprocess
import tempfile
import requests
import json

from dotenv import load_dotenv
load_dotenv()

def check_for_unpushed_commits():
    """Check for commits that haven't been pushed to the remote repository."""
    return subprocess.check_output(['git', 'log', '--branches', '--not', '--remotes']).decode().strip()

def get_git_diffs():
    """Get diffs of staged changes in the repository."""
    subprocess.run(['git', 'add', '.'])  # Ensure all changes are staged
    changed_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode().splitlines()
    diff_output = ""

    for file in changed_files:
        diff_output += f"\n📄 {file}\n"
        diff_output += "-" * len(file) + "\n"
        file_diff = subprocess.check_output(['git', 'diff', '--cached', file]).decode()
        diff_output += file_diff + "\n"

    return diff_output

def generate_commit_message(diffs):
    """Generate a commit message using GPT-4 and format the response as JSON."""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_api_key}'
    }

    prompt = f"""
        I need a detailed and specific commit message for the following Git code changes.
        The message should reflect the actual code modifications, improvements, or fixes made.
        Please provide the message in JSON format, with distinct sections for a summary
        message, bullet points detailing specific changes, and any necessary warnings about
        the code, such as potential issues or areas needing attention.

        Changes:
        {diffs}

        Please format the response as follows:
        {{
            "message": "A concise summary, specifically describing the key change or improvement",
            "bullets": [
                "Specific detail about a particular code change, including file and function names if applicable",
                "Description of another specific change, noting how it affects the functionality or structure of the code",
                ...
            ],
            "warnings": [
                "Optional. Necessary warnings or notes of caution about specific parts of the changes, such as areas that need further testing or review",
                ...
            ]
        }}

        The response should be technically specific, aligning closely with the provided code changes, and avoiding generic or placeholder text.
        Be concise and on-point, without providing excess information.
    """

    data = {
        "model": "gpt-4-1106-preview",
        "messages": [
            {"role": "system", "content": "You are an assistant, and you only reply with JSON."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {
            "type": "json_object"
        }
    }

    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers=headers,
        data=json.dumps(data)
    )

    response_json = response.json()
    response_text = response_json['choices'][0]['message']['content']

    try:
        # Assuming the response_text is a string in JSON format
        formatted_response = json.loads(response_text)
    except json.JSONDecodeError:
        # Fallback in case the response isn't in the expected JSON format
        formatted_response = {"message": "Failed to parse response", "bullets": []}

    return formatted_response

def format_commit_message_from_json(commit_json):
    """Format the commit message from JSON to a string."""
    message_str = commit_json.get("message", "")
    bullets = commit_json.get("bullets", [])
    
    formatted_bullets = "\n".join(f"- {bullet}" for bullet in bullets)
    return f"{message_str}\n\n{formatted_bullets}"

def edit_message_in_editor(message):
    """Open the message in a text editor (Nano) for editing."""
    with tempfile.NamedTemporaryFile(suffix=".tmp", delete=False, mode='w+') as tf:
        tf_path = tf.name
        tf.write(message)
        tf.flush()

    editor = os.getenv('EDITOR', 'nano')  # Use Nano or the default editor set in the environment
    subprocess.call([editor, tf_path])

    with open(tf_path, "r") as tf:
        edited_message = tf.read()

    os.remove(tf_path)  # Clean up the temporary file
    return edited_message

def print_warnings(warnings):
    """Prints warnings in a formatted manner."""
    if warnings:
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("\n✅ No warnings.")

def main():
    print("\n🔍 Checking for unpushed commits...")
    unpushed_commits = check_for_unpushed_commits()
    if unpushed_commits:
        print("\n========================================")
        print("🚧 There are unpushed commits:\n")
        print(unpushed_commits)
        user_decision = input("\n🚀 Do you want to push these commits? (yes/no): ").strip().lower()

        if user_decision == 'yes':
            subprocess.run(['git', 'push', 'origin', 'main'])
            print("\n✅ Unpushed commits have been pushed to the remote main branch.")
        else:
            subprocess.run(['git', 'reset', '--soft', 'origin/main'])
            print("\n🔄 Unpushed commits have been reset. Changes are kept in the working directory.")

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
        if show_warnings or not warnings:
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

    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', commit_message])
    print("🎉 Changes committed to the main branch.\n")

    subprocess.run(['git', 'push', 'origin', 'main'])
    print("🌍 Changes pushed to the remote main branch.")

if __name__ == "__main__":
    main()
