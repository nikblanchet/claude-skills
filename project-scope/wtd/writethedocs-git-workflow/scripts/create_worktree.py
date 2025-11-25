#!/usr/bin/env python3
"""Create git worktree for WTD project with shared resource symlinks.

Requires Python 3.9+.

This script automates the creation of git worktrees for the Write the Docs
repository, which uses a bare repo structure with shared resources.

Usage:
    create_worktree.py <worktree-name> [branch-name] [OPTIONS]

Positional Arguments:
    worktree-name       Name of the worktree directory (e.g., issue-123)
    branch-name         Name of the git branch (default: same as worktree-name)

Options:
    --source-branch SOURCE
        Branch to create the new branch from (default: main)

    --include-changes {none,uncommitted,unpushed,all}
        Include changes from source worktree (non-interactive mode)
        - none: Branch from last pushed commit
        - uncommitted: Include uncommitted changes only
        - unpushed: Include unpushed commits only
        - all: Include both uncommitted and unpushed

    --exclude-changes
        Exclude all changes (same as --include-changes=none)

    --no-venv
        Skip Python virtual environment creation

    --list-symlinks
        Show symlinks that would be created and exit

Examples:
    # Basic usage (branches from main)
    create_worktree.py issue-123

    # With explicit branch name
    create_worktree.py issue-123 issue-123-fix-schedule

    # Branch from feature branch
    create_worktree.py fix-docs fix-docs-typos --source-branch feature-xyz

    # Skip venv creation
    create_worktree.py quick-fix --no-venv

Repository Structure:
    wtd/
    ├── .bare/          # Bare git repository
    ├── .git -> .bare   # Symlink for git commands
    ├── .shared/        # Shared untracked resources
    ├── main/           # Main branch worktree
    └── {feature}/      # New worktrees created here
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import NoReturn, Optional, Union


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
    SymlinkSpec(
        link_name=".claude",
        target="../.shared/.claude",
        description="Claude Code configuration",
        required=True,
    ),
    SymlinkSpec(
        link_name=".envrc",
        target="../.shared/.envrc",
        description="direnv configuration for uv/Python",
        required=False,
    ),
    SymlinkSpec(
        link_name=".planning",
        target="../.shared/.planning",
        description="Planning documents",
        required=True,
    ),
    SymlinkSpec(
        link_name=".scratch",
        target="../.shared/.scratch",
        description="Scratch/temp files",
        required=True,
    ),
    SymlinkSpec(
        link_name=".vscode",
        target="../.shared/.vscode",
        description="VS Code settings",
        required=True,
    ),
    SymlinkSpec(
        link_name="CLAUDE.md",
        target="../.shared/CLAUDE.md",
        description="Claude documentation",
        required=True,
    ),
]


class Colors:
    """ANSI color codes for terminal output."""

    GREEN = "\033[0;32m"
    RED = "\033[0;31m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"  # No Color


def print_error(message: str) -> None:
    """Print error message in red to stderr."""
    print(f"{Colors.RED}Error: {message}{Colors.NC}", file=sys.stderr)


def print_info(message: str) -> None:
    """Print informational message in blue."""
    print(f"{Colors.BLUE}{message}{Colors.NC}")


def print_success(message: str) -> None:
    """Print success message in green."""
    print(f"{Colors.GREEN}{message}{Colors.NC}")


def print_warning(message: str) -> None:
    """Print warning message in yellow."""
    print(f"{Colors.YELLOW}{message}{Colors.NC}")


def exit_with_error(message: str) -> NoReturn:
    """Print error message and exit with status 1."""
    print_error(message)
    sys.exit(1)


def run_git(
    *args: str, cwd: Optional[Path] = None, check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run git command and return result."""
    try:
        return subprocess.run(
            ["git", *args],
            cwd=cwd,
            check=check,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        exit_with_error(f"Git command failed: {e.stderr.strip()}")


def check_uv_available() -> bool:
    """Check if uv is installed and available."""
    try:
        subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            check=True,
            timeout=5,
        )
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.CalledProcessError):
        return False


