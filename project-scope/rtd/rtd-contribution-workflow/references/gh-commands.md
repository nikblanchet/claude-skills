# GitHub CLI Commands Reference

Comprehensive reference for `gh` CLI commands when working with Read the Docs contributions.

## Pull Request Commands

### Viewing PRs

```bash
# List all open PRs
gh pr list --repo readthedocs/readthedocs.org

# List your PRs
gh pr list --repo readthedocs/readthedocs.org --author @me

# List PRs by label
gh pr list --repo readthedocs/readthedocs.org --label "good first issue"

# View specific PR details
gh pr view --repo readthedocs/readthedocs.org 12583

# View PR in browser
gh pr view --repo readthedocs/readthedocs.org 12583 --web

# View PR diff
gh pr diff --repo readthedocs/readthedocs.org 12583
```

### Creating PRs

```bash
# Create PR with prompts (interactive)
gh pr create --repo readthedocs/readthedocs.org

# Create PR with all details (non-interactive)
gh pr create \
  --repo readthedocs/readthedocs.org \
  --base main \
  --head username:branch-name \
  --title "Category: description (#issue)" \
  --body "Description here"

# Create draft PR
gh pr create \
  --repo readthedocs/readthedocs.org \
  --draft \
  --title "WIP: Feature name"
```

### Checking CI Status

```bash
# Check all CI checks for a PR
gh pr checks --repo readthedocs/readthedocs.org 12583

# Watch CI checks (auto-refresh)
gh pr checks --repo readthedocs/readthedocs.org 12583 --watch

# Check specific workflow
gh run list --repo readthedocs/readthedocs.org --branch branch-name
```

### Updating PRs

```bash
# Add comment to PR
gh pr comment --repo readthedocs/readthedocs.org 12583 --body "Updated based on feedback"

# Edit PR title/description
gh pr edit --repo readthedocs/readthedocs.org 12583 --title "New title"

# Mark PR as ready for review (un-draft)
gh pr ready --repo readthedocs/readthedocs.org 12583
```

## Issue Commands

### Viewing Issues

```bash
# List all open issues
gh issue list --repo readthedocs/readthedocs.org

# List by label
gh issue list --repo readthedocs/readthedocs.org --label "good first issue"
gh issue list --repo readthedocs/readthedocs.org --label "Sprintable"

# View specific issue
gh issue view --repo readthedocs/readthedocs.org 7761

# View issue in browser
gh issue view --repo readthedocs/readthedocs.org 7761 --web
```

### Common Patterns

```bash
# Find good first issues
gh issue list --repo readthedocs/readthedocs.org --label "good first issue" --label "Accepted"

# Search issues
gh search issues --repo readthedocs/readthedocs.org "documentation"

# Check issue status
gh issue view --repo readthedocs/readthedocs.org 7761 --json state,assignees,labels
```
