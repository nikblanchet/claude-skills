---
name: exhaustive-testing
description: Write comprehensive test coverage across unit, integration, regression, end-to-end, and manual tests. Watch for deprecation warnings in test output and address them immediately. Use when writing tests, implementing features, or before creating pull requests.
---

# Exhaustive Testing

Tests are not optional. Exhaustive testing is expected and valued.

## Core Principle: Tests Are a Feature

**Time allocation:**
- Spending 60% of time writing tests vs 40% coding is perfectly acceptable
- Tests catch problems early and provide confidence
- The only exception: truly disposable throwaway scripts

## Test Coverage Expectations

Write tests across multiple dimensions:

### Unit Tests

Test individual functions, methods, and classes in isolation.

**Requirements:**
- Mock dependencies to test logic independently
- Cover edge cases, error conditions, and boundary values
- Every public method should have corresponding unit tests
- Test both success paths and failure paths

**Example:**
```python
def test_calculate_impact_score_simple_function():
    scorer = ImpactScorer()
    assert scorer.calculate(complexity=1) == 5

def test_calculate_impact_score_with_audit():
    scorer = ImpactScorer()
    assert scorer.calculate(complexity=15, audit_rating=1) == 77

def test_calculate_impact_score_caps_at_100():
    scorer = ImpactScorer()
    assert scorer.calculate(complexity=50) == 100
```

### Integration Tests

Test how components work together.

**Requirements:**
- Verify interfaces between modules
- Test data flow through the system
- Ensure dependencies interact correctly
- Test realistic combinations of components

**Example:**
- Test that DocumentationAnalyzer correctly uses PythonParser and ImpactScorer together
- Test that TypeScript CLI correctly calls Python subprocess and parses JSON response
- Test that PluginManager loads and executes validation plugins

### Regression Tests

Prevent bugs from reappearing.

**Process:**
1. When a bug is found, write a test that reproduces it
2. Fix the bug, verify the test passes
3. Keep the test to prevent regression

**Example:**
```python
def test_parser_handles_nested_arrow_functions():
    """Regression test for issue #123 - parser crashed on nested arrows."""
    code = "const outer = () => { const inner = () => {}; }"
    items = parser.parse(code)
    assert len(items) == 2  # Should find both functions
```

### End-to-End Tests

Test complete user workflows.

**Requirements:**
- Verify the system works as a whole
- Test realistic usage scenarios
- Ensure CLI commands produce expected outputs
- May use actual files or fixtures

**Example:**
- Run `docimp analyze ./examples` and verify output format
- Run full improve workflow with mocked Claude API
- Test that generated documentation is actually written to files

### Manual Tests

Avoid manual testing when possible, but when automated testing isn't feasible, document the manual test procedure clearly.

**When manual testing is needed:**
- Features requiring external API keys (that can't/shouldn't be mocked)
- Interactive user input flows
- Visual inspection of terminal output formatting
- Complex integration scenarios requiring human judgment

**Documentation requirements:**
- Clear step-by-step instructions
- Expected outcomes at each step
- How to verify success/failure
- Prerequisites (API keys, environment setup, etc.)

**Where to document manual tests:**

1. **Products with test folders:** Create README in test folder
   - Example: `tests/MANUAL_TESTS.md` or `test-samples/README.md`
   - Link from project README
   - Link from CONTRIBUTING.md if it exists

2. **If unclear where to document:** Ask before creating

**Example manual test documentation:**

```markdown
# Manual Testing Guide

## Testing the Improve Workflow with Claude API

**Prerequisites:**
- ANTHROPIC_API_KEY environment variable set
- Sample codebase in `examples/` directory

**Test Steps:**

1. Run: `docimp improve ./examples`
2. Select a function to document (e.g., #1)
3. Verify Claude generates appropriate documentation suggestion
4. Choose [A] Accept
5. Verify documentation is written to source file
6. Run `git diff` to inspect changes

**Expected Outcomes:**
- Documentation follows project style guide (NumPy/JSDoc)
- Parameters and return types match function signature
- Documentation is inserted at correct location
- File remains syntactically valid

**How to verify:**
- Visual inspection of git diff
- Run tests to ensure nothing broke
- Check that linters/formatters accept the changes
```

