---
name: GitHub Pull Requests
description: Create and manage pull requests with automatic CI/CD monitoring, issue linking, and squash merges using gh CLI
version: 1.0.0
---

# GitHub Pull Requests

Use GitHub CLI (`gh`) for creating PRs and merging. Always monitor CI/CD checks and link issues appropriately.

## Creating Pull Requests

Use `gh pr create` with clear title and body:

```bash
gh pr create --title "Add feature X" --body "Description of changes..."
```

**Title guidelines:**
- Clear and descriptive
- Summarize the change
- Use imperative mood

**Body guidelines:**
- Explain what changed and why
- Include testing notes if relevant
- Link related issues (see below)
- Remember: No emoji (developer-facing content)

## Linking Issues in PRs

**When the PR fixes or resolves issues**, use GitHub's auto-closing keywords in the PR description or commit messages:

- `Fixes #123`
- `Closes #456`
- `Resolves #789`

These keywords will automatically close the referenced issues when the PR is merged.

**When the PR references but doesn't fix issues** (e.g., citing a known bug, mentioning related work):

- Use plain references: `See #123` or `Related to #456`
- Do NOT use auto-closing keywords
- These issues should remain open after merge

**Multiple issues in one PR:**
```markdown
Fixes #123
Resolves #456

This PR addresses the parser validation errors and improves error messages.
See also #789 for related future work.
```

## Automatic CI/CD Monitoring

**After opening a PR, automatically monitor CI/CD checks.**

- If checks fail, investigate and fix the underlying issue immediately
- Don't wait to be prompted
- Things aren't ready for review until all checks pass
- Push fixes and verify checks pass before requesting review

```bash
# Check PR status
gh pr status

# View detailed check results
gh pr checks
```

## Merging

**Always use Squash and Merge** when merging to main:

```bash
gh pr merge --squash
```

This keeps main history clean while preserving detailed development history on the feature branch.

## After Merging: Verify and Clean Up

**1. Verify the PR was successfully merged:**
```bash
gh pr view --json state,mergedAt
# Or for human-readable output:
gh pr view
```

**2. Check any issues that were referenced:**

If issues were supposed to be auto-closed (`Fixes #123`):
- Verify they are closed
- Manually close any that weren't auto-closed

If issues were only referenced (`See #123`):
- Verify they were NOT auto-closed
- Reopen if accidentally closed, with a comment explaining why

```bash
# Single issue
gh issue view 123

# Multiple issues (efficient, parallel)
echo "123 456 789" | xargs -n1 -P4 gh issue view

# Close if needed
gh issue close 123 --comment "Fixed in PR #XYZ"

# Reopen if accidentally closed
gh issue reopen 789 --comment "This issue was referenced but not fixed in PR #XYZ"
```

**3. Check out the target branch and clean up:**

**Feature branch → main:**
```bash
git checkout main
git pull
git branch -d feature-branch-name  # Delete local feature branch
# DO NOT delete remote feature branch (keep for history)
```

**Issue branch → feature branch:**
```bash
git checkout feature-branch-name
git pull
git branch -d issue-branch-name  # Delete local issue branch
# DO NOT delete remote issue branch (keep for history)
# Continue working on the feature
```

## Quick Reference

```bash
# Create PR with issue links
gh pr create --title "Fix parser validation" --body "Fixes #123

Improves error handling in the TypeScript parser.

See #456 for related future work."

# Check CI/CD status
gh pr status
gh pr checks

# Merge when checks pass
gh pr merge --squash

# Verify merge succeeded
gh pr view --json state,mergedAt

# Verify issues were handled correctly (parallel check)
echo "123 456" | xargs -n1 -P4 gh issue view

# Clean up: checkout the TARGET branch
git checkout <branch-that-was-merged-into>
git pull
git branch -d <branch-that-was-merged>
```

## Remember

- Use auto-closing keywords (`Fixes`, `Closes`, `Resolves`) for issues being fixed
- Use plain references (`See #123`) for issues not being fixed
- Verify PR merge succeeded before checking issues
- Verify issue state after merge (use parallel xargs for multiple issues)
- Check out the branch that was merged INTO (main or feature branch)
- CI/CD checks must pass before merge
- Squash and merge keeps main clean
- Keep remote branches for history
- No emoji in PR content (developer-facing)
