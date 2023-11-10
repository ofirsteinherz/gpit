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
    subprocess.run(['git', 'add', '.']) # Ensure all changes are staged
    diff_output = subprocess.check_output(['git', 'diff', '--cached']).decode()
    return diff_output

def generate_commit_message(diffs):
    """Generate a commit message using GPT-4 and format the response as JSON."""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_api_key}'
    }

    prompt = f"""
        Create a commit message for the following changes, in JSON format with a message and bullet points:

        {diffs}

        Format the response like this:
        {{
        "message": "<message>",
        "bullets": ["<bullet1>", "<bullet2>", ...]
        }}

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

def main():
    unpushed_commits = check_for_unpushed_commits()
    if unpushed_commits:
        print("There are unpushed commits:")
        print(unpushed_commits)
        user_decision = input("Do you want to push these commits? (yes/no): ").strip().lower()

        if user_decision == 'yes':
            subprocess.run(['git', 'push', 'origin', 'main'])
            print("Unpushed commits have been pushed to the remote main branch.")
        else:
            # Reset the HEAD to the last pushed state, keeping the changes in the working directory
            subprocess.run(['git', 'reset', '--soft', 'origin/main'])
            print("Unpushed commits have been reset. Changes are kept in the working directory.")

    diffs = get_git_diffs()
    if not diffs:
        print("No changes to commit.")
        return

    print("Detected changes:")
    print(diffs)

    while True:
        # Generate or regenerate the commit message based on diffs
        suggested_message_json = generate_commit_message(diffs)
        suggested_message = format_commit_message_from_json(suggested_message_json)
        print("\nSuggested commit message:")
        print(suggested_message)

        user_decision = input("Choose an option (1-3):\n"
                              "1. Use the current commit message\n"
                              "2. Generate a new commit message\n"
                              "3. Edit the current commit message\n"
                              "Your choice (1/2/3): ").strip()

        if user_decision == '1':
            commit_message = suggested_message
            break
        elif user_decision == '2':
            # This will loop back and regenerate the commit message
            continue
        elif user_decision == '3':
            commit_message = edit_message_in_editor(suggested_message)
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    # Committing the changes
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', commit_message])
    print("Changes committed to main branch.")

    # Pushing the changes to the remote main branch
    subprocess.run(['git', 'push', 'origin', 'main'])
    print("Changes pushed to the remote main branch.")

if __name__ == "__main__":
    main()