**Link from project README:**
```markdown
## Testing

### Manual Testing

Some **manual testing is required** on this project! See [Manual Testing Guide](tests/MANUAL_TESTS.md).

### Automated Testing

Run automated tests:
```bash
pytest -v
npm test
```

## Test Quality Standards

**Readable and maintainable:**
- Test names clearly describe what's being tested
- Use Arrange-Act-Assert pattern for clarity
- Keep tests focused and understandable

**One thing per test:**
- Each test should verify one behavior
- Don't pack multiple assertions for unrelated things
- Easier to debug when failures are isolated

**Deterministic:**
- No flaky tests
- Tests should pass or fail consistently
- Mock external dependencies (API calls, file system, time)
- Use fixtures for repeatable test data

**Must pass before merge:**
- All tests must pass before code can be merged
- No exceptions
- CI/CD enforces this

## When to Write Tests

**Write tests alongside implementation:**
- Not as an afterthought
- TDD is encouraged when it helps clarify requirements
- At minimum: tests must exist before PR is merged

**Examples of good timing:**
- Write test for edge case, then implement handling
- Write test that fails, implement feature, verify test passes
- Add tests in same commit as feature implementation

## Test Failures Are Blockers

**All tests must pass:**
- Flaky tests must be fixed or removed, not ignored
- If a test is difficult to write, that's often a signal the code needs refactoring
- Don't merge with failing tests
- Don't skip tests to "fix later"

## Deprecation Warnings During Testing

**CRITICAL: Pay attention to deprecation warnings in test output.**

When running tests, you may see deprecation warnings from libraries. Don't ignore them - address them immediately.

**Why this matters:** Claude Code ignores deprecation warnings by default, so when you see them in test output, explicitly notice and act on them. These warnings signal upcoming breaking changes that should be addressed now, not later.

**See the `handle-deprecation-warnings` skill for detailed workflow:** Read the warning, check migration guides, update code to use recommended APIs, don't suppress warnings.

## Test Organization

**Structure tests to mirror source code:**
```
project/
  src/
    parsers/
      python_parser.py
    scoring/
      impact_scorer.py
  tests/
    test_parsers.py        # or parsers/test_python_parser.py
    test_scoring.py        # or scoring/test_impact_scorer.py
    MANUAL_TESTS.md        # Manual testing guide
```

**Use fixtures and test helpers:**
- Extract common setup to fixtures
- Create helper functions for repetitive test patterns
- Share test data across related tests

## Example Test Coverage for a Feature

**Feature: Impact Scorer**

```python
# Unit tests
def test_simple_complexity_scoring()
def test_complex_function_scoring()
def test_score_caps_at_100()
def test_audit_rating_penalty_terrible()
def test_audit_rating_penalty_ok()
def test_audit_rating_penalty_good()
def test_audit_rating_penalty_excellent()
def test_negative_complexity_raises_error()
def test_invalid_audit_rating_raises_error()

# Integration tests
def test_scorer_integrates_with_analyzer()
def test_scorer_results_used_in_coverage_report()

# Regression tests
def test_audit_None_doesnt_crash()  # Issue #45

# End-to-end tests
def test_cli_shows_correct_scores_in_output()

# Manual tests (documented in tests/MANUAL_TESTS.md)
# - Verify scores display correctly with color formatting
# - Test interactive prompts with various user inputs
```

## Remember

- Tests are not optional
- 60% time on tests is acceptable
- Cover unit, integration, regression, e2e, and manual (when needed)
- Document manual tests clearly with step-by-step procedures
- One thing per test
- Deterministic, no flaky tests
- Must pass before merge
- Write alongside implementation