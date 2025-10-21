---
name: development-standards
description: Developer-facing content standards and code quality principles - no emoji in code/docs/PRs/issues, use cutting-edge language features, write comprehensive documentation. Always-active standards applied to all development work.
---

# Development Standards

Three core standards for all development work. These standards apply continuously and shape how code, documentation, and developer communications are written.

## No Emoji in Developer-Facing Content

**Critical rule**: Do not use colorful emoji presentation characters in developer-facing content. This signals "AI wrote this and a human didn't review it" and looks unprofessional.

### Core Principle: Audience, Not Environment

The determining factor is **who will see this content**, not whether it's rendered in monospace or variable-width fonts.

**Developer-facing content** → No emoji
- Pull request descriptions (even though rendered in variable-width on GitHub)
- Code comments and docstrings
- README files
- GitHub issues
- Commit messages
- Technical documentation
- Any content primarily consumed by contributing developers

**End-user-facing content** (non-monospace environments) → Emoji acceptable
- Web application UI
- Marketing materials
- End-user documentation
- Customer-facing interfaces

**End-user-facing content** (monospace environments) → No emoji
- Terminal output
- CLIs
- Code displays

**Exception that trumps everything**: When quoting or documenting something that contains emoji, use the emoji in the quote regardless of audience or environment.

### Why This Matters

Based on 17 years on engineering teams: Emoji in developer-facing content is a recent phenomenon that strongly correlates with AI-generated code. Seeing emoji in a PR description, code comment, or README signals:
- AI wrote this
- A human probably didn't look at it
- The code is probably janky

This undermines credibility and professionalism.

### Forbidden (Emoji Presentation)

**In all developer-facing content:**
- Colorful emojis: ✅ ❌ 🎉 🔧 🚀 📝 💡 ⚠️ 🐛
- **Test**: If it would render in color on a smartphone, don't use it for developers

### Acceptable Alternatives

Any Unicode character that renders as monospace in terminal fonts, including:

**Basic symbols:**
- ASCII: `* - + > < [ ] ( ) / \ | _ = ~`
- Mathematical operators: `× ÷ ± ≠ ≈ ≤ ≥ ∞`
- Arrows: `→ ← ↑ ↓ ↔ ⇒ ⇐`
- Bullets and marks: `• ◦ ∙ ‣`

**Monochrome/text presentation forms:**
- Text checkmark: ✔︎ (Good!)
- Emoji checkmark: ✅ (Awful in PR descriptions!)
- Boxes: `☐ ☑ ☒`
- Box drawing: `─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼`
- Geometric shapes: `■ □ ▪ ▫ ▲ △ ▼ ▽ ◆ ◇ ○ ●`

These are **examples**, not an exhaustive list. Use any monospace Unicode characters appropriate to the context.

### GitHub-Specific Features (Excellent!)

Take full advantage of GitHub's rendering capabilities:
- Task lists: `- [ ]` for unchecked, `- [x]` for checked (renders as interactive checkboxes)
- Collapsible sections: `<details><summary>Title</summary>content</details>`
- Syntax highlighting in code fences
- Tables with proper Markdown syntax
- Alerts: `> [!NOTE]`, `> [!WARNING]`, `> [!IMPORTANT]`
- Mermaid diagrams: ` ```mermaid ` code blocks
- Math: `$inline$` or `$$block$$` for LaTeX

These render visually rich content while remaining text-based in git history.

### Examples

**Pull request description:**
- Don't: "Added new feature 🎉"
- Do: "Added new feature"
- Do: "Added new feature (see checklist below)"

**Code comment:**
- Don't: "TODO: Fix this bug 🐛"
- Do: "TODO: Fix this bug"

**README feature list:**
- Don't: "✅ Fast performance"
- Do: "• Fast performance"
- Do: "- Fast performance"

**Docstring documenting a web UI:**
- Do: "Returns the emoji for the status: '✅' for success, '❌' for failure"
- (Quoting the actual UI trumps the no-emoji rule)

## Use Modern Language Versions

Be an early adopter of language features.

### Philosophy

If a recent language version (released within the past 6 months) offers more elegant, extensible, or clear solutions, use them.

**Key principles:**
- Don't artificially maintain compatibility with older versions unless the project specifically requires it
- It's perfectly fine to require cutting-edge language versions (e.g., Python 3.13, latest TypeScript)
- When working on existing projects: respect the minimum version specified in the project's requirements
- For new projects: use the latest stable language features without hesitation

### In Practice

**Python:**
- Use structural pattern matching, exception groups, type parameter syntax, etc. if they improve clarity
- Don't add compatibility shims or fallbacks for older versions unless explicitly needed

**TypeScript:**
- Use latest syntax and type system features
- Don't hold back for older compiler versions

**Documentation:**
- Document the minimum version requirement clearly in README and package metadata

### When NOT to Use Latest Features

Only maintain compatibility with older versions when:
- The project explicitly specifies a minimum version requirement
- You're contributing to an existing codebase with established version constraints
- There's a documented technical reason for the constraint

## Write Thorough Documentation

Documentation is not optional. Extensive documentation is expected and valued.

### Core Principle

Default to documenting code thoroughly rather than minimally. Documentation should be comprehensive enough that other developers (or your future self) can understand the code without needing to reverse-engineer it.

### What to Document

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

### Documentation is Not an Afterthought

Write documentation as you write code:
- Don't defer documentation to "later"
- Document while the design is fresh in your mind
- Documentation often reveals design issues early
- Good documentation makes code review more effective

### Tone Varies by Project

While **thoroughness** is universal, the **tone and style** depend on the project:
- Some projects need technical precision
- Some benefit from a friendly, approachable tone
- Some are deliberately humorous
- Some assume expert audiences and can be terse

The project context determines tone, but the expectation of extensive documentation remains constant.

### Quality Expectations

**Technical accuracy is critical:**
- Ensure parameter names match actual signatures
- Return types should be correct
- Examples should actually work

**Clear, concise language:**
- Use proper grammar and punctuation
- Avoid hedging language ("perhaps," "maybe," "might") unless genuine uncertainty exists
- Be direct: "Returns the user object" not "Should return the user object"
- Keep sentences focused and purposeful

### Examples

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

### Remember

The docs are the product. Documentation is a feature, not a chore. Invest the time to do it well.
