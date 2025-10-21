---
name: handle-deprecation-warnings
description: Notice and address deprecation warnings immediately in test output, CI/CD logs, and development - read the warning, check migration guides, update code to use recommended APIs, don't suppress warnings. Use when seeing deprecation warnings, DeprecationWarning messages, or deprecated API notices.
---

# Handle Deprecation Warnings

Take deprecation warnings seriously. Address them immediately, don't ignore them.

## Core Principle: Proactive Migration

**Don't accumulate technical debt by ignoring deprecation warnings.**

- If a feature will be removed in an upcoming version, use the preferred approach now
- Proactive migration is easier than forced refactoring later
- Code is more maintainable when you stay current with library evolution
- Deprecation warnings are the library authors giving you advance notice - respect that

## When You'll See Deprecation Warnings

**During test runs:**
- Test output often shows deprecation warnings
- Don't ignore them thinking "tests pass, so it's fine"
- Fix immediately while context is fresh

**During development:**
- Running code locally
- Interactive shells or notebooks
- CI/CD output

**During dependency updates:**
- Updating a library may introduce new deprecation warnings
- Address them as part of the update process

## How to Handle a Deprecation Warning

**1. Read the warning carefully**

Deprecation warnings usually tell you:
- What is deprecated
- What to use instead
- When it will be removed

```
DeprecationWarning: parse_config(file) is deprecated and will be removed in v2.0.
Use parse_config(path=file) instead.
```

**2. Check the library's migration guide or changelog**

- Look for migration documentation
- Check release notes for the version that deprecated the feature
- Look for examples of the new approach

**3. Update to the recommended approach immediately**

Don't defer to "later" - fix it now:

```python
# Old (deprecated)
config = parse_config(config_file)

# New (recommended)
config = parse_config(path=config_file)
```

**4. Don't just suppress the warning**

Suppressing warnings without fixing the underlying issue is technical debt:

```python
# BAD - Just hiding the problem
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
```

Fix the code instead.

## Examples

### Python: Positional to Keyword Argument

```python
# Deprecation warning:
# DeprecationWarning: Passing 'timeout' as positional argument is deprecated.
# Pass as keyword argument instead.

# Old (deprecated)
response = client.request(url, 30)

# New (recommended)
response = client.request(url, timeout=30)
```

### Python: Function Renamed

```python
# Deprecation warning:
# DeprecationWarning: get_items() is deprecated. Use fetch_items() instead.

# Old (deprecated)
items = service.get_items()

# New (recommended)
items = service.fetch_items()
```

### TypeScript: Method Signature Change

```typescript
// Deprecation warning:
// [Deprecated] configure(options) is deprecated. Use configure({options}) instead.

// Old (deprecated)
analyzer.configure(true, false, "strict");

// New (recommended)
analyzer.configure({
  validate: true,
  strict: "strict",
  cache: false
});
```

### Node.js: Import Path Change

```javascript
// Deprecation warning:
// [DEP0148] Use of deprecated folder mapping "./" in "exports" field

// Old (deprecated)
import { Parser } from "library/internal/parser";

// New (recommended)
import { Parser } from "library";
```

## If You Can't Fix Immediately

Sometimes a deprecation requires significant refactoring. In this case:

**1. Create an issue to track it:**

```bash
gh issue create \
  --title "Migrate from deprecated parse_config() API" \
  --body "Library xyz deprecated parse_config(file) in favor of parse_config(path=file).

**Deprecation Warning:**
\`\`\`
DeprecationWarning: parse_config(file) is deprecated and will be removed in v2.0.
\`\`\`

**Affected Files:**
- src/config/loader.py:45
- src/api/client.py:67

**Estimate:** 2 hours to update all call sites and tests

**Target:** Before upgrading to xyz v2.0" \
  --label "dependency,deprecation-warning"
```

**2. Don't suppress the warning without tracking it**

The warning should remain visible until the issue is resolved.

**3. Prioritize based on removal timeline**

- "Will be removed in next major version" → High priority
- "Will be removed in 2 years" → Medium priority
- Plan the migration before the removal deadline

## Integration with Other Workflows

**See also:**
- `dependency-management` skill for updating dependencies
- `exhaustive-testing` skill for handling warnings during test runs

When updating dependencies, always check for and address new deprecation warnings as part of the update.

## Quick Reference

```bash
# 1. See deprecation warning during tests
pytest -v

# 2. Read warning carefully, check migration docs
# (library documentation, changelog, migration guide)

# 3. Update code to use recommended approach
# (fix the actual code, don't suppress)

# 4. If can't fix immediately, create tracking issue
gh issue create --title "Migrate deprecated API" --body "..." --label "technical-debt"

# 5. Verify warning is gone
pytest -v  # Should be clean
```

## Remember

- Address deprecation warnings immediately
- Read the warning and check migration guides
- Fix the code, don't suppress the warning
- If significant work, create an issue to track it
- Proactive migration is easier than forced refactoring
- Deprecation warnings are advance notice - respect that