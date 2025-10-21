---
name: No Emoji for Developers
description: Never use emoji presentation characters in developer-facing content - signals AI-generated code that wasn't reviewed
version: 1.0.0
---

# No Emoji for Developers

**Critical rule**: Do not use colorful emoji presentation characters in developer-facing content. This signals "AI wrote this and a human didn't review it" and looks unprofessional.

## Core Principle: Audience, Not Environment

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

## Why This Matters

Based on 17 years on engineering teams: Emoji in developer-facing content is a recent phenomenon that strongly correlates with AI-generated code. Seeing emoji in a PR description, code comment, or README signals:
- AI wrote this
- A human probably didn't look at it
- The code is probably janky

This undermines credibility and professionalism.

## Forbidden (Emoji Presentation)

**In all developer-facing content:**
- Colorful emojis: ✅ ❌ 🎉 🔧 🚀 📝 💡 ⚠️ 🐛
- **Test**: If it would render in color on a smartphone, don't use it for developers

## Acceptable Alternatives

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

## GitHub-Specific Features (Excellent!)

Take full advantage of GitHub's rendering capabilities:
- Task lists: `- [ ]` for unchecked, `- [x]` for checked (renders as interactive checkboxes)
- Collapsible sections: `<details><summary>Title</summary>content</details>`
- Syntax highlighting in code fences
- Tables with proper Markdown syntax
- Alerts: `> [!NOTE]`, `> [!WARNING]`, `> [!IMPORTANT]`
- Mermaid diagrams: ` ```mermaid ` code blocks
- Math: `$inline$` or `$$block$$` for LaTeX

These render visually rich content while remaining text-based in git history.

## Examples

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