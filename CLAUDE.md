# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a personal collection of **Claude Code skills** - reusable instruction sets that modify Claude's behavior when working on projects. Skills provide specialized capabilities, enforce development standards, and automate complex workflows.

## Architecture Overview

### Dual-Scope System

The repository implements a two-tier skill architecture:

- **global-scope/**: Universal development standards applied to all projects (8 active skills)
- **project-scope/**: Project-specific overrides and extensions organized by project name (docimp, brotein-buddy)

Project skills can inherit from global skills or completely replace their implementation.

### Skill Structure

Every skill follows a standard directory structure:

```
skill-name/
├── SKILL.md                    # Main skill definition with YAML frontmatter
├── scripts/                    # Executable automation (Python, Bash, etc.)
├── references/                 # Detailed documentation loaded on-demand
└── assets/                     # Templates and boilerplate files
```

SKILL.md files begin with YAML frontmatter:
```yaml
---
name: skill-name
description: When to use this skill and what it does
---
```

### Skill Activation

Skills are activated by symlinking them to `~/.claude/skills/`:

```bash
# Activate a skill
ln -s ~/Code/repos/custom-claude-skills/global-scope/skill-name ~/.claude/skills/skill-name

# Deactivate a skill
rm ~/.claude/skills/skill-name

# List active skills
ls ~/.claude/skills/
```

The `access-skill-resources` skill teaches how to navigate symlinks and locate bundled resources (scripts/, references/, assets/) within skill directories.

## Critical Development Standards

### NO EMOJI Rule (Critical)

**Zero colorful emoji presentation characters in developer-facing content.**

- Forbidden: ✅ ❌ 🎉 and all colored emoji
- Applies to: code, commits, PRs, issues, documentation, CLI output
- Test: If it renders in color on a smartphone, don't use it
- Rationale: Emoji signals "AI wrote this and a human didn't review it"
- Exceptions: Quoting external content that contains emoji
- Acceptable: Emoticons `:)`, monospace symbols `✓`, ANSI color codes

### Modern Language Features

- Default to latest stable versions (Python 3.13+, latest TypeScript)
- Use cutting-edge features when they improve code clarity
- Don't maintain backward compatibility unless explicitly required
- Document minimum version requirements clearly

### Testing Philosophy

- Exhaustive testing is expected: unit, integration, regression, E2E, manual
- Spending 60% of time on tests vs 40% coding is acceptable and encouraged
- All tests must pass before merge
- Watch for deprecation warnings in test output and address immediately
- Document manual test procedures when automation isn't feasible

### Dependency Management

- Use quality dependencies freely - don't reinvent the wheel
- Python: Prefer conda over pip, maintain separate `requirements-conda.txt` and `requirements-pip.txt`
- Stay reasonably current with updates and address security advisories

### CLI UX Standards

- Colorful terminal output is excellent - use ANSI color codes
- Standard conventions: red=error, yellow=warning, green=success, blue=info
- Use libraries: `rich` (Python), `chalk` (Node.js)
- Respect `NO_COLOR` environment variable
- Test in both light and dark terminal themes

## Git Workflows

### Standard Feature Branch Workflow

```bash
# Start new feature
git checkout main && git pull
git checkout -b descriptive-feature-name

# Work incrementally - commit after each logical unit
git add <files>
git commit -m "Clear, descriptive message"
git push

# Create PR with issue linking
gh pr create --title "Feature description" --body "Fixes #123..."
```

**Principles:**
- Incremental commits after each logical unit of work
- Push early, push often - don't let work sit locally
- All work happens on feature branches
- Squash and merge to main for clean history
- Keep remote branches after merge (don't delete)

### Worktree-based Workflow (DocImp Project)

The docimp project uses git worktrees for parallel development with git hooks enforcing the workflow.

**One-time setup:**
```bash
# Install hooks to protect main branch
/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 .claude/skills/git-workflow/scripts/install_hooks.py
```

**Create worktree for feature/issue:**
```bash
# Script handles branch creation, worktree setup, and symlink creation
/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 .claude/skills/git-workflow/scripts/create_worktree.py <branch-name> [base-branch]
```

The script:
- Creates feature branch from base (defaults to current branch)
- Sets up worktree in `../.docimp-wt/<branch-name>/`
- Creates symlinks to shared context (`.claude/`, `.scratch/`, planning docs)
- Sets up isolated `.venv/` for the worktree
- Detects uncommitted changes and handles them appropriately

**Work in worktree:**
```bash
cd ../.docimp-wt/<branch-name>
# Make changes, commit, push as normal
git add <files> && git commit -m "Message" && git push
```

**Cleanup after merge:**
```bash
cd <project-root>
git checkout main && git pull
git worktree remove ../.docimp-wt/<branch-name>
git branch -d <branch-name>
```

**Git hooks protect main branch:**
- `pre-commit`: Blocks commits on main branch in main worktree
- `post-checkout`: Blocks branch checkouts in main worktree
- Forces use of worktrees for all feature development
- Hooks only affect main worktree; feature worktrees remain unrestricted

## Key Architectural Patterns

### Skill Consolidation

The repository evolved from granular skills to consolidated skills:
- Original: 7 separate skills (no-emoji, modern-language-versions, thorough-documentation, etc.)
- Consolidated: Merged into single `development-standards` skill
- Rationale: Related concepts are easier to understand and apply when grouped together

### References Separation

Skills separate core instructions from detailed reference material:
- **SKILL.md**: Concise, action-oriented guidance for quick reference
- **references/**: Deep-dive documentation loaded only when needed
- Examples: `review-dimensions.md`, `severity-classifications.md`, `python-313-conventions.md`

### Bundled Scripts

Complex workflows are automated with well-documented Python scripts:
- `create_worktree.py`: Sophisticated worktree creation with change detection and symlink setup
- `install_hooks.py`: Git hook installation with validation and error handling
- Scripts use colored terminal output (ANSI codes, not emoji)
- Comprehensive docstrings and usage examples

### Shared Context via Symlinks

In worktree-based development, shared files are symlinked into each worktree:
- `.claude/` directory (skills, settings)
- `.scratch/` directory (code reviews, temporary files)
- Planning documents (WARP.md, PROGRESS.md)
- Enables access to shared context across all worktrees
- Per-worktree isolation for `.venv/` and code changes

## Common Development Commands

### Testing

```bash
# Python
/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 -m pytest -v
/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 -m pytest --cov

# Node.js
npm test
npm run test:coverage
npm run test:e2e
```

### Code Quality

```bash
# Python
ruff check
mypy src/

# Node.js
npm run lint
npm run format
npm run check
```

## GitHub Workflow

- Check for duplicate issues before creating new ones
- Pull label list before applying labels to issues/PRs
- Monitor CI/CD immediately after opening PR
- Link issues appropriately:
  - `Fixes #123` for auto-closing when PR merges
  - `See #123` for references without auto-closing
- Squash and merge to main
- Keep remote branches for history (don't delete after merge)

## Code Review Standards

Reviews follow an 11-dimension framework covering:
- Functional completeness (verify PR implements all requirements from linked issues)
- Architecture and design patterns
- Testing coverage and quality
- Security vulnerabilities
- Performance implications
- Maintainability and code quality
- Documentation
- Error handling
- Dependencies and version compatibility
- Backward compatibility
- Deployment and rollback

Severity classifications:
- **Blocker**: Must fix before merge (security, data loss, critical bugs)
- **Critical**: Should fix before merge (major bugs, significant issues)
- **Important**: Should fix soon (moderate issues, technical debt)
- **Enhancement**: Nice to have (optimizations, minor improvements)
- **Nitpick**: Optional (style preferences, tiny optimizations)

Save detailed reviews to `.scratch/code-review-pr-{NUMBER}-{ISO-DATE}.md`

## Project-Specific Notes

### DocImp
- Worktree-based development enforced via git hooks
- Shared context architecture with symlinks
- Per-worktree Python virtual environments
- Main worktree is read-only (no commits or branch switching)

### BroteinBuddy
- 90% overall coverage, 100% critical paths required
- Tech stack: Svelte 5 + TypeScript, Vite, Vitest, Playwright
- Pre-commit hooks via Husky + lint-staged
- Documentation: README.md (user), DEVELOPING.md (developer), ADRs

## Repository Metadata

- **Main branch**: `main`
- **Git hosting**: GitHub
- **Local settings**: Pre-approved permissions in `.claude/settings.local.json` for common git/bash operations
