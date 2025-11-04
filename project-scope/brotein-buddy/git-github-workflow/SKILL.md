---
name: git-github-workflow
description: This skill must be used for all git and GitHub operations in BroteinBuddy project. Defines worktree-based workflow, branch naming conventions (setup/, feature/, bug/), commit standards (many small commits), PR creation with gh CLI, testing requirements (90% coverage), and squash-merge strategy. Should be used proactively when creating worktrees, managing branches, committing code, creating pull requests, or performing any git/GitHub workflow operations.
---

# Git & GitHub Workflow for BroteinBuddy

## Overview

This skill provides the git and GitHub workflow for BroteinBuddy, which uses git worktrees to enable multiple Claude Code instances to work on different features simultaneously. Follow these conventions for branch naming, commits, pull requests, and testing.

## Bundled Resources

This skill includes bundled resources in standard subdirectories:
- `scripts/setup-worktree.py` - Interactive worktree creation script
- `references/*.md` - Detailed guides (agent invocation, CI/CD, skill dependencies)

**Accessing bundled resources:**
1. Locate this skill at `.claude/skills/git-github-workflow/` (from project root)
2. Follow any symlinks to reach the actual skill directory
3. Access resources in subdirectories: `scripts/`, `references/`

**If you have trouble locating bundled resources, invoke the `access-skill-resources` skill.**

**Requirements for setup-worktree.py script:**
- Must be run from the `bbud` conda environment
- Use the Python interpreter from your bbud environment: `<python-path>`
- Script is interactive and will prompt for branch and directory names
- See README.md in this skill directory for setup details

## When to Use

This skill should be used when:
- Creating a new worktree for parallel development
- Starting work on a new feature, bug fix, or setup task
- Committing code changes
- Creating pull requests
- Understanding testing requirements before merge
- Managing branch cleanup

## Worktree Structure

BroteinBuddy uses a hybrid worktree structure for parallel development:

```
BroteinBuddy/               ← repo root (contains .git)
├── wt/                     ← all worktrees live here
│   ├── main/              ← main branch worktree
│   ├── random-selection/  ← feature worktree (short name)
│   └── inventory-mgmt/    ← another feature worktree
└── .shared/               ← files shared across worktrees (not committed)
    ├── CLAUDE.md         ← project context
    ├── CLAUDE_CONTEXT.md ← confidential info
    ├── .planning/        ← planning documents
    ├── .scratch/         ← throwaway files
    └── .claude/          ← Claude Code settings and skills
        ├── settings.local.json
        ├── skills/       ← symlinks to individual skills
        └── agents/       ← symlinks to individual subagents
```

## Creating a New Worktree

Use the `setup-worktree.py` script to create a new worktree. The script is interactive and will guide you through the process.

**Command:**
```bash
<python-path> .claude/skills/git-github-workflow/scripts/setup-worktree.py
```

**Interactive prompts:**
1. Select a source worktree to branch from (defaults to 'main')
2. Pull latest changes from the source worktree
3. Enter the branch name with prefix (e.g., `feature/random-selection`)
4. Enter the directory name for `wt/` folder (e.g., `random-selection`)

**Examples of branch/directory pairs:**
```
Branch: setup/skills-and-subagents  → Directory: skills-and-subagents
Branch: feature/random-selection    → Directory: random-selection
Branch: bug/123-fix-inventory       → Directory: 123-fix-inventory
```

**What the script does:**
1. Finds repository root and verifies `.shared/` directory exists
2. Pulls latest changes from the selected source worktree
3. Creates new git branch from the source branch
4. Assigns unique port for dev server (main=5173, others=random 10000-60000)
5. Creates worktree at `wt/<directory-name>` tracking `<branch-name>`
6. Symlinks shared files (CLAUDE.md, CLAUDE_CONTEXT.md, .planning, .scratch)
7. Symlinks `.claude/` directory (settings.local.json, skills/, agents/)
8. Creates `.env.local` with VITE_PORT and BASE_URL for parallel development
9. Validates and updates `.gitignore` with required entries (including .env.local)
10. Runs `npm install` to install dependencies

