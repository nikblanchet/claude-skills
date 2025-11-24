---
name: rtd-docs-standards
description: Documentation writing standards for Read the Docs. Use when writing or editing ReStructuredText documentation files. Covers RST style guide, Diátaxis framework, Vale linting, brand guidelines, headline hierarchy, cross-references, and word list. Essential for documentation PRs.
---

# Read the Docs Documentation Standards

## Overview

This skill defines the documentation writing standards for Read the Docs. Follow these guidelines when creating or editing documentation to ensure consistency, quality, and successful Vale linting checks.

## Brand Guidelines

### Project Name

**Correct:** "Read the Docs" (three words, title case)
**Incorrect:** "Read The Docs", "ReadTheDocs", "RTD" (in prose)

**Acronym:** "RTD" is acceptable in technical contexts (URLs, code) but spell out "Read the Docs" in prose.

### Capitalization

Use **sentence case** for all headings and titles:
- **Correct:** "Install Read the Docs"
- **Incorrect:** "Install Read The Docs"

Only capitalize proper nouns and the first word.

## ReStructuredText Style

### Headline Hierarchy

Use this exact hierarchy for section headers:

```rst
Header Level 1
==============

Header Level 2
--------------

Header Level 3
~~~~~~~~~~~~~~

Header Level 4
^^^^^^^^^^^^^^
```

**Important:** The underline must be at least as long as the title text.

### Line Breaks

Break lines at **semantic boundaries** (periods, commas), not at arbitrary character counts (e.g., 80 chars).

**Good:**
```rst
This is a complete sentence that describes a concept.
It breaks at the period, maintaining readability.
```

**Bad:**
```rst
This is a complete sentence that describes a
concept. It breaks mid-sentence arbitrarily.
```

### Inline Markup

Use specific roles for different elements:

**Interactive elements:**
```rst
:menuselection:`File --> Save` - For menu navigation
:guilabel:`Save` - For buttons, labels, inputs
:kbd:`Ctrl+S` - For keyboard shortcuts
```

**Technical elements:**
```rst
:program:`git` - For program/command names
:command:`git commit` - For shell commands
:file:`.readthedocs.yaml` - For file paths
:code:`variable_name` - For inline code
```

**Bold text** (use `**text**`) for non-interactive visual elements that don't fit other roles.

### Code Blocks

Use code-block directive with language specification:

```rst
.. code-block:: python

   def hello_world():
       print("Hello, world!")

.. code-block:: yaml

   version: 2
   build:
     os: ubuntu-22.04

.. code-block:: bash

   git commit -m "Update documentation"
```

### Lists

**All bullet list items must end with periods:**

```rst
- This is a list item.
- This is another list item.
- Even single-line items need periods.
```

**Numbered lists:**

```rst
1. First step with period.
2. Second step with period.
3. Third step with period.
```

### Cross-References

**Link to other pages:**
```rst
:doc:`/path/to/document`
:doc:`Link text </path/to/document>`
```

**Link to sections:**
```rst
.. _section-label:

Section Title
-------------

Later reference it:
:ref:`section-label`
:ref:`Custom text <section-label>`
```

**External links:**
```rst
`Link text <https://example.com>`_
```

## Diátaxis Framework

All documentation must fit one of these four categories:

### 1. Tutorial
- **Purpose:** Learning-oriented, teaching
- **Content:** Step-by-step lessons for beginners
- **Tone:** Encouraging, patient
- **Example:** "Getting started with Read the Docs"

### 2. How-to Guide
- **Purpose:** Problem-oriented, practical
- **Content:** Steps to solve specific problems
- **Tone:** Direct, focused on goals
- **Example:** "How to configure custom domains"

### 3. Reference
- **Purpose:** Information-oriented, factual
- **Content:** Technical descriptions, API specs
- **Tone:** Dry, precise, comprehensive
- **Example:** "Configuration file reference"

### 4. Explanation
- **Purpose:** Understanding-oriented, conceptual
- **Content:** Background, context, alternatives
- **Tone:** Thoughtful, clarifying
- **Example:** "Understanding build environments"

**When writing, identify which category your content fits and follow that pattern.**

## Word List

Use these specific terms consistently:

### Version Control
- **Git** (uppercase) except when referencing the command: :program:\`git\`
- **Git repository** (not "VCS" or "repo" in prose)
- **Git provider** for GitHub/GitLab/Bitbucket/Gitea

### Configuration
- **`.readthedocs.yaml`** is the canonical config file name
- **Configuration file** (not "config file" in formal docs)

### Documentation Terms
- **how-to guide** (with hyphens, lowercase unless starting sentence)
- **documentation** (not "docs" in formal prose)

### Read the Docs Specific
- **Project** - A documentation project on Read the Docs
- **Version** - A specific version of documentation (e.g., "latest", "stable")
- **Build** - The process of building documentation

## Vale Linting

Read the Docs uses Vale for prose quality checking.

### Running Vale

```bash
# Check user documentation
vale docs/user/

