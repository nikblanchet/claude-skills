# Git & GitHub Workflow Skill for BroteinBuddy

This skill defines the complete git and GitHub workflow for the BroteinBuddy project, including worktree management, branch naming conventions, commit standards, PR workflow, and merge strategy.

## Running Python in This Skill

Throughout this skill's documentation, Python is run with `uv run`. There is no interpreter path to look up or substitute.

BroteinBuddy is a Svelte 5 + TypeScript project with no Python dependencies: it has no `pyproject.toml`, `uv.lock`, or `requirements.txt`, and no Python tests. Its tests are Vitest and Playwright suites run through npm (`npm test`, `npm run test:e2e`).

The only Python involved is this skill's bundled `scripts/setup-worktree.py`. It imports only the standard library and needs Python 3.7 or newer:

```bash
uv run .claude/skills/git-github-workflow/scripts/setup-worktree.py
```

There is nothing to install and no environment to activate.

If BroteinBuddy ever gains Python code with dependencies, declare them in a `pyproject.toml` managed by uv (see the `dependency-management` skill) and run its tests with `uv run pytest`.

### Local Setup

My local environment uses:
- **uv** for Python, with isolated per-project environments
- No packages installed into a global or system interpreter
- **nvm** for Node.js

Earlier versions of this skill used a `<python-path>` placeholder that resolved to the interpreter of a BroteinBuddy-specific Python environment. That environment no longer exists and the placeholder has been retired: every command that used it is now either a `uv run` command or an npm script.

### Customizing for Your Environment

You have two options for using this skill with your own setup:

#### Option 1: SessionStart Hook (Recommended for Seamless Operation)

The best approach is a Claude Code SessionStart hook that tells every session how Python is managed on your machine. This provides zero-friction usage - skills just work without you restating the rules.

**Setup Instructions:**

1. **Locate or create your SessionStart hook:**
   - Default location: `~/.claude/detect-python-env.sh` (or similar)
   - If you don't have one, create it and register it in `~/.claude/settings.json`

2. **Report the interpreter, uv, and the active virtual environment:**

```bash
#!/bin/bash
# Detect the Python setup and communicate it to Claude Code

# Interpreter on PATH
PYTHON_PATH=$(which python || which python3)

# uv manages environments, dependencies, and tools
UV_PATH=$(which uv)

# Active virtual environment, if any
if [ -n "$VIRTUAL_ENV" ]; then
    ENV_INFO="Virtual environment: $VIRTUAL_ENV"
else
    ENV_INFO="No virtual environment active"
fi

# Add to your hook output
echo "Python Environment Detected:"
echo "- Python: $PYTHON_PATH"
echo "- uv: $UV_PATH"
echo "- $ENV_INFO"
echo ""
echo "This machine uses uv with isolated environments."
echo "Never install packages into a global interpreter."
echo "Run project code and scripts with: uv run <command>"
```

3. **Benefits:**
   - Completely automatic - skills work seamlessly
   - No manual path substitution needed
   - Same guidance in every project - no per-project detection to maintain
   - Graceful fallback if hook isn't configured

**See also:** For a complete working example, check the hook at `~/.claude/detect-python-env.sh` in my setup. It has no BroteinBuddy-specific logic: it reports the interpreter path, the uv path, and the active virtual environment, and tells sessions to use `uv run`.

#### Option 2: Any Python 3.7+ Interpreter (Fallback)

If uv is not installed, `setup-worktree.py` still runs with any Python 3.7 or newer interpreter, because it needs only the standard library:

```bash
python3 .claude/skills/git-github-workflow/scripts/setup-worktree.py
```

Do not install packages into that interpreter.

### Why uv run?

Using `uv run` makes this skill:
- **Portable**: The same command works on any machine with uv installed
- **Isolated**: Nothing is installed into a global or system interpreter
- **Privacy-preserving**: Doesn't expose local machine details in committed files

## Getting Started

See [SKILL.md](SKILL.md) for the complete workflow documentation.

## Resources

- `scripts/setup-worktree.py` - Interactive worktree creation script
- `references/code-reviewer-guide.md` - How to invoke the code-reviewer agent
- `references/teacher-mentor-guide.md` - How to invoke the teacher-mentor agent
- `references/skill-dependencies.md` - When to invoke related skills
- `references/ci-cd-monitoring.md` - Monitoring GitHub Actions checks
