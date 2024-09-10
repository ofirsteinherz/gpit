import subprocess

def get_current_branch():
    """Get the name of the current Git branch."""
    try:
        current_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stderr=subprocess.DEVNULL).decode().strip()
        return current_branch
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Error: Failed to get the current branch name. Git command returned error: {e}")
        return None

def get_default_branch():
    """Get the default branch of the remote repository (e.g., origin/main or origin/master)."""
    try:
        # Try to get the default branch from origin/HEAD
        default_branch_ref = subprocess.check_output(
            ['git', 'symbolic-ref', 'refs/remotes/origin/HEAD'], stderr=subprocess.DEVNULL
        ).decode().strip()
        default_branch = default_branch_ref.replace('refs/remotes/origin/', '')
        return default_branch
    except subprocess.CalledProcessError:
        # If 'origin/HEAD' doesn't exist, fall back to checking for common branches
        print("⚠️ Warning: Could not determine the default branch from 'origin/HEAD'. Falling back to guess.")
        try:
            # Try to list remote branches and guess the default
            remote_branches = subprocess.check_output(
                ['git', 'branch', '-r'], stderr=subprocess.DEVNULL
            ).decode().strip().splitlines()
            # Heuristic: prefer 'main', otherwise try 'master'
            if 'origin/main' in remote_branches:
                return 'main'
            elif 'origin/master' in remote_branches:
                return 'master'
            else:
                return None
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Error: Could not list remote branches. Git command returned error: {e}")
            return None

def get_upstream_branch():
    """Get the name of the upstream branch (remote branch tracking the current branch)."""
    try:
        upstream_branch = subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}'],
            stderr=subprocess.DEVNULL  # Suppress Git error messages
        ).decode().strip()
        return upstream_branch
    except subprocess.CalledProcessError:
        # If no upstream is set, return None
        return None

def check_for_unpushed_commits():
    """Check for commits that haven't been pushed to the remote repository."""
    try:
        current_branch = get_current_branch()
        if not current_branch:
            print("⚠️ Warning: Could not determine the current branch. Skipping unpushed commits check.")
            return None

        # Check if the current branch has an upstream branch
        upstream_branch = get_upstream_branch()
        if upstream_branch:
            compare_branch = upstream_branch
        else:
            # If no upstream branch, try to use the default branch
            default_branch = get_default_branch()
            if default_branch:
                print(f"⚠️ Warning: Current branch '{current_branch}' has no upstream branch. Comparing with default branch '{default_branch}' instead.")
                compare_branch = f'origin/{default_branch}'
            else:
                print(f"⚠️ Warning: Could not find an upstream or default branch to compare with.")
                return None

        # Check for unpushed commits
        unpushed_commits = subprocess.check_output(['git', 'log', f'{compare_branch}..HEAD']).decode().strip()
        
        if unpushed_commits:
            return unpushed_commits
        else:
            return None  # No unpushed commits

    except subprocess.CalledProcessError as e:
        print(f"⚠️ Error: Failed to check for unpushed commits. Git command returned error: {e}")
        return None
    except Exception as e:
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
