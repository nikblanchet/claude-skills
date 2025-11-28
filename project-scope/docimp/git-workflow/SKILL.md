---
name: git-workflow
description: Git worktree-based workflow for docimp project. This skill should be used when creating worktrees, committing code, working with GitHub issues/PRs, monitoring CI/CD, or cleaning up after merge. Covers the complete development lifecycle from worktree creation through cleanup.
---

# Git Workflow

This project uses a bare-repo worktree structure where all branches (including main) exist as separate worktree directories. This enables parallel development across multiple Claude Code instances with shared context.

## Repository Structure

```
docimp/
├── .bare/                     # Bare git repository
├── .git -> .bare              # Symlink for git commands at root
├── .shared/                   # Shared untracked resources
│   ├── .claude/
│   ├── .planning/
│   ├── .scratch/
│   ├── CLAUDE.md
│   └── CLAUDE_CONTEXT.md
├── .claude -> .shared/.claude # Root-level symlinks for Claude Code
├── main/                      # Main branch worktree
├── issue-336/                 # Feature worktrees (siblings of main/)
└── content-policy/
```

Key points:
- All branches are worktrees, including `main`
- Shared resources live in `.shared/` and are symlinked into each worktree
- Each worktree has its own `.venv/` (not shared)
- Run Python commands from within a worktree, not from repo root

## Creating a Worktree

**NEVER create worktrees manually.** Always use the script:

```bash
uv run python .claude/skills/git-workflow/scripts/create_worktree.py <worktree-name> <branch-name>

# Example:
uv run python .claude/skills/git-workflow/scripts/create_worktree.py issue-400 issue-400-fix-parser

# Branch from non-main:
uv run python .claude/skills/git-workflow/scripts/create_worktree.py hotfix hotfix-urgent --base-branch issue-400
```

The script path works from repo root or any worktree (via symlinks). Run `--help` for all options.

The script automatically:
- Creates the worktree with a new branch
- Sets up all symlinks to shared resources
- Creates Python virtual environment
- Installs dependencies
- Enables direnv

## Commit Workflow

Make incremental commits as logical units complete. Every commit must leave the program in a working state.

### When to Commit

Commit after each logical unit of work is complete and working:
- Tests pass
- No broken functionality
- Code runs without errors

Avoid batching multiple changes. Each commit should be self-contained and understandable in isolation.

### Commit Messages

- Use imperative mood: "Add feature" not "Added feature"
- Focus on "what" and "why"
- Be clear and descriptive

### Push Early, Push Often

Push to remote after commits. Avoid letting work sit locally.

## GitHub Issues

### When to Create Issues

Create a GitHub issue when:
- Work requires tracking or discussion
- Changes affect multiple components
- Bug needs documentation for future reference
- Feature request from user needs acknowledgment

Skip issue creation for:
- Trivial fixes (typos, formatting)
- Work already tracked elsewhere

### Creating Issues

```bash
gh issue create --title "Brief description" --body "Detailed explanation..."
```

Check for duplicates first: `gh issue list --search "keyword"`

## Pull Requests

### Creating a PR

From the worktree, push and create PR:

```bash
git push -u origin <branch-name>
gh pr create --title "Description" --body "Fixes #123..."
```

Link issues appropriately:
- `Fixes #123` - auto-closes issue when PR merges
- `See #123` - references without auto-closing

### CI/CD Monitoring

**Proactively monitor CI/CD checks after creating a PR.** Check status immediately without waiting for user prompting.

```bash
# Check PR status
gh pr checks

# View specific check details
gh pr view --json statusCheckRollup
```

If checks fail:
1. Read the failure logs
2. Fix the issue
3. Push fixes
4. Re-check status

## Code Review

### When to Invoke Code Review

Use the code-review agent before creating a PR for:
- Significant new features
- Complex refactoring
- Security-sensitive changes

For minor fixes, self-review is sufficient.

### Responding to Review Feedback

- Address all comments before requesting re-review
- Push fixes as additional commits (for reviewability)
- Mark conversations as resolved when addressed

## Merging and Cleanup

After PR is approved and merged:

```bash
# From any worktree or repo root
cd <repo-root>
git fetch origin main:main          # Update local main
git worktree remove <worktree-name> # Remove worktree
git branch -d <branch-name>         # Delete local branch
```

Use **squash and merge** to keep main history clean. Remote branches are kept for history.

## Quick Reference

```bash
# List all worktrees
git worktree list

# Create new worktree (always use script!)
uv run python .claude/skills/git-workflow/scripts/create_worktree.py <name> <branch>

# After logical unit complete
git add <files> && git commit -m "Message" && git push

# Create PR
gh pr create --title "..." --body "Fixes #..."

# Check CI status
gh pr checks

# After merge
git worktree remove <name> && git branch -d <branch>
```
