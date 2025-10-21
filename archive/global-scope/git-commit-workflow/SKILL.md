---
name: Git Commit Workflow
description: Make incremental commits frequently - each commit should be a self-contained, working change
version: 1.0.0
---

# Git Commit Workflow

Make incremental commits as you work. Don't wait until everything is done.

## Core Principle: Every Commit Must Leave the Program in a Good State

**Required for every commit:**
- Tests pass
- No broken functionality
- Code runs without errors

A commit should represent a complete, working increment of functionality - however small.

## When to Commit

**Commit after each logical unit of work is complete and working.**

Don't batch up multiple changes before committing. Each commit should be a self-contained change that could be understood in isolation.

### Example: Display System Feature

Instead of one large commit at the end:

```
Commit 1: Add IDisplay interface
Commit 2: Add display dependencies to package.json
Commit 3: Implement TerminalDisplay class
Commit 4: Refactor command to inject display
```

Each commit is:
- A complete unit of work
- Independently understandable
- In a working state (tests pass, code runs)

## Push Early, Push Often

- Push to remote ASAP after commits
- Don't let work sit locally
- Makes work visible and creates backups
- Enables collaboration and early feedback

## Commit Messages

**Good commit messages:**
- Use clear, descriptive language
- Focus on "what" and "why" rather than just "how"
- Use imperative mood ("Add feature" not "Added feature" or "Adds feature")
- Follow project conventions if they exist

**Examples:**
- "Add IDisplay interface for terminal output abstraction"
- "Implement incremental commit workflow in git-commit skill"
- "Fix type validation in JSDoc plugin"

## Remember: Squash and Merge Cleans Up Main

Feature branches show granular work with many small commits. When you squash and merge to main, the history is clean and focused. This means:

- **On feature branches**: Commit frequently, keep commits small and focused
- **On main**: Each merge represents a complete feature or fix
- You get the best of both worlds: detailed history during development, clean history in main

## What This Is Not

This is not:
- Committing broken code ("I'll fix it in the next commit")
- Committing work-in-progress that doesn't run
- Holding off on commits until a feature is "perfect"
- Making commits so large they include multiple unrelated changes

## Quick Reference

```bash
# After completing a logical unit of work:
git add <files>
git commit -m "Clear, descriptive message"
git push

# Repeat frequently throughout the day
```
