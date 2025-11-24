---
name: rtd-code-standards
description: Code quality and style standards for Read the Docs contributions. Use when writing Python code, creating tests, or preparing code changes for PR submission. Covers Ruff configuration, testing requirements, pre-commit hooks, import sorting, and migration checks.
---

# Read the Docs Code Standards

## Overview

This skill defines the code quality and style standards for contributing Python code to Read the Docs. Follow these standards to ensure code changes pass CI checks and meet project quality expectations.

## Python Style Standards

### Code Formatting

Read the Docs uses **Ruff** for both linting and formatting.

**Key rules:**
- Line length: **100 characters maximum**
- Indentation: **4 spaces** (no tabs)
- Python version target: **Python 3.12**
- Quote style: Double quotes preferred

**Configuration location:** `common/.ruff.toml` (symlinked from common submodule)

### Import Sorting

Imports must be sorted using Ruff's isort functionality:

**Rules:**
- **Single-line imports** (not multi-line from imports)
- **Case-insensitive** alphabetical sorting
- **Grouping order:**
  1. Standard library
  2. Third-party packages
  3. First-party (readthedocs, readthedocsext, readthedocscinc)
  4. Local/relative imports

**Example:**
```python
import os
import sys
from pathlib import Path

from django.conf import settings
from django.db import models
import requests

from readthedocs.builds.models import Build
from readthedocs.core.utils import trigger_build
from readthedocsext.theme import apply_theme

from .utils import helper_function
```

### Running Code Formatters

```bash
# Run all pre-commit hooks (includes Ruff)
pre-commit run --all-files

# Via tox
tox -e pre-commit

# Ruff directly (if needed)
ruff check .
ruff format .
```

## Testing Requirements

### Test Organization

Tests are **co-located** with code in each Django app:

```
readthedocs/
├── projects/
│   ├── models.py
│   ├── views.py
│   └── tests/
│       ├── test_models.py
│       ├── test_views.py
│       └── test_api.py
├── builds/
│   └── tests/
└── rtd_tests/  # Shared test utilities
    ├── base.py
    ├── fixtures/
    ├── mocks/
    └── utils.py
```

### Pytest Markers

Use markers to categorize tests by instance type:

```python
import pytest

# No marker = main instance test (default)
def test_project_creation():
    pass

# Proxito instance test
@pytest.mark.proxito
def test_doc_serving():
    pass

# Requires Elasticsearch
@pytest.mark.search
def test_search_indexing():
    pass

# Embed API test
@pytest.mark.embed_api
def test_embed_endpoint():
    pass
```

### Writing Tests

**Requirements:**
- Every new function/class needs tests
- Test both happy path and error cases
- Use fixtures from `readthedocs/rtd_tests/`
- Mock external dependencies
- Follow existing patterns in the app

**Example test structure:**
```python
from django.test import TestCase
from readthedocs.projects.models import Project
from readthedocs.rtd_tests.base import RequestFactoryTestMixin

class ProjectModelTest(RequestFactoryTestMixin, TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="test-project",
            slug="test-project"
        )

    def test_project_creation(self):
        """Test that projects are created correctly."""
        self.assertEqual(self.project.name, "test-project")
        self.assertEqual(self.project.slug, "test-project")

    def test_project_str_representation(self):
        """Test string representation."""
        self.assertEqual(str(self.project), "test-project")
```

### Running Tests

```bash
# Run all tests
tox

# Run specific test environment
tox -e py312

# Run specific test file
tox -e py312 -- readthedocs/projects/tests/test_models.py

# Run specific test function
tox -e py312 -- -k test_project_creation

# Run tests excluding search (don't need Elasticsearch)
tox -e py312 -- -m "not search"

# Inside Docker
inv docker.test
inv docker.test --arguments "-e py312 -- -k test_name"
```

### Test Coverage

- All code changes should maintain or improve coverage
- Coverage reports generated in CI via Codecov
- Check coverage locally: `tox -e coverage`

## Pre-Commit Hooks

Read the Docs uses pre-commit hooks for automated quality checks.

