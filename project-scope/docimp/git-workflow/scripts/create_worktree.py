#!/usr/bin/env python3
"""Create a new git worktree for the docimp project with all necessary symlinks.

This script creates a new worktree branched from a specified source branch (default: main).
It automatically detects if the source branch is checked out in another worktree and offers
to include uncommitted changes and/or unpushed commits from that worktree.

Usage:
    create_worktree.py <worktree-name> <branch-name> [OPTIONS]

Positional Arguments:
    worktree-name       Name of the worktree directory (e.g., issue-221)
    branch-name         Name of the git branch (e.g., issue-221-improve-styleguides)

Options:
    --source-branch SOURCE
        Branch to create the new branch from (default: main)
        Supports local branches (e.g., feature-xyz) and remote branches (e.g., origin/feature-xyz)

    --include-changes {none,uncommitted,unpushed,all}
        Include changes from source worktree (non-interactive mode)
        - none: Branch from last pushed commit (excludes all local work)
        - uncommitted: Include uncommitted changes only
        - unpushed: Include unpushed commits only
        - all: Include both uncommitted changes and unpushed commits

    --exclude-changes
        Exclude all changes from source worktree (same as --include-changes=none)

    --install-hooks-if-missing
        Automatically install git hooks if missing (no prompt)

Interactive Mode:
    When the source branch is checked out in a worktree and has uncommitted changes
    or unpushed commits, the script will prompt you to choose what to include.
    This prompt is skipped if --include-changes or --exclude-changes is specified.

Examples:
    # Basic usage (branches from main)
    create_worktree.py issue-221 issue-221-improve-styleguides

    # Branch from feature branch
    create_worktree.py issue-123 fix-parser --source-branch feature-validation

    # Branch from remote branch
    create_worktree.py issue-456 nested-fix --source-branch origin/feature-xyz

    # Include all changes from source worktree (non-interactive)
    create_worktree.py issue-200 quick-fix --source-branch issue-150 --include-changes=all

    # Exclude all local changes (non-interactive)
    create_worktree.py issue-200 clean-branch --source-branch issue-150 --exclude-changes

What This Script Does:
    1. Validates source branch exists (local or remote)
    2. Finds worktree containing source branch (if any)
    3. Detects uncommitted changes and unpushed commits
    4. Prompts to include changes (unless flags specify behavior)
    5. Creates new worktree in ../.docimp-wt/<worktree-name>/
    6. Creates all necessary symlinks to shared files
    7. Configures Husky hooks for the worktree
    8. Installs npm dependencies
"""

import argparse
import os
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


def configure_husky_hooks(worktree_path: Path) -> None:
    """Configure Husky hooks for the new worktree.

    Sets up per-worktree git config and generates Husky dispatcher files.
    Handles errors gracefully - warns but doesn't fail if configuration fails.

    Args:
        worktree_path: Path to the newly created worktree
    """
    print_info("Configuring Husky hooks...")

    try:
        # Enable per-worktree config (one-time, safe to run multiple times)
        subprocess.run(
            ['git', 'config', 'extensions.worktreeConfig', 'true'],
            cwd=worktree_path,
            check=True,
            capture_output=True,
            text=True
        )

        # Set worktree-specific hooksPath
        # Use git rev-parse to get the absolute path to the worktree root
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            cwd=worktree_path,
            check=True,
            capture_output=True,
            text=True
        )
        worktree_root = result.stdout.strip()
        hooks_path = f"{worktree_root}/.husky/_"

        subprocess.run(
            ['git', 'config', '--worktree', 'core.hooksPath', hooks_path],
            cwd=worktree_path,
            check=True,
            capture_output=True,
            text=True
        )

        # Generate Husky dispatcher files
        try:
            subprocess.run(
                ['npx', 'husky'],
                cwd=worktree_path,
                check=True,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout for npx
            )
            print_success("✓ Configured Husky hooks for worktree")
        except FileNotFoundError:
            print_warning("Warning: npx not found - Husky hooks not configured")
            print_warning("Install Node.js/npm and run 'npx husky' manually in the worktree")
        except subprocess.TimeoutExpired:
            print_warning("Warning: npx husky timed out - Husky hooks may not be fully configured")
        except subprocess.CalledProcessError as e:
            print_warning(f"Warning: Failed to run 'npx husky': {e.stderr.strip() if e.stderr else 'unknown error'}")
            print_warning("You may need to run 'npx husky' manually in the worktree")

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else 'unknown error'
        print_warning(f"Warning: Failed to configure Husky hooks: {error_msg}")
        print_warning("You can configure manually by running:")
        print_warning("  git config extensions.worktreeConfig true")
        print_warning(f"  git config --worktree core.hooksPath \"$(git rev-parse --show-toplevel)/.husky/_\"")
        print_warning("  npx husky")


