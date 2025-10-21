---
name: Git Feature Branch Workflow
description: Use feature branches with nested issue branches, descriptive names, and squash-merge to main
version: 1.0.0
---

# Git Feature Branch Workflow

Use feature branches for all work. When issues arise during feature development, create issue-specific branches from the feature branch.

## Branching Strategy

**When in doubt, branch and open a PR.**

### Feature Branches

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

### Issue Branches (Nested)

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

### Merging to Main

When the feature is complete:
- Open a PR from feature branch to `main`
- Use **squash and merge** to keep main history clean
- Feature branch shows granular work, main stays focused

## Working on Collaborative Repositories

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

## After Merging to Main

```bash
# Switch back to main and update
git checkout main
git pull

# Delete local feature branch (cleanup)
git branch -d feature-name

# DO NOT delete remote feature branch (keep history)
```

## Why This Works

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

# Work found an issue during feature development?
git checkout -b fix-specific-issue
# Fix, commit, push, PR to feature branch

# After issue fixed, continue feature work
git checkout descriptive-feature-name

# Feature complete?
# Open PR to main with squash-and-merge
```
