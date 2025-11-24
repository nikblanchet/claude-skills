# Read the Docs Skills

This directory contains Claude Code skills specific to the Read the Docs project.

## Project Overview

Read the Docs (https://github.com/readthedocs/readthedocs.org) is an open-source platform for hosting and building documentation. The project is a Django monolith with a multi-instance architecture where the same codebase is deployed as three separate instances:

- **Web** - Dashboard, user interface, and API
- **Build** - Executes documentation builds in isolated Docker containers
- **Proxito** - Serves documentation pages to end users

All development is done via Docker Compose with PostgreSQL, Redis, Elasticsearch, MinIO (S3-compatible storage), and nginx for routing.

## Technology Stack

- Django (Python web framework)
- Docker and Docker Compose
- PostgreSQL (database)
- Redis (caching and task queue)
- Elasticsearch (search functionality)
- Celery (async task processing)
- Sphinx and MkDocs (documentation builders)

## Development Approach

- Docker-first development environment
- Pytest with instance-specific test markers
- Pre-commit hooks for code quality
- Fork-based contribution workflow
- Class-based settings inheritance
- Custom database routing for telemetry
- Git submodule for shared configuration (common/)

## Skills in This Directory

- **rtd-code-standards** - Code quality and style standards for Python contributions
- **rtd-contribution-workflow** - Fork-based Git and PR workflow for contributing
- **rtd-docs-standards** - ReStructuredText documentation standards

## Key Characteristics

- Multi-instance Django architecture (web, build, proxito)
- Isolated Docker-based documentation builds with gVisor sandboxing
- Test suite separated by instance type using pytest markers
- Settings organized using class-based inheritance
- Development requires invoke tasks for common operations
- Strong emphasis on code quality (Ruff, pre-commit, tox)
