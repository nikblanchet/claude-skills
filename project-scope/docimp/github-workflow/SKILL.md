---
name: github-workflow
description: GitHub workflow using gh CLI - create issues with duplicate checking and labels, create PRs with CI/CD monitoring, link issues to PRs, squash-merge to main. Use when creating issues, filing bugs, opening PRs, merging pull requests, or managing GitHub workflow.
---

# GitHub Workflow

Use GitHub CLI (`gh`) for creating issues and managing pull requests. Always check for duplicates, use appropriate labels, monitor CI/CD, and link issues to PRs.

## Issue Management

Create clear, well-labeled issues. Always check for duplicates first and manage labels effectively.

### Before Creating New Issues

**CRITICAL: Check for duplicates first.**

1. Search existing **open** issues
2. Search **closed** issues too (the problem may have been addressed)
3. If duplicate exists, add context to existing issue rather than creating new one

```bash
# List and search existing issues
gh issue list
gh issue list --state all  # Include closed issues
gh issue list --search "keyword"
```

### Creating Issues

**1. Pull the current list of labels:**
```bash
gh label list
```

**2. Create the issue with appropriate existing labels:**
```bash
gh issue create --title "..." --body "..." --label "bug,documentation"
```

**3. If a label gap exists:**

Create a new label when:
- Something would add clarity
- The category would come up repeatedly
- No existing label captures the concept

```bash
# Create new label
gh label create "label-name" --description "..." --color "..."

# Then apply it to the issue
gh issue edit ISSUE_NUMBER --add-label "label-name"
```

### Issue Quality Standards

**Titles:**
- Clear and descriptive
- Summarize the issue
- Good: "Parser fails on nested arrow functions"
- Bad: "Bug in parser" or "Fix this"

**Body content:**
- **For bugs**: What's wrong, why it matters, how to reproduce
- **For features**: What you want, why it's valuable, acceptance criteria
- **For documentation**: What's missing or unclear, where it should go
- Provide context that helps others understand without back-and-forth

**Remember**: No emoji (developer-facing content) unless quoting

### Labeling Strategy

**Common label categories:**
- Type: `bug`, `enhancement`, `documentation`, `question`
- Priority: `high-priority`, `low-priority`
- Status: `needs-investigation`, `ready-for-review`, `blocked`
- Area: `parser`, `cli`, `testing`, `ci-cd`

**Apply multiple labels when appropriate:**
```bash
gh issue create --title "Add JSDoc validation" \
  --body "..." \
  --label "enhancement,documentation,parser"
```

## Pull Request Workflow

Use GitHub CLI (`gh`) for creating PRs and merging. Always monitor CI/CD checks and link issues appropriately.

### Creating Pull Requests

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

### Linking Issues in PRs

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

### Automatic CI/CD Monitoring

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

### Merging

**Always use Squash and Merge** when merging to main:

```bash
gh pr merge --squash
```

This keeps main history clean while preserving detailed development history on the feature branch.

### After Merging: Verify and Clean Up

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
# Create issue - check duplicates first
gh issue list --search "keyword"
gh label list
gh issue create --title "..." --body "..." --label "bug,enhancement"

# Create PR with issue links
gh pr create --title "Fix parser validation" --body "Fixes #123

Improves error handling in the TypeScript parser.

See #456 for related future work."

# Monitor CI/CD status
gh pr status
gh pr checks

# Merge when checks pass
gh pr merge --squash

# Verify merge and issues
gh pr view --json state,mergedAt
echo "123 456" | xargs -n1 -P4 gh issue view

# Clean up: checkout the TARGET branch
git checkout <branch-that-was-merged-into>
git pull
git branch -d <branch-that-was-merged>
```

## Remember

- Check for duplicate issues before creating (open AND closed)
- Pull label list before creating issues
- Use clear, descriptive titles
- Apply appropriate existing labels
- Use auto-closing keywords (`Fixes`, `Closes`, `Resolves`) for issues being fixed
- Use plain references (`See #123`) for issues not being fixed
- Monitor CI/CD checks immediately after creating PR
- Fix failures before requesting review
- Squash and merge keeps main clean
- Verify merge succeeded before checking issues
- Check out the branch that was merged INTO (main or feature branch)
- Keep remote branches for history
- No emoji in issues or PR content (developer-facing)