def validate_wtd_repo() -> None:
    """Validate we're in the WTD repo root (has .bare/ directory).

    The WTD repository uses a bare repo structure where .bare/ contains
    the git data and .git is a symlink to .bare/.
    """
    bare_dir = Path(".bare")
    git_link = Path(".git")
    shared_dir = Path(".shared")

    if not bare_dir.is_dir():
        exit_with_error(
            "Not in a WTD repository root\n"
            "Expected .bare/ directory (bare git repository)\n"
            "Please run this script from the wtd/ directory"
        )

    if not git_link.exists():
        exit_with_error(
            ".git symlink not found\n"
            "Expected .git -> .bare symlink"
        )

    if not shared_dir.is_dir():
        exit_with_error(
            ".shared/ directory not found\n"
            "Expected .shared/ with Claude configuration and planning docs"
        )


def validate_source_branch(branch_name: str) -> tuple[bool, str]:
    """Validate that the source branch exists (local or remote).

    Returns:
        Tuple of (is_valid, branch_type) where branch_type is 'local' or 'remote'
    """
    # Check if it's a local branch
    result = run_git(
        "show-ref", "--verify", "--quiet", f"refs/heads/{branch_name}", check=False
    )
    if result.returncode == 0:
        return (True, "local")

    # Check if it's a remote branch
    result = run_git(
        "show-ref", "--verify", "--quiet", f"refs/remotes/{branch_name}", check=False
    )
    if result.returncode == 0:
        return (True, "remote")

    return (False, "")


def find_worktree_for_branch(branch_name: str) -> Optional[Path]:
    """Find the worktree path that has the specified branch checked out."""
    result = run_git("worktree", "list", "--porcelain", check=False)
    if result.returncode != 0:
        return None

    current_worktree = None
    current_branch = None

    for line in result.stdout.strip().split("\n"):
        if line.startswith("worktree "):
            current_worktree = Path(line.split(" ", 1)[1])
        elif line.startswith("branch "):
            current_branch = (
                line.split("refs/heads/", 1)[1] if "refs/heads/" in line else None
            )
        elif line == "":
            if current_branch == branch_name and current_worktree:
                return current_worktree
            current_worktree = None
            current_branch = None

    if current_branch == branch_name and current_worktree:
        return current_worktree

    return None


def check_local_changes(worktree_path: Path) -> dict[str, Union[bool, int, str]]:
    """Check for uncommitted and unpushed changes in specified worktree."""
    changes: dict[str, Union[bool, int, str]] = {
        "uncommitted": False,
        "uncommitted_output": "",
        "unpushed": False,
        "unpushed_count": 0,
        "unpushed_log": "",
    }

    # Check for uncommitted changes
    status_result = run_git("status", "--porcelain", cwd=worktree_path, check=False)
    if status_result.returncode == 0 and status_result.stdout.strip():
        changes["uncommitted"] = True
        changes["uncommitted_output"] = status_result.stdout

    # Check for unpushed commits
    upstream_result = run_git(
        "rev-parse", "--abbrev-ref", "@{u}", cwd=worktree_path, check=False
    )
    if upstream_result.returncode == 0:
        count_result = run_git(
            "rev-list", "--count", "@{u}..HEAD", cwd=worktree_path, check=False
        )
        if count_result.returncode == 0:
            count = int(count_result.stdout.strip())
            if count > 0:
                changes["unpushed"] = True
                changes["unpushed_count"] = count

                log_result = run_git(
                    "log",
                    "@{u}..HEAD",
                    "--oneline",
                    "--no-decorate",
                    cwd=worktree_path,
                    check=False,
                )
                if log_result.returncode == 0:
                    changes["unpushed_log"] = log_result.stdout.strip()

    return changes


def prompt_include_changes(
    branch_name: str, worktree_path: Path, changes_info: dict[str, Union[bool, int, str]]
) -> str:
    """Prompt user about including changes from source worktree."""
    print()
    print_info(f"Changes detected in source worktree: {worktree_path}")
    print()

    if changes_info["uncommitted"]:
        print_warning("Uncommitted changes:")
        uncommitted_output = str(changes_info["uncommitted_output"])
        lines = uncommitted_output.strip().split("\n")
        for line in lines[:10]:
            print(f"  {line}")
        if len(lines) > 10:
            print(f"  ... and {len(lines) - 10} more files")
        print()

    if changes_info["unpushed"]:
        unpushed_count = int(changes_info["unpushed_count"])
        print_warning(f"Unpushed commits ({unpushed_count}):")
        unpushed_log = str(changes_info["unpushed_log"])
        for line in unpushed_log.split("\n")[:5]:
            print(f"  {line}")
        if unpushed_count > 5:
            print(f"  ... and {unpushed_count - 5} more commits")
        print()

    print("Include changes in new worktree?")
    options: dict[str, str] = {}
    option_num = 1

    options[str(option_num)] = "none"
    print(f"  {option_num}. None (branch from last pushed commit)")
    option_num += 1

    if changes_info["uncommitted"]:
        options[str(option_num)] = "uncommitted"
        print(f"  {option_num}. Uncommitted only")
        option_num += 1

    if changes_info["unpushed"]:
        options[str(option_num)] = "unpushed"
        print(f"  {option_num}. Unpushed commits only")
        option_num += 1

    if changes_info["uncommitted"] and changes_info["unpushed"]:
        options[str(option_num)] = "all"
        print(f"  {option_num}. All changes (uncommitted + unpushed)")
        default_choice = str(option_num)
    elif changes_info["uncommitted"]:
        default_choice = "2"
    elif changes_info["unpushed"]:
        default_choice = "2"
    else:
        default_choice = "1"

    print()

    while True:
        choice = input(f"Choice [default: {default_choice}]: ").strip()

        if choice == "":
            return options[default_choice]

        if choice in options:
            return options[choice]

        print(f"Please enter a number between 1 and {len(options)}")


