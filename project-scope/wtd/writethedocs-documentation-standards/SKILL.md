---
name: writethedocs-documentation-standards
description: RST/Markdown writing standards, Vale rules, YAML data management, and content guidelines for Write the Docs. Use when writing documentation, creating conference pages, or ensuring content meets style requirements.
---

# Write the Docs Documentation Standards

This skill provides RST/Markdown formatting standards, Vale prose linting rules, YAML schema requirements, and content guidelines for the Write the Docs project.

## When to Use This Skill

Use this skill when:
- Writing or editing RST/Markdown content
- Creating conference pages with YAML data
- Fixing Vale linting failures
- Understanding heading capitalization rules
- Managing conference YAML files
- Ensuring content meets community standards

## File Formats

Write the Docs uses multiple formats:
- **1,644 RST files** (primary format)
- **108 Markdown files** (secondary, mainly conferences)
- **100+ YAML files** (conference data)

Both RST and Markdown supported via Sphinx + myst-parser.

## RST/Markdown Style Standards

### Heading Capitalization

**Rule**: Use sentence case for all headings

**Correct**:
```rst
This is a proper heading
========================

Getting started with documentation
-----------------------------------
```

**Wrong**:
```rst
This Is A Proper Heading
========================

Getting Started With Documentation
-----------------------------------
```

**Exceptions** (proper nouns always capitalized):
- Write the Docs
- Read the Docs
- Sphinx
- Git, GitHub
- API, REST, JSON
- Python, JavaScript
- macOS, Linux, Windows

### Branding Guidelines

**Strict enforcement** (error level):

**Write the Docs**:
- ✅ "Write the Docs"
- ❌ "Write The Docs"
- ❌ "Write the docs"
- ✅ "WTD" (acronym acceptable)

**Read the Docs**:
- ✅ "Read the Docs"
- ❌ "Read The Docs"
- ❌ "ReadTheDocs"

### Inclusivity Rules

**Replace problematic terms**:
- ❌ "tribe" → ✅ "people", "group", "team"
- Avoid gendered language when gender-neutral alternatives exist
- Use "they/them" as singular pronoun

### Sentence Length

**Guideline**: Maximum 28 words per sentence (suggestion, not error)

**Why**: Improves readability and scannability

**How to fix**: Split long sentences with periods or semicolons

### Writing Tone

From contributing guide:
- Use friendly and encouraging tone
- Write for a general audience
- Avoid tool advocacy - present use cases and results
- Focus on general principles, not personal preferences
- Attribute links and explain why they're useful

## Vale Enforcement Levels

Write the Docs uses **3 Vale configurations** with different strictness:

### 1. General Content (`vale/vale.ini`)

**Applies to**: Most documentation pages

**Rules**:
- WTD styles (headings, branding, inclusivity)
- proselint (many rules disabled for legacy content)
- TheEconomist.Hectoring
- Warning level minimum

**Test locally**:
```bash
vale --config=vale/vale.ini docs/
```

### 2. Guide Content (`vale/guide.ini`)

**Applies to**: `docs/guide/` directory

**Rules** (stricter):
- All WTD styles enforced
- Heading sentence case (error level)
- Inclusivity rules (error level)
- Gender bias checking enabled
- Sentence length enforced

**Test locally**:
```bash
vale --config=vale/guide.ini docs/guide/
```

### 3. Conference News (`vale/news.ini`)

**Applies to**: `docs/conf/**/news/*`

**Rules** (minimal):
- Don't use `.. contents::` directive in newsletter posts
- Error level enforcement

**Test locally**:
```bash
vale --config=vale/news.ini --glob=docs/conf/**/news/* docs
```

### Common Vale Failures

**Heading capitalization**:
```rst
# Wrong
Getting Started With The API
=============================

# Correct
Getting started with the API
=============================
```

**Branding**:
```rst
# Wrong
The Write The Docs community...

# Correct
The Write the Docs community...
```

**Sentence length**:
```rst
# Too long (>28 words)
This is an example of a sentence that goes on for far too long without any breaks and makes it difficult for readers to follow the main point being conveyed.

# Better (split into two)
This sentence is too long without breaks. It makes it difficult for readers to follow the main point.
```

## YAML Data Standards

All conference YAML must validate against schemas in `docs/_data/schema-*.yaml`.

See `references/yaml-schemas.md` for complete details.

### Three YAML Types

**1. Config YAML** (`{shortcode}-{year}-config.yaml`):
- Conference metadata (name, dates, location)
- Sponsor information
- Feature flags (flagcfp, flagspeakersannounced, etc.)
- Timezone and time format settings

**2. Sessions YAML** (`{shortcode}-{year}-sessions.yaml`):
- Speaker information (name, bio, photo)
- Talk details (title, abstract, slug)
- YouTube video IDs (post-conference)

