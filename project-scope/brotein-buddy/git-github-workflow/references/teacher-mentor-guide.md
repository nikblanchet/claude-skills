# Teacher-Mentor Agent - Invocation Guide

## When to Invoke

**Critical Timing:** The teacher-mentor agent is invoked as the FINAL STEP before merging the PR.

Invoke only after:
1. All planned implementation is complete
2. All CI/CD checks pass
3. Code-reviewer agent has completed its review
4. All blockers from code review have been addressed
5. Subsequent code reviews completed if non-trivial changes were made
6. User has reviewed the code review and confirmed ready to merge

**Do NOT invoke until user explicitly confirms ready to merge.**

## Why This Timing Matters

The teacher-mentor agent creates educational documentation explaining what was delivered in its final state. Invoking too early means:
- Documentation may describe incomplete features
- Documentation may miss enhancements added during code review
- Documentation may reference code that gets changed later

Invoking at the end ensures:
- Documentation describes the final delivered state
- All enhancements and scope expansions are included
- Code review improvements are incorporated
- Teaching docs reflect what actually got merged

## Required Context to Provide

When invoking the teacher-mentor agent, provide comprehensive context:

### 1. Pull Request Information

Provide the PR description and comments:

```bash
gh pr view <pr-number>
```

Tell the agent to read:
- PR title and description
- Summary of what was delivered
- Any discussions or clarifications in PR comments

### 2. Planning Context

Direct the agent to read the relevant section from `.planning/PLAN.md`:
- The specific step or phase being implemented
- Original requirements and goals
- Any constraints or considerations mentioned

### 3. Commit Messages

Provide the complete commit history:

```bash
git log main..HEAD
```

Commit messages help the agent understand:
- What work was done (in final form)
- How features were built up incrementally
- What the implementation approach was

### 4. Code Review Files

Direct the agent to read all code review files from `.scratch/`:

```bash
ls .scratch/code-review-pr-{pr-number}-*.md
```

Example: `.scratch/code-review-pr-42-2025-10-28T10:30:00-0700.md`

Code reviews provide:
- What issues were found and fixed
- What enhancements were suggested and implemented
- How scope expanded during development
- Final quality assessment

### 5. Environment Context

Inform the agent about the bbud conda environment:
- If the agent needs to run any scripts, use `<python-path>`
- Tests can be run via `<python-path> -m pytest`
- This ensures any verification happens in the correct environment

## What the Agent Should Focus On

### DO Focus On (Final Delivered State)

**What was delivered:**
- Features and functionality in their final form
- How components fit together
- Design decisions and trade-offs
- Why certain approaches were chosen
- How the code works (final implementation)

**Enhancements and scope expansions:**
- Features added beyond original scope
- Improvements made during development
- Quality enhancements from code review
- Additional considerations addressed

**Teaching value:**
- How the solution works conceptually
- Why design patterns were chosen
- What trade-offs were made
- How this fits into the larger project
- Key learnings for future reference

### DO NOT Focus On (Development Process/Story)

**Avoid:**
- The chronological story of development
- Missteps or bugs encountered during development
- Failed approaches that were later changed
- Intermediate states that no longer exist
- Trial-and-error narratives

**Why avoid these:**
- Teaching docs should explain the final solution, not the journey
- Focus on "what is" not "what was tried"
- Readers want to understand the delivered code, not the development history
- Code review and commit messages already document the process

## Agent Output

The teacher-mentor agent creates teaching documentation (markdown files) that:
- Explain what was delivered
- Provide context and rationale
- Help future developers understand the code
- Serve as reference material

These files are typically created in:
- `docs/` directory (for ADRs, architectural decisions)
- `DEVELOPING.md` updates (for development workflow changes)
- Component-specific documentation (for complex features)

## After Agent Completes

After the teacher-mentor agent finishes:

1. **Review the documentation:**
   - Check that it accurately describes the final state
   - Verify it's helpful for learning and reference
   - Ensure it doesn't include development story/missteps

2. **Commit documentation changes:**
   ```bash
   git add docs/ DEVELOPING.md (or whatever files were created/updated)
   git commit -m "Add teaching documentation for [feature/fix]

   Generated with Claude Code

   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

3. **Push documentation:**
   ```bash
   git push
   ```

4. **Monitor CI/CD checks:**
   ```bash
   gh pr checks <pr-number>
   ```
   - These should pass (we only added markdown documentation)
   - If checks fail, investigate and fix before merging

5. **Proceed to merge:**
   - Once CI/CD passes, merge the PR
   - Follow post-merge cleanup procedures

## Example Invocation

```
I need you to invoke the teacher-mentor agent to create teaching documentation for PR #42.

IMPORTANT: This is the final step before merging. All code reviews are complete and I've confirmed ready to merge.

Context to provide:
1. Read the PR description and comments: gh pr view 42
2. Read the relevant section from .planning/PLAN.md (Section 2.4: Implement random selection)
3. Review commit messages: git log main..HEAD (complete history)
4. Read all code review files from .scratch/code-review-pr-42-*.md
5. Environment: Use bbud conda environment (<python-path>) if needed

Instructions for the agent:
- Focus on the FINAL DELIVERED STATE, not the development story
- Explain what was delivered (features, enhancements, scope expansions)
- Provide teaching value: why decisions were made, how things fit together
- DO NOT focus on missteps, bugs encountered during development, or intermediate states
- Create documentation that helps future developers understand the code
- Write in a patient, educational style
```

## Decision Points

After teacher-mentor agent completes:

**Documentation looks good:**
- Commit documentation changes
- Push to feature branch
- Monitor CI/CD checks
- If CI/CD passes, proceed to merge

**Documentation needs adjustments:**
- Edit documentation files directly
- Commit adjustments
- Push to feature branch
- Monitor CI/CD checks
- If CI/CD passes, proceed to merge

**CI/CD fails after pushing docs:**
- Investigate failure (should be unlikely for markdown-only changes)
- Fix issue if identified
- Re-run checks
- Once passing, proceed to merge

## Best Practices

1. **Only invoke after user confirms ready to merge:** Don't jump ahead
2. **Provide all context:** PR, PLAN.md, commits, code reviews
3. **Emphasize final state:** Remind agent to focus on delivered solution, not process
4. **Review before committing:** Ensure docs are accurate and helpful
5. **Verify CI/CD:** Even markdown changes should pass checks before merge
6. **One agent, one PR:** Don't re-run teacher-mentor unless absolutely necessary

## Why This Is The Last Step

Teaching documentation should reflect:
- The complete, final implementation
- All enhancements and scope changes
- Code that passed all quality checks
- What actually gets merged to main

Running it last ensures the documentation is accurate, complete, and valuable for future reference.
