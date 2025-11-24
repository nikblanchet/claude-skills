---
name: rtd-contribution-workflow
description: Guide the Git and pull request workflow for contributing to Read the Docs (readthedocs/readthedocs.org) from a personal fork. Use when creating branches, making commits, or submitting PRs to the Read the Docs project. Covers fork-based workflow, branch naming, commit messages, PR creation, CI/CD checks, and review process.
---

# Read the Docs Contribution Workflow

## Overview

This skill provides the complete workflow for contributing to Read the Docs (readthedocs/readthedocs.org) from a personal fork. It covers Git operations, branch management, commit formatting, cross-repository pull request creation, and the review process.

## Fork-Based Workflow

Read the Docs follows a standard fork-based contribution model where contributors work in their own forks and submit cross-repository pull requests.

### Initial Setup

```bash
# Fork the repository on GitHub first (via web UI)

# Clone your fork
git clone --recurse-submodules git@github.com:YOUR-USERNAME/readthedocs.org.git
cd readthedocs.org

# Add upstream remote
git remote add upstream https://github.com/readthedocs/readthedocs.org.git

# Verify remotes
git remote -v
# Should show:
# origin    git@github.com:YOUR-USERNAME/readthedocs.org.git (fetch/push)
# upstream  https://github.com/readthedocs/readthedocs.org.git (fetch/push)
```

### Keeping Fork in Sync

Before starting work on any issue, sync your fork with upstream:

```bash
# Fetch latest changes from upstream
git fetch upstream

# Update your local main branch
git checkout main
git merge upstream/main --ff-only

# Push updates to your fork
git push origin main
```

## Branch Naming Conventions

Branch names should follow the pattern: `category/brief-description`

**Common categories:**
- `docs/` - Documentation changes
- `fix/` - Bug fixes
- `build/` - Build system changes
- `search/` - Search-related features
- `api/` - API changes
- `test/` - Test improvements
- `feature/` - New features

**Examples:**
```bash
# For issue #7761 (document --backupdb argument)
git checkout -b docs/document-backupdb-argument

# For a bug fix
git checkout -b fix/multiple-integrations-error

# For a build improvement
git checkout -b build/update-python-versions
```

**Pattern:** Use lowercase, hyphens for spaces, descriptive but concise

## Commit Message Format

Commit messages must follow this exact format:

```
Category: brief description in imperative mood (#issue)
```

**Rules:**
- Start with category (same as branch prefix: Docs, Fix, Build, Search, API, etc.)
- Use imperative mood ("add" not "added", "fix" not "fixed")
- Capitalize only the first word (sentence case)
- No trailing period
- Include issue number in parentheses if applicable
- Keep under 72 characters for the subject line

**Examples:**
```bash
git commit -m "Docs: document --backupdb argument (#7761)"
git commit -m "Fix: handle MultipleObjectsReturned in integration lookup (#12581)"
git commit -m "Build: add Python 3.14 to build images (#12523)"
git commit -m "Search: optimize queryset for subproject search"
git commit -m "Dependencies: update all packages via pip-tools"
```

**What NOT to do:**
```bash
# ❌ Wrong: not imperative mood
git commit -m "Docs: documented the backupdb argument"

# ❌ Wrong: trailing period
git commit -m "Fix: handle duplicate integrations."

# ❌ Wrong: missing category
git commit -m "Update documentation for backupdb"

# ❌ Wrong: title case instead of sentence case
git commit -m "Docs: Document --backupdb Argument"
```

## Creating a Pull Request

### Pre-Submit Checklist

Before creating a PR, verify all checks pass:

```bash
# 1. Run full test suite
tox
# or inside Docker:
inv docker.test

# 2. Run linting
tox -e pre-commit
# or directly:
pre-commit run --all-files

# 3. Check for missing migrations (if code changes models)
tox -e migrations
# or:
inv docker.manage makemigrations --check --dry-run

# 4. If documentation changes, build locally
cd docs && make html
# or:
tox -e docs
```

### Push to Your Fork

```bash
# Push your feature branch to your fork
git push origin docs/document-backupdb-argument

# If you need to force push after rebase (use with caution)
git push origin docs/document-backupdb-argument --force-with-lease
```

### Create Cross-Repository PR

Since you're working from a fork, the PR must specify both repositories:

```bash
# Using GitHub CLI (recommended)
gh pr create \
  --repo readthedocs/readthedocs.org \
  --base main \
  --head YOUR-USERNAME:docs/document-backupdb-argument \
  --title "Docs: document --backupdb argument (#7761)" \
  --body "$(cat <<'EOF'
[Problem statement - what issue this solves]

## Changes

- [Bullet point of change 1]
- [Bullet point of change 2]
- [Bullet point of change 3]

[Verification statement - how you tested]

Closes #7761
EOF
)"
```

