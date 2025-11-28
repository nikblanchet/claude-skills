---
name: commit-style
description: Custom commit message and PR description conventions. This skill should be used when making git commits or creating pull requests to ensure consistent attribution formatting.
---

# Commit Style

## Overview

This skill defines the commit message footer and PR description signature format for this repository and related projects.

## Commit Message Format

End all commit messages with the following footer:

```
Generated with [Claude Code](https://claude.com/claude-code)
Steered and verified by @nikblanchet (PARENTHETICAL)
```

## PR Description Format

End all PR descriptions with the same signature format:

```
Generated with [Claude Code](https://claude.com/claude-code)
Steered and verified by @nikblanchet (PARENTHETICAL)
```

## Parenthetical Generation

Generate a fresh, creative 2-5 word humorous expression for each commit/PR. Do NOT reuse parentheticals within a session.

**Style guidelines:**
- Be creative, absurd, witty, or referential
- Pop culture, tech, gaming, music, languages all welcome
- Proper nouns and initialisms can be capitalized
- Intentional misspellings for comedic effect are fine
- Can be questions, phrases, descriptions, or non-sequiturs
- Multilingual expressions are welcome

**Example parentheticals for inspiration** (generate new ones, don't reuse these):
- mostly human
- caffeinated primate
- Spock's ex-boyfriend
- confused DM
- SoundCloud zealot
- ironic Apple fanboi
- is Henry Cavill single
- merge conflict survivor
- rubber duck consultant
- regex whisperer
- async/await sommelier

## Important Notes

- Do NOT use robot emoji or any other emoji in the signature
- Do NOT include the `Co-Authored-By` trailer
- Each parenthetical should be unique and freshly generated
