---
name: GitHub Issue Management
description: Create well-labeled GitHub issues following best practices for duplicate detection and label management
version: 1.0.0
---

# GitHub Issue Management

Create clear, well-labeled issues. Always check for duplicates first and manage labels effectively.

## Before Creating New Issues

**CRITICAL: Check for duplicates first.**

1. Search existing **open** issues
2. Search **closed** issues too (the problem may have been addressed)
3. If duplicate exists, add context to existing issue rather than creating new one

```bash
# List and search existing issues
gh issue list
gh issue list --state all  # Include closed issues
gh issue list --search "keyword"
```

## Creating Issues

**1. Pull the current list of labels:**
```bash
gh label list
```

**2. Create the issue with appropriate existing labels:**
```bash
gh issue create --title "..." --body "..." --label "bug,documentation"
```

**3. If a label gap exists:**

Create a new label when:
- Something would add clarity
- The category would come up repeatedly
- No existing label captures the concept

```bash
# Create new label
gh label create "label-name" --description "..." --color "..."

# Then apply it to the issue
gh issue edit ISSUE_NUMBER --add-label "label-name"
```

## Issue Quality Standards

**Titles:**
- Clear and descriptive
- Summarize the issue
- Good: "Parser fails on nested arrow functions"
- Bad: "Bug in parser" or "Fix this"

**Body content:**
- **For bugs**: What's wrong, why it matters, how to reproduce
- **For features**: What you want, why it's valuable, acceptance criteria
- **For documentation**: What's missing or unclear, where it should go
- Provide context that helps others understand without back-and-forth

**Remember**: No emoji (developer-facing content) unless quoting

## Labeling Strategy

**Common label categories:**
- Type: `bug`, `enhancement`, `documentation`, `question`
- Priority: `high-priority`, `low-priority`
- Status: `needs-investigation`, `ready-for-review`, `blocked`
- Area: `parser`, `cli`, `testing`, `ci-cd`

**Apply multiple labels when appropriate:**
```bash
gh issue create --title "Add JSDoc validation" \
  --body "..." \
  --label "enhancement,documentation,parser"
```

## Quick Reference

```bash
# Check for duplicates
gh issue list --search "parser validation"
gh issue list --state all --search "jsdoc"

# Get available labels
gh label list

# Create issue with labels
gh issue create \
  --title "Fix parser validation for arrow functions" \
  --body "The parser fails when validating nested arrow functions..." \
  --label "bug,parser,high-priority"

# Create new label if needed
gh label create "needs-investigation" \
  --description "Requires research before implementation" \
  --color "d4c5f9"

# Add label to existing issue
gh issue edit 123 --add-label "needs-investigation"
```

## Remember

- Always check for duplicates first (open AND closed)
- Pull label list before creating issues
- Use clear, descriptive titles
- Provide context in the body
- Apply appropriate existing labels
- Create new labels for recurring categories
- No emoji in issue titles or descriptions (developer-facing)