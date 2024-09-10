import subprocess

def get_current_branch():
    """Get the name of the current Git branch."""
    try:
        # Get the current branch name
        current_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()
        return current_branch
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Error: Failed to get the current branch name. Git command returned error: {e}")
        return None

def check_for_unpushed_commits():
    """Check for commits that haven't been pushed to the remote repository, handling errors gracefully."""
    try:
        current_branch = get_current_branch()
        if not current_branch:
            print("⚠️ Warning: Could not determine the current branch. Skipping unpushed commits check.")
            return None
        
        # Check if the current branch is tracking a remote branch
        branch_status = subprocess.check_output(['git', 'status', '-b', '--porcelain']).decode().splitlines()
        if not any(f"origin/{current_branch}" in line for line in branch_status):
            print(f"⚠️ Warning: Current branch '{current_branch}' is not tracking any remote branch. Skipping unpushed commits check.")
            return None

        # If the branch is tracking a remote, check for unpushed commits
        unpushed_commits = subprocess.check_output(['git', 'log', '--branches', '--not', '--remotes']).decode().strip()
        
        if unpushed_commits:
            return unpushed_commits
        else:
            return None  # No unpushed commits
    except subprocess.CalledProcessError as e:
        # Handle specific Git errors
        print(f"⚠️ Error: Failed to check for unpushed commits. Git command returned error: {e}")
        return None
    except Exception as e:
        # Handle unexpected errors
        print(f"⚠️ Unexpected error: {e}")
        return None

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

def stage_changes():
    """Stage all changes in the repository."""
    subprocess.run(['git', 'add', '.'])
    
def commit_changes(commit_message):
    """Commit changes with a given message."""
    subprocess.run(['git', 'commit', '-m', commit_message])

def push_changes(branch_name='main'):
    """Push changes to the remote repository."""
    subprocess.run(['git', 'push', 'origin', branch_name])