# Check developer documentation
vale docs/dev/

# Check specific file
vale docs/user/config-file/v2.rst

# Via pre-commit
pre-commit run vale --all-files
```

### Common Vale Errors

**Passive voice:**
- **Bad:** "The configuration is read by Read the Docs"
- **Good:** "Read the Docs reads the configuration"

**Wordy phrases:**
- **Bad:** "In order to configure..."
- **Good:** "To configure..."

**Unclear antecedents:**
- **Bad:** "It will build the documentation"
- **Good:** "Read the Docs will build the documentation"

**Spelling and capitalization:**
- Vale checks against custom dictionary
- Follow brand guidelines strictly

## Building Documentation Locally

Before submitting documentation PRs:

```bash
# Build user docs
cd docs && make html
# Or: tox -e docs

# Build developer docs
cd docs && PROJECT=dev make html
# Or: tox -e docs-dev

# View output
open _build/html/index.html
```

### Common Build Errors

**Missing references:**
```rst
WARNING: undefined label: section-name
```
Fix: Check `:ref:` labels exist and are spelled correctly

**Missing files:**
```rst
WARNING: document isn't included in any toctree
```
Fix: Add document to a `.. toctree::` directive

## Documentation Structure

### Developer Documentation

Located in `docs/dev/`:
- `install.rst` - Installation and setup
- `contribute.rst` - Contribution guidelines
- `tests.rst` - Testing guide
- `style-guide.rst` - Documentation style (this skill's source)
- `design/` - Design decisions and architecture

### User Documentation

Located in `docs/user/`:
- `intro/` - Getting started guides (tutorials)
- `guides/` - How-to guides
- `reference/` - Configuration and API reference
- `explanation/` - Conceptual documentation

## Placeholders

Use angle brackets for abstract concepts and variables:

```rst
Replace <username> with your GitHub username.
Configure the <build.os> setting in your configuration file.
```

## Examples and Code Samples

**Provide context:**
```rst
Here's an example configuration file for a Python project using Sphinx:

.. code-block:: yaml

   version: 2
   build:
     os: ubuntu-22.04
     tools:
       python: "3.12"

   python:
     install:
       - requirements: docs/requirements.txt
```

**Explain what it does:**
```rst
This configuration:

- Uses Ubuntu 22.04 for builds.
- Installs Python 3.12.
- Installs dependencies from docs/requirements.txt.
```

## Common Patterns

### Documenting Commands

```rst
To check your configuration, run:

.. code-block:: bash

   readthedocs-build --config .readthedocs.yaml

This validates your configuration file without starting a build.
```

### Documenting Configuration Options

```rst
.. option:: build.os

   The operating system for the build environment.

   **Type:** String

   **Options:** ``ubuntu-20.04``, ``ubuntu-22.04``, ``ubuntu-24.04``

   **Default:** ``ubuntu-22.04``

   **Example:**

   .. code-block:: yaml

      build:
        os: ubuntu-22.04
```

### Warning and Note Boxes

```rst
.. note::

   This feature is only available for projects using configuration file v2.

.. warning::

   Changing this setting will trigger a rebuild of all versions.

.. tip::

   Use :menuselection:`Admin --> Advanced Settings` to configure this.
```

## Quality Checklist

Before submitting documentation PRs:

- [ ] Headlines use correct hierarchy (====, ----, ~~~~, ^^^^)
- [ ] Lines break at semantic boundaries
- [ ] All bullet points end with periods
- [ ] Interactive elements use :guilabel: and :menuselection:
- [ ] Code blocks specify language
- [ ] "Read the Docs" spelled correctly (not "Read The Docs")
- [ ] Sentence case for headings
- [ ] Cross-references use :doc: and :ref: correctly
- [ ] Vale linting passes: `vale docs/user/ docs/dev/`
- [ ] Documentation builds successfully: `cd docs && make html`
- [ ] Fits Diátaxis category (Tutorial, How-to, Reference, Explanation)

## Building and Testing

### Full Documentation Build

```bash
# From project root
cd docs

# Build user docs (default)
make html

# Build developer docs
PROJECT=dev make html

# Clean build (removes cached files)
make clean html
```

### Via Tox

```bash
# User docs
tox -e docs

# Developer docs
tox -e docs-dev
```

### Preview Build

After pushing to PR, Read the Docs automatically generates a preview build. Check the link in PR comments to verify rendering.

## Resources

This skill focuses on documentation standards. For code standards, use the `rtd-code-standards` skill. For Git workflow and PR process, use the `rtd-contribution-workflow` skill.

## References

- Official style guide: `docs/dev/style-guide.rst`
- Vale configuration: `common/vale.ini`
- Diátaxis framework: https://diataxis.fr/
- Sphinx ReStructuredText primer: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