**Result:**
- Local directory: `wt/<directory-name>` (clean, short name)
- Git branch: `<branch-name>` (full name with prefix for GitHub)
- Unique port assigned in `.env.local` (enables parallel dev servers without conflicts)
- All dependencies installed and ready to work

**Note:** The script must be run with the bbud conda environment Python interpreter. Do not use `conda activate` in bash commands - instead use the full path to the Python executable (represented as `<python-path>` in this documentation).

## Port Assignment for Parallel Development

The script automatically assigns unique ports to each worktree to enable running multiple dev servers simultaneously without port conflicts.

**Port Assignment Strategy:**
- `main` worktree: Always uses port 5173 (Vite default)
- All other worktrees: Random port in range 10000-60000
- Port availability verified via socket check before assignment
- Configuration stored in `.env.local` (not committed to git)

**How It Works:**
- `vite.config.ts` reads `VITE_PORT` from environment to set dev server port
- `playwright.config.ts` reads `BASE_URL` from environment for E2E tests
- `.env.local` provides both values automatically per worktree
- No manual configuration needed - just run `npm run dev` and `npm run test:e2e`

**Benefits:**
- Run dev servers in multiple worktrees simultaneously (e.g., main + 2 features)
- Run E2E tests in parallel across worktrees
- No port collision with other projects
- Zero cognitive load - everything just works

**To find a worktree's assigned port:**
```bash
cat .env.local  # Shows VITE_PORT and BASE_URL
```

## Branch Naming Conventions

Use these prefixes for branch names:

- `setup/` - Infrastructure and tooling setup
- `feature/` - New features or functionality
- `bug/` - Bug fixes
- `test/` - Test-related changes
- `docs/` - Documentation updates

**Format:** `<prefix>/<descriptive-name>`

**Examples:**
- `setup/ci-cd-pipeline`
- `feature/random-flavor-selection`
- `bug/inventory-count-error`

## Directory Naming for Worktrees

Keep directory names in `wt/` short and clean by stripping the prefix:

| Branch Name | Directory Name |
|-------------|----------------|
| `setup/skills-and-subagents` | `skills-and-subagents` |
| `feature/random-selection` | `random-selection` |
| `bug/123-fix-inventory` | `123-fix-inventory` |

## Commit Workflow

### Commit Message Standards

**CRITICAL**: Follow development-standards skill for all commit messages:
- **No emoji** in commit messages (colorful emoji like ✅ ❌ 🎉 🚀 are forbidden)
- Use clear, descriptive language
- Focus on the "why" rather than just the "what"

### Commit Frequency

Make **many small, incremental commits** as work progresses. Each commit should represent a logical unit of work.

**Do:**
- Commit after completing a logical unit
- Commit working code frequently
- Use descriptive commit messages

**Don't:**
- Make large commits covering multiple unrelated changes
- Wait until the end to make commits after-the-fact

### Testing Requirements

**Before creating a PR:**
- All tests must pass (`npm test`)
- Coverage requirements met: 90% overall, 100% for critical paths
- Linting passes (`npm run lint`)

## Pull Request Workflow

### Complete Workflow Timeline

This section defines all steps from initial PR creation through merge, including when to invoke agents.

#### 1. Complete Planned Implementation
- All features/fixes from `.planning/PLAN.md` implemented
- Many small commits made throughout (not after-the-fact)
- All commits pushed to feature branch

#### 2. Ensure All CI/CD Checks Pass
- Monitor: `gh pr checks <pr-number>`
- Verify all tests pass, linting passes, build succeeds
- Use bbud conda environment for local verification: `<python-path> -m pytest`
- See references/ci-cd-monitoring.md for detailed monitoring procedures

#### 3. Invoke code-reviewer Agent
- Timing: After tests pass, before considering merge
- See references/code-reviewer-guide.md for complete invocation instructions
- Provide: PR description, relevant `.planning/PLAN.md` section, commit history, bbud conda env context

#### 4. Address Code Review Blockers
- Fix all issues identified by code-reviewer agent
- Make commits for each fix (many small commits)
- Push all fixes to feature branch
- Monitor CI/CD checks again - ensure they still pass

#### 5. User Review and Enhancement Opportunity
- Review the code review file saved in `.scratch/`
- Decide if any additional enhancements or issues should be addressed
- Add scope if warranted

