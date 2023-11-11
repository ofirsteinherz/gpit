import subprocess

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

def stage_changes():
    """Stage all changes in the repository."""
    subprocess.run(['git', 'add', '.'])
    
def commit_changes(commit_message):
    """Commit changes with a given message."""
    subprocess.run(['git', 'commit', '-m', commit_message])

def push_changes(branch_name='main'):
    """Push changes to the remote repository."""
    subprocess.run(['git', 'push', 'origin', branch_name])