### Hooks Enabled

From `common/pre-commit-config.yaml`:

1. **Ruff** (v0.11.5)
   - Linting and formatting
   - Import sorting
   - Auto-fixes applied

2. **django-upgrade** (1.24.0)
   - Modernizes Django patterns
   - Target: Django 5.2

3. **blacken-docs** (1.19.1)
   - Formats code blocks in documentation

4. **Standard hooks**
   - Trailing whitespace removal
   - End-of-file fixer
   - YAML/JSON syntax validation
   - Merge conflict detection

### Running Pre-Commit

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run all hooks on staged files only
pre-commit run

# Run specific hook
pre-commit run ruff --all-files

# Via tox
tox -e pre-commit
```

**Before every PR:**
```bash
# REQUIRED: Run this before submitting PR
tox -e pre-commit
```

## Database Migrations

### Migration Requirements

If code changes modify Django models, migrations are **required**.

### Checking for Missing Migrations

```bash
# Via tox (what CI runs)
tox -e migrations

# Via invoke (inside Docker)
inv docker.manage makemigrations --check --dry-run

# Direct Django command
python manage.py makemigrations --check --dry-run
```

### Creating Migrations

```bash
# Inside Docker
inv docker.manage makemigrations

# With specific app
inv docker.manage makemigrations projects

# Outside Docker
python manage.py makemigrations
```

### Migration Best Practices

- Review generated migrations before committing
- Name migrations descriptively if needed
- Test migrations can be applied and reversed
- Include migrations in same commit as model changes
- Document complex data migrations

## Code Quality Checklist

Before submitting a PR, verify:

### 1. Formatting and Linting
```bash
✓ pre-commit run --all-files
```

### 2. Tests
```bash
✓ tox -e py312
# All tests pass
# New tests added for new code
```

### 3. Migrations
```bash
✓ tox -e migrations
# No missing migrations
```

### 4. Test Coverage
```bash
✓ tox -e coverage
# Coverage maintained or improved
```

### 5. Code Review Ready
- [ ] Code follows Python 3.12 patterns
- [ ] Imports properly sorted
- [ ] Tests co-located with code
- [ ] Docstrings on public functions/classes
- [ ] No commented-out code
- [ ] No debug print statements
- [ ] No unnecessary complexity

## Common Patterns

### Django Model Patterns

```python
from django.db import models

class MyModel(models.Model):
    """Model docstring explaining purpose."""

    # Fields with help_text
    name = models.CharField(
        max_length=255,
        help_text="Human-readable name"
    )

    class Meta:
        ordering = ["-created"]
        verbose_name_plural = "my models"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Custom save logic
        super().save(*args, **kwargs)
```

### View Patterns

```python
from django.views.generic import DetailView
from .models import Project

class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/project_detail.html"

    def get_queryset(self):
        # Custom queryset logic
        return super().get_queryset().filter(active=True)
```

### Test Fixture Usage

```python
from readthedocs.rtd_tests.fixtures import get_factory

def test_with_fixture():
    # Use fixture factories
    project = get_factory("Project").create(name="test")
    build = get_factory("Build").create(project=project)
```

## Django-Specific Standards

### Settings Configuration

- Use class-based settings (inherit from `CommunityBaseSettings`)
- Override with `@property` decorator for dynamic values
- Never hardcode secrets
- Use environment variables for configuration

### Database Queries

- Use `select_related()` and `prefetch_related()` to avoid N+1 queries
- Index frequently queried fields
- Be mindful of query performance

### Celery Tasks

- Use `@app.task` decorator
- Make tasks idempotent
- Handle failures gracefully
- Log task execution

## Resources

This skill focuses on code standards. For documentation standards, use the `rtd-docs-standards` skill. For Git workflow and PR process, use the `rtd-contribution-workflow` skill.

## CI/CD Integration

CircleCI runs these checks on every PR:

**checks job:**
- `pre-commit run --all-files`
- `tox -e migrations`

**tests job:**
- `tox -e py312`
- Coverage report to Codecov

All must pass before merge.