**PR Title Format:**
- Must match commit message format: `Category: description (#issue)`
- Will be used as the merge commit message

**PR Description Template:**
```markdown
[1-2 sentence problem statement explaining what issue this addresses]

## Changes

- [Specific change 1]
- [Specific change 2]
- [Specific change 3]

[1-2 sentences about how changes were tested and verified]

Closes #ISSUE_NUMBER
```

**Real Example (from merged PR #12583):**
```markdown
Docusaurus requires the `trailingSlash` option to be explicitly set when hosting on Read the Docs to avoid redirect issues.

## Changes

- Added section to Docusaurus guide documenting the `trailingSlash: true` requirement
- Explained why this is necessary (Read the Docs URL structure)
- Included code example in the configuration

Successfully built documentation locally and verified rendering.

Closes #12570
```

### Alternative: Create PR via GitHub Web UI

If not using `gh` CLI:

1. Push branch to your fork (see above)
2. Visit https://github.com/readthedocs/readthedocs.org
3. GitHub will show "Compare & pull request" banner
4. Verify base repository is `readthedocs/readthedocs.org` and base branch is `main`
5. Verify head repository is `YOUR-USERNAME/readthedocs.org` and compare branch is your feature branch
6. Fill in title and description following format above
7. Click "Create pull request"

## CI/CD Checks

Read the Docs uses CircleCI. All PRs must pass three jobs:

### 1. checks
- Pre-commit hooks (linting, formatting)
- Migration checks
- **Must pass** before merge

### 2. tests
- Main test suite (Python 3.12)
- Includes search tests with Elasticsearch
- Full pytest run with coverage
- **Must pass** before merge

### 3. tests-embedapi
- Embed API test suite
- Separate test configuration
- **Must pass** before merge

### Monitoring CI Status

```bash
# Check PR status and CI checks
gh pr view --repo readthedocs/readthedocs.org PR_NUMBER

# Check only CI status
gh pr checks --repo readthedocs/readthedocs.org PR_NUMBER

# View PR in browser
gh pr view --repo readthedocs/readthedocs.org PR_NUMBER --web
```

### Common CI Failures

**Vale linting failures:**
- Run locally: `vale docs/user/` or `vale docs/dev/`
- Fix prose style issues
- Commit and push fixes

**Migration check failures:**
- Run: `inv docker.manage makemigrations`
- Commit generated migrations
- Push to PR

**Test failures:**
- Run locally: `tox -e py312 -- -k test_name`
- Debug and fix
- Verify all tests pass before pushing

## Review Process

### What to Expect

1. **Response time:** Core team typically responds within 1-2 business days
2. **Review depth:** Expect thorough, constructive feedback
3. **Iteration:** Multiple review rounds are common for complex changes
4. **Documentation previews:** Check auto-generated preview link in PR comments

### Responding to Review Feedback

**When reviewer requests changes:**

```bash
# Make requested changes in your branch
git add changed-files
git commit -m "Address review feedback"
git push origin docs/document-backupdb-argument
```

**When reviewer suggests specific edits:**
- Implement suggestions
- Reply to comments acknowledging changes
- Use "Resolve conversation" when fully addressed

**Response tone:**
- Professional and collaborative
- Don't argue or defend - iterate
- Ask clarifying questions if feedback is unclear
- Thank reviewers for their time

### Example Review Interactions

**Good response:**
```
Thanks for the feedback! I've updated the documentation to:
- Use :guilabel: for the button reference (line 45)
- Break the sentence at semantic boundaries (lines 52-54)
- Add periods to all bullet points (lines 60-65)

Let me know if this looks better!
```

**Request for clarification:**
```
Thanks for reviewing! Quick question about your suggestion on line 30:

> "Consider using a code-block directive here"

Do you mean a `.. code-block:: python` directive, or the inline `:code:` role?
The current example is just a one-liner - want to make sure I understand the preferred style.
```

## Merge and Cleanup

Once approved and CI passes, the core team will merge your PR.

### Post-Merge Cleanup

```bash
# Switch to main branch
git checkout main

# Fetch and merge upstream changes (includes your PR)
git fetch upstream
git merge upstream/main --ff-only

# Push to your fork
git push origin main

# Delete your feature branch locally
git branch -d docs/document-backupdb-argument

# Delete your feature branch on your fork
git push origin --delete docs/document-backupdb-argument
```

## Resources

### references/gh-commands.md

Comprehensive GitHub CLI command reference for working with PRs and issues. Load this when you need advanced GitHub CLI functionality beyond the basics covered here.

### Additional References

- CircleCI dashboard: https://circleci.com/gh/readthedocs/readthedocs.org
- Good first issues: https://github.com/readthedocs/readthedocs.org/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22
- Contributing guide: https://docs.readthedocs.io/en/latest/contribute.html
