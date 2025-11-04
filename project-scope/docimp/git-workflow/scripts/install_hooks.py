#!/usr/bin/env python3
"""Install git hooks to protect main branch in the docimp repository.

This script copies hook files from scripts/hooks/ to .git/hooks/ and makes them executable.
It's idempotent and safe to run multiple times.

Usage: install_hooks.py
"""

import shutil
import sys
from pathlib import Path
from typing import NoReturn


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


def print_error(message: str) -> None:
    """Print error message in red."""
    print(f"{Colors.RED}Error: {message}{Colors.NC}", file=sys.stderr)


def print_info(message: str) -> None:
    """Print info message in blue."""
    print(f"{Colors.BLUE}{message}{Colors.NC}")


def print_success(message: str) -> None:
    """Print success message in green."""
    print(f"{Colors.GREEN}{message}{Colors.NC}")


def print_warning(message: str) -> None:
    """Print warning message in yellow."""
    print(f"{Colors.YELLOW}{message}{Colors.NC}")


def exit_with_error(message: str) -> NoReturn:
    """Print error and exit with status 1."""
    print_error(message)
    sys.exit(1)


def validate_git_repo() -> None:
    """Validate we're in a git repository."""
    if not Path('.git').is_dir():
        exit_with_error("Not in a git repository\nPlease run this script from the repository root")


def get_hooks_source_dir() -> Path:
    """Get the source directory containing hook files."""
    # Script is in .claude/skills/git-workflow/scripts/ (via symlink)
    # Hooks are in .claude/skills/git-workflow/scripts/hooks/
    script_dir = Path(__file__).parent.resolve()
    hooks_dir = script_dir / 'hooks'

    if not hooks_dir.exists():
        exit_with_error(f"Hooks directory not found at {hooks_dir}")

    return hooks_dir


def install_hook(hook_source: Path, hooks_target_dir: Path) -> None:
    """Install a single hook file.

    Validates that hook has a valid shebang before installation.
    """
    hook_name = hook_source.name
    hook_target = hooks_target_dir / hook_name

    # Validate shebang exists
    with open(hook_source, 'r') as f:
        first_line = f.readline()
        if not first_line.startswith('#!'):
            print_warning(f"Warning: {hook_name} missing shebang (starts with '{first_line[:20]}')")

    # Copy the hook file
    shutil.copy2(hook_source, hook_target)

    # Make executable (chmod +x)
    hook_target.chmod(0o755)

    print_success(f"✓ Installed: {hook_name}")


def main() -> int:
    """Main entry point."""
    # Validate we're in a git repository
    validate_git_repo()

    # Get source and target directories
    hooks_source_dir = get_hooks_source_dir()
    hooks_target_dir = Path('.git/hooks')

    if not hooks_target_dir.exists():
        exit_with_error(f"Git hooks directory not found at {hooks_target_dir}")

    # Find all hook files (non-directory files in hooks/)
    hook_files = [f for f in hooks_source_dir.iterdir() if f.is_file()]

    if not hook_files:
        exit_with_error(f"No hook files found in {hooks_source_dir}")

    print_info("Installing git hooks...")

    # Install each hook
    for hook_file in sorted(hook_files):
        install_hook(hook_file, hooks_target_dir)

    print()
    print_success("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print_success("✓ Git hooks installed successfully!")
    print_success("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    print_info("What the hooks do:")
    print("  pre-commit:    Blocks commits on main branch")
    print("  post-checkout: Blocks branch checkouts in main worktree")
    print()
    print_info("To bypass hooks temporarily (for maintenance):")
    print("  git commit --no-verify")
    print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
