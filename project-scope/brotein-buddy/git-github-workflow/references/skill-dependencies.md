# Skill Dependencies for BroteinBuddy Workflow

## Overview

The BroteinBuddy project relies on several skills (both project-specific and user-global) for maintaining code quality, standards, and workflow consistency.

**Important:** These skills often don't auto-trigger reliably based on context. Best practice is to explicitly invoke relevant skills at appropriate workflow decision points.

## Project Skills

Project skills are specific to BroteinBuddy and located at `.claude/skills/` (relative to project root).

### git-github-workflow

**Type:** Project skill
**Location:** `.claude/skills/git-github-workflow/`

**Purpose:** Defines the complete git and GitHub workflow including worktree management, branch naming, commit standards, PR workflow, and merge strategy.

**When to invoke:**
- Creating a new worktree
- Starting work on a new feature, bug, or setup task
- Before committing code
- Creating pull requests
- Managing branch cleanup
- Any git or GitHub operation

**Trigger keywords:** git, worktree, branch, commit, PR, pull request, merge, GitHub

**Invocation:**
```
Invoke the git-github-workflow skill
```

### brotein-buddy-standards

**Type:** Project skill
**Location:** `.claude/skills/brotein-buddy-standards/`

**Purpose:** BroteinBuddy-specific development standards including testing requirements (90% coverage, 100% critical paths), code quality tooling (ESLint, Prettier, Husky), documentation structure (README, DEVELOPING, ADRs), and tech stack conventions.

**When to invoke:**
- Before creating commits or PRs
- When writing tests (to verify coverage requirements)
- When setting up CI/CD checks
- When documenting features or decisions
- Any time project-specific standards need to be applied

**Trigger keywords:** testing, coverage, standards, documentation, ADR, code quality

**Invocation:**
```
Invoke the brotein-buddy-standards skill
```

## User Skills

User skills are globally available across all projects and located at `~/.claude/skills/`.

### development-standards

**Type:** User skill
**Location:** `~/.claude/skills/development-standards/`

**Purpose:** Standards enforced when writing code, creating pull requests, committing changes, or documenting features. Critical standard: No emoji in developer-facing content (code/docs/PRs/issues/commits) or CLI output. Also defines standards for using cutting-edge language features and writing comprehensive documentation.

**When to invoke:**
- Before writing commit messages
- Before creating PRs (titles and descriptions)
- When creating documentation
- When writing code comments
- Before any developer-facing communication

**Trigger keywords:** commit message, PR description, emoji, documentation, code comments, standards

**Invocation:**
```
Invoke the development-standards skill
```

**Key reminders:**
- No emoji in commit messages (❌ ✅ 🎉 🚀 etc.)
- No emoji in PR titles or descriptions
- Use GitHub task lists (`- [ ]`, `- [x]`) instead of emoji checkboxes
- Use GitHub alerts (`> [!NOTE]`, `> [!WARNING]`) for emphasis

### dependency-management

**Type:** User skill
**Location:** `~/.claude/skills/dependency-management/`

**Purpose:** Use quality dependencies freely - default to using existing libraries over reinventing. For Python prefer conda over pip, maintain separate requirements-conda.txt and requirements-pip.txt.

**When to invoke:**
- Adding new dependencies
- Installing packages
- Evaluating whether to use a library vs custom implementation
- Setting up project dependencies
- Managing Python/Node.js package versions

**Trigger keywords:** npm install, dependency, package, library, requirements, conda, pip

**Invocation:**
```
Invoke the dependency-management skill
```

**Key reminders for BroteinBuddy:**
- Use bbud conda environment: `/Users/nik/miniconda3/envs/bbud/bin/python`
- For Node.js: `npm install` (standard process)
- Prefer established libraries over reinventing solutions

### exhaustive-testing

**Type:** User skill
**Location:** `~/.claude/skills/exhaustive-testing/`

**Purpose:** Write comprehensive test coverage across unit, integration, regression, end-to-end, and manual tests. Watch for deprecation warnings in test output and address them immediately.

**When to invoke:**
- Writing tests for new features
- Before creating PRs (verify coverage requirements)
- When test failures occur
- Setting up test infrastructure
- Evaluating test completeness

**Trigger keywords:** test, testing, coverage, unit test, integration test, e2e, test suite

**Invocation:**
```
Invoke the exhaustive-testing skill
```

**Key reminders for BroteinBuddy:**
- 90% coverage overall required
- 100% coverage for critical paths required
- Run tests in bbud conda environment
- Address deprecation warnings immediately

### handle-deprecation-warnings

**Type:** User skill
**Location:** `~/.claude/skills/handle-deprecation-warnings/`