def enable_direnv(worktree_path: Path) -> None:
    """Enable direnv for the new worktree.

    Runs 'direnv allow' to authorize the .envrc file in the worktree.
    This is required for direnv to automatically load the environment
    when entering the worktree directory.
    Handles errors gracefully - warns but doesn't fail if direnv unavailable.

    Args:
        worktree_path: Path to the newly created worktree
    """
    envrc_path = worktree_path / '.envrc'

    if not envrc_path.exists():
        print_info("No .envrc file found - skipping direnv setup")
        return

    print_info("Enabling direnv for worktree...")

    try:
        result = subprocess.run(
            ['direnv', 'allow'],
            cwd=worktree_path,
            check=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        print_success("✓ direnv enabled - environment will auto-load on cd")
    except FileNotFoundError:
        print_warning("Warning: direnv not found - .envrc will not auto-load")
        print_warning("Install direnv: brew install direnv")
        print_warning(f"Then run: cd {worktree_path} && direnv allow")
    except subprocess.TimeoutExpired:
        print_warning("Warning: direnv allow timed out")
        print_warning(f"You may need to run 'direnv allow' manually in {worktree_path}")
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else 'unknown error'
        print_warning(f"Warning: direnv allow failed: {error_msg}")
        print_warning(f"You can enable manually by running:")
        print_warning(f"  cd {worktree_path}")
        print_warning("  direnv allow")


def install_npm_dependencies(worktree_path: Path) -> None:
    """Install npm dependencies and build TypeScript in the cli directory.

    Runs npm install followed by npm run build in the cli/ directory to ensure
    all dependencies are available and TypeScript is compiled to dist/.
    The build step is required for Python tests to find the TypeScript parser helper.
    Handles errors gracefully - warns but doesn't fail if installation or build fails.

    Args:
        worktree_path: Path to the newly created worktree
    """
    cli_path = worktree_path / 'cli'

    if not cli_path.exists():
        print_warning("Warning: cli/ directory not found in worktree")
        print_warning("Skipping npm install")
        return

    print_info("Installing npm dependencies (this may take 30-60 seconds)...")

    try:
        result = subprocess.run(
            ['npm', 'install'],
            cwd=cli_path,
            check=True,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout for npm install
        )
        print_success("✓ npm dependencies installed successfully")

        # Show any warnings from npm (but not the full verbose output)
        if result.stderr and 'warn' in result.stderr.lower():
            # Just show first few lines of warnings
            warn_lines = [line for line in result.stderr.split('\n') if 'warn' in line.lower()][:3]
            if warn_lines:
                for line in warn_lines:
                    print_warning(f"  npm: {line}")

    except FileNotFoundError:
        print_warning("Warning: npm not found - dependencies not installed")
        print_warning("Install Node.js/npm and run 'npm install' in cli/ directory")
        return  # Skip build if npm not found
    except subprocess.TimeoutExpired:
        print_warning("Warning: npm install timed out after 5 minutes")
        print_warning("You may need to run 'npm install' manually in cli/")
        return  # Skip build if install timed out
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else 'unknown error'
        print_warning(f"Warning: npm install failed: {error_msg}")
        print_warning("You can install manually by running:")
        print_warning(f"  cd {cli_path}")
        print_warning("  npm install")
        return  # Skip build if install failed

    # Build TypeScript after successful install
    print_info("Building TypeScript (this may take 10-30 seconds)...")

    try:
        result = subprocess.run(
            ['npm', 'run', 'build'],
            cwd=cli_path,
            check=True,
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout for build
        )
        print_success("✓ TypeScript compiled successfully")

        # Show any build warnings (but not the full verbose output)
        if result.stderr and 'warning' in result.stderr.lower():
            warn_lines = [line for line in result.stderr.split('\n') if 'warning' in line.lower()][:3]
            if warn_lines:
                for line in warn_lines:
                    print_warning(f"  tsc: {line}")

    except subprocess.TimeoutExpired:
        print_warning("Warning: npm run build timed out after 2 minutes")
        print_warning("You may need to run 'npm run build' manually in cli/")
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else 'unknown error'
        print_warning(f"Warning: npm run build failed: {error_msg}")
        print_warning("You can build manually by running:")
        print_warning(f"  cd {cli_path}")
        print_warning("  npm run build")


def setup_python_venv(worktree_path: Path) -> None:
    """Create per-worktree Python virtual environment using uv's managed Python.

    Uses 'uv python install' to download and manage an isolated Python version,
    then creates .venv using 'uv venv --python X.Y'. This approach provides
    containerization - Python is isolated from system Python and managed by uv.
    This prevents lock contention and conflicts when multiple worktrees
    run Python commands simultaneously.

    Args:
        worktree_path: Path to the newly created worktree
    """
    print_info("Setting up isolated Python environment...")

    # Read Python version from .python-version file
    python_version_file = worktree_path / '.python-version'
    python_version = None
    if python_version_file.exists():
        try:
            python_version = python_version_file.read_text().strip()
        except Exception:
            pass

    if not python_version:
        python_version = '3.13'  # Default fallback

    # Ensure uv has the requested Python version installed (managed by uv)
    # This downloads an isolated Python if not already present
    print_info(f"Ensuring Python {python_version} is available via uv...")
    try:
        subprocess.run(
            ['uv', 'python', 'install', python_version],
            check=True,
            capture_output=True,
            text=True,
            timeout=120  # Allow time for download if needed
        )
    except FileNotFoundError:
        raise RuntimeError(
            "uv not found. Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError(
            f"Python {python_version} download timed out. Check network connection."
        )
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else 'unknown error'
        raise RuntimeError(
            f"Failed to install Python {python_version} via uv: {error_msg}"
        )

    # Create venv using uv's managed Python
    print_info("Creating per-worktree virtual environment...")
    try:
        result = subprocess.run(
            ['uv', 'venv', '--python', python_version],
            cwd=worktree_path,
            check=True,
            capture_output=True,
            text=True,
            timeout=30  # Should be fast with managed Python
        )

        # Verify Python version
        venv_python = worktree_path / '.venv' / 'bin' / 'python'
        version_result = subprocess.run(
            [str(venv_python), '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        actual_version = version_result.stdout.strip()
        print_success(f"✓ Virtual environment created with isolated {actual_version}")
        print_success(f"✓ Python managed by uv (containerized, not system Python)")
    except subprocess.TimeoutExpired:
        raise RuntimeError(
            "Virtual environment creation timed out. This may indicate a uv issue."
        )
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else 'unknown error'
        raise RuntimeError(
            f"Failed to create virtual environment with uv: {error_msg}"
        )

    # Install dependencies into the worktree's venv using uv sync
    # uv sync automatically uses the local .venv and installs from uv.lock
    print_info("Installing Python dependencies...")

    try:
        result = subprocess.run(
            ['uv', 'sync', '--extra', 'dev'],
            cwd=worktree_path,
            check=True,
            capture_output=True,
            text=True,
            timeout=120
        )
        print_success("✓ Dependencies installed (anthropic, pytest, ruff, mypy)")
    except subprocess.TimeoutExpired:
        raise RuntimeError(
            "Dependency installation timed out. Check network connection."
        )
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else 'unknown error'
        raise RuntimeError(
            f"Failed to install dependencies: {error_msg}"
        )


def setup_node_version(worktree_path: Path) -> None:
    """Ensure Node version specified in .nvmrc is installed in worktree.

    Uses nvm to install the Node version if .nvmrc exists.
    This ensures the worktree has the correct containerized Node version
    matching the project requirements, similar to Python's uv-managed environment.
    Handles errors gracefully - warns but doesn't fail if nvm unavailable.

    Args:
        worktree_path: Path to the newly created worktree
    """
    nvmrc_path = worktree_path / '.nvmrc'

    if not nvmrc_path.exists():
        print_info("No .nvmrc file found - skipping Node version setup")
        return

    try:
        node_version = nvmrc_path.read_text().strip()
    except Exception:
        print_warning("Failed to read .nvmrc - skipping Node version setup")
        return

    print_info(f"Ensuring Node {node_version} is installed via nvm...")

    # Check if nvm is available
    try:
        subprocess.run(
            ['bash', '-c', 'source ~/.nvm/nvm.sh && nvm --version'],
            check=True,
            capture_output=True,
            text=True,
            timeout=10
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        print_warning("nvm not found - Node version not managed automatically")
        print_warning("Install nvm: https://github.com/nvm-sh/nvm")
        print_warning(f"Then run: cd {worktree_path} && nvm install {node_version}")
        return
    except subprocess.TimeoutExpired:
        print_warning("nvm check timed out")
        return

    # Install the Node version if not already present
    # Note: 'nvm install' is idempotent - it won't re-download if already installed
    try:
        result = subprocess.run(
            ['bash', '-c', f'source ~/.nvm/nvm.sh && nvm install {node_version}'],
            cwd=worktree_path,
            check=True,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes for download if needed
        )
        print_success(f"✓ Node {node_version} ready (nvm)")
    except subprocess.TimeoutExpired:
        print_warning(f"Node {node_version} installation timed out")
        print_warning(f"Run manually: cd {worktree_path} && nvm install {node_version}")
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else 'unknown error'
        print_warning(f"Failed to setup Node version: {error_msg}")
        print_warning(f"Run manually: cd {worktree_path} && nvm install {node_version}")


def validate_source_branch(branch_name: str) -> tuple[bool, str]:
    """Validate that the source branch exists (local or remote).

    Args:
        branch_name: Name of the branch to validate (e.g., 'main', 'feature-xyz', 'origin/feature-xyz')

    Returns:
        Tuple of (is_valid, branch_type) where branch_type is 'local', 'remote', or empty string if invalid
    """
    # Check if it's a local branch
    result = run_git('show-ref', '--verify', '--quiet', f'refs/heads/{branch_name}', check=False)
    if result.returncode == 0:
        return (True, 'local')

    # Check if it's a remote branch
    result = run_git('show-ref', '--verify', '--quiet', f'refs/remotes/{branch_name}', check=False)
    if result.returncode == 0:
        return (True, 'remote')

    return (False, '')


def find_worktree_for_branch(branch_name: str) -> Path | None:
    """Find the worktree path that has the specified branch checked out.

    Args:
        branch_name: Name of the branch to find (e.g., 'main', 'issue-123')

    Returns:
        Path to worktree if found, None if branch not checked out in any worktree
    """
    result = run_git('worktree', 'list', '--porcelain', check=False)
    if result.returncode != 0:
        return None

    current_worktree = None
    current_branch = None

    for line in result.stdout.strip().split('\n'):
        if line.startswith('worktree '):
            current_worktree = Path(line.split(' ', 1)[1])
        elif line.startswith('branch '):
            # Extract branch name from refs/heads/<branch>
            current_branch = line.split('refs/heads/', 1)[1] if 'refs/heads/' in line else None
        elif line == '':
            # End of worktree entry
            if current_branch == branch_name and current_worktree:
                return current_worktree
            current_worktree = None
            current_branch = None

    # Check last entry
    if current_branch == branch_name and current_worktree:
        return current_worktree

    return None


def check_local_changes(worktree_path: Path) -> dict:
    """Check for uncommitted and unpushed changes in specified worktree.

    Args:
        worktree_path: Path to the worktree to check

    Returns:
        Dictionary with:
            - uncommitted: bool (has uncommitted changes)
            - uncommitted_output: str (git status output)
            - unpushed: bool (has unpushed commits)
            - unpushed_count: int (number of unpushed commits)
            - unpushed_log: str (formatted log of unpushed commits)
    """
    changes = {
        'uncommitted': False,
        'uncommitted_output': '',
        'unpushed': False,
        'unpushed_count': 0,
        'unpushed_log': ''
    }

    # Check for uncommitted changes
    status_result = run_git('status', '--porcelain', cwd=worktree_path, check=False)
    if status_result.returncode == 0 and status_result.stdout.strip():
        changes['uncommitted'] = True
        changes['uncommitted_output'] = status_result.stdout

    # Check for unpushed commits (requires upstream branch)
    # First check if upstream exists
    upstream_result = run_git('rev-parse', '--abbrev-ref', '@{u}', cwd=worktree_path, check=False)
    if upstream_result.returncode == 0:
        # Count unpushed commits
        count_result = run_git('rev-list', '--count', '@{u}..HEAD', cwd=worktree_path, check=False)
        if count_result.returncode == 0:
            count = int(count_result.stdout.strip())
            if count > 0:
                changes['unpushed'] = True
                changes['unpushed_count'] = count

                # Get formatted log of unpushed commits
                log_result = run_git(
                    'log', '@{u}..HEAD', '--oneline', '--no-decorate',
                    cwd=worktree_path, check=False
                )
                if log_result.returncode == 0:
                    changes['unpushed_log'] = log_result.stdout.strip()

    return changes


def prompt_include_changes(branch_name: str, worktree_path: Path, changes_info: dict) -> str:
    """Prompt user about including changes from source worktree.

    Args:
        branch_name: Name of the source branch
        worktree_path: Path to the source worktree
        changes_info: Dictionary from check_local_changes()

    Returns:
        'none' | 'uncommitted' | 'unpushed' | 'all'
    """
    print()
    print_info(f"Changes detected in source worktree: {worktree_path}")
    print()

    # Show uncommitted changes
    if changes_info['uncommitted']:
        print_warning("Uncommitted changes:")
        # Show first 10 lines of status output
        lines = changes_info['uncommitted_output'].strip().split('\n')
        for line in lines[:10]:
            print(f"  {line}")
        if len(lines) > 10:
            print(f"  ... and {len(lines) - 10} more files")
        print()

    # Show unpushed commits
    if changes_info['unpushed']:
        print_warning(f"Unpushed commits ({changes_info['unpushed_count']}):")
        for line in changes_info['unpushed_log'].split('\n')[:5]:
            print(f"  {line}")
        if changes_info['unpushed_count'] > 5:
            print(f"  ... and {changes_info['unpushed_count'] - 5} more commits")
        print()

    # Build menu options based on what changes exist
    print("Include changes in new worktree?")
    options = {}
    option_num = 1

    # Always offer "none"
    options[str(option_num)] = 'none'
    print(f"  {option_num}. None (branch from last pushed commit)")
    option_num += 1

    # Offer uncommitted if they exist
    if changes_info['uncommitted']:
        options[str(option_num)] = 'uncommitted'
        print(f"  {option_num}. Uncommitted only")
        option_num += 1

    # Offer unpushed if they exist
    if changes_info['unpushed']:
        options[str(option_num)] = 'unpushed'
        print(f"  {option_num}. Unpushed commits only")
        option_num += 1

    # Offer "all" if both exist
    if changes_info['uncommitted'] and changes_info['unpushed']:
        options[str(option_num)] = 'all'
        print(f"  {option_num}. All changes (uncommitted + unpushed)")
        default_choice = str(option_num)
    elif changes_info['uncommitted']:
        default_choice = '2'  # Uncommitted only
    elif changes_info['unpushed']:
        default_choice = '2'  # Unpushed only
    else:
        default_choice = '1'  # None

    print()

    # Get user choice
    while True:
        choice = input(f"Choice [default: {default_choice}]: ").strip()

        if choice == '':
            return options[default_choice]

        if choice in options:
            return options[choice]

        print(f"Please enter a number between 1 and {len(options)}")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Create a new git worktree for the docimp project with all necessary symlinks',
        epilog='Examples:\n'
               '  create_worktree.py issue-221 issue-221-improve-styleguides\n'
               '  create_worktree.py issue-123 fix-parser --source-branch feature-validation\n'
               '  create_worktree.py issue-456 nested-fix --source-branch origin/feature-xyz',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('worktree_name', help='Name of the worktree directory (e.g., issue-221)')
    parser.add_argument('branch_name', help='Name of the git branch (e.g., issue-221-improve-styleguides)')
    parser.add_argument(
        '--source-branch',
        default='main',
        help='Branch to create the new branch from (default: main). Supports local and remote branches (e.g., feature-xyz or origin/feature-xyz)'
    )
    parser.add_argument(
        '--include-changes',
        choices=['none', 'uncommitted', 'unpushed', 'all'],
        help='Include changes from source worktree (non-interactive). Options: none, uncommitted, unpushed, all'
    )
    parser.add_argument(
        '--exclude-changes',
        action='store_true',
        help='Exclude all changes from source worktree (same as --include-changes=none)'
    )
    parser.add_argument(
        '--install-hooks-if-missing',
        action='store_true',
        help='Automatically install git hooks if missing (no prompt)'
    )

    args = parser.parse_args()

    # Validate conflicting flags
    if args.exclude_changes and args.include_changes:
        exit_with_error("Cannot specify both --exclude-changes and --include-changes")

    # Resolve include_changes value
    if args.exclude_changes:
        include_changes_choice = 'none'
    elif args.include_changes:
        include_changes_choice = args.include_changes
    else:
        include_changes_choice = None  # Will prompt if needed

    # Validate we're in the docimp repo
    validate_docimp_repo()

    # Validate source branch exists
    print_info(f"Validating source branch '{args.source_branch}'...")
    is_valid, branch_type = validate_source_branch(args.source_branch)
    if not is_valid:
        exit_with_error(f"Source branch '{args.source_branch}' does not exist\n"
                       f"Use 'git branch -a' to see available branches")

    # Find worktree for source branch (if it's checked out somewhere)
    source_worktree_path = None
    if branch_type == 'local':
        source_worktree_path = find_worktree_for_branch(args.source_branch)

    # Check for changes in source worktree
    changes_info = None
    if source_worktree_path:
        print_info(f"Found worktree for '{args.source_branch}': {source_worktree_path}")
        changes_info = check_local_changes(source_worktree_path)

        # Determine what changes to include
        if changes_info['uncommitted'] or changes_info['unpushed']:
            # Changes exist - determine what to include
            if include_changes_choice is None:
                # No flags specified - prompt user interactively
                include_changes_choice = prompt_include_changes(
                    args.source_branch,
                    source_worktree_path,
                    changes_info
                )
            else:
                # Flags specified - use non-interactive mode
                print_info(f"Using --include-changes={include_changes_choice} (non-interactive)")
        else:
            # No changes exist
            include_changes_choice = 'none'
    else:
        # Source branch not in a worktree - must fetch/pull it
        include_changes_choice = 'none'

        if branch_type == 'local':
            print_info(f"Source branch '{args.source_branch}' not checked out in any worktree")
            print_info("Checking out and pulling...")
            run_git('checkout', args.source_branch)
            run_git('pull')
        elif branch_type == 'remote':
            print_info(f"Fetching remote branch '{args.source_branch}'...")
            run_git('fetch')

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

    # Create the worktree from source branch
    print_info(f"Creating worktree: {worktree_path}")
    print_info(f"  Branching from: {args.source_branch}")

    # Handle different include_changes scenarios
    if include_changes_choice == 'none':
        # Branch from remote tracking branch if possible, otherwise from source branch
        if source_worktree_path and changes_info and changes_info['unpushed']:
            # Get remote tracking branch
            upstream_result = run_git('rev-parse', '--abbrev-ref', '@{u}', cwd=source_worktree_path, check=False)
            if upstream_result.returncode == 0:
                upstream_branch = upstream_result.stdout.strip()
                print_info(f"  Excluding unpushed commits (branching from {upstream_branch})")
                run_git('worktree', 'add', str(worktree_path), '-b', args.branch_name, upstream_branch)
            else:
                # No upstream, just use source branch
                run_git('worktree', 'add', str(worktree_path), '-b', args.branch_name, args.source_branch)
        else:
            # Standard case: branch from committed state
            run_git('worktree', 'add', str(worktree_path), '-b', args.branch_name, args.source_branch)

    elif include_changes_choice == 'unpushed':
        # Branch from HEAD of source worktree (includes unpushed commits, excludes uncommitted)
        print_info("  Including: unpushed commits only")
        run_git('branch', args.branch_name, cwd=source_worktree_path)
        run_git('worktree', 'add', str(worktree_path), args.branch_name)

    elif include_changes_choice in ('uncommitted', 'all'):
        # Branch from HEAD + working directory (includes everything)
        print_info(f"  Including: {include_changes_choice} changes")

        # First stash any uncommitted changes in source worktree
        stash_result = run_git('stash', 'push', '-m', f'temp-for-{args.branch_name}',
                              cwd=source_worktree_path, check=False)
        stashed = (stash_result.returncode == 0 and 'No local changes' not in stash_result.stdout)

        # Create new branch from current HEAD
        run_git('branch', args.branch_name, cwd=source_worktree_path)

        # Create worktree for new branch
        run_git('worktree', 'add', str(worktree_path), args.branch_name)

        # If we stashed changes, apply them to the new worktree
        if stashed:
            print_info("  Applying uncommitted changes to new worktree...")
            apply_result = run_git('stash', 'apply', 'stash@{0}', cwd=worktree_path, check=False)
            if apply_result.returncode != 0:
                print_warning(f"Failed to apply stashed changes: {apply_result.stderr}")
                print_warning("Changes remain stashed in source worktree")
            else:
                # Successfully applied, drop from source worktree
                run_git('stash', 'drop', 'stash@{0}', cwd=source_worktree_path, check=False)

    else:
        # Fallback
        run_git('worktree', 'add', str(worktree_path), '-b', args.branch_name, args.source_branch)

    # Create symlinks with cleanup on failure
    try:
        print_info("Creating symlinks to shared files...")

        # Root-level symlinks
        create_symlink('../../.docimp-shared/CLAUDE.md', worktree_path / 'CLAUDE.md')
        create_symlink('../../.docimp-shared/CLAUDE.md', worktree_path / 'WARP.md')
        create_symlink('../../.docimp-shared/CLAUDE_CONTEXT.md', worktree_path / 'CLAUDE_CONTEXT.md')
        create_symlink('../../.docimp-shared/.planning', worktree_path / '.planning')
        create_symlink('../../.docimp-shared/.scratch', worktree_path / '.scratch')

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

    # Configure Husky hooks for the new worktree
    print()
    configure_husky_hooks(worktree_path)

    # Install npm dependencies
    print()
    install_npm_dependencies(worktree_path)

    # Setup Python virtual environment
    print()
    setup_python_venv(worktree_path)

    # Setup Node version
    print()
    setup_node_version(worktree_path)

    # Enable direnv for the worktree (uses .envrc from git branch)
    print()
    enable_direnv(worktree_path)

    # Print success summary
    print()
    print_success("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print_success("✓ Worktree created successfully!")
    print_success("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    print_info("Worktree details:")
    print(f"  Location:     {worktree_path}")
    print(f"  Branch:       {args.branch_name}")
    print(f"  Source:       {args.source_branch}")
    print()
    print_info("All symlinks created:")
    print("  ✓ CLAUDE.md → ../../.docimp-shared/CLAUDE.md")
    print("  ✓ WARP.md → ../../.docimp-shared/CLAUDE.md")
    print("  ✓ CLAUDE_CONTEXT.md → ../../.docimp-shared/CLAUDE_CONTEXT.md")
    print("  ✓ .planning → ../../.docimp-shared/.planning")
    print("  ✓ .scratch → ../../.docimp-shared/.scratch")
    print("  ✓ .claude/skills → ../../../.docimp-shared/.claude/skills")
    print("  ✓ .claude/settings.local.json → ../../.docimp-shared/.claude/settings.local.json")
    print()
    print_info("Husky hooks configured:")
    print("  ✓ Per-worktree config enabled")
    print("  ✓ Hooks path set to .husky/_")
    print("  ✓ Dispatcher files generated")
    print()
    print_info("npm dependencies:")
    print("  ✓ Installed in cli/ directory")
    print("  ✓ TypeScript compiled to dist/")
    print("  ✓ Worktree ready for development")
    print()
    print_info("Python environment:")
    print("  ✓ Per-worktree .venv/ created")
    print("  ✓ Isolated from other worktrees")
    print()
    print_info("Node.js environment:")
    print("  ✓ Node version managed by nvm (.nvmrc)")
    print("  ✓ Containerized per-project (not system-wide)")
    print()
    print_info("direnv configuration:")
    print("  ✓ .envrc authorized for worktree")
    print("  ✓ Python commands will auto-redirect to uv")
    print("  ✓ Node version auto-switches via nvm")
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
