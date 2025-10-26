import subprocess
from pathlib import Path

STATE_FILE = Path(".last_git_state")


def repo_get_state() -> str:
    """Return a unique hash representing the current git state (HEAD + changes)."""
    head_hash = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    diff_hash = subprocess.check_output(["git", "diff"], text=True)
    return f"{head_hash}-{hash(diff_hash)}"


def repo_has_changed() -> bool:
    """Check if code has changed since last run."""
    current_state = repo_get_state()
    previous_state = STATE_FILE.read_text().strip() if STATE_FILE.exists() else None
    if current_state != previous_state:
        STATE_FILE.write_text(current_state)
        return True
    return False

def repo_has_changed_since(previous_state: str) -> bool:
    """Return True if the repo state has changed compared to a provided hash."""
    current_state = repo_get_state()
    return current_state != previous_state