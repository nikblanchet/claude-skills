# Git & GitHub Workflow Skill for BroteinBuddy

This skill defines the complete git and GitHub workflow for the BroteinBuddy project, including worktree management, branch naming conventions, commit standards, PR workflow, and merge strategy.

## Path Placeholders in Documentation

Throughout this skill's documentation, you'll see `<python-path>` used as a placeholder. This represents the path to your Python interpreter.

### Local Setup

My local environment uses:
- **Conda environments** for Python dependency management
- **pip** as a fallback for packages not available in conda
- Specific conda environment for BroteinBuddy: `bbud`

In my setup, `<python-path>` resolves to: `/Users/nik/miniconda3/envs/bbud/bin/python`

### Customizing for Your Environment

You have several options for using this skill with your own setup:

#### Option 1: Create a Local Configuration File (Recommended)

Create a gitignored file (e.g., `LOCAL_SETUP.md` at the repository root) that documents your actual paths:

```markdown
# Local Environment Setup

## Python Path
<python-path> = /your/actual/path/to/python

## Example Commands
- Run tests: /your/actual/path/to/python -m pytest
- Create worktree: /your/actual/path/to/python .claude/skills/git-github-workflow/scripts/setup-worktree.py
```

#### Option 2: Use Environment Detection

If you have a SessionStart hook that detects your Python environment, you can reference the detected environment when Claude Code reads this skill.

#### Option 3: Direct Substitution

Simply replace `<python-path>` with your actual path wherever you see it in the documentation.

### Why Placeholders?

Using placeholders makes this skill:
- **Portable**: Can be shared across different machines and setups
- **Flexible**: Works with any Python environment (conda, virtualenv, system Python, etc.)
- **Privacy-preserving**: Doesn't expose local machine details in committed files

## Getting Started

See [SKILL.md](SKILL.md) for the complete workflow documentation.

## Resources

- `scripts/setup-worktree.py` - Interactive worktree creation script
- `references/code-reviewer-guide.md` - How to invoke the code-reviewer agent
- `references/teacher-mentor-guide.md` - How to invoke the teacher-mentor agent
- `references/skill-dependencies.md` - When to invoke related skills
- `references/ci-cd-monitoring.md` - Monitoring GitHub Actions checks