**Purpose:** Notice and address deprecation warnings immediately in test output, CI/CD logs, and development - read the warning, check migration guides, update code to use recommended APIs, don't suppress warnings.

**When to invoke:**
- When seeing deprecation warnings in test output
- When DeprecationWarning messages appear
- During code review if warnings are present
- When updating dependencies
- Any time deprecated API notices appear

**Trigger keywords:** deprecation, DeprecationWarning, deprecated, warning, API deprecation

**Invocation:**
```
Invoke the handle-deprecation-warnings skill
```

**Key principle:** Address deprecation warnings immediately; don't suppress or ignore them.

## Skill Invocation Best Practices

### Explicit Invocation Pattern

Since skills don't reliably auto-trigger, use explicit invocation at workflow decision points:

**Before committing:**
```
Before I commit this code, let me invoke the development-standards skill to ensure commit message format is correct.
```

**When adding a dependency:**
```
I need to add a new library. Let me invoke the dependency-management skill to ensure I'm following best practices.
```

**Before creating a PR:**
```
Before creating this PR, let me invoke:
1. development-standards skill (for PR format and no-emoji policy)
2. brotein-buddy-standards skill (for project-specific requirements)
3. exhaustive-testing skill (to verify test coverage is adequate)
```

**When writing tests:**
```
I'm about to write tests for this feature. Let me invoke the exhaustive-testing skill to ensure I cover all test types appropriately.
```

### Common Workflow Checkpoints

**Starting new work:**
1. Invoke `git-github-workflow` skill (create worktree)
2. Invoke `brotein-buddy-standards` skill (understand requirements)

**During development:**
1. Invoke `dependency-management` skill (when adding dependencies)
2. Invoke `exhaustive-testing` skill (when writing tests)
3. Invoke `handle-deprecation-warnings` skill (when warnings appear)

**Before committing:**
1. Invoke `development-standards` skill (commit message format)
2. Invoke `exhaustive-testing` skill (verify tests pass, coverage adequate)

**Creating PR:**
1. Invoke `development-standards` skill (PR format, no emoji)
2. Invoke `brotein-buddy-standards` skill (project standards)
3. Invoke `git-github-workflow` skill (PR workflow, merge strategy)

**During code review:**
1. Invoke relevant skills based on review feedback
2. Invoke `handle-deprecation-warnings` skill (if warnings in CI/CD)

## Why Skills Don't Auto-Trigger Reliably

Skills are designed to activate based on context keywords in the conversation. However, in practice:

- Context may be ambiguous
- Keywords may not be present in user's message
- Multiple skills may be relevant but not all trigger
- Workflow-critical skills may be missed

**Solution:** Explicitly invoke skills at known decision points rather than relying on auto-triggering.

## Quick Reference Table

| Skill Name | Type | Primary Use Case | Key Trigger |
|------------|------|------------------|-------------|
| git-github-workflow | Project | Git operations, PRs, worktrees | git, branch, commit, PR |
| brotein-buddy-standards | Project | Project-specific standards | testing, coverage, documentation |
| development-standards | User | Commit messages, PRs, no emoji | commit, PR, documentation |
| dependency-management | User | Adding dependencies | npm install, dependency, package |
| exhaustive-testing | User | Writing and verifying tests | test, coverage, test suite |
| handle-deprecation-warnings | User | Addressing deprecation notices | deprecation, warning, deprecated |

## Example: Complete Feature Development Workflow

Here's how skills integrate throughout a complete feature development:

1. **Start work:**
   ```
   Invoke git-github-workflow skill to create new worktree
   Invoke brotein-buddy-standards skill to review project requirements
   ```

2. **Add dependency (if needed):**
   ```
   Invoke dependency-management skill to determine if library is appropriate
   ```

3. **Write code and tests:**
   ```
   Invoke exhaustive-testing skill to ensure comprehensive test coverage
   ```

4. **Handle deprecation warnings:**
   ```
   Invoke handle-deprecation-warnings skill to address any deprecation notices
   ```

5. **Commit changes:**
   ```
   Invoke development-standards skill to format commit message correctly
   ```

6. **Create PR:**
   ```
   Invoke development-standards skill for PR format (no emoji, proper structure)
   Invoke git-github-workflow skill for PR workflow steps
   ```

7. **Monitor CI/CD:**
   ```
   Follow git-github-workflow skill's CI/CD monitoring procedures
   ```

8. **Code review and merge:**
   ```
   Follow git-github-workflow skill's code review and merge workflow
   ```

By explicitly invoking skills at these checkpoints, you ensure consistent application of standards and best practices throughout the development lifecycle.
