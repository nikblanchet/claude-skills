---
name: git-workflow
description: Git branching and commit workflow - make incremental working commits after completing logical units, use feature branches with nested issue branches, squash-merge to main. Use when committing code, creating branches, pushing changes, or managing git workflow.
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

## Feature Branch Workflow

Use feature branches for all work. When issues arise during feature development, create issue-specific branches from the feature branch.

### Branching Strategy

**When in doubt, branch and open a PR.**

#### Feature Branches

Create a feature branch from `main` for each logical unit of work:

```bash
git checkout main
git pull
git checkout -b feature-name
```

**Branch naming:**
- Use descriptive names that explain the work
- Include context about what's being built
- Good: `add-display-system`, `implement-jsdoc-validation`, `refactor-scoring-algorithm`
- Bad: `feature-1`, `my-branch`, `updates`

#### Issue Branches (Nested)

When you discover an issue while working on a feature branch:

1. **Create an issue-specific branch from the feature branch**
   ```bash
   git checkout feature-name
   git checkout -b fix-type-error-in-parser
   ```

2. **Address the issue** using frequent commits

3. **Open a PR back to the feature branch** (not main)
   - This keeps work organized
   - Allows independent review of fixes
   - Maintains clear history of what was found and fixed during feature development

4. **Merge to feature branch**, then continue feature work

#### Merging to Main

When the feature is complete:
- Open a PR from feature branch to `main`
- Use **squash and merge** to keep main history clean
- Feature branch shows granular work, main stays focused

### Working on Collaborative Repositories

This workflow is universal and works even when you don't control the repository:

**On your own repositories:**
- Branch directly in the repo
- Create PRs from feature branches

**On others' repositories:**
- Fork the repository
- Use the same feature branch workflow in your fork
- Create PRs from your fork to the upstream repository
- Use nested branches across forks for issue fixes

The branching philosophy remains the same regardless of repository ownership.

### After Merging to Main

```bash
# Switch back to main and update
git checkout main
git pull

# Delete local feature branch (cleanup)
git branch -d feature-name

# DO NOT delete remote feature branch (keep history)
```

### Why This Works

**Feature branches:**
- Isolate work in progress from stable main branch
- Enable parallel development on multiple features
- Provide clear context about what's being built
- Allow experimentation without breaking main

**Issue branches from feature branches:**
- Keep fixes organized and reviewable
- Don't interrupt feature development flow
- Create clear history of problems found and solved
- Allow fixes to be reviewed independently

**Squash and merge:**
- Main branch gets clean, focused history
- Feature branches preserve detailed development history
- Best of both worlds: detail during development, clarity in main

## Quick Reference

```bash
# Start new feature
git checkout main && git pull
git checkout -b descriptive-feature-name

# After completing a logical unit of work:
git add <files>
git commit -m "Clear, descriptive message"
git push

# Work found an issue during feature development?
git checkout -b fix-specific-issue
# Fix, commit, push, PR to feature branch

# After issue fixed, continue feature work
git checkout descriptive-feature-name

# Feature complete?
# Open PR to main with squash-and-merge
```
