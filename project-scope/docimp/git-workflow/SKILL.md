---
name: git-workflow
description: Git worktree-based workflow for parallel development with shared context. Incremental commits after logical units, feature branches with nested issue branches, squash-merge to main. Use when creating/managing worktrees, working on parallel features, committing code, creating branches, or handling branch cleanup.
---

# Git Workflow

Use incremental commits and feature branch workflow for all development work. Make commits frequently as logical units complete, and organize work using feature branches with nested issue branches.

## Commit Workflow

Make incremental commits as you work. Don't wait until everything is done.

### Core Principle: Every Commit Must Leave the Program in a Good State

**Required for every commit:**
- Tests pass
- No broken functionality
- Code runs without errors

A commit should represent a complete, working increment of functionality - however small.

### When to Commit

**Commit after each logical unit of work is complete and working.**

Don't batch up multiple changes before committing. Each commit should be a self-contained change that could be understood in isolation.

#### Example: Display System Feature

Instead of one large commit at the end:

```
Commit 1: Add IDisplay interface
Commit 2: Add display dependencies to package.json
Commit 3: Implement TerminalDisplay class
Commit 4: Refactor command to inject display
```

Each commit is:
- A complete unit of work
- Independently understandable
- In a working state (tests pass, code runs)

### Push Early, Push Often

- Push to remote ASAP after commits
- Don't let work sit locally
- Makes work visible and creates backups
- Enables collaboration and early feedback

### Commit Messages

**Good commit messages:**
- Use clear, descriptive language
- Focus on "what" and "why" rather than just "how"
- Use imperative mood ("Add feature" not "Added feature" or "Adds feature")
- Follow project conventions if they exist

**Examples:**
- "Add IDisplay interface for terminal output abstraction"
- "Implement incremental commit workflow in git-commit skill"
- "Fix type validation in JSDoc plugin"

### Remember: Squash and Merge Cleans Up Main

Feature branches show granular work with many small commits. When you squash and merge to main, the history is clean and focused. This means:

- **On feature branches**: Commit frequently, keep commits small and focused
- **On main**: Each merge represents a complete feature or fix
- You get the best of both worlds: detailed history during development, clean history in main

### What This Is Not

This is not:
- Committing broken code ("I'll fix it in the next commit")
- Committing work-in-progress that doesn't run
- Holding off on commits until a feature is "perfect"
- Making commits so large they include multiple unrelated changes

## Worktree-Based Development (DocImp Default)

This project uses **git worktrees** for all development. Each feature or issue gets its own worktree (separate working directory) with its own branch.

### Why Worktrees

- **Parallel development**: Work on multiple features simultaneously in separate Claude Code instances
- **Shared context**: Code reviews, planning docs, and runbooks accessible across all worktrees
- **Clean isolation**: Each worktree has its own branch and working directory
- **No context switching**: No need to stash changes when switching between features

### Creating a New Worktree

**Default workflow:** Use the helper script for all new features/issues:

```bash
cd <project-root>
python3 .claude/skills/git-workflow/scripts/create_worktree.py <worktree-name> <branch-name>

# Example for new feature (branches from main):
python3 .claude/skills/git-workflow/scripts/create_worktree.py issue-260 issue-260-display-consistency

# Branch from a different source branch:
python3 .claude/skills/git-workflow/scripts/create_worktree.py issue-200 fix-parser --source-branch issue-150

# Exclude uncommitted/unpushed changes from source:
python3 .claude/skills/git-workflow/scripts/create_worktree.py issue-200 fix-parser --source-branch issue-150 --exclude-changes

# Include all changes from source (non-interactive):
python3 .claude/skills/git-workflow/scripts/create_worktree.py issue-200 fix-parser --source-branch issue-150 --include-changes=all

# Auto-install hooks if missing:
python3 .claude/skills/git-workflow/scripts/create_worktree.py issue-260 issue-260-display-consistency --install-hooks-if-missing
```

The script automatically sets up symlinks, hooks, and dependencies. See script `--help` for full options.

### Per-Worktree Python Environments

Each worktree gets its own isolated Python virtual environment:

- `.venv/` created via `uv venv` during worktree setup
- `.envrc` copied from main repo for direnv integration
- Run `direnv allow` to enable automatic activation
- No shared state between worktrees (prevents lock contention)
- Dependencies managed per-worktree with uv

