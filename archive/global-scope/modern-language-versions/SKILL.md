---
name: Modern Language Versions
description: Adopt cutting-edge language features for cleaner, more elegant code
version: 1.0.0
---

# Modern Language Versions

Be an early adopter of language features.

## Philosophy

If a recent language version (released within the past 6 months) offers more elegant, extensible, or clear solutions, use them.

**Key principles:**
- Don't artificially maintain compatibility with older versions unless the project specifically requires it
- It's perfectly fine to require cutting-edge language versions (e.g., Python 3.13, latest TypeScript)
- When working on existing projects: respect the minimum version specified in the project's requirements
- For new projects: use the latest stable language features without hesitation

## In Practice

**Python:**
- Use structural pattern matching, exception groups, type parameter syntax, etc. if they improve clarity
- Don't add compatibility shims or fallbacks for older versions unless explicitly needed

**TypeScript:**
- Use latest syntax and type system features
- Don't hold back for older compiler versions

**Documentation:**
- Document the minimum version requirement clearly in README and package metadata

## When NOT to Use Latest Features

Only maintain compatibility with older versions when:
- The project explicitly specifies a minimum version requirement
- You're contributing to an existing codebase with established version constraints
- There's a documented technical reason for the constraint
