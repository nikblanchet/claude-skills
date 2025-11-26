#!/usr/bin/env python3
"""Create a new git worktree for the docimp project with complete setup.

This script automates the entire worktree setup process:
- Creates git worktree with new branch
- Sets up symlinks to shared resources (.planning, .scratch, .claude/*, etc.)
- Creates Python virtual environment (.venv)
- Installs all dependencies (production + dev)
- Enables direnv
- Optionally installs git hooks

Usage: create_worktree.py <worktree-name> <branch-name> [--install-hooks-if-missing]
Example: create_worktree.py issue-221 issue-221-improve-styleguides
"""

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import NoReturn


@dataclass
class SymlinkSpec:
    """Specification for a symlink to create in the worktree.

    Attributes:
        link_name: Path relative to worktree root where symlink should be created
        target: Relative path from symlink location to the target
        description: Human-readable description for documentation/messages
        required: If True, fail if target doesn't exist; if False, warn and skip
    """
    link_name: str
    target: str
    description: str
    required: bool = True


# Symlinks to create in each new worktree
# All paths are relative to worktree root
WORKTREE_SYMLINKS = [
    # Root-level shared files
    SymlinkSpec(
        link_name='CLAUDE.md',
        target='../.shared/CLAUDE.md',
        description='Main project context for Claude Code',
        required=True
    ),
    SymlinkSpec(
        link_name='CLAUDE_CONTEXT.md',
        target='../.shared/CLAUDE_CONTEXT.md',
        description='User-specific workflow preferences',
        required=True
    ),
    SymlinkSpec(
        link_name='.planning',
        target='../.shared/.planning',
        description='Shared planning documents',
        required=True
    ),
    SymlinkSpec(
        link_name='.scratch',
        target='../.shared/.scratch',
        description='Shared code reviews and runbooks',
        required=True
    ),

    # .claude directory shared resources
    SymlinkSpec(
        link_name='.claude/skills',
        target='../../.shared/.claude/skills',
        description='Project-specific Claude Code skills',
        required=True
    ),
    SymlinkSpec(
        link_name='.claude/agents',
        target='../../.shared/.claude/agents',
        description='Custom Claude Code agents',
        required=True
    ),
    SymlinkSpec(
        link_name='.claude/settings.local.json',
        target='../../.shared/.claude/settings.local.json',
        description='Shared local Claude Code settings',
        required=True
    ),
]


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


def exit_with_error(message: str, show_help_hint: bool = True) -> NoReturn:
    """Print error and exit with status 1.

    Args:
        message: Error message to display
        show_help_hint: Whether to show "Run with --help" hint
    """
    print_error(message)
    if show_help_hint:
        print_info("Run with --help for usage information")
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


