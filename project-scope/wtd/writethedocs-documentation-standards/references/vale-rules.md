# Vale Rules Reference

Complete reference for Vale prose linting rules used in Write the Docs.

## Vale Configurations

Write the Docs uses 3 separate Vale configurations with different rule sets:

1. **General content** (`vale/vale.ini`) - Most pages
2. **Guide content** (`vale/guide.ini`) - `docs/guide/` directory (stricter)
3. **Conference news** (`vale/news.ini`) - `docs/conf/**/news/*` (minimal)

## WTD Custom Rules

Located in `vale/WTD/` directory.

### Headings (`WTD/headings.yml`)

**Rule**: Headings must use sentence case

**Error level**: error

**Regex pattern**: Matches title case headings (multiple capitalized words)

**Exceptions** (proper nouns):
- Write the Docs
- Read the Docs
- Sphinx
- reStructuredText
- Git, GitHub, GitLab
- API, REST, JSON, XML, HTML, CSS
- Python, JavaScript, Ruby, Go
- Linux, macOS, Windows
- MySQL, PostgreSQL
- Docker, Kubernetes

**Examples**:

```rst
# Wrong (Title Case)
Getting Started With The API
=============================

How To Write Good Documentation
--------------------------------

# Correct (Sentence case)
Getting started with the API
=============================

How to write good documentation
----------------------------------

# Correct (Proper nouns capitalized)
Using the Sphinx documentation tool
====================================

Integrating with the GitHub API
================================
```

### Branding (`WTD/Branding.yml`)

**Rule**: Enforce correct branding for Write the Docs and Read the Docs

**Error level**: error

**Patterns**:

**Write the Docs**:
- ✅ "Write the Docs"
- ❌ "Write The Docs"
- ❌ "write the docs"
- ❌ "Write the docs"
- ✅ "WTD" (acronym OK)

**Read the Docs**:
- ✅ "Read the Docs"
- ❌ "Read The Docs"
- ❌ "ReadTheDocs"
- ❌ "read the docs"

**Examples**:

```rst
# Wrong
The Write The Docs community hosts annual conferences.
Read The Docs provides free hosting for documentation.

# Correct
The Write the Docs community hosts annual conferences.
Read the Docs provides free hosting for documentation.

# Acronym acceptable
Join the WTD Slack for community discussion.
```

### Inclusivity (`WTD/inclusivity.yml`)

**Rule**: Replace "tribe" with more inclusive terms

**Error level**: error

**Replacement suggestions**:
- people
- group
- team
- community

**Example**:

```rst
# Wrong
Find your tribe of documentarians.

# Correct
Find your people of documentarians.
Find your community of documentarians.
```

### Inclusivity Avoid (`WTD/inclusivity-avoid.yml`)

**Rule**: Avoid non-inclusive language

**Error level**: error

**Additional patterns** (beyond "tribe"):
- Gendered language where gender-neutral exists
- Unnecessarily gendered pronouns

**Best practice**: Use "they/them" as singular pronoun

**Example**:

```rst
# Less inclusive
When a developer writes his code, he should document it.

# More inclusive
When a developer writes their code, they should document it.
When developers write code, they should document it.
```

### Sentence Length (`WTD/SentenceLength.yml`)

**Rule**: Sentences should not exceed 28 words

**Error level**: suggestion (not error)

**Why**: Improves readability and scannability

**Example**:

```rst
# Too long (38 words)
This is an example of a sentence that goes on for far too long without any breaks which makes it difficult for readers to follow the main point that is being conveyed and may cause confusion.

# Better (split into two sentences, 19 + 11 words)
This sentence is too long without breaks, making it difficult for readers to follow the main point. Split long sentences to improve readability.
```

### Newsletter Contents (`WTD/contents.yml`)

**Rule**: Don't use `.. contents::` directive in newsletter posts

**Error level**: error

**Applies to**: Conference news only (`vale/news.ini`)

**Reason**: Newsletter format doesn't support table of contents

**Example**:

```rst
# Wrong (in newsletter post)
.. contents::
   :local:
   :depth: 2

# Correct (omit TOC in newsletters)
# Just write content directly
```

## Proselint Rules

Located in `vale/proselint/` directory.

Write the Docs uses proselint but **many rules are disabled** for legacy content compatibility.

**Enabled proselint rules**:
- Basic grammar checks
- Some redundancy detection
- Obvious style issues

**Disabled proselint rules** (many):
- Strict style preferences
- Rules that conflict with technical writing
- Rules with too many false positives on legacy content

**Note**: Proselint rules apply at warning level for general content, higher for guide content.

## TheEconomist Rules

Located in `vale/TheEconomist/` directory.

