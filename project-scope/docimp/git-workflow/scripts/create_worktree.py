#!/usr/bin/env python3
"""Create a new git worktree for the docimp project with complete setup.

This script automates the entire worktree setup process:
- Creates git worktree with new branch
- Sets up symlinks to shared resources (.planning, .scratch, .claude/*, etc.)
- Creates Python virtual environment (.venv)
- Installs all dependencies (production + dev)
- Enables direnv
- Optionally installs git hooks

Usage:
    # CLI mode (all options via command line)
    create_worktree.py <worktree-name> <branch-name> [--base-branch main]

    # Interactive mode (prompts for all options)
    create_worktree.py --interactive

Examples:
    create_worktree.py issue-221 issue-221-improve-styleguides
    create_worktree.py -i
    create_worktree.py feature-x feature-branch --base-branch develop
"""

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from collections.abc import Callable
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


def prompt_input(
    prompt: str,
    default: str | None = None,
    validator: Callable[[str], bool] | None = None,
    error_message: str = "Invalid input"
) -> str:
    """Prompt for user input with optional default and validation.

    Args:
        prompt: The prompt to display
        default: Default value (shown in brackets, used if user presses Enter)
        validator: Optional function that returns True if input is valid
        error_message: Message to show when validation fails

    Returns:
        The validated user input or default value
    """
    prompt_text = f"{Colors.BLUE}{prompt}"
    if default:
        prompt_text += f" [{default}]"
    prompt_text += f": {Colors.NC}"

    while True:
        user_input = input(prompt_text).strip()

        # Use default if empty input
        if not user_input and default:
            return default
        elif not user_input:
            print_warning("Input required")
            continue

        # Validate if validator provided
        if validator and not validator(user_input):
            print_warning(error_message)
            continue

        return user_input


def prompt_yes_no(prompt: str, default: bool = True) -> bool:
    """Prompt for yes/no input.

    Args:
        prompt: The prompt to display
        default: Default value (True for yes, False for no)

    Returns:
        True for yes, False for no
    """
    default_hint = "Y/n" if default else "y/N"
    prompt_text = f"{Colors.BLUE}{prompt} [{default_hint}]: {Colors.NC}"

    while True:
        user_input = input(prompt_text).strip().lower()

        if not user_input:
            return default
        elif user_input in ('y', 'yes'):
            return True
        elif user_input in ('n', 'no'):
            return False
        else:
            print_warning("Please enter 'y' or 'n'")


def get_local_branches() -> list[str]:
    """Get list of local branch names."""
    try:
        result = subprocess.run(
            ['git', 'branch', '--format=%(refname:short)'],
            capture_output=True, text=True, check=True
        )
        return [b.strip() for b in result.stdout.strip().split('\n') if b.strip()]
    except subprocess.CalledProcessError:
        return ['main']


def branch_exists(branch_name: str) -> bool:
    """Check if a branch already exists."""
    result = subprocess.run(
        ['git', 'show-ref', '--verify', '--quiet', f'refs/heads/{branch_name}'],
        capture_output=True
    )
    return result.returncode == 0


def worktree_path_exists(worktree_name: str) -> bool:
    """Check if a worktree path already exists."""
    worktree_path = Path('..') / worktree_name
    return worktree_path.exists()


def prompt_worktree_name(default: str | None = None) -> str:
    """Prompt for worktree directory name with validation.

    Args:
        default: Default value from CLI args

    Returns:
        Valid worktree name that doesn't already exist
    """
    def validate(name: str) -> bool:
        if worktree_path_exists(name):
            print_warning(f"Worktree already exists at ../{name}")
            return False
        return True

    return prompt_input(
        "Worktree directory name",
        default=default,
        validator=validate,
        error_message="Please choose a different name"
    )


