---
name: dependency-management
description: Use quality dependencies freely - default to using existing libraries over reinventing. For Python use uv with isolated per-project environments and never install packages into a global or system interpreter. Use when adding dependencies, installing packages, or evaluating whether to use a library.
---

# Dependency Management

Reinventing the wheel is dumb. If a respected, reliable library exists and is easily, freely available, use it.

## Core Philosophy

**Coding is building with Legos, not creating from scratch.**

- We don't write in Assembly, so take advantage of the free skilled labor others have contributed
- Dependencies don't bother me - add them freely to pyproject.toml or package.json
- A 50-line utility from a well-maintained library is better than writing those 50 lines yourself

## When to Use a Dependency

**Default answer: Yes, if it solves the problem well.**

- Don't reimplement common functionality that's available in quality libraries
- Use existing solutions for standard problems (parsing, validation, formatting, etc.)
- Leverage community-maintained code rather than maintaining your own version

## When to Second-Guess a Dependency

Only hesitate when there are concrete technical concerns:

**Compromises in functionality:**
- The library doesn't quite do what we need
- We'd have to work around limitations
- Better to implement exactly what we want

**Version incompatibility:**
- Conflicts with our Python version or other dependencies
- Creates dependency resolution issues
- Requires downgrades of other packages

**Architectural conflicts:**
- The library's approach conflicts with our architecture
- Doesn't fit with our patterns (sync vs async, class-based vs functional)
- Would force awkward integration

**Otherwise, err on the side of using existing solutions.**

## Evaluating Library Quality

Use common sense and consider:

**Maintenance history:**
- Active maintenance is better than abandoned repos
- Recent commits and releases show ongoing support
- Responsive to issues and PRs

**Documentation quality:**
- Well-documented libraries save time
- Clear examples and API references
- Good error messages

**API design:**
- Does it fit naturally with our code?
- Intuitive to use?
- Composable with other libraries?

**Maturity vs. fit:**
- A 6-month-old tool may be appropriate if it does exactly what we need and nothing else would
- Sometimes the newer tool is the right choice
- Don't be overly conservative about library age

**Community:**
- GitHub stars (indicator, not requirement)
- Issues activity and responsiveness to bugs
- Active community discussions

**Testing:**
- Does the library have its own test suite?
- Are tests comprehensive?
- CI/CD in place?

## Python Package Management: uv

**Every project gets its own environment, managed by uv.**

**Critical: Never install packages into a global or system interpreter**
- No bare `pip install` or `pip3 install`, no `sudo pip`, no `--system`, no `--break-system-packages`
- Project packages belong in the project's `.venv`; standalone tools get their own isolated environment via `uv tool`

**Best practice: pyproject.toml + uv.lock**

- `pyproject.toml` - Declares the project's dependencies
- `uv.lock` - Locks the exact resolved versions; commit it

**Project workflow:**

```bash
# Start a new project (creates pyproject.toml)
uv init

# Add a dependency (updates pyproject.toml, uv.lock, and .venv)
uv add package-name

# Add a development-only dependency
uv add --dev package-name

# Bring .venv in line with uv.lock (after cloning or pulling)
uv sync

# Run a command in the project's environment - no activation needed
uv run pytest
```

**Existing projects that only have requirements.txt:**

```bash
uv venv                               # Create .venv in the project
uv pip install -r requirements.txt    # Installs into the project's .venv only
```

**Scripts, tools, and interpreters:**

```bash
# One-off script that needs a library (temporary environment)
uv run --with package-name script.py

# Command-line tools: install in isolation, or run without installing
uv tool install tool-name
uvx tool-name

# Install an interpreter, then pin the project to it (.python-version)
uv python install {version}
uv python pin {version}
```

## Node.js Package Management

```bash
# Add and install
npm install package-name

# Add as dev dependency
npm install --save-dev package-name
```

Package manager (npm, yarn, pnpm) automatically updates package.json and lockfile.

## Dependency Updates

**Stay reasonably current with dependency versions:**

- Address security advisories promptly
- Update periodically to avoid falling too far behind
- When updating dependencies, migrate away from deprecated APIs at the same time
- Test after updates to catch breaking changes

**Balance:**
- Don't chase every minor version immediately
- Do update when there are security fixes or important features
- Do keep dependencies reasonably current (not years behind)

**See also:** `handle-deprecation-warnings` skill for guidance on migrating deprecated APIs proactively.

## Documentation

**Document non-obvious dependency choices:**

If a dependency choice isn't obvious, add a comment in `pyproject.toml` or nearby documentation:

```toml
# pyproject.toml

[project]
dependencies = [
    # Using radon for cyclomatic complexity (industry standard)
    "radon>=6.0.1",

    # anthropic SDK for Claude API access (official client)
    "anthropic>=0.18.0",
]
```

This helps future maintainers understand why dependencies exist.

## Examples of Good Dependency Usage

**Good reasons to add a dependency:**
- "Using `click` for CLI argument parsing instead of writing our own parser"
- "Adding `pytest` for testing - industry standard with excellent features"
- "Using `chalk` for terminal colors - handles edge cases and platform differences"
- "Adding `anthropic` SDK for API access - official, well-maintained"

**Good reasons NOT to add a dependency:**
- "This library is 500KB just to capitalize strings - we can write that in 2 lines"
- "This requires Python 3.8 but we need 3.13 features"
- "This is callback-based but our codebase is async/await throughout"

## Quick Reference

```bash
# Python with uv (isolated per-project environment)
uv sync
uv run pytest

# Add new Python dependency
uv add package-name
uv add --dev dev-package

# One-off script or command-line tool
uv run --with package-name script.py
uvx tool-name

# Node.js
npm install package-name
npm install --save-dev dev-package
```

## Remember

- Default to using dependencies
- Don't reimplement what exists
- Evaluate quality with common sense
- For Python: Use uv, with an isolated environment per project
- Declare dependencies in pyproject.toml and commit uv.lock
- Never install packages into a global or system interpreter
- Stay reasonably current with updates
- When updating dependencies, migrate deprecated APIs (see handle-deprecation-warnings skill)
- Add dependencies freely
