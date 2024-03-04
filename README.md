# GPiT
> Effortless Git Integration with GPT-Powered Commit Assistance

## Overview
This tool is designed to automate several common Git operations, enhancing the standard Git workflow with additional features. It helps in managing unpushed commits, checking for local changes, generating commit messages using OpenAI's GPT-4 API, editing commit messages, and handling the push operation to a remote repository.

https://github.com/ofirsteinherz/gpit/assets/29001725/e699afd0-f219-48b5-b1e9-563d5f31845a

## Features
- 🔍 **Check for Unpushed Commits**: Quickly identify any commits that haven't been pushed to the remote repository.
- 📝 **Detect Local Changes**: View a summary of local changes that are not yet committed.
- 💬 **Generate Commit Messages**: Utilizes GPT-4 to suggest commit messages based on the detected changes.
- ✏️ **Edit Commit Messages**: Offers an interactive editor for customizing commit messages.
- 🚀 **Stage, Commit, and Push**: Automates the process of staging changes, committing them with a chosen message, and pushing to the remote repository.

## Installation
GPIT can be installed directly from PyPI:

```bash
pip install gpit
```

This tool requires Python 3.x. Make sure you have Python installed on your system.

## Setting Up OpenAI API Key
Before using the tool, make sure to set your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY='your_openai_api_key'
```
Alternatively, you can set it in a `.env` file in the same directory as the script.
The most recommended way to save the key is through "Shell Profile Files":
Open or create the .bashrc file:
```bash
nano ~/.bashrc
```
Add your export statement:
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```
Save and exit. Apply the changes:
```bash
source ~/.bashrc
```
Verifying the Variable:
```bash
echo $OPENAI_API_KEY
```

## Usage
Once installed, you can run GPIT from any Git repository on your system. Simply use the following command:

```bash
gpit
```

Follow the on-screen prompts to manage your Git operations.

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
