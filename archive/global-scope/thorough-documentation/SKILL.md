---
name: Thorough Documentation
description: Write extensive, comprehensive documentation - documentation is not optional
version: 1.0.0
---

# Thorough Documentation

Documentation is not optional. Extensive documentation is expected and valued.

## Core Principle

Default to documenting code thoroughly rather than minimally. Documentation should be comprehensive enough that other developers (or your future self) can understand the code without needing to reverse-engineer it.

## What to Document

**Always document:**
- Public APIs (functions, classes, methods exposed to users or other modules)
- Complex logic or algorithms
- Non-obvious design decisions
- Parameters, return values, and exceptions
- Side effects and state changes
- Preconditions and postconditions
- Examples of usage for non-trivial functionality
- Known issues/compromises (with reference to GitHub issue if appropriate)

**Internal/private code:**
- Document if the logic is complex or non-obvious
- Simple getters/setters may not need documentation
- Use judgment: would a new team member understand this in 6 months?

## Documentation is Not an Afterthought

Write documentation as you write code:
- Don't defer documentation to "later"
- Document while the design is fresh in your mind
- Documentation often reveals design issues early
- Good documentation makes code review more effective

## Tone Varies by Project

While **thoroughness** is universal, the **tone and style** depend on the project:
- Some projects need technical precision
- Some benefit from a friendly, approachable tone
- Some are deliberately humorous
- Some assume expert audiences and can be terse

The project context determines tone, but the expectation of extensive documentation remains constant.

## Quality Expectations

**Technical accuracy is critical:**
- Ensure parameter names match actual signatures
- Return types should be correct
- Examples should actually work

**Clear, concise language:**
- Use proper grammar and punctuation
- Avoid hedging language ("perhaps," "maybe," "might") unless genuine uncertainty exists
- Be direct: "Returns the user object" not "Should return the user object"
- Keep sentences focused and purposeful

## Examples

**Good documentation:**
```python
def calculate_impact_score(complexity: int, audit_rating: Optional[int] = None) -> float:
    """
    Calculate priority score for documentation needs.

    Combines cyclomatic complexity with optional audit quality ratings to
    determine which code items need documentation most urgently. Higher scores
    indicate higher priority.

    Parameters:
        complexity: Cyclomatic complexity (1+)
        audit_rating: Optional quality rating (1-4, where 1=terrible, 4=excellent)

    Returns:
        Score from 0-100, where higher values indicate higher documentation priority

    Examples:
        >>> calculate_impact_score(5)
        25.0
        >>> calculate_impact_score(15, audit_rating=1)
        77.0
    """
```

**Insufficient documentation:**
```python
def calculate_impact_score(complexity: int, audit_rating: Optional[int] = None) -> float:
    """Calculate score."""
```

## Remember

The docs are the product. Documentation is a feature, not a chore. Invest the time to do it well.