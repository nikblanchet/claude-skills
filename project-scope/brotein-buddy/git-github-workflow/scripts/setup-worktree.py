#!/usr/bin/env python3
"""
setup-worktree.py - Create a new worktree with shared files symlinked

This script creates a new git worktree branched from an existing worktree,
with proper symlinks to shared files in the .shared directory.

IMPORTANT: Run this script with the bbud conda environment activated:
    conda activate bbud
    ./setup-worktree.py
"""

import argparse
import os
import random
import socket
import subprocess
import sys
from pathlib import Path


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Create a new git worktree with shared files symlinked',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Interactive mode (prompts for all inputs)
  ./setup-worktree.py

  # CLI mode (non-interactive)
  ./setup-worktree.py --source-worktree main --branch-name feature/new-thing --dir-name new-thing

  # Hybrid mode (CLI with some interactive prompts)
  ./setup-worktree.py --source-worktree main --branch-name feature/new-thing

  # Exclude local changes from source worktree
  ./setup-worktree.py --source-worktree main --exclude-changes

Branch naming conventions:
  - setup/name         -> for setup tasks
  - feature/name       -> for new features
  - bug/name           -> for bug fixes
  - bug/123-name       -> for bug fixes with issue number
        '''
    )

    parser.add_argument(
        '--source-worktree',
        type=str,
        help='Name of the source worktree to branch from (e.g., "main"). If not provided, will prompt interactively.'
    )

    parser.add_argument(
        '--branch-name',
        type=str,
        help='Name of the new branch (e.g., "feature/new-thing"). If not provided, will prompt interactively.'
    )

    parser.add_argument(
        '--dir-name',
        type=str,
        help='Directory name for the worktree in wt/ folder (e.g., "new-thing"). If not provided, will prompt interactively.'
    )

    parser.add_argument(
        '--exclude-changes',
        action='store_true',
        help='Exclude local changes from source worktree (default: include changes if they exist)'
    )

    return parser.parse_args()


def run_git_command(cmd, cwd=None, check=True):
    """Run a git command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        return e


def get_repo_root():
    """Get the repository root directory (where .shared lives)."""
    # Get the common git directory (works for both worktrees and regular repos)
    result = run_git_command(['git', 'rev-parse', '--git-common-dir'])
    if result.returncode != 0:
        print("Error: Not in a git repository")
        sys.exit(1)

    git_common_dir = Path(result.stdout.strip())

    # If it's a relative path, resolve it
    if not git_common_dir.is_absolute():
        git_common_dir = (Path.cwd() / git_common_dir).resolve()

    # The repo root is the parent of .git (or the common dir itself for _root)
    if git_common_dir.name == '.git':
        return git_common_dir.parent
    else:
        # For worktrees, git-common-dir points to the main .git directory
        return git_common_dir.parent


def get_worktrees():
    """Get list of worktrees, excluding _root."""
    result = run_git_command(['git', 'worktree', 'list', '--porcelain'])
    if result.returncode != 0:
        print("Error: Failed to get worktree list")
        sys.exit(1)

    worktrees = []
    current_wt = {}

    for line in result.stdout.strip().split('\n'):
        if line.startswith('worktree '):
            current_wt['path'] = line.split(' ', 1)[1]
        elif line.startswith('branch '):
            current_wt['branch'] = line.split('refs/heads/', 1)[1]
        elif line == '':
            if current_wt and 'branch' in current_wt:
                # Exclude _root worktree
                if not current_wt['path'].endswith('/_root') and not current_wt['path'].endswith('/BroteinBuddy'):
                    worktrees.append(current_wt)
            current_wt = {}

    # Handle last worktree
    if current_wt and 'branch' in current_wt:
        if not current_wt['path'].endswith('/_root') and not current_wt['path'].endswith('/BroteinBuddy'):
            worktrees.append(current_wt)

    return worktrees


def select_source_worktree(worktrees, source_worktree_name=None):
    """Select which worktree to branch from (CLI arg or interactive)."""
    # If source worktree name provided via CLI, validate and use it
    if source_worktree_name:
        for wt in worktrees:
            if wt['branch'] == source_worktree_name:
                print(f"\nUsing source worktree: {source_worktree_name}")
                return wt

        # Name not found, show error with available options
        print(f"\nError: Source worktree '{source_worktree_name}' not found")
        print("\nAvailable worktrees:")
        for wt in worktrees:
            print(f"  - {wt['branch']}")
        sys.exit(1)

    # Interactive mode - prompt user to select
    print("\nAvailable worktrees to branch from:")
    print()

    # Find main worktree for default
    main_index = 0
    for i, wt in enumerate(worktrees, 1):
        branch = wt['branch']
        path = wt['path']

        # Extract directory name from path
        dir_name = Path(path).name

        print(f"  {i}. {branch} -> wt/{dir_name}/")

        if branch == 'main':
            main_index = i

    print()
    default_msg = f" (default: {main_index})" if main_index > 0 else ""

    while True:
        choice = input(f"Select source worktree{default_msg}: ").strip()

        if choice == '' and main_index > 0:
            return worktrees[main_index - 1]

        try:
            idx = int(choice)
            if 1 <= idx <= len(worktrees):
                return worktrees[idx - 1]
            else:
                print(f"Please enter a number between 1 and {len(worktrees)}")
        except ValueError:
            print("Please enter a valid number")


def pull_and_check_status(worktree_path, exclude_changes=False):
    """Pull from remote and check for conflicts or local changes."""
    print(f"\nPulling latest changes in {worktree_path}...")

    # Pull from remote
    result = run_git_command(['git', 'pull'], cwd=worktree_path, check=False)

    if result.returncode != 0:
        # Check if there are merge conflicts
        if 'CONFLICT' in result.stdout or 'CONFLICT' in result.stderr:
            print("\nError: Merge conflicts detected!")
            print(result.stdout)
            print(result.stderr)
            print("\nPlease resolve conflicts in the source worktree and try again.")
            sys.exit(1)
        else:
            print(f"\nError pulling from remote: {result.stderr}")
            sys.exit(1)

    print(result.stdout)

    # Check for uncommitted local changes
    status_result = run_git_command(['git', 'status', '--porcelain'], cwd=worktree_path)

    if status_result.stdout.strip():
        print("\nLocal changes detected:")
        print(status_result.stdout)

        # If --exclude-changes flag is set, automatically exclude without prompting
        if exclude_changes:
            print("\nExcluding local changes (--exclude-changes flag set)")
            return False

        # Interactive mode - prompt user
        while True:
            choice = input("\nInclude these local changes in the new worktree? (y/n): ").strip().lower()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' or 'n'")

    return False


def get_branch_details(branch_name=None, dir_name=None):
    """Get branch name and directory name (CLI args or interactive)."""
    # If both provided via CLI, use them
    if branch_name and dir_name:
        print(f"\nUsing branch: {branch_name} -> wt/{dir_name}/")
        return branch_name, dir_name

    # Need to prompt for missing values
    print("\nEnter details for the new worktree:")
    print("Examples:")
    print("  Branch: setup/skills-and-subagents  -> Directory: skills-and-subagents")
    print("  Branch: feature/random-selection    -> Directory: random-selection")
    print("  Branch: bug/123-fix-inventory       -> Directory: 123-fix-inventory")
    print()

    # Get branch name (use CLI arg or prompt)
    if branch_name:
        branch = branch_name
        print(f"Branch name: {branch} (from CLI)")
    else:
        branch = input("Branch name: ").strip()
        if not branch:
            print("Error: Branch name is required")
            sys.exit(1)

    # Get directory name (use CLI arg or prompt)
    if dir_name:
        final_dir_name = dir_name
        print(f"Directory name (for wt/ folder): {final_dir_name} (from CLI)")
    else:
        final_dir_name = input("Directory name (for wt/ folder): ").strip()
        if not final_dir_name:
            print("Error: Directory name is required")
            sys.exit(1)

    return branch, final_dir_name


def is_port_available(port):
    """Check if a port is actually free on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return True
        except OSError:
            return False


def assign_port(branch):
    """Assign a port for the worktree's dev server.

    - main branch always gets 5173 (Vite default)
    - Other worktrees get random port in 10000-60000 range
    - Verifies port is actually available via socket check
    """
    # Special case: main always uses default Vite port
    if branch == 'main':
        return 5173

    # For other worktrees: find an available random port
    max_attempts = 10
    for _ in range(max_attempts):
        port = random.randint(10000, 60000)

        if is_port_available(port):
            return port

    # Fallback: if we can't find a random port, try sequential from 10000
    for port in range(10000, 11000):
        if is_port_available(port):
            return port

    raise Exception("Could not find an available port after checking 1000+ ports")


def create_env_file(wt_dir, port):
    """Create .env.local file with port configuration for Vite and Playwright."""
    env_path = wt_dir / '.env.local'

    env_content = f"""# Auto-generated by setup-worktree.py
# This file configures the dev server port and Playwright baseURL
# to enable parallel development across multiple worktrees

VITE_PORT={port}
BASE_URL=http://localhost:{port}
"""

    with open(env_path, 'w') as f:
        f.write(env_content)

    print(f"  Created .env.local with port {port}")


def create_worktree(repo_root, source_path, branch, dir_name, include_local_changes):
    """Create the new worktree."""
    wt_dir = repo_root / 'wt' / dir_name

    # Check if worktree already exists
    if wt_dir.exists():
        print(f"\nError: Worktree already exists at wt/{dir_name}")
        sys.exit(1)

    # Create branch if needed
    if include_local_changes:
        # Create branch from current HEAD (includes uncommitted changes)
        print(f"\nCreating branch '{branch}' from current state (with local changes)...")
        result = run_git_command(['git', 'branch', branch], cwd=source_path, check=False)

        if result.returncode != 0 and 'already exists' not in result.stderr:
            print(f"Error creating branch: {result.stderr}")
            sys.exit(1)
    else:
        # Create branch from last commit
        print(f"\nCreating branch '{branch}' from last commit...")
        result = run_git_command(['git', 'branch', branch], cwd=source_path, check=False)

        if result.returncode != 0 and 'already exists' not in result.stderr:
            print(f"Error creating branch: {result.stderr}")
            sys.exit(1)

    # Create worktree
    print(f"Creating worktree for branch: {branch}")
    result = run_git_command(['git', 'worktree', 'add', str(wt_dir), branch], cwd=repo_root, check=False)

    if result.returncode != 0:
        print(f"\nError: Failed to create worktree")
        print(result.stderr)
        sys.exit(1)

    return wt_dir


def create_symlinks(wt_dir, repo_root):
    """Create symlinks to shared files."""
    print("\nSymlinking shared files...")

    shared_dir = repo_root / '.shared'

    # Verify .shared exists
    if not shared_dir.exists():
        print("Error: .shared directory not found")
        print("   Run init-shared.sh first")
        sys.exit(1)

    # Create symlinks to root-level files
    symlinks = [
        ('CLAUDE.md', '../../.shared/CLAUDE.md'),
        ('CLAUDE_CONTEXT.md', '../../.shared/CLAUDE_CONTEXT.md'),
        ('.planning', '../../.shared/.planning'),
        ('.scratch', '../../.shared/.scratch'),
    ]

    for target, source in symlinks:
        target_path = wt_dir / target
        if target_path.exists() or target_path.is_symlink():
            target_path.unlink()
        target_path.symlink_to(source)

    # Create .claude directory with symlinks
    claude_dir = wt_dir / '.claude'
    claude_dir.mkdir(exist_ok=True)

    claude_symlinks = [
        ('settings.local.json', '../../../.shared/.claude/settings.local.json'),
        ('skills', '../../../.shared/.claude/skills'),
        ('agents', '../../../.shared/.claude/agents'),
    ]

    for target, source in claude_symlinks:
        target_path = claude_dir / target
        if target_path.exists() or target_path.is_symlink():
            target_path.unlink()
        target_path.symlink_to(source)


def validate_and_fix_gitignore(wt_dir):
    """Validate and fix .gitignore entries."""
    gitignore_path = wt_dir / '.gitignore'

    if not gitignore_path.exists():
        print("\nWarning: .gitignore not found, skipping validation")
        return

    print("\nValidating .gitignore...")

    # Entries that MUST be in .gitignore
    required_entries = {
        'CLAUDE.md',
        'CLAUDE_CONTEXT.md',
        '.planning',
        '.scratch',
        '.claude/settings.local.json',
        '.claude/agents',
        '.claude/skills',
        '.env.local',
    }

    # Entries that must NOT be in .gitignore
    forbidden_entries = {
        '.claude',
        '.claude/',
    }

    # Read current .gitignore
    with open(gitignore_path, 'r') as f:
        lines = f.readlines()

    # Parse existing entries (excluding comments and empty lines)
    existing_entries = set()
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('#'):
            existing_entries.add(stripped)

    # Check what's missing and what shouldn't be there
    missing_entries = required_entries - existing_entries
    forbidden_found = forbidden_entries & existing_entries

    if not missing_entries and not forbidden_found:
        print("  .gitignore is valid")
        return

    # Need to fix .gitignore
    print("  Fixing .gitignore...")

    # Remove forbidden entries
    if forbidden_found:
        new_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped not in forbidden_found:
                new_lines.append(line)
        lines = new_lines
        print(f"    Removed: {', '.join(forbidden_found)}")

    # Add missing entries
    if missing_entries:
        # Find the Claude Code section to add entries
        claude_section_index = None
        for i, line in enumerate(lines):
            if 'Claude Code personal settings' in line:
                claude_section_index = i
                break

        if claude_section_index is not None:
            # Add missing entries after the section comment
            insert_index = claude_section_index + 1
            for entry in sorted(missing_entries):
                lines.insert(insert_index, f"{entry}\n")
                insert_index += 1
        else:
            # No Claude section found, append at the end
            lines.append("\n# Claude Code personal settings (symlinked in worktrees)\n")
            for entry in sorted(missing_entries):
                lines.append(f"{entry}\n")

        print(f"    Added: {', '.join(sorted(missing_entries))}")

    # Write updated .gitignore
    with open(gitignore_path, 'w') as f:
        f.writelines(lines)

    print("  .gitignore fixed successfully")


def install_dependencies(wt_dir):
    """Install npm dependencies."""
    print("\nInstalling dependencies...")
    result = subprocess.run(['npm', 'install'], cwd=wt_dir)

    if result.returncode != 0:
        print("Warning: npm install failed")
        return False
    return True


def print_success_message(dir_name, branch, port):
    """Print success message with next steps."""
    print()
    print(f"Worktree created successfully: wt/{dir_name}")
    print(f"   Branch: {branch}")
    print(f"   Port: {port}")
    print()
    print("Shared items symlinked:")
    print("  - CLAUDE.md (project context)")
    print("  - CLAUDE_CONTEXT.md (confidential info)")
    print("  - .planning/ (planning docs)")
    print("  - .scratch/ (throwaway files)")
    print("  - .claude/settings.local.json")
    print("  - .claude/skills/")
    print("  - .claude/agents/")
    print()
    print("Environment configured:")
    print(f"  - .env.local created with VITE_PORT={port}")
    print(f"  - Dev server will run on http://localhost:{port}")
    print(f"  - Playwright tests will use http://localhost:{port}")
    print()
    print("Next steps:")
    print(f"  cd wt/{dir_name}")
    print("  code .              # Open in VS Code")
    print(f"  npm run dev         # Start dev server on port {port}")
    print("  claude              # Start Claude Code")
    print()


def main():
    """Main script execution."""
    # Parse CLI arguments
    args = parse_arguments()

    # Get repository root
    repo_root = get_repo_root()

    # Get available worktrees
    worktrees = get_worktrees()

    if not worktrees:
        print("Error: No worktrees found (excluding _root)")
        print("You need at least one worktree to branch from")
        sys.exit(1)

    # Select source worktree (CLI arg or interactive)
    source_wt = select_source_worktree(worktrees, args.source_worktree)
    source_path = Path(source_wt['path'])
    source_branch = source_wt['branch']

    print(f"\nSelected: {source_branch}")

    # Pull and check for local changes (respecting --exclude-changes flag)
    include_local = pull_and_check_status(source_path, args.exclude_changes)

    # Get new branch details (CLI args or interactive)
    branch, dir_name = get_branch_details(args.branch_name, args.dir_name)

    # Assign port for this worktree
    port = assign_port(branch)

    # Create worktree
    wt_dir = create_worktree(repo_root, source_path, branch, dir_name, include_local)

    # Create symlinks
    create_symlinks(wt_dir, repo_root)

    # Create .env.local with port configuration
    create_env_file(wt_dir, port)

    # Validate and fix .gitignore
    validate_and_fix_gitignore(wt_dir)

    # Install dependencies
    install_dependencies(wt_dir)

    # Print success message
    print_success_message(dir_name, branch, port)


if __name__ == '__main__':
    main()
