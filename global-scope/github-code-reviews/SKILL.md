---
name: github-code-reviews
description: Conduct comprehensive code reviews examining 11 dimensions - functional completeness (verify requirements from linked issues), architecture, testing, security, performance, maintainability, and cross-cutting concerns. Use when reviewing PRs, reviewing code, or performing code reviews.
---

# GitHub Code Reviews

Perform thorough, structured code reviews that examine code from multiple dimensions, then track findings appropriately.

## Review Process

**1. Understand the requirements**

Before reviewing code, understand what it's supposed to do:
- Run `gh pr view <NUMBER>` to see PR description and linked issues
- Run `gh issue view <NUMBER>` for each linked issue
- Note design decisions, acceptance criteria, and requirements
- Understand the intended use cases

**2. Perform comprehensive code review**

Examine the code deeply across all dimensions (see below).
Start with functional completeness - verify the PR actually implements what it claims.

**3. After identifying actionable feedback, research existing issues**

For each problem or enhancement identified:
- Search existing issues (open and closed)
- If related issue exists, link to it prominently

**4. Structure and save the review**

- Save detailed review to `.scratch/code-review-pr-{NUMBER}-{ISO-8601-DATETIME-WITH-TZ-OFFSET}.md`
- Create `.scratch/` directory if needed (add to `.gitignore`)
- Post summary as PR comment

See `references/review-structure.md` for detailed templates and examples.

## Review Dimensions

Examine code across these 11 dimensions:

### 1. Functional Completeness
**CRITICAL: Check FIRST before diving into code quality details.**

Does the PR implement ALL requirements from the linked issue(s)? Are all acceptance criteria met? Does it follow the design decisions from the issue discussion?

See `references/review-dimensions.md` for detailed guidance on verifying completeness.

### 2. Code Quality and Development Preferences
Uses modern language features appropriately? Follows project conventions and style guides? Clear, descriptive naming? Appropriate use of comments?

### 3. Code Architecture
Follows established architectural patterns? Proper separation of concerns? Dependency injection used appropriately? Module boundaries respected?

### 4. Test Coverage
Adequate unit test coverage? Integration tests for component interactions? Edge cases tested? Error conditions tested? Tests maintainable and clear?

### 5. Documentation Quality
Public APIs documented? Complex logic explained? Docstrings/JSDoc accurate and complete? Examples provided where helpful? README updated if needed?

### 6. Edge Cases
Null/undefined handling? Empty collections handled? Boundary conditions tested? Concurrent access considered? Resource limits considered?

### 7. Error Handling
Errors caught and handled appropriately? Error messages clear and actionable? Graceful degradation where possible? Logging sufficient for debugging? Resources cleaned up on error paths?

### 8. Performance & Scalability
Algorithm complexity appropriate? Database queries efficient? Caching used where beneficial? Memory usage reasonable? Will this scale with growth?

### 9. Maintainability & Future-Proofing
Code readable and understandable? Duplication minimized? Easy to modify without breaking? Dependencies managed well? Migration path for breaking changes?

### 10. Security & Safety
Input validation and sanitization? SQL injection protection? XSS protection? Authentication/authorization correct? Secrets not hardcoded or committed? Rate limiting where needed?

### 11. Cross-Cutting Concerns
**Compare with stable code in the system:**
- Pattern consistency: Follows established patterns? If deviates, clear justification?
- Polyglot interactions: Language boundaries handled correctly? (e.g., Python ↔ JavaScript)
- Data structure consistency: Uses established data models?
- API design consistency: Error handling, parameters, return types consistent?

See `references/review-dimensions.md` for deep dive on each dimension with examples.

## Severity Classifications

Classify each finding by severity with time estimates:

- **Blocker**: Must fix before merge (missing requirements, security vulnerabilities, architectural violations, crashes)
- **Critical**: Should fix before merge (significant reliability/quality impact, missing critical error handling, performance regressions)
- **Important**: Fix soon after merge (code duplication, maintainability issues, minor architectural inconsistencies)
- **Enhancement**: Consider for future (performance optimizations, better logging, nice-to-have features)
- **Nitpick**: Very minor style issues (usually not worth mentioning)

See `references/severity-classifications.md` for detailed definitions, examples, and classification decision tree.

## Documenting Reviews

**Detailed review format:**
Save to `.scratch/code-review-pr-{NUMBER}-{ISO-8601-DATETIME-WITH-TZ-OFFSET}.md` with:
- Summary of changes
- Findings organized by severity (Blocker, Critical, Important, Enhancement)
- Each finding includes: File, Dimension, Severity, Complexity, Time Estimate, Fix Location, Related Issue
- Positive feedback section

**PR comment summary:**
Post to PR with:
- Link to detailed review in `.scratch/`
- Count of findings by severity
- Top blockers and critical items listed
- Directive to see detailed review for full analysis

See `references/review-structure.md` for complete templates and examples.

## After Review: Issue Management

**For each finding, search existing issues:**

```bash
# Search for related issues
gh issue list --search "SQL injection"
gh issue list --state all --search "parser pattern"
```

**Link to existing issues prominently in review:**
- "Related to #123 (parser refactoring)"
- "As side effect of issue #456, this doesn't handle..."
- "Known issue #789 affects this code path"

**Create new issues only for untracked findings:**

```bash
gh issue create \
  --title "SQL injection vulnerability in query builder" \
  --body "Found in PR #123 code review.

**Severity:** Blocker
**Dimension:** Security
**Complexity:** Simple
**Time Estimate:** 30 minutes

See .scratch/code-review-pr-123-2025-10-18.md for details.

**File:** src/db/queries.ts:67
**Problem:** Using string concatenation for SQL queries
**Fix:** Use parameterized queries" \
  --label "security,blocker"
```

## Quick Reference

```bash
# 1. Understand requirements first
gh pr view <NUMBER>            # Get PR description and linked issues
gh issue view <ISSUE-NUMBER>   # Read each linked issue thoroughly

# 2. Perform comprehensive review examining all 11 dimensions
#    START with functional completeness (does it actually work?)
#    See references/review-dimensions.md for detailed guidance

# 3. Create .scratch directory if needed
mkdir -p .scratch
echo ".scratch/" >> .gitignore  # If not already there

# 4. Save detailed review
# .scratch/code-review-pr-{NUMBER}-{ISO-8601-DATETIME-WITH-TZ-OFFSET}.md
# See references/review-structure.md for template

# 5. Research existing issues for each finding
gh issue list --search "relevant keywords"
gh issue list --state all --search "..."

# 6. Create new issues for untracked findings
gh issue create --title "..." --body "..." --label "..."

# 7. Post summary to PR
gh pr comment {NUMBER} --body "$(cat summary.md)"
```

## Remember

- Read the linked issue(s) FIRST - understand what the PR is supposed to do
- Start with functional completeness - does it actually implement the requirements?
- Verify ALL acceptance criteria are met
- Check that implementation matches design decisions from issue discussion
- Then examine all other dimensions deeply
- Pay special attention to cross-cutting concerns
- Classify by severity with time estimates (see references/severity-classifications.md)
- Save detailed review to `.scratch/`
- Link to existing issues prominently
- Create new issues only for untracked findings
- Post summary to PR
- No emoji (developer-facing content)