**3. Schedule YAML** (`{shortcode}-{year}-schedule.yaml`):
- Time-ordered conference agenda
- Links to sessions via slugs
- Break times, meals, social events
- Multi-timezone support

### YAML Validation

**Required before PR**:
```bash
cd docs/_scripts
./validate-yaml.sh
```

**Common validation errors**:
- Missing required fields
- Wrong data types (string instead of int)
- Invalid enum values (time_format must be '12h' or '24h')
- Malformed YAML syntax (tabs instead of spaces)

### YAML Linting

**Configuration**: `.yamllint.yaml` (relaxed rules)

Disabled rules:
- line-length
- hyphens
- new-line-at-end-of-file
- trailing-spaces

Focus is on schema validation, not formatting nitpicks.

## Conference Page Structure

### Required Metadata

Every conference index.rst must have:

```rst
:template: {{year}}/index.html
:banner: _static/conf/images/headers/{{shortcode}}-{{year}}-small-group.jpg
:og:image: _static/conf/images/headers/{{shortcode}}-{{year}}-opengraph.png
:orphan:

.. title:: Home | Write the docs {{ name }} {{ year }}
```

### Standard Pages

```
conf/{shortcode}/{year}/
├── index.rst           # Homepage
├── cfp.rst            # Call for proposals
├── schedule.rst       # Conference schedule
├── speakers.rst       # Speaker list
├── tickets.rst        # Ticket information
├── sponsors/          # Sponsorship info
├── news/              # Conference announcements
├── venue.rst          # Venue details (if applicable)
└── team.rst           # Organizing team
```

### File Naming Conventions

**RST files**: lowercase-with-hyphens.rst
- `code-of-conduct.rst`
- `getting-started.rst`
- `contribution-guide.rst`

**YAML data files**: `{shortcode}-{year}-{type}.yaml`
- `berlin-2025-config.yaml`
- `portland-2025-sessions.yaml`
- `atlantic-2024-schedule.yaml`

**Schemas**: `schema-{type}.yaml`
- `schema-config.yaml`
- `schema-sessions.yaml`
- `schema-schedule.yaml`

## Python Code Standards

When writing custom Sphinx extensions or scripts:

**Style**:
- 4-space indentation (not tabs)
- snake_case for functions and variables
- Descriptive variable names
- Clear docstrings explaining purpose and return values

**No automated linters** configured (no black, flake8, pylint)

**Example from `docs/_ext/core.py`**:
```python
def load_conference_page_context(app, page):
    """
    Check whether this is a conference page, and if so, have the
    conference specific YAML data loaded.
    Conference data is cached, so only loaded once.

    Returns an empty dict if it isn't run on a proper conference page.
    """
    # Implementation...
```

**Security**:
- Use `yaml.safe_load()` not `yaml.load()`
- Explicitly specify UTF-8 encoding for file operations
- Handle exceptions with descriptive error messages

## Content Guidelines

From `docs/guide/contributing.rst`:

**1. Use friendly tone**
- Encourage contributors
- Be welcoming to all experience levels

**2. Attribute sources**
- Link to original sources
- Explain why links are useful
- Give credit where due

**3. Focus on principles**
- General best practices, not personal preferences
- Applicable across tools and contexts

**4. Avoid tool advocacy**
- Present use cases and results
- Let readers choose appropriate tools
- Document what works, not what you prefer

**5. General audience**
- Content should interest broad readership
- Not overly specific to niche use cases
- Explain technical concepts clearly

## AI-Friendly Documentation (2025 Best Practices)

From Write the Docs newsletter:

**1. Structured writing**
- Use clear headings and organization
- Consistent naming for features/processes
- Standard documentation patterns

**2. Clear language**
- Write in second person ("you" not "we" or "they")
- Simple, direct sentences
- Active voice preferred

**3. Enhanced FAQs**
- Add FAQ sections to pages
- Include extra detail and context
- Help both humans and AI find answers

**Writing well for humans makes documentation usable for everyone**, including AI systems.

## Screenshot Guidelines

When adding images to documentation:

**Technical requirements**:
- Capture from laptop/desktop (not mobile)
- Maximum width: 1000px
- Thin black border to distinguish from background
- Descriptive file names

**Content requirements**:
- Blur or anonymize real data
- Use believable but fictional data in examples
- Protect user privacy

**Accessibility**:
- Descriptive alt text (brief but accurate)
- Don't rely solely on images to convey information
- Supplement with text descriptions

## Additional Resources

- See `references/vale-rules.md` for complete Vale configuration
- See `references/yaml-schemas.md` for detailed schema requirements
- Contributing guide: https://www.writethedocs.org/guide/contributing/
- Style guide principles: https://www.writethedocs.org/guide/