def run_command(cmd: list[str], cwd: Path | None = None, check: bool = True, show_output: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return result.

    Args:
        cmd: Command and arguments to run
        cwd: Working directory to run command in
        check: Whether to raise on non-zero exit
        show_output: Whether to print stdout in real-time

    Returns:
        CompletedProcess result

    Raises:
        SystemExit: If command fails and check=True
    """
    try:
        if show_output:
            # Run with live output
            result = subprocess.run(cmd, cwd=cwd, check=check, text=True)
        else:
            # Capture output
            result = subprocess.run(cmd, cwd=cwd, check=check, capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        error_msg = f"Command failed: {' '.join(cmd)}"
        if e.stderr:
            error_msg += f"\n{e.stderr.strip()}"
        exit_with_error(error_msg)


def validate_docimp_repo() -> Path:
    """Validate we're in the docimp repository and return the repo root.

    Returns:
        Path to the repository root (where cli/ and analyzer/ are located)

    Raises:
        SystemExit: If not in a git repository or can't find docimp structure
    """
    # Check for .git (can be directory in main repo or file in worktree)
    if not Path('.git').exists():
        exit_with_error("Not in a git repository\nPlease run this script from the docimp repository or a worktree")

    # Try to find docimp structure in current directory or main/ subdirectory
    current = Path('.')
    main_subdir = Path('main')

    # Check current directory first
    if (current / 'cli' / 'package.json').exists() or (current / 'analyzer' / 'pyproject.toml').exists():
        return current

    # Check main/ subdirectory (running from parent)
    if (main_subdir / 'cli' / 'package.json').exists() or (main_subdir / 'analyzer' / 'pyproject.toml').exists():
        return main_subdir

    # Not found in either location
    exit_with_error(
        "Cannot find docimp repository structure (cli/ and analyzer/ directories)\n"
        "Please run this script from either:\n"
        "  1. The main worktree (where cli/ and analyzer/ are located)\n"
        "  2. The parent directory (where main/ worktree is located)"
    )


def check_hooks_installed() -> bool:
    """Check if git hooks are installed (non-.sample files exist)."""
    # Use git rev-parse to find the actual git directory (handles worktrees)
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--git-common-dir'],
            capture_output=True, text=True, check=True
        )
        git_common_dir = Path(result.stdout.strip())
        hooks_dir = git_common_dir / 'hooks'
    except subprocess.CalledProcessError:
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


def create_symlink(target: str, link_name: Path, verbose: bool = False) -> None:
    """Create a symlink and print success message.

    Validates that no file exists at link location before creating symlink.
    If symlink already exists and points to the correct target, skips creation.

    Args:
        target: Relative or absolute path to symlink target
        link_name: Path where symlink should be created
        verbose: Whether to show detailed progress messages

    Raises:
        SystemExit: If file exists at link location or symlink creation fails
    """
    # Check if link already exists
    if link_name.exists() or link_name.is_symlink():
        # If it's already a symlink to the correct target, skip
        if link_name.is_symlink() and link_name.readlink() == Path(target):
            if verbose:
                print_info(f"  Symlink already exists: {link_name.name}")
            return
        # Otherwise, refuse to overwrite
        exit_with_error(f"File or symlink already exists at {link_name}, refusing to overwrite")

    # Create the symlink
    try:
        link_name.symlink_to(target)
        if verbose:
            print_success(f"✓ Created symlink: {link_name.name}")
    except OSError as e:
        exit_with_error(f"Failed to create symlink {link_name.name}: {e}")


def validate_symlink_target(spec: SymlinkSpec, worktree_path: Path) -> bool:
    """Validate that a symlink target exists.

    Args:
        spec: Symlink specification
        worktree_path: Path to the worktree being created

    Returns:
        True if target exists or should proceed anyway, False to skip

    Raises:
        SystemExit: If required target doesn't exist
    """
    # Calculate expected link location
    link_path = worktree_path / spec.link_name

    # Resolve target path relative to link location
    # If link is at worktree/foo/bar and target is ../../../shared/baz,
    # we need to resolve from worktree/foo/bar's parent directories
    link_dir = link_path.parent
    target_path = (link_dir / spec.target).resolve()

    if target_path.exists():
        return True

    if spec.required:
        print_error(f"Required symlink target does not exist: {target_path}")
        print_error(f"For symlink: {spec.link_name} → {spec.target}")
        print_error(f"Description: {spec.description}")
        exit_with_error("Cannot create worktree with missing required symlink targets")

    # Optional target missing - warn and skip
    print_warning(f"Optional symlink target missing: {target_path}")
    print_warning(f"Skipping: {spec.link_name}")
    return True


def setup_python_environment(worktree_path: Path, verbose: bool = False) -> None:
    """Set up Python virtual environment in the worktree.

    Args:
        worktree_path: Path to the worktree directory
        verbose: Whether to show detailed progress messages

    Raises:
        SystemExit: If any setup command fails
    """
    if verbose:
        print()
        print_info("Setting up Python environment...")

    # Create virtual environment
    if verbose:
        print_info("  Creating virtual environment (.venv)...")
    run_command(['uv', 'venv'], cwd=worktree_path, show_output=verbose)

    # Path to the venv's python executable (used to ensure uv installs to THIS venv)
    venv_python = worktree_path / '.venv' / 'bin' / 'python'

    # Install dev dependencies with explicit --python flag
    # This ensures uv installs to the worktree's venv, not main's venv
    if verbose:
        print_info("  Installing dev dependencies...")
    run_command(['uv', 'pip', 'sync', '--python', str(venv_python), 'requirements-dev.lock'], cwd=worktree_path, show_output=verbose)

    # Install package in editable mode with explicit --python flag
    if verbose:
        print_info("  Installing docimp-analyzer in editable mode...")
    run_command(['uv', 'pip', 'install', '--python', str(venv_python), '-e', '.'], cwd=worktree_path, show_output=verbose)

    if verbose:
        print_success("✓ Python environment ready")


def enable_direnv(worktree_path: Path, verbose: bool = False) -> None:
    """Enable direnv for the worktree.

    Args:
        worktree_path: Path to the worktree directory
        verbose: Whether to show detailed progress messages

    Raises:
        SystemExit: If direnv command fails
    """
    if verbose:
        print()
        print_info("Enabling direnv...")

    try:
        run_command(['direnv', 'allow'], cwd=worktree_path, show_output=False)
        if verbose:
            print_success("✓ direnv enabled")
    except SystemExit:
        if verbose:
            print_warning("Failed to enable direnv - you may need to run 'direnv allow' manually")
            print_warning("This is non-critical and won't prevent the worktree from working")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Create a fully configured git worktree for the docimp project (includes symlinks, Python venv, dependencies, and direnv)',
        epilog='Example: create_worktree.py issue-221 issue-221-improve-styleguides\n\n'
               'Note: For token efficiency, avoid --verbose unless debugging the script.\n'
               'The default output is concise and optimized for AI assistants.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('worktree_name', nargs='?', help='Name of the worktree directory (e.g., issue-221)')
    parser.add_argument('branch_name', nargs='?', help='Name of the git branch (e.g., issue-221-improve-styleguides)')
    parser.add_argument(
        '--install-hooks-if-missing',
        action='store_true',
        help='Automatically install git hooks if missing (no prompt)'
    )
    parser.add_argument(
        '--list-symlinks',
        action='store_true',
        help='List all symlinks that would be created and exit'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output and full tracebacks on error (increases token usage)'
    )

    args = parser.parse_args()

    # Handle --list-symlinks flag (no worktree needed)
    if args.list_symlinks:
        print_info("Symlinks created by this script:")
        print()
        for spec in WORKTREE_SYMLINKS:
            print(f"  {spec.link_name}")
            print(f"    Target: {spec.target}")
            print(f"    Description: {spec.description}")
            print(f"    Required: {spec.required}")
            print()
        return 0

    # Validate required arguments for worktree creation
    if not args.worktree_name or not args.branch_name:
        parser.error("worktree_name and branch_name are required (unless using --list-symlinks)")

    # Validate we're in the docimp repo and get the repo root
    repo_root = validate_docimp_repo()

    # Change to repo root if we're in parent directory
    if repo_root != Path('.'):
        if args.verbose:
            print_info(f"Changing to repository root: {repo_root}")
        import os
        os.chdir(repo_root)

    # Ensure main is up to date
    if args.verbose:
        print_info("Ensuring main branch is up to date...")
    run_git('checkout', 'main')
    run_git('pull')

    # Create worktrees directory if needed
    worktree_dir = Path('..')
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
    if args.verbose:
        print_info(f"Creating worktree: {worktree_path}")
    run_git('worktree', 'add', str(worktree_path), '-b', args.branch_name)

    # Create symlinks with cleanup on failure
    try:
        if args.verbose:
            print_info("Creating symlinks to shared files...")

        # Pre-validate all required targets exist
        for spec in WORKTREE_SYMLINKS:
            validate_symlink_target(spec, worktree_path)

        # Create parent directories as needed
        parent_dirs_created = set()
        for spec in WORKTREE_SYMLINKS:
            link_path = worktree_path / spec.link_name
            parent_dir = link_path.parent

            if parent_dir != worktree_path and parent_dir not in parent_dirs_created:
                parent_dir.mkdir(parents=True, exist_ok=True)
                parent_dirs_created.add(parent_dir)

        # Create all symlinks
        for spec in WORKTREE_SYMLINKS:
            link_path = worktree_path / spec.link_name
            create_symlink(spec.target, link_path, verbose=args.verbose)

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

    # Print success summary (verbose or concise based on --verbose flag)
    if args.verbose:
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
        for spec in WORKTREE_SYMLINKS:
            print(f"  ✓ {spec.link_name} → {spec.target}")
        print()

    # Check/install hooks
    if args.install_hooks_if_missing:
        if not check_hooks_installed():
            install_hooks()
    else:
        prompt_install_hooks()

    # Set up Python environment
    setup_python_environment(worktree_path, verbose=args.verbose)

    # Enable direnv
    enable_direnv(worktree_path, verbose=args.verbose)

    # Print final status (concise by default, detailed with --verbose)
    print()
    if args.verbose:
        print_success("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print_success("✓ Worktree fully configured and ready!")
        print_success("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print()
        print_info("Your new worktree is ready to use:")
        print(f"  cd {worktree_path}")
        print()
        print_info("Everything is set up:")
        print("  ✓ Git worktree created")
        print("  ✓ Symlinks to shared resources")
        print("  ✓ Python virtual environment (.venv)")
        print("  ✓ Dev dependencies installed")
        print("  ✓ docimp-analyzer installed (editable mode)")
        print("  ✓ direnv enabled")
        print()
        print_info("To view all worktrees:")
        print("  git worktree list")
        print()
    else:
        # Concise output optimized for token efficiency
        print_success(f"✓ Worktree ready: {worktree_path} (branch: {args.branch_name})")
        print(f"  cd {worktree_path}")

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        # Get verbose flag from sys.argv to handle exceptions before argparse
        verbose = '--verbose' in sys.argv or '-v' in sys.argv
        if verbose:
            # Show full traceback in verbose mode
            raise
        else:
            # Concise error in normal mode
            print_error(f"Error: {str(e)}")
            print_info("Run with --help for usage information")
            print_info("Run with --verbose for detailed error information")
            sys.exit(1)