def create_symlink(target: str, link_name: Path) -> None:
    """Create a symlink and print success message."""
    if link_name.exists() or link_name.is_symlink():
        if link_name.is_symlink() and link_name.readlink() == Path(target):
            print_info(f"  Symlink already exists: {link_name.name}")
            return
        exit_with_error(f"File or symlink already exists at {link_name}")

    try:
        link_name.symlink_to(target)
        print_success(f"  [ok] {link_name.name}")
    except OSError as e:
        exit_with_error(f"Failed to create symlink {link_name.name}: {e}")


def validate_symlink_target(spec: SymlinkSpec, worktree_path: Path) -> bool:
    """Validate that a symlink target exists."""
    link_path = worktree_path / spec.link_name
    link_dir = link_path.parent
    target_path = (link_dir / spec.target).resolve()

    if target_path.exists():
        return True

    if spec.required:
        print_error(f"Required symlink target does not exist: {target_path}")
        print_error(f"For symlink: {spec.link_name} -> {spec.target}")
        exit_with_error("Cannot create worktree with missing required symlink targets")

    print_warning(f"Optional symlink target missing: {target_path}")
    print_warning(f"Skipping: {spec.link_name}")
    return False


def create_symlinks(worktree_path: Path) -> list[SymlinkSpec]:
    """Create all symlinks to .shared/ resources.

    Returns:
        List of SymlinkSpec that were successfully created (for summary output).
    """
    print_info("Creating symlinks to shared resources...")

    # Pre-validate and collect valid specs (skips optional missing targets)
    valid_specs = []
    for spec in WORKTREE_SYMLINKS:
        if validate_symlink_target(spec, worktree_path):
            valid_specs.append(spec)

    # Create symlinks only for valid targets
    for spec in valid_specs:
        link_path = worktree_path / spec.link_name
        create_symlink(spec.target, link_path)

    return valid_specs


