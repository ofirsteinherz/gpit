# GPiT
> Effortless Git Integration with GPT-Powered Commit Assistance

## Overview
This tool is designed to automate several common Git operations, enhancing the standard Git workflow with additional features. It helps in managing unpushed commits, checking for local changes, generating commit messages using OpenAI's GPT-4 API, editing commit messages, and handling the push operation to a remote repository.

## Features
- 🔍 **Check for Unpushed Commits**: Quickly identify any commits that haven't been pushed to the remote repository.
- 📝 **Detect Local Changes**: View a summary of local changes that are not yet committed.
- 💬 **Generate Commit Messages**: Utilizes GPT-4 to suggest commit messages based on the detected changes.
- ✏️ **Edit Commit Messages**: Offers an interactive editor for customizing commit messages.
- 🚀 **Stage, Commit, and Push**: Automates the process of staging changes, committing them with a chosen message, and pushing to the remote repository.

## Installation
Clone this repository to your local machine using:
```bash
git clone https://github.com/ofirsteinherz/gpit
cd git-auto-commit
```

Ensure that you have Python installed on your system. This tool requires Python 3.x.

## Usage
Navigate to your Git repository and run the script:
```bash
python main.py
```

Follow the on-screen prompts to manage your Git operations.

## Configuration
Before using the tool, make sure to set your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY='your_openai_api_key'
```
Alternatively, you can set it in a `.env` file in the same directory as the script.

## Dependencies
- Git
- Python 3.x
- Requests library for Python
- python-dotenv (for managing environment variables)

Install Python dependencies using:
```bash
pip install requests python-dotenv
```

## Contributing
Contributions to this project are welcome! Please fork the repository and submit a pull request with your proposed changes.