#!/usr/bin/env python3
"""
setup-worktree.py - Create a new worktree with shared files symlinked

This script creates a new git worktree branched from an existing worktree,
with proper symlinks to shared files in the .shared directory.

IMPORTANT: Run this script with the bbud conda environment activated:
    conda activate bbud
    ./setup-worktree.py
"""

import os
import subprocess
import sys
from pathlib import Path


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


def select_source_worktree(worktrees):
    """Interactively select which worktree to branch from."""
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


def pull_and_check_status(worktree_path):
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

        while True:
            choice = input("\nInclude these local changes in the new worktree? (y/n): ").strip().lower()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' or 'n'")

    return False


def get_branch_details():
    """Get branch name and directory name from user."""
    print("\nEnter details for the new worktree:")
    print("Examples:")
    print("  Branch: setup/skills-and-subagents  -> Directory: skills-and-subagents")
    print("  Branch: feature/random-selection    -> Directory: random-selection")
    print("  Branch: bug/123-fix-inventory       -> Directory: 123-fix-inventory")
    print()

    branch = input("Branch name: ").strip()
    if not branch:
        print("Error: Branch name is required")
        sys.exit(1)

    dir_name = input("Directory name (for wt/ folder): ").strip()
    if not dir_name:
        print("Error: Directory name is required")
        sys.exit(1)

    return branch, dir_name


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


def print_success_message(dir_name, branch):
    """Print success message with next steps."""
    print()
    print(f"Worktree created successfully: wt/{dir_name}")
    print(f"   Branch: {branch}")
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
    print("Next steps:")
    print(f"  cd wt/{dir_name}")
    print("  code .              # Open in VS Code")
    print("  npm run dev         # Start dev server")
    print("  claude              # Start Claude Code")
    print()


def main():
    """Main script execution."""
    # Get repository root
    repo_root = get_repo_root()

    # Get available worktrees
    worktrees = get_worktrees()

    if not worktrees:
        print("Error: No worktrees found (excluding _root)")
        print("You need at least one worktree to branch from")
        sys.exit(1)

    # Select source worktree
    source_wt = select_source_worktree(worktrees)
    source_path = Path(source_wt['path'])
    source_branch = source_wt['branch']

    print(f"\nSelected: {source_branch}")

    # Pull and check for local changes
    include_local = pull_and_check_status(source_path)

    # Get new branch details
    branch, dir_name = get_branch_details()

    # Create worktree
    wt_dir = create_worktree(repo_root, source_path, branch, dir_name, include_local)

    # Create symlinks
    create_symlinks(wt_dir, repo_root)

    # Validate and fix .gitignore
    validate_and_fix_gitignore(wt_dir)

    # Install dependencies
    install_dependencies(wt_dir)

    # Print success message
    print_success_message(dir_name, branch)


if __name__ == '__main__':
    main()