def prompt_branch_name(worktree_name: str, default: str | None = None) -> str:
    """Prompt for branch name with validation.

    Args:
        worktree_name: Worktree name to suggest as default
        default: Default value from CLI args (takes precedence over worktree_name)

    Returns:
        Valid branch name that doesn't already exist
    """
    suggested_default = default or worktree_name

    def validate(name: str) -> bool:
        if branch_exists(name):
            print_warning(f"Branch '{name}' already exists")
            return False
        return True

    return prompt_input(
        "Git branch name",
        default=suggested_default,
        validator=validate,
        error_message="Please choose a different branch name"
    )


def prompt_base_branch(default: str | None = None) -> str:
    """Prompt for base branch with validation.

    Args:
        default: Default value from CLI args

    Returns:
        Valid base branch name that exists
    """
    branches = get_local_branches()
    suggested_default = default or 'main'

    # Show available branches
    print_info(f"Available branches: {', '.join(branches[:10])}")
    if len(branches) > 10:
        print_info(f"  ... and {len(branches) - 10} more")

    def validate(name: str) -> bool:
        if name not in branches:
            print_warning(f"Branch '{name}' does not exist")
            return False
        return True

    return prompt_input(
        "Base branch to create from",
        default=suggested_default,
        validator=validate,
        error_message="Please choose an existing branch"
    )


def run_interactive_prompts(args) -> None:
    """Run interactive prompts to populate args.

    Args:
        args: Parsed argparse namespace to populate
    """
    print()
    print_info("=== Interactive Worktree Setup ===")
    print()

    # Prompt for worktree name
    args.worktree_name = prompt_worktree_name(default=args.worktree_name)

    # Prompt for branch name (suggest worktree name as default)
    args.branch_name = prompt_branch_name(
        args.worktree_name,
        default=args.branch_name
    )

    # Prompt for base branch
    args.base_branch = prompt_base_branch(default=args.base_branch)

    # Prompt for verbose mode
    print()
    args.verbose = prompt_yes_no("Enable verbose output?", default=False)

    # Prompt for hooks installation
    args.install_hooks_if_missing = prompt_yes_no(
        "Auto-install git hooks if missing?",
        default=True
    )

    # Show confirmation summary
    print()
    print_info("=== Configuration Summary ===")
    print(f"  Worktree directory: ../{args.worktree_name}")
    print(f"  Branch name:        {args.branch_name}")
    print(f"  Base branch:        {args.base_branch}")
    print(f"  Verbose mode:       {'Yes' if args.verbose else 'No'}")
    print(f"  Auto-install hooks: {'Yes' if args.install_hooks_if_missing else 'No'}")
    print()

    if not prompt_yes_no("Proceed with these settings?", default=True):
        print_info("Aborted by user")
        sys.exit(0)

    print()


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
        epilog='Examples:\n'
               '  create_worktree.py issue-221 issue-221-improve-styleguides\n'
               '  create_worktree.py --interactive\n'
               '  create_worktree.py feature-x feature-branch --base-branch develop\n\n'
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
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Interactive mode: prompt for all options'
    )
    parser.add_argument(
        '--base-branch',
        default=None,
        help='Base branch to create worktree from (default: main)'
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

    # Validate we're in the docimp repo and get the repo root
    repo_root = validate_docimp_repo()

    # Change to repo root first (needed for interactive validation)
    if repo_root != Path('.'):
        if args.verbose:
            print_info(f"Changing to repository root: {repo_root}")
        import os
        os.chdir(repo_root)

    # Handle interactive mode
    if args.interactive:
        run_interactive_prompts(args)
    elif not args.worktree_name or not args.branch_name:
        parser.error("worktree_name and branch_name are required (use --interactive or --list-symlinks)")

    # Set default base branch if not specified
    if not args.base_branch:
        args.base_branch = 'main'

    # Ensure base branch is up to date
    if args.verbose:
        print_info(f"Ensuring {args.base_branch} branch is up to date...")
    run_git('checkout', args.base_branch)
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
