#!/usr/bin/env python3
"""Create a new git worktree for the docimp project with all necessary symlinks.

Usage: create_worktree.py <worktree-name> <branch-name> [--install-hooks-if-missing]
Example: create_worktree.py issue-221 issue-221-improve-styleguides
"""

import argparse
import subprocess
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


def run_git(*args: str, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    """Run git command and return result."""
    try:
        return subprocess.run(
            ['git'] + list(args),
            cwd=cwd,
            check=check,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        exit_with_error(f"Git command failed: {e.stderr.strip()}")


def validate_docimp_repo() -> None:
    """Validate we're in the docimp repository."""
    if not Path('.git').is_dir():
        exit_with_error("Not in a git repository\nPlease run this script from the docimp main repository directory")

    if not Path('cli/package.json').exists() and not Path('analyzer/setup.py').exists():
        print_warning("Warning: This doesn't appear to be the docimp repository")
        print("Are you in the correct directory?")
        response = input("Continue anyway? (y/N) ").strip().lower()
        if response not in ('y', 'yes'):
            sys.exit(1)


def check_hooks_installed() -> bool:
    """Check if git hooks are installed (non-.sample files exist)."""
    hooks_dir = Path('.git/hooks')
    if not hooks_dir.exists():
        return False

    # Check for any non-.sample hook files
    for hook_file in hooks_dir.iterdir():
        if hook_file.is_file() and not hook_file.name.endswith('.sample'):
            return True

    return False


def install_hooks() -> None:
    """Call install_hooks.py to install git hooks."""
    install_hooks_script = Path(__file__).parent / 'install_hooks.py'

    if not install_hooks_script.exists():
        exit_with_error(f"install_hooks.py not found at {install_hooks_script}")

    try:
        result = subprocess.run(
            [sys.executable, str(install_hooks_script)],
            check=True,
            capture_output=True,
            text=True
        )
        # Forward stdout (success messages from install_hooks.py)
        if result.stdout:
            print(result.stdout, end='')
    except subprocess.CalledProcessError as e:
        # Show detailed error message with stderr if available
        error_msg = f"Failed to install hooks: {e.stderr.strip()}" if e.stderr else "Failed to install hooks"
        exit_with_error(error_msg)


def prompt_install_hooks() -> None:
    """Prompt user to install hooks if not already installed."""
    if check_hooks_installed():
        return  # Hooks already installed

    print_warning("\nGit hooks not installed!")
    print("Hooks protect the main branch from accidental commits and checkouts.")
    response = input("Install hooks now? [Y/n] ").strip().lower()

    if response in ('', 'y', 'yes'):
        install_hooks()


def create_symlink(target: str, link_name: Path) -> None:
    """Create a symlink and print success message.

    Validates that no file exists at link location before creating symlink.
    If symlink already exists and points to the correct target, skips creation.

    Args:
        target: Relative or absolute path to symlink target
        link_name: Path where symlink should be created

    Raises:
        SystemExit: If file exists at link location or symlink creation fails
    """
    # Check if link already exists
    if link_name.exists() or link_name.is_symlink():
        # If it's already a symlink to the correct target, skip
        if link_name.is_symlink() and link_name.readlink() == Path(target):
            print_info(f"  Symlink already exists: {link_name.name}")
            return
        # Otherwise, refuse to overwrite
        exit_with_error(f"File or symlink already exists at {link_name}, refusing to overwrite")

    # Create the symlink
    try:
        link_name.symlink_to(target)
        print_success(f"✓ Created symlink: {link_name.name}")
    except OSError as e:
        exit_with_error(f"Failed to create symlink {link_name.name}: {e}")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Create a new git worktree for the docimp project with all necessary symlinks',
        epilog='Example: create_worktree.py issue-221 issue-221-improve-styleguides'
    )
    parser.add_argument('worktree_name', help='Name of the worktree directory (e.g., issue-221)')
    parser.add_argument('branch_name', help='Name of the git branch (e.g., issue-221-improve-styleguides)')
    parser.add_argument(
        '--install-hooks-if-missing',
        action='store_true',
        help='Automatically install git hooks if missing (no prompt)'
    )

    args = parser.parse_args()

    # Validate we're in the docimp repo
    validate_docimp_repo()

    # Ensure main is up to date
    print_info("Ensuring main branch is up to date...")
    run_git('checkout', 'main')
    run_git('pull')

    # Create worktrees directory if needed
    worktree_dir = Path('../.docimp-wt')
    if not worktree_dir.exists():
        print_info(f"Creating worktrees directory: {worktree_dir}")
        worktree_dir.mkdir(parents=True)

    # Check if worktree already exists
    worktree_path = worktree_dir / args.worktree_name
    if worktree_path.exists():
        exit_with_error(f"Worktree already exists at {worktree_path}")

    # Check if branch already exists
    result = run_git('show-ref', '--verify', '--quiet', f'refs/heads/{args.branch_name}', check=False)
    if result.returncode == 0:
        exit_with_error(f"Branch '{args.branch_name}' already exists\nUse a different branch name or delete the existing branch first")

    # Create the worktree
    print_info(f"Creating worktree: {worktree_path}")
    run_git('worktree', 'add', str(worktree_path), '-b', args.branch_name)

    # Create symlinks with cleanup on failure
    try:
        print_info("Creating symlinks to shared files...")

        # Root-level symlinks
        create_symlink('../../.docimp-shared/CLAUDE.md', worktree_path / 'CLAUDE.md')
        create_symlink('../../.docimp-shared/CLAUDE.md', worktree_path / 'WARP.md')
        create_symlink('../../.docimp-shared/CLAUDE_CONTEXT.md', worktree_path / 'CLAUDE_CONTEXT.md')
        create_symlink('../../.docimp-shared/.planning', worktree_path / '.planning')
        create_symlink('../../.docimp-shared/.scratch', worktree_path / '.scratch')

        # docs/patterns symlink
        docs_dir = worktree_path / 'docs'
        docs_dir.mkdir(exist_ok=True)
        create_symlink('../../../.docimp-shared/docs/patterns', docs_dir / 'patterns')

        # .claude directory symlinks
        claude_dir = worktree_path / '.claude'
        claude_dir.mkdir(exist_ok=True)
        create_symlink('../../../.docimp-shared/.claude/skills', claude_dir / 'skills')
        create_symlink('../../../.docimp-shared/.claude/settings.local.json', claude_dir / 'settings.local.json')
    except SystemExit as e:
        # Cleanup on failure - remove the worktree
        print_error(f"Symlink creation failed")
        print_info("Cleaning up worktree...")
        try:
            run_git('worktree', 'remove', str(worktree_path), '--force')
            print_info("Worktree removed successfully")
        except Exception as cleanup_error:
            print_warning(f"Failed to clean up worktree: {cleanup_error}")
            print_warning(f"Please manually remove: git worktree remove {worktree_path}")
        # Re-raise to preserve original exit code
        raise

    # Print success summary
    print()
    print_success("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print_success("✓ Worktree created successfully!")
    print_success("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    print_info("Worktree details:")
    print(f"  Location: {worktree_path}")
    print(f"  Branch:   {args.branch_name}")
    print()
    print_info("All symlinks created:")
    print("  ✓ CLAUDE.md → ../../.docimp-shared/CLAUDE.md")
    print("  ✓ WARP.md → ../../.docimp-shared/CLAUDE.md")
    print("  ✓ CLAUDE_CONTEXT.md → ../../.docimp-shared/CLAUDE_CONTEXT.md")
    print("  ✓ .planning → ../../.docimp-shared/.planning")
    print("  ✓ .scratch → ../../.docimp-shared/.scratch")
    print("  ✓ docs/patterns → ../../../.docimp-shared/docs/patterns")
    print("  ✓ .claude/skills → ../../../.docimp-shared/.claude/skills")
    print("  ✓ .claude/settings.local.json → ../../../.docimp-shared/.claude/settings.local.json")
    print()

    # Check/install hooks
    if args.install_hooks_if_missing:
        if not check_hooks_installed():
            install_hooks()
    else:
        prompt_install_hooks()

    # Print next steps
    print()
    print_info("Next steps:")
    print(f"  cd {worktree_path}")
    print("  # Open in Claude Code or your editor")
    print()
    print_info("To view all worktrees:")
    print("  git worktree list")
    print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