#### 6. Subsequent Code Reviews (If Needed)
- For non-trivial changes since last review: Re-invoke code-reviewer agent
- See references/code-reviewer-guide.md for subsequent review instructions
- Repeat steps 4-6 until both agent and user are satisfied

#### 7. Invoke teacher-mentor Agent (FINAL STEP BEFORE MERGE)
- Timing: ONLY after user explicitly confirms ready to merge
- See references/teacher-mentor-guide.md for complete invocation instructions
- Agent creates educational documentation about what was delivered
- Commit documentation changes (markdown files only)
- Push documentation commits
- Verify CI/CD checks pass (should - we only added markdown)

#### 8. Merge and Cleanup
- Squash merge to main: `gh pr merge <pr-number> --squash`
- Pull latest main: `cd wt/main && git pull`
- Remove worktree: `git worktree remove ../feature-name`
- Delete branch: `git branch -d feature/feature-name`

**Key Timing Principle:** teacher-mentor agent is invoked LAST (after all code reviews complete and user confirms ready to merge) to ensure it documents the final delivered state, not intermediate states or development missteps.

### PR Content Standards

**CRITICAL**: Follow development-standards skill for all PR content:
- **No emoji** in title or description (colorful emoji like ✅ ❌ 🎉 🚀 are forbidden)
- Use GitHub's task lists (`- [ ]` and `- [x]`) instead of emoji checkboxes
- Use GitHub alerts (`> [!NOTE]`, `> [!WARNING]`) for emphasis
- Use collapsible sections, tables, and code blocks for rich formatting

### Creating Pull Requests

Use `gh` CLI to create pull requests:

```bash
gh pr create --title "<descriptive-title>" --body "$(cat <<'EOF'
## Summary
<1-3 bullet points>

## Test Plan
- [ ] Unit tests pass
- [ ] Coverage requirements met (90% overall, 100% critical paths)

Generated with Claude Code
EOF
)"
```

### Merge Strategy

**All merges to main use squash merge:**
```bash
gh pr merge <pr-number> --squash
```

## Post-Merge Cleanup

```bash
cd wt/main
git pull
git worktree remove ../feature-name
git branch -d feature/feature-name
```

## CI/CD Monitoring

Monitor GitHub Actions checks throughout the PR workflow to ensure code quality and catch issues early.

**Check status:**
```bash
gh pr checks <pr-number>      # Summary of all checks
gh run list --limit 5         # Recent workflow runs
gh run view <run-id>          # Detailed run information
```

**When to check:**
- After creating PR
- After pushing new commits
- After addressing code review feedback
- Before invoking teacher-mentor agent
- Before merging

**Common checks:**
- Tests (must run in bbud conda environment: `<python-path> -m pytest`)
- Linting (`npm run lint`)
- Type checking (`npx tsc`)
- Build (`npm run build`)

**For detailed procedures, troubleshooting common failures, and interpreting results, see references/ci-cd-monitoring.md.**

## Skill Dependencies

This workflow depends on several other skills that must be explicitly invoked at appropriate points.

**Project skills:**
- `git-github-workflow` (this skill) - All git/GitHub operations
- `brotein-buddy-standards` - Project-specific standards

**User skills:**
- `development-standards` - Commit messages, PR format, no emoji policy
- `dependency-management` - Adding/managing dependencies
- `exhaustive-testing` - Test coverage requirements (90% overall, 100% critical)
- `handle-deprecation-warnings` - Addressing deprecation notices

**Important:** These skills often don't auto-trigger reliably. Best practice is to explicitly invoke them at workflow decision points.

**For complete details on when and how to invoke each skill, see references/skill-dependencies.md.**

## Quick Reference

**Create worktree:** `<python-path> .claude/skills/git-github-workflow/scripts/setup-worktree.py` (interactive)
**Commit:** Make many small commits, test before pushing
**PR:** Use `gh pr create`, ensure tests pass
**Merge:** Squash merge only
**Cleanup:** Remove worktree and branch after merge
**CI/CD:** Monitor with `gh pr checks <pr-number>` (see references/ci-cd-monitoring.md)
**Skills:** Explicitly invoke related skills (see references/skill-dependencies.md)
