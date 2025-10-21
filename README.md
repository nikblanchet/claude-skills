# Custom Claude Skills

Personal collection of Claude Code skills organized by scope.

## Structure

- `global-scope/` - Skills that apply to all projects
- `project-scope/` - Project-specific skills (organization TBD)
- `archive/` - Deprecated or replaced skills (kept for reference)

### Project-Scope Organization (TBD)

We haven't decided on the organization for project-specific skills yet. Two options:

**Option A: Flat structure** (e.g., `project-scope/docimp-parser-workflow/`)
- **Advantage:** Same skill can be used across multiple projects without duplication
- **Disadvantage:** Cannot have skills with the same name for different projects

**Option B: Nested by project** (e.g., `project-scope/docimp/parser-workflow/`)
- **Advantage:** Allows skills with the same name in different projects
- **Disadvantage:** Requires copying/symlinking to share skills across projects

Decision deferred until we have actual project-specific skills to organize.

## Active Skills

Active skills are symlinked to `~/.claude/skills/` from this repository.

### Global Skills (8)

1. **development-standards** - No emoji, modern language features, thorough documentation
2. **git-workflow** - Commit and branching workflow
3. **github-workflow** - Issue management and PR workflow with gh CLI
4. **github-code-reviews** - Comprehensive code review process (11 dimensions)
5. **exhaustive-testing** - Testing philosophy and practices
6. **handle-deprecation-warnings** - Address deprecation warnings proactively
7. **dependency-management** - Using dependencies freely (conda/pip workflow)
8. **cli-ux-colorful** - Colorful CLI output design

### Archived Skills (7)

Merged into consolidated skills, kept for reference:
- no-emoji-for-developers → merged into development-standards
- modern-language-versions → merged into development-standards
- thorough-documentation → merged into development-standards
- git-commit-workflow → merged into git-workflow
- git-feature-branch-workflow → merged into git-workflow
- github-issue-management → merged into github-workflow
- github-pull-requests → merged into github-workflow

## Usage

To activate a skill, create a symlink:
```bash
ln -s ~/Code/repos/custom-claude-skills/global-scope/skill-name ~/.claude/skills/skill-name
```

To deactivate a skill, remove the symlink:
```bash
rm ~/.claude/skills/skill-name
```