**Enabled rule**:
- `Hectoring.yml` - Avoid hectoring/preachy tone

**Level**: warning

**Example**:

```rst
# Hectoring (avoid)
You must always write documentation.
You should never skip tests.

# Better
Write documentation for all features.
Include tests for new functionality.
```

## Configuration Files

### General Content (`vale/vale.ini`)

```ini
StylesPath = vale
MinAlertLevel = warning

[*.{rst,md}]
BasedOnStyles = WTD, proselint
WTD.headings = YES
WTD.Branding = YES
WTD.inclusivity = YES
WTD.inclusivity-avoid = YES
WTD.SentenceLength = suggestion
TheEconomist.Hectoring = warning

# Many proselint rules disabled for legacy content
proselint.Very = NO
proselint.Cliches = NO
# ... many more disabled
```

### Guide Content (`vale/guide.ini`)

```ini
StylesPath = vale
MinAlertLevel = error  # Stricter!

[*.{rst,md}]
BasedOnStyles = WTD, proselint
WTD.headings = error
WTD.Branding = error
WTD.inclusivity = error
WTD.inclusivity-avoid = error
WTD.SentenceLength = error  # Enforced for guide!

# Fewer proselint rules disabled
# Guide content held to higher standard
```

### Conference News (`vale/news.ini`)

```ini
StylesPath = vale
MinAlertLevel = error

[*.{rst,md}]
BasedOnStyles = WTD
WTD.contents = error  # Only check for contents directive

# Minimal rules for announcements
```

## Testing Locally

### General Content

```bash
vale --config=vale/vale.ini docs/

# Specific file
vale --config=vale/vale.ini docs/guide/contributing.rst

# Ignore warnings, errors only
vale --config=vale/vale.ini --minAlertLevel=error docs/
```

### Guide Content

```bash
vale --config=vale/guide.ini docs/guide/

# Single file
vale --config=vale/guide.ini docs/guide/writing/style-guides.rst
```

### Conference News

```bash
vale --config=vale/news.ini --glob='docs/conf/**/news/*' docs

# Specific conference
vale --config=vale/news.ini docs/conf/portland/2025/news/
```

## CI/CD Integration

**Workflow file**: `.github/workflows/vale.yml`

**Three separate checks**:
1. Vale general (uses `vale/vale.ini`)
2. Vale guide (uses `vale/guide.ini`)
3. Vale news (uses `vale/news.ini`)

**Reporter**: reviewdog (comments directly on PR)

**Failure behavior**: All must pass (fail_on_error: true)

## Common Vale Failures and Fixes

### Heading Capitalization

```
docs/guide/api-documentation.rst:15:1: error: Headings must use sentence case
    Writing API Documentation
```

**Fix**: Change to sentence case
```rst
# Before
Writing API Documentation
=========================

# After
Writing API documentation
=========================
```

### Branding

```
docs/conf/portland/2025/index.rst:22:5: error: Use 'Write the Docs' not 'Write The Docs'
    Welcome to Write The Docs Portland 2025
```

**Fix**: Correct capitalization
```rst
# Before
Welcome to Write The Docs Portland 2025

# After
Welcome to Write the Docs Portland 2025
```

### Sentence Length

```
docs/guide/writing.rst:45:1: suggestion: Sentence is too long (32 words)
```

**Fix**: Split into multiple sentences
```rst
# Before
This sentence contains far too many words and subordinate clauses which make it difficult to read and understand the main point being communicated.

# After
This sentence is too long. Split it into shorter sentences for better readability.
```

### Inclusivity

```
docs/guide/community.rst:78:10: error: Replace 'tribe' with 'people', 'group', or 'team'
    Find your tribe at Write the Docs
```

**Fix**: Use inclusive term
```rst
# Before
Find your tribe at Write the Docs

# After
Find your people at Write the Docs
Find your community at Write the Docs
```

## Ignoring Vale Warnings

**Rarely necessary** - fix the issue instead!

If absolutely needed (false positive):

```rst
<!-- vale off -->
This text will not be checked by Vale.
<!-- vale on -->
```

**Better approach**: Update Vale rules if there are systematic false positives.

## Vale Version

Write the Docs uses **Vale 3.4.2**

Specified in `.github/workflows/vale.yml`:
```yaml
version: 3.4.2
```

Ensure local Vale matches CI version for consistent results.

## Adding New Rules

If proposing new Vale rules:

1. Create rule file in `vale/WTD/`
2. Test thoroughly on existing content
3. Update configurations (`vale.ini`, `guide.ini`)
4. Document in this file
5. Submit PR with justification

**Note**: New rules should not break existing content unless fixing systematic issues.
