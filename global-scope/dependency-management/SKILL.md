---
name: dependency-management
description: Use quality dependencies freely - default to using existing libraries over reinventing. For Python prefer conda over pip, maintain separate requirements-conda.txt and requirements-pip.txt. Use when adding dependencies, installing packages, or evaluating whether to use a library.
---

# Dependency Management

Reinventing the wheel is dumb. If a respected, reliable library exists and is easily, freely available, use it.

## Core Philosophy

**Coding is building with Legos, not creating from scratch.**

- We don't write in Assembly, so take advantage of the free skilled labor others have contributed
- Dependencies don't bother me - add them freely to requirements files or package.json
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

## Python Package Management: Conda + Pip

**Prefer conda over pip when available.**

Conda handles system-level dependencies better, but not all packages are available in conda.

**Best practice: Separate requirements files**

Maintain two requirements files:
- `requirements-conda.txt` - Packages available in conda
- `requirements-pip.txt` - Packages only available via pip

This ensures you use conda when possible and only fall back to pip when necessary.

**Installation workflow:**

```bash
# Activate the project's conda environment
conda activate {env-name}

# Install conda packages first
conda install --file requirements-conda.txt

# Then install pip packages within the conda environment
pip install -r requirements-pip.txt
```

**Critical: Always install pip packages within the conda environment**
- Don't switch to pip globally
- The `conda activate {env}` ensures pip installs into the conda environment
- Note the `-r` flag for pip (required for reading from file)

**Adding new dependencies:**

```bash
# Check if available in conda first
conda search package-name

# If available in conda:
conda install package-name
echo "package-name>=1.2.0" >> requirements-conda.txt

# If only available via pip:
conda activate {env-name}
pip install package-name
echo "package-name>=1.2.0" >> requirements-pip.txt
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

If a dependency choice isn't obvious, add a comment in the requirements file or nearby documentation:

```
# requirements-conda.txt

# Using radon for cyclomatic complexity (industry standard)
radon>=6.0.1

# anthropic SDK for Claude API access (official client)
anthropic>=0.18.0
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
# Python with conda environment
conda activate project-env
conda install --file requirements-conda.txt
pip install -r requirements-pip.txt

# Add new Python dependency
conda search package-name  # Check conda first
conda install package-name && echo "package-name>=1.2.0" >> requirements-conda.txt
# OR
pip install package-name && echo "package-name>=1.2.0" >> requirements-pip.txt

# Node.js
npm install package-name
npm install --save-dev dev-package
```

## Remember

- Default to using dependencies
- Don't reimplement what exists
- Evaluate quality with common sense
- For Python: Use conda when available, pip when necessary
- Maintain separate requirements-conda.txt and requirements-pip.txt
- Always install pip packages within conda environment
- Stay reasonably current with updates
- When updating dependencies, migrate deprecated APIs (see handle-deprecation-warnings skill)
- Add dependencies freely