### Branch Naming

- Use descriptive names that explain the work
- Include issue number for traceability
- **Good**: `issue-260-display-consistency`, `issue-221-improve-styleguides`
- **Bad**: `feature-1`, `my-branch`, `updates`

### Nested Issue Branches

When you discover a sub-issue while working on a feature:

1. **Create a new worktree from the feature branch** (not main):
   ```bash
   cd <project-root>
   python3 .claude/skills/git-workflow/scripts/create_worktree.py issue-260-fix issue-260-fix --source-branch issue-260
   ```

2. **Address the sub-issue** using frequent commits

3. **Open a PR back to the feature branch** (not main)
   - Keeps work organized
   - Allows independent review of fixes
   - Maintains clear history

4. **Merge to feature branch**, then continue feature work in original worktree

### Merging to Main

When the feature is complete:

1. **From the worktree**, push your branch:
   ```bash
   cd ../.docimp-wt/issue-260
   git push -u origin issue-260-display-consistency
   ```

2. **Open a PR** to `main` using GitHub CLI or web interface:
   ```bash
   gh pr create --title "Fix progress display consistency" --body "Fixes #260..."
   ```

3. **After merge**, clean up:
   ```bash
   cd <project-root>                    # Return to main repo
   git checkout main && git pull        # Update main
   git worktree remove ../.docimp-wt/issue-260  # Remove worktree
   git branch -d issue-260-display-consistency  # Delete local branch
   # Remote branch kept for history
   ```

Use **squash and merge** to keep main history clean while preserving detailed development history on the feature branch.

### Why Worktrees Work Better

**vs. Traditional Branching:**
- No need to stash/commit incomplete work when switching tasks
- Each worktree has independent state (no conflicts)
- Shared context files (code reviews, planning) accessible everywhere
- Can run tests in one worktree while coding in another
- Can run multiple instances of Claude Code in separate worktrees

**Squash and merge:**
- Main branch gets clean, focused history
- Feature branches preserve detailed development history
- Best of both worlds: detail during development, clarity in main

## Protecting Main Branch

Git hooks protect the main branch from accidental commits and branch checkouts. These hooks only affect the main worktree - feature worktrees remain unrestricted.

### Installing Hooks

Install hooks once when setting up the repository:

```bash
cd <project-root>
python3 scripts/install_hooks.py
```

The `create_worktree.py` script automatically checks if hooks are installed and prompts to install them if missing. Use the `--install-hooks-if-missing` flag to auto-install without prompting.

### What the Hooks Do

**pre-commit hook:**
- Blocks commits on the main branch in the main worktree
- Displays error message with instructions to use worktrees
- Feature worktrees unaffected

**post-checkout hook:**
- Blocks checking out branches other than main in the main worktree
- Automatically reverts back to main branch
- Displays error message with worktree creation instructions
- Feature worktrees unaffected

### Bypassing Hooks

For maintenance tasks that legitimately require working on main:

```bash
git commit --no-verify  # Skip pre-commit hook
```

Use sparingly and only for necessary maintenance tasks.

### Hook Behavior Examples

**Blocked commit on main:**
```bash
cd <project-root>
git checkout main
echo "test" > file.txt
git add file.txt
git commit -m "Test"

# Output:
# ✗ COMMIT BLOCKED
# Cannot commit on main branch in the main worktree.
# Use: python3 scripts/create_worktree.py <name> <branch>
```

**Blocked branch checkout:**
```bash
cd <project-root>
git checkout feature-branch

# Output:
# ✗ CHECKOUT BLOCKED
# Cannot check out branch 'feature-branch' in the main worktree.
# Automatically reverting to main branch...
```

**Allowed in feature worktree:**
```bash
cd ../.docimp-wt/issue-260
git checkout -b hotfix  # Works fine
git commit -m "Fix"     # Works fine
```

## Quick Reference

```bash
# Install hooks (one-time setup)
cd <project-root>
python3 scripts/install_hooks.py

# Start new feature/issue (DEFAULT WORKFLOW)
cd <project-root>
python3 scripts/create_worktree.py issue-260 issue-260-display-consistency
cd ../.docimp-wt/issue-260

# After completing a logical unit of work:
git add <files>
git commit -m "Clear, descriptive message"
git push

# Feature complete?
gh pr create --title "..." --body "Fixes #260..."

# After PR merged:
cd <project-root>
git checkout main && git pull
git worktree remove ../.docimp-wt/issue-260 && git branch -d issue-260-display-consistency

# Check all worktrees:
git worktree list
```

