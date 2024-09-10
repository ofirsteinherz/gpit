import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def generate_commit_message(diffs):
    """Generate a commit message using GPT-4 and format the response as JSON."""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL")
    
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
            "message": "A concise summary, specifically describing the key change or improvement. Must be 72 chars or less",
            "bullets": [
                "Specific detail about a particular code change, including file and function names if applicable",
                "Description of another specific change, noting how it affects the functionality or structure of the code",
                ...
            ],
            "warnings": [
                "Optional. Necessary warnings or notes of caution about specific parts of the changes",
                ...
            ]
        }}

        The response should be technically specific, aligning closely with the provided code changes, and avoiding generic or placeholder text.
        Be concise and on-point, without providing excess information.
    """

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an assistant, and you only reply with JSON."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {
            "type": "json_object"
        }
    }

    print(f"Sending resuest to {model}...")
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers=headers,
        data=json.dumps(data)
    )

    response_json = response.json()
    print(response)
    response_text = response_json['choices'][0]['message']['content']

    try:
        # Assuming the response_text is a string in JSON format
        formatted_response = json.loads(response_text)
    except json.JSONDecodeError:
        # Fallback in case the response isn't in the expected JSON format
        formatted_response = {"message": "Failed to parse response", "bullets": []}

    print(formatted_response)
    return formatted_response

def format_commit_message_from_json(commit_json):
    """Format the commit message from JSON to a string."""
    message_str = commit_json.get("message", "")
    bullets = commit_json.get("bullets", [])
    
    formatted_bullets = "\n".join(f"- {bullet}" for bullet in bullets)
    return f"{message_str}\n\n{formatted_bullets}"