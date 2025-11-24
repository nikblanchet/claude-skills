---
name: writethedocs-git-workflow
description: Git workflow, PR process, commit standards, and CI/CD requirements for contributing to Write the Docs (writethedocs.org). Use when creating pull requests, managing branches, or ensuring CI checks pass.
---

# Write the Docs Git Workflow

This skill provides the git workflow, pull request process, commit message standards, and CI/CD requirements for contributing to the Write the Docs project (writethedocs.org repository).

## When to Use This Skill

Use this skill when:
- Creating a pull request to Write the Docs
- Setting up a fork-based workflow
- Writing commit messages
- Troubleshooting failed CI checks
- Understanding what tests must pass before merge

## Repository Information

- **Upstream repository**: https://github.com/writethedocs/www
- **Main branch**: `main` (not `master`)
- **Workflow**: Fork-based contributions
- **Python version**: 3.9 (migrating to 3.12)

## Git Workflow

### 1. Fork and Clone

```bash
# Fork writethedocs/www on GitHub first, then:
git clone git@github.com:YOUR_USERNAME/writethedocs.git
cd writethedocs

# Add upstream remote
git remote add upstream https://github.com/writethedocs/www.git

# Verify remotes
git remote -v
```

### 2. Create Feature Branch

Use descriptive branch names with hyphens:

```bash
# Update your main branch first
git checkout main
git pull upstream main

# Create feature branch
git checkout -b descriptive-feature-name
```

**Good branch names**:
- `fix-typo-in-contributing-guide`
- `add-berlin-2025-speakers`
- `update-python-dependencies`

**Avoid**:
- `patch-1` (non-descriptive)
- `fix_stuff` (underscores, vague)
- `MyFeature` (not lowercase)

### 3. Make Changes and Commit

**Commit message format**:
- Use imperative mood ("Add feature" not "Added feature" or "Adding feature")
- First line: concise summary (50-72 characters)
- Optional body: detailed explanation after blank line
- Reference PR numbers in format `(#1234)` when applicable

**Good commit messages**:
```
Add Berlin 2025 thank you post (#2463)

Update day of week dates for 2026 (#2475)

Fix broken link in contributing guide

Update dependencies for Python 3.12 migration

- myst-parser: 0.18.0 → 4.0.1
- lxml: 4.8.0 → 5.3.2
- Werkzeug: 0.16.1 → 3.1.3
```

**Avoid**:
```
fixed stuff
Updated files
WIP
asdf
```

### 4. Push and Create PR

```bash
# Push to your fork
git push -u origin your-branch-name

# Create PR on GitHub
# Title should be descriptive, like commit message
# Description should explain what/why
```

**PR best practices**:
- Descriptive title (similar to commit message)
- Clear description of changes and rationale
- Reference related issues if applicable
- Mark as draft if work-in-progress
- For cross-repo PRs (fork to upstream): this is standard workflow

## Required CI/CD Checks

All pull requests must pass **6 automated checks** before merge. See `references/ci-checks.md` for detailed information.

### Quick Overview

1. **Ubuntu Build** - Sphinx build must succeed on Linux
2. **Windows Build** - Sphinx build must succeed on Windows
3. **Spellcheck** - No spelling errors (codespell)
4. **Vale Linting** - 3 separate prose checks (general, guide, news)
5. **YAML Validation** - All conference YAML must pass schema validation
6. **Read the Docs Preview** - Automatic preview build

### Common Failures and Fixes

**Build failures**:
```bash
# Test locally first
cd docs
make clean html

# Check for errors in output
```

**Spellcheck failures**:
- Check `codespell/ignore.txt` for allowed exceptions
- Fix actual typos (don't add to ignore list if it's a real error)

**Vale failures**:
- Most common: heading capitalization (must be sentence case)
- Branding: "Write the Docs" not "Write The Docs"
- Test locally: `vale --config=vale/vale.ini docs/`

**YAML validation failures**:
```bash
# Run validation script
cd docs/_scripts
./validate-yaml.sh

# Check schema files in docs/_data/schema-*.yaml
```

## Local Testing Before PR

**Minimum testing**:
```bash
# 1. Build docs
cd docs
make clean html

# 2. Check for warnings/errors in output

# 3. Test live preview (optional but recommended)
make livehtml
# Open http://127.0.0.1:8888
```

**Comprehensive testing** (recommended for large changes):
```bash
# Run all local checks
cd docs

# Build
make clean html

# Spellcheck (if installed)
codespell docs/

# Vale linting (if installed)
vale --config=vale/vale.ini docs/

# YAML validation
cd _scripts
./validate-yaml.sh

# Link checking (if Ruby/htmlproofer installed)
cd ..
bundle exec htmlproofer --ignore-files "/404/,/2013/,/2014/,/2015/,/2016/,/2017/,/search\/index.html/,/archive\/tag\/index/" \
  --allow-hash-href=true --enforce-https=false --ignore-missing-alt=true --disable-external=true _build/html
```

## Cross-Repo PR Considerations

When creating PRs from your fork to upstream `writethedocs/www`:

**What to include**:
- Only changes relevant to the feature/fix
- No fork-specific files (like CLAUDE.md)
- No local configuration changes

**What to exclude**:
- Add fork-specific files to `.git/info/exclude` (local-only ignore)
- Use feature branches, not main branch
- Keep main branch clean for syncing with upstream

**Syncing with upstream**:
```bash
# Regularly update your fork's main branch
git checkout main
git pull upstream main
git push origin main

# Rebase feature branch if needed
git checkout your-feature-branch
git rebase main
```

## Team Review Process

- **Community-driven reviews**: Anyone can review and comment
- **Team leads**: Have final merge authority
- **Response time**: Varies (community-driven, no SLA)
- **Respectful communication**: Follow Code of Conduct

## Additional Resources

- See `references/ci-checks.md` for detailed CI/CD documentation
- Contributing guide: https://www.writethedocs.org/guide/contributing/
- Code of Conduct: https://www.writethedocs.org/code-of-conduct/
