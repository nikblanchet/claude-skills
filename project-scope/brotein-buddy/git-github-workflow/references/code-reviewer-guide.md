# Code Reviewer Agent - Invocation Guide

## When to Invoke

Invoke the code-reviewer agent at these points in the PR workflow:

1. **Initial review:** After all tests pass and CI/CD checks succeed, before considering merge
2. **Subsequent reviews:** After addressing non-trivial changes from previous code review feedback
3. **Final verification:** Before invoking teacher-mentor agent (optional, if significant changes were made)

## Required Context to Provide

When invoking the code-reviewer agent, provide comprehensive context:

### 1. Pull Request Information

Fetch and provide the PR description and any comments:

```bash
gh pr view <pr-number>
```

Tell the agent to read the full PR description and comments thread.

### 2. Planning Context

Direct the agent to read the relevant section from `.planning/PLAN.md` that describes:
- What this PR is intended to deliver
- The step or phase being implemented
- Any specific requirements or constraints

### 3. Commit History

Provide the full commit history for this branch:

```bash
git log main..HEAD
```

For subsequent reviews, emphasize that the agent should review the complete commit history to understand:
- What was changed since the last review
- How scope may have expanded
- What enhancements were added

### 4. Environment Context

Inform the agent about the bbud conda environment:
- Tests must be run using `<python-path> -m pytest`
- Any Python scripts use the bbud environment
- This ensures tests run correctly during the review process

### 5. Project Standards

Remind the agent to apply:
- `brotein-buddy-standards` skill for project-specific requirements
- `development-standards` skill for commit messages, code quality
- `exhaustive-testing` skill for test coverage expectations

## First Review vs Subsequent Reviews

### First Review (Initial Code Review)

For the first code review on a PR:

**Scope:** Comprehensive review of all changes in the PR
**Focus:**
- Code quality across all 11 dimensions
- Test coverage (90% overall, 100% critical paths)
- Adherence to project standards
- Security concerns
- Performance considerations
- Documentation completeness

**Instructions to agent:**
- Read PR description and comments
- Read relevant PLAN.md section
- Review complete commit history
- Run tests to verify they pass
- Identify blockers, suggestions, and enhancements

### Subsequent Reviews (2nd, 3rd, etc.)

When running a subsequent code review after addressing previous feedback:

**Critical: Review the ENTIRE PR, not just changes since last review**

**Scope:** Full PR review with awareness of iteration history
**Focus:**
- How previous feedback was addressed
- Whether new changes introduced issues
- Whether scope expanded appropriately
- Overall quality of the complete PR (not just deltas)

**Instructions to agent:**
- This is a subsequent code review (mention which iteration: 2nd, 3rd, etc.)
- Read PR description and ALL comments (including previous code review discussions)
- Read relevant PLAN.md section
- Review COMPLETE commit history from main..HEAD (not just recent commits)
- Understand what changed since the last review and why
- Account for scope changes or enhancements added during development
- Review the ENTIRE PR holistically, not just the diff since last review
- Run tests to verify they still pass
- Assess whether previous blockers were resolved
- Identify any new issues introduced by changes
- Evaluate whether the overall PR is now ready for merge

## Example Invocation

### First Review Example

```
I need you to invoke the code-reviewer agent to perform a comprehensive code review of PR #42.

Context to provide:
1. Read the PR description and comments: gh pr view 42
2. Read the relevant section from .planning/PLAN.md (Section 2.4: Implement random selection)
3. Review commit history: git log main..HEAD (show complete history)
4. Environment: Use bbud conda environment (<python-path>) for running tests
5. Apply brotein-buddy-standards, development-standards, and exhaustive-testing skills

Focus on all 11 code review dimensions. Identify blockers, suggestions, and potential enhancements.
```

### Subsequent Review Example

```
I need you to invoke the code-reviewer agent for a SECOND code review of PR #42.

Context to provide:
1. This is the 2nd code review iteration
2. Read the PR description and ALL comments: gh pr view 42
3. Read the relevant section from .planning/PLAN.md (Section 2.4: Implement random selection)
4. Review COMPLETE commit history: git log main..HEAD (entire branch, not just recent commits)
5. Environment: Use bbud conda environment (<python-path>) for running tests
6. Apply brotein-buddy-standards, development-standards, and exhaustive-testing skills

Important instructions for the agent:
- Review the ENTIRE PR holistically, not just changes since the first review
- Assess how feedback from the first review was addressed
- Account for any scope expansions or enhancements added
- Identify whether previous blockers are resolved
- Check for any new issues introduced by recent changes
- Determine if the PR is now ready for merge or needs further iteration
```

## Agent Output Location

The code-reviewer agent saves its review to:

```
.scratch/code-review-pr-{pr-number}-{timestamp}.md
```

Example: `.scratch/code-review-pr-42-2025-10-28T10:30:00-0700.md`

After the agent completes:
1. Review the code review file
2. Determine if there are blockers to address
3. If blockers exist: Address them, commit fixes, push, verify CI/CD passes
4. If non-trivial changes were made: Run subsequent code review
5. If satisfied: Proceed to user review and eventual teacher-mentor invocation

## Decision Points

After each code review:

**Blockers found:**
- Address all blockers
- Make commits for fixes
- Push to feature branch
- Monitor CI/CD checks
- If changes were non-trivial, run subsequent code review

**No blockers, only suggestions:**
- Decide whether to implement suggestions
- If implementing: Make changes, commit, push
- If changes were non-trivial, consider subsequent code review
- Otherwise: Proceed to teacher-mentor agent invocation

**Clean review:**
- Proceed to teacher-mentor agent invocation (after user confirms ready to merge)

## Best Practices

1. **Always provide complete context:** Don't skip PR description, commit history, or PLAN.md
2. **Environment matters:** Always mention bbud conda environment
3. **Subsequent reviews are full reviews:** Emphasize reviewing the entire PR, not just deltas
4. **Read all comments:** On subsequent reviews, ensure agent reads all PR comment threads
5. **Run tests:** Code reviewer should verify tests pass in the correct environment
6. **Save reviews:** All reviews saved to .scratch/ for reference by teacher-mentor agent
