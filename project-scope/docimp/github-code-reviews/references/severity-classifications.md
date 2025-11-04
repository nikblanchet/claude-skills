# Severity Classifications for Code Review Findings

This document defines severity levels for code review findings with examples and guidance for classification.

## Severity Levels

### Blocker
**Definition:** Must be fixed before merge. Issues that fundamentally break requirements, introduce serious risks, or violate core architectural patterns.

**Characteristics:**
- Prevents PR from being merged
- Requires immediate attention
- No workarounds acceptable
- Fixing is non-negotiable

**Examples:**

**Missing Required Features:**
- PR claims to implement feature X but only implements 70% of it
- Acceptance criteria from linked issue not met
- Design decisions from issue discussion were ignored
- Implementation doesn't match the agreed-upon approach

**Security Vulnerabilities:**
- SQL injection vulnerabilities
- XSS (Cross-Site Scripting) risks
- Authentication/authorization bypasses
- Hardcoded secrets or credentials
- Missing input validation on user data

**Data Loss Risks:**
- Code could delete or corrupt user data
- Missing transaction handling in critical operations
- Race conditions in data writes

**Breaking Changes:**
- Breaking changes to public APIs without migration path
- Incompatible changes to data formats
- Removal of features without deprecation cycle

**Architectural Violations:**
- Violates established patterns without justification
- Breaks core abstractions or contracts
- Creates circular dependencies
- Inconsistent with system architecture

**Crashes or Fatal Errors:**
- Code causes application to crash
- Unhandled exceptions in critical paths
- Resource leaks (memory, file handles, connections)

**Cross-Cutting Inconsistencies:**
- Pattern inconsistency that breaks system uniformity
- Polyglot boundary violations (e.g., incorrect serialization between languages)
- Dependency injection pattern violations

### Critical
**Definition:** Should be fixed before merge. Serious issues that don't completely block but significantly compromise quality, reliability, or maintainability.

**Characteristics:**
- Very important to address
- May be acceptable in follow-up PR if timeline critical
- Impacts system reliability or quality
- Creates technical debt if not addressed

**Examples:**

**Partial Implementation:**
- Most features work but some edge cases are missing
- Core functionality implemented but error handling incomplete
- Main use cases covered but important scenarios missing

**Missing Critical Error Handling:**
- Network errors not handled
- Timeout scenarios ignored
- Malformed input not validated
- Missing error recovery in important paths

**Performance Regressions:**
- Significantly slower than previous implementation
- Inefficient algorithm (O(n²) where O(n) possible)
- Missing caching that was present before
- Memory usage substantially increased

**Missing Test Coverage:**
- Important code paths not tested
- Error conditions not covered in tests
- Integration tests missing for new feature
- No tests for critical business logic

**Documentation Gaps:**
- Public APIs undocumented
- Complex logic unexplained
- Migration guide missing for breaking change
- Configuration options not documented

### Important
**Definition:** Should be fixed soon after merge. Issues that impact code quality or maintainability but don't critically compromise the system.

**Characteristics:**
- Can be addressed in follow-up PR
- Creates moderate technical debt
- Impacts long-term maintainability
- Should be tracked in an issue

**Examples:**

**Code Duplication:**
- Logic duplicated across multiple files
- Copy-paste code that should be extracted
- Similar patterns that could be unified

**Non-Critical Error Handling Gaps:**
- Edge case errors not handled
- Generic error messages that could be more specific
- Missing logging for debugging
- Errors swallowed without logging

**Maintainability Issues:**
- Functions too long or complex
- Poor variable naming
- Insufficient comments on complex logic
- Inconsistent code style

**Minor Architectural Inconsistencies:**
- Slight deviation from established patterns
- Could use better abstraction
- Coupling that could be reduced

**Missing Minor Features:**
- Nice-to-have configuration options
- Helpful utility functions
- Minor convenience features

### Enhancement
**Definition:** Consider for future work. Improvements that would be nice but aren't necessary for the current change.

**Characteristics:**
- Optional improvements
- No technical debt if not addressed
- Could improve user experience or developer experience
- Good candidates for separate feature work

**Examples:**

**Performance Optimizations:**
- Could be faster but current performance acceptable
- Potential caching opportunities
- Algorithm improvements that aren't critical

**Better Logging:**
- Additional debug logging
- More detailed metrics
- Better structured log messages

**Code Style Improvements:**
- Could use newer language features
- More idiomatic approaches available
- Better variable names possible

**Nice-to-Have Features:**
- Additional configuration options
- Extra convenience methods
- Enhanced error messages
- UI/UX improvements

### Nitpick
**Definition:** Very minor style or formatting issues. Often not worth mentioning unless pervasive.

**Characteristics:**
- Personal preference
- No functional impact
- No maintainability impact
- May not even warrant a comment

**Examples:**
- Variable naming preferences
- Comment formatting
- Whitespace preferences
- Order of imports (if not enforced by linter)

**Guidance:** Only mention nitpicks if they're pervasive or the code review has no more serious issues to discuss.

## Classification Decision Tree

1. **Does it prevent the feature from working as specified in the issue?**
   → Yes: **Blocker** (Missing Required Features)

2. **Does it introduce security vulnerabilities or data loss risks?**
   → Yes: **Blocker** (Security/Data Loss)

3. **Does it violate core architectural patterns without justification?**
   → Yes: **Blocker** (Architectural Violation)

4. **Does it significantly impact reliability or quality?**
   → Yes: **Critical** (if affects main paths) or **Important** (if affects edge cases)

5. **Does it impact maintainability or create technical debt?**
   → Yes: **Important** (significant debt) or **Enhancement** (minor improvement)

6. **Is it a style or preference issue?**
   → Yes: **Nitpick** (if worth mentioning at all)

## Time Estimates

Include rough time estimates for each finding to help prioritize:

- **Simple:** < 1 hour
- **Moderate:** 1-4 hours
- **Complex:** 4+ hours

This helps the author understand the scope and decide whether to fix immediately or in a follow-up.