## Advanced: Worktree Setup Details

The sections above cover the standard workflow. This section provides details about the worktree infrastructure for troubleshooting or manual setup.

### Directory Structure

```
~/projects/
├── docimp/                    # Main repo (main branch)
├── .docimp-wt/               # Hidden worktrees directory
│   ├── issue-221/            # Worktree branches
│   └── issue-243/
└── .docimp-shared/           # Shared gitignored files
    ├── CLAUDE.md
    ├── CLAUDE_CONTEXT.md
    ├── .planning/
    ├── .scratch/             # Code reviews, runbooks
    └── .claude/
        ├── skills/           # Shared skills
        └── settings.local.json  # Shared local settings
```

### Helper Script Details

The `create_worktree.py` script automates worktree creation. See script docstring for full documentation.

**Key flags:**
- `--source-branch SOURCE`: Branch to create from (default: main)
- `--include-changes {none,uncommitted,unpushed,all}`: Include changes from source worktree
- `--exclude-changes`: Exclude all changes from source worktree
- `--install-hooks-if-missing`: Auto-install hooks without prompting

### Manual Worktree Creation (Troubleshooting Only)

```bash
cd <project-root>
git checkout main && git pull
mkdir -p ../.docimp-wt  # First time only
git worktree add ../.docimp-wt/issue-XXX -b issue-XXX-description

# Create symlinks in new worktree
cd ../.docimp-wt/issue-XXX
ln -s ../../.docimp-shared/CLAUDE.md CLAUDE.md
ln -s ../../.docimp-shared/CLAUDE_CONTEXT.md CLAUDE_CONTEXT.md
ln -s ../../.docimp-shared/.planning .planning
ln -s ../../.docimp-shared/.scratch .scratch
mkdir -p docs
ln -s ../../../.docimp-shared/docs/patterns docs/patterns
mkdir -p .claude
ln -s ../../../.docimp-shared/.claude/skills .claude/skills
ln -s ../../../.docimp-shared/.claude/settings.local.json .claude/settings.local.json
```

### Initial Shared Directory Setup (One-Time)

If setting up shared files for the first time:

```bash
cd <project-root>

# Create shared directory
mkdir -p ../.docimp-shared/.planning ../.docimp-shared/.scratch

# Move existing files to shared location
mv CLAUDE.md ../.docimp-shared/ 2>/dev/null || true
mv CLAUDE_CONTEXT.md ../.docimp-shared/ 2>/dev/null || true
mv .planning/* ../.docimp-shared/.planning/ 2>/dev/null || true
mv .scratch/* ../.docimp-shared/.scratch/ 2>/dev/null || true
rmdir .planning .scratch 2>/dev/null || true

# Create symlinks in main repo
ln -s ../.docimp-shared/CLAUDE.md CLAUDE.md
ln -s ../.docimp-shared/CLAUDE_CONTEXT.md CLAUDE_CONTEXT.md
ln -s ../.docimp-shared/.planning .planning
ln -s ../.docimp-shared/.scratch .scratch
```

### Benefits

- **Parallel development**: Work on multiple issues simultaneously in separate Claude Code instances
- **Shared context**: Code reviews, runbooks, and planning docs accessible across all worktrees
- **Clean isolation**: Each worktree has its own branch and working directory
- **Easy switching**: Open different worktrees in different windows/instances

### Parallel Development Example

Work on two independent issues simultaneously:

```bash
# Terminal 1: Create and work on Issue #221
cd <project-root>
python3 scripts/create_worktree.py issue-221 issue-221-styleguides
cd ../.docimp-wt/issue-221
# Open in Claude Code instance 1

# Terminal 2: Create and work on Issue #243
cd <project-root>
python3 scripts/create_worktree.py issue-243 issue-243-api-timeout
cd ../.docimp-wt/issue-243
# Open in Claude Code instance 2

# Both worktrees have access to:
# - Shared code reviews in .scratch/
# - Shared planning docs in .planning/
# - Same project-specific skills in .claude/skills/
# - Same local settings in .claude/settings.local.json
```

**Check all active worktrees:**

```bash
git worktree list
```
