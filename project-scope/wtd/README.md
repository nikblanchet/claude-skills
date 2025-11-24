# Write the Docs Skills

This directory contains Claude Code skills specific to the Write the Docs project.

## Project Overview

Write the Docs (https://github.com/writethedocs/www) is the official website for the Write the Docs global community, serving documentarians, technical writers, and documentation enthusiasts worldwide. The site features conference information, documentation guides, blog posts, and video archives.

## Technology Stack

- Sphinx 5.3.0 (static site generator)
- Python 3.9.21
- reStructuredText and Markdown (via MyST parser)
- Jinja2 templating throughout
- YAML-driven conference data
- Deployed on Read the Docs

## Development Approach

- Jinja preprocessing on all RST files before Sphinx rendering
- Data-driven conference pages with YAML schemas
- Video archive system generating pages from YAML
- Vale prose linting for content quality
- HTML proofer for link validation
- Fork-based contribution workflow
- Comprehensive CI/CD with 6 automated checks

## Skills in This Directory

- **writethedocs-conference-workflow** - Complete workflow for creating and managing conference websites
- **writethedocs-documentation-standards** - RST/Markdown standards, Vale rules, YAML schema management
- **writethedocs-git-workflow** - Git workflow, PR process, and CI/CD checks

## Key Characteristics

- Conference data lives in structured YAML files with strict schemas
- ALL RST files are Jinja-preprocessed with automatic context injection
- Video builds are opt-in (slow) and filtered by year
- Multi-timezone schedule support with DST awareness
- Custom Sphinx extensions for video archives, meetups, and datatemplates
- Legacy vs modern data formats (pre-2020 vs 2020+)
- Strong emphasis on content quality (Vale, spellcheck, YAML validation)
- Photo management with automatic fallbacks for missing images
