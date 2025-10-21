# Code Review Structure and Documentation

This document provides detailed templates and examples for documenting code reviews.

## Review Documentation Format

### Detailed Review: `.scratch/code-review-pr-{NUMBER}-{ISO-8601-DATETIME-WITH-TZ-OFFSET}.md`

```markdown
# Code Review: PR #{NUMBER} - {TITLE}

**Reviewer:** Claude Code
**Date:** {DATE}
**PR:** {URL}

## Summary

Brief overview of changes and overall assessment.

## Blockers (Must fix before merge)

### 1. Missing Required Feature from Issue Requirements
- **File:** Multiple files
- **Dimension:** Functional Completeness
- **Severity:** Blocker
- **Complexity:** Moderate
- **Time Estimate:** 4 hours
- **Fix Location:** This branch, before merge
- **Related Issue:** #121 (original feature request)

**Description:**
Issue #121 requires three features:
1. Basic validation (IMPLEMENTED)
2. Async validation support (MISSING)
3. Custom error messages (MISSING)

Only 1 of 3 requirements is implemented. The acceptance criteria in #121 specifically states:
"Must support async validators for API calls" - this is not present in the implementation.

**Recommendation:**
Implement async validation and custom error messages as specified in #121 before merging.

### 2. SQL Injection Vulnerability
- **File:** `src/db/queries.ts:67`
- **Dimension:** Security
- **Severity:** Blocker
- **Complexity:** Simple
- **Time Estimate:** 30 minutes
- **Fix Location:** This branch, before merge
- **Related Issue:** None found (searched "SQL injection", "query security")

**Description:**
Query uses string concatenation: `SELECT * FROM users WHERE id = ${userId}`
Vulnerable to SQL injection attacks.

**Recommendation:**
Use parameterized queries:
\```typescript
db.query('SELECT * FROM users WHERE id = ?', [userId])
\```

### 3. Inconsistent Pattern with Existing Parsers
- **File:** `src/parsers/new-parser.ts`
- **Dimension:** Cross-cutting (Pattern Consistency)
- **Severity:** Blocker
- **Complexity:** Moderate
- **Time Estimate:** 3 hours
- **Fix Location:** This branch, before merge
- **Related Issue:** As side effect of #123 (parser refactoring)

**Description:**
Other parsers (PythonParser, TypeScriptParser) inherit from BaseParser and implement
parse_file(). This parser doesn't follow that pattern, making it inconsistent with
established architecture.

As side effect of issue #123, the parser refactoring effort expects all parsers to
follow the BaseParser contract.

**Recommendation:**
Refactor to extend BaseParser and implement the standard interface.

## Critical (Should fix before merge)

### 1. Missing Test Coverage for Error Path
- **File:** `src/api/client.ts:45-60`
- **Dimension:** Test Coverage, Error Handling
- **Severity:** Critical
- **Complexity:** Moderate
- **Time Estimate:** 2 hours
- **Fix Location:** This branch or follow-up PR
- **Related Issue:** None found (searched "API client tests", "error handling")

**Description:**
Function handles network errors but tests only cover success case.
Missing tests for timeout, connection refused, malformed response.

**Recommendation:**
Add test cases for error conditions with mocked failures.

## Important (Fix soon after merge)

[Similar format for Important-level findings]

## Enhancements (Consider for future work)

[Similar format for Enhancement-level findings]

## Positive Feedback

- Clean dependency injection in UserService
- Good use of TypeScript strict mode features
- Clear variable naming throughout
```

### PR Comment Summary

```markdown
## Code Review Summary

Detailed review: `.scratch/code-review-pr-123-2025-10-18.md`

### Blockers (3) - Must fix before merge
1. **Missing required features from #121** (async validation, custom errors) - 4hrs, fix in this branch
2. **SQL injection vulnerability** (queries.ts:67) - 30min, fix in this branch
3. **Inconsistent parser pattern** (new-parser.ts) - Related to #123 - 3hrs, fix in this branch

### Critical (1) - Should fix before merge
1. **Missing error test coverage** (client.ts:45-60) - 2hrs, this branch or follow-up

### Important (3) - Fix soon after merge
[List items]

### Enhancements (2) - Consider for future
[List items]

See detailed review for full analysis, recommendations, and time estimates.
```

## Field Definitions

**File:** Location in the codebase where the finding occurs

**Dimension:** Which review dimension this falls under (see review-dimensions.md)

**Severity:** Classification level (see severity-classifications.md)

**Complexity:** Estimated implementation difficulty (Simple/Moderate/Complex)

**Time Estimate:** Rough estimate for fixing the issue

**Fix Location:** Where the fix should be made:
- "This branch, before merge" - Blocker that must be fixed now
- "This branch or follow-up PR" - Critical/Important that could be separate PR
- "Follow-up PR" - Enhancement for future work

**Related Issue:** Link to existing issues if applicable
- "None found (searched keywords)" - Document search attempts
- "#123 (description)" - Link to related issue
- "As side effect of #456" - Secondary effect of another issue

## Storage and Sharing

**Detailed reviews:**
- Save to `.scratch/code-review-pr-{NUMBER}-{DATE}.md`
- `.scratch/` directory is gitignored (create if needed)
- Preserves full analysis for reference
- Can be consulted later without reading full code again

**PR comments:**
- Post summary as PR comment using `gh pr comment`
- Links to detailed review for full context
- Provides actionable summary for quick triage