def setup_direnv(worktree_path: Path) -> None:
    """Run direnv allow if direnv is installed and .envrc exists."""
    envrc_path = worktree_path / ".envrc"
    if not envrc_path.exists() and not envrc_path.is_symlink():
        return  # No .envrc to allow

    # Check if direnv is installed
    try:
        subprocess.run(
            ["direnv", "version"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        print_info("  direnv not installed, skipping direnv allow")
        print_info("  (Install direnv for automatic Python environment activation)")
        return

    # Run direnv allow from within the worktree directory
    # (direnv allow without a path argument works more reliably with symlinks)
    print_info("  Running direnv allow...")
    try:
        subprocess.run(
            ["direnv", "allow"],
            cwd=worktree_path,
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        print_success("  [ok] direnv allowed")
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else "unknown error"
        print_warning(f"  direnv allow failed: {error_msg}")
        print_warning(f"  Run manually: cd {worktree_path} && direnv allow")
    except subprocess.TimeoutExpired:
        print_warning("  direnv allow timed out")
        print_warning(f"  Run manually: cd {worktree_path} && direnv allow")


def setup_python_venv(worktree_path: Path) -> None:
    """Create venv using uv and install requirements."""
    print_info("Setting up Python environment...")

    # Read Python version from .python-version file
    python_version_file = worktree_path / ".python-version"
    python_version = None
    if python_version_file.exists():
        try:
            python_version = python_version_file.read_text().strip()
        except Exception:
            pass

    if not python_version:
        python_version = "3.9"  # Default for WTD project

    # Ensure uv has the requested Python version
    print_info(f"  Ensuring Python {python_version} is available...")
    try:
        subprocess.run(
            ["uv", "python", "install", python_version],
            check=True,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else "unknown error"
        print_warning(f"  Could not install Python {python_version}: {error_msg}")
        print_warning("  Continuing with default Python...")

    # Create venv
    print_info("  Creating virtual environment...")
    try:
        subprocess.run(
            ["uv", "venv", "--python", python_version],
            cwd=worktree_path,
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else "unknown error"
        print_warning(f"  Failed to create venv with Python {python_version}: {error_msg}")
        # Try without specific version
        try:
            subprocess.run(
                ["uv", "venv"],
                cwd=worktree_path,
                check=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
        except subprocess.CalledProcessError:
            raise RuntimeError("Failed to create virtual environment")

    # Install requirements
    requirements_file = worktree_path / "requirements.txt"
    if requirements_file.exists():
        print_info("  Installing dependencies...")
        try:
            subprocess.run(
                ["uv", "pip", "install", "-r", "requirements.txt"],
                cwd=worktree_path,
                check=True,
                capture_output=True,
                text=True,
                timeout=300,
            )
            print_success("  [ok] Dependencies installed")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else "unknown error"
            print_warning(f"  Failed to install dependencies: {error_msg}")
            print_warning("  You may need to install them manually")
    else:
        print_info("  No requirements.txt found, skipping dependency installation")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Create a new git worktree for the WTD project with symlinks",
        epilog="Example: create_worktree.py issue-123 issue-123-fix-schedule",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "worktree_name",
        nargs="?",
        help="Name of the worktree directory (e.g., issue-123)",
    )
    parser.add_argument(
        "branch_name",
        nargs="?",
        help="Name of the git branch (default: same as worktree_name)",
    )
    parser.add_argument(
        "--source-branch",
        default="main",
        help="Branch to create the new branch from (default: main)",
    )
    parser.add_argument(
        "--include-changes",
        choices=["none", "uncommitted", "unpushed", "all"],
        help="Include changes from source worktree (non-interactive)",
    )
    parser.add_argument(
        "--exclude-changes",
        action="store_true",
        help="Exclude all changes (same as --include-changes=none)",
    )
    parser.add_argument(
        "--no-venv",
        action="store_true",
        help="Skip Python virtual environment creation",
    )
    parser.add_argument(
        "--list-symlinks",
        action="store_true",
        help="List all symlinks that would be created and exit",
    )

    args = parser.parse_args()

    # Handle --list-symlinks flag
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

    # Validate required arguments
    if not args.worktree_name:
        parser.error("worktree_name is required (unless using --list-symlinks)")

    # Default branch name to worktree name
    branch_name = args.branch_name or args.worktree_name

    # Validate we're in the WTD repo root
    validate_wtd_repo()

    # Check for uv if venv is needed
    if not args.no_venv and not check_uv_available():
        print_warning("uv not found - skipping venv creation")
        print_warning("Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh")
        args.no_venv = True

    # Validate conflicting flags
    if args.exclude_changes and args.include_changes:
        exit_with_error("Cannot specify both --exclude-changes and --include-changes")

    # Resolve include_changes value
    if args.exclude_changes:
        include_changes_choice: Optional[str] = "none"
    elif args.include_changes:
        include_changes_choice = args.include_changes
    else:
        include_changes_choice = None

    # Validate source branch exists
    print_info(f"Validating source branch '{args.source_branch}'...")
    is_valid, branch_type = validate_source_branch(args.source_branch)
    if not is_valid:
        exit_with_error(
            f"Source branch '{args.source_branch}' does not exist\n"
            f"Use 'git branch -a' to see available branches"
        )

    # Find worktree for source branch
    source_worktree_path = None
    if branch_type == "local":
        source_worktree_path = find_worktree_for_branch(args.source_branch)

    # Check for changes in source worktree
    changes_info = None
    if source_worktree_path:
        print_info(f"Found worktree for '{args.source_branch}': {source_worktree_path}")
        changes_info = check_local_changes(source_worktree_path)

        if changes_info["uncommitted"] or changes_info["unpushed"]:
            if include_changes_choice is None:
                include_changes_choice = prompt_include_changes(
                    args.source_branch, source_worktree_path, changes_info
                )
            else:
                print_info(f"Using --include-changes={include_changes_choice}")
        else:
            include_changes_choice = "none"
    else:
        include_changes_choice = "none"

    # Determine worktree path (sibling directory to main/)
    repo_root = Path.cwd()
    worktree_path = repo_root / args.worktree_name

    # Check if worktree already exists
    if worktree_path.exists():
        exit_with_error(f"Worktree already exists at {worktree_path}")

    # Check if branch already exists
    result = run_git(
        "show-ref", "--verify", "--quiet", f"refs/heads/{branch_name}", check=False
    )
    if result.returncode == 0:
        exit_with_error(
            f"Branch '{branch_name}' already exists\n"
            f"Use a different branch name or delete the existing branch first"
        )

    # Create the worktree
    print_info(f"Creating worktree: {worktree_path}")
    print_info(f"  Branching from: {args.source_branch}")

    # Handle different include_changes scenarios
    if include_changes_choice == "none":
        if source_worktree_path and changes_info and changes_info["unpushed"]:
            upstream_result = run_git(
                "rev-parse", "--abbrev-ref", "@{u}",
                cwd=source_worktree_path, check=False
            )
            if upstream_result.returncode == 0:
                upstream_branch = upstream_result.stdout.strip()
                print_info(f"  Excluding unpushed commits (from {upstream_branch})")
                run_git(
                    "worktree", "add", str(worktree_path),
                    "-b", branch_name, upstream_branch
                )
            else:
                run_git(
                    "worktree", "add", str(worktree_path),
                    "-b", branch_name, args.source_branch
                )
        else:
            run_git(
                "worktree", "add", str(worktree_path),
                "-b", branch_name, args.source_branch
            )

    elif include_changes_choice == "unpushed":
        print_info("  Including: unpushed commits only")
        run_git("branch", branch_name, cwd=source_worktree_path)
        run_git("worktree", "add", str(worktree_path), branch_name)

    elif include_changes_choice in ("uncommitted", "all"):
        print_info(f"  Including: {include_changes_choice} changes")

        stash_result = run_git(
            "stash", "push", "-m", f"temp-for-{branch_name}",
            cwd=source_worktree_path, check=False
        )
        stashed = (
            stash_result.returncode == 0
            and "No local changes" not in stash_result.stdout
        )

        run_git("branch", branch_name, cwd=source_worktree_path)
        run_git("worktree", "add", str(worktree_path), branch_name)

        if stashed:
            print_info("  Applying uncommitted changes...")
            apply_result = run_git(
                "stash", "apply", "stash@{0}", cwd=worktree_path, check=False
            )
            if apply_result.returncode != 0:
                print_warning(f"Failed to apply stashed changes: {apply_result.stderr}")
                print_warning("Changes remain stashed in source worktree")
            else:
                run_git("stash", "drop", "stash@{0}", cwd=source_worktree_path, check=False)
    else:
        run_git(
            "worktree", "add", str(worktree_path),
            "-b", branch_name, args.source_branch
        )

    # Create symlinks
    print()
    created_symlinks = []
    try:
        created_symlinks = create_symlinks(worktree_path)
    except SystemExit:
        print_error("Symlink creation failed, cleaning up...")
        try:
            run_git("worktree", "remove", str(worktree_path), "--force")
            print_info("Worktree removed")
        except Exception:
            print_warning(f"Please manually remove: git worktree remove {worktree_path}")
        raise

    # Setup direnv (auto-allow .envrc if direnv is installed)
    setup_direnv(worktree_path)

    # Setup Python venv
    if not args.no_venv:
        print()
        try:
            setup_python_venv(worktree_path)
        except RuntimeError as e:
            print_warning(f"Venv setup failed: {e}")
            print_warning("You can set up the environment manually later")

    # Print success summary
    print()
    print_success("=" * 60)
    print_success("Worktree created successfully!")
    print_success("=" * 60)
    print()
    print_info("Worktree details:")
    print(f"  Location:     {worktree_path}")
    print(f"  Branch:       {branch_name}")
    print(f"  Source:       {args.source_branch}")
    print()
    print_info("Symlinks created:")
    for spec in created_symlinks:
        print(f"  [ok] {spec.link_name} -> {spec.target}")
    print()
    print_info("Next steps:")
    print(f"  cd {worktree_path}")
    if not args.no_venv:
        print("  source .venv/bin/activate")
    print("  # Start development")
    print()
    print_info("To view all worktrees:")
    print("  git worktree list")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
