---
name: access-skill-resources
description: Locate scripts, references, and assets bundled with skills. Use when a skill mentions bundled resources (scripts/, references/, assets/ subdirectories) but you cannot immediately find them. Teaches standard skill directory structure and symlink navigation.
---

# Accessing Skill Bundled Resources

## Overview

Skills can include bundled resources beyond the main SKILL.md file. These resources live in standard subdirectories within the skill's directory:

- `scripts/` - Executable code (Python, Bash, etc.)
- `references/` - Documentation and guides to load as needed
- `assets/` - Templates, boilerplate, or files used in output

Skills may be accessed through symlinks. This skill teaches how to follow symlinks and reliably locate bundled resources in any skill.

## Standard Skill Directory Structure

Every skill with bundled resources follows this standard structure:

```
{skill-name}/
├── SKILL.md                    # Main skill file (always present)
├── scripts/                    # Executable code (optional)
│   ├── script1.py
│   ├── script2.sh
│   └── helper.py
├── references/                 # Documentation to load as needed (optional)
│   ├── detailed-guide.md
│   ├── api-reference.md
│   └── workflow.md
└── assets/                     # Templates and output files (optional)
    ├── template.txt
    ├── config-example.json
    └── boilerplate/
        └── starter-files...
```

Once the skill's main directory is located, all bundled resources are accessible in these standard subdirectories.

## Skill Storage Locations

### User Skills

User skills are stored in the standard Claude Code user skills directory:

```
~/.claude/skills/{skill-name}/
```

This path may be:
- A regular directory containing SKILL.md and subdirectories
- A symlink pointing to the actual skill location

### Project Skills

Project skills are stored in the project's Claude configuration directory:

```
{project-root}/.claude/skills/{skill-name}/
```

In many project setups:
- `.claude/skills/` itself may be a symlink to a shared skills directory
- Individual skill directories may also be symlinks
- Multiple levels of symlinks may exist

## Directory Structure Example

For a project like BroteinBuddy:

```
BroteinBuddy/
├── wt/
│   └── main/                          # Main worktree (project root)
│       └── .claude/
│           └── skills/                # Symlink to shared skills
│               ├── git-github-workflow/  # May also be symlink
│               │   ├── SKILL.md
│               │   ├── scripts/
│               │   │   └── setup-worktree.py
│               │   └── references/
│               │       └── code-reviewer-guide.md
│               └── brotein-buddy-standards/
│                   └── SKILL.md
```

## Locating Bundled Resources: Step-by-Step

Follow these steps to reliably locate and access bundled resources:

### Step 1: Identify Skill Type and Starting Location

**User skill:**
- Start at: `~/.claude/skills/{skill-name}/`

**Project skill:**
- Start at: `{project-root}/.claude/skills/{skill-name}/`
- Navigate from current working directory to project root, then to `.claude/skills/{skill-name}/`

### Step 2: Follow Symlinks if Present

Symlinks may exist at multiple levels. Use these approaches:

**Option A: Let tools follow symlinks automatically**
- The Read tool automatically follows symlinks
- Simply use the standard path, symlinks will be resolved transparently
- Example: `Read .claude/skills/git-github-workflow/scripts/setup-worktree.py`

**Option B: Manually check symlink destination**
- Use `readlink -f {path}` to resolve full path including all symlinks
- Use `stat {path}` to check if path is a symlink
- Example:
  ```bash
  readlink -f ~/.claude/skills/my-skill
  ```

### Step 3: Verify Skill Directory Contents

Before accessing bundled resources, verify the skill directory structure:

```bash
ls -la {skill-path}/
```

Look for:
- SKILL.md (always present)
- scripts/ directory (if skill mentions scripts)
- references/ directory (if skill mentions references)
- assets/ directory (if skill mentions assets)

### Step 4: Access Bundled Resources

Once the skill directory is located (whether through symlinks or direct paths), access resources using standard subdirectory paths:

**Scripts:**
```
{skill-directory}/scripts/{script-name}.py
{skill-directory}/scripts/{script-name}.sh
```

**References:**
```
{skill-directory}/references/{doc-name}.md
{skill-directory}/references/{guide-name}.md
```

**Assets:**
```
{skill-directory}/assets/{file-name}
{skill-directory}/assets/{subdirectory}/
```

### Step 5: Verify Before Use

Always verify a file exists before attempting to execute or use it:

```
Read {skill-directory}/scripts/{script-name}.py
```

If the Read succeeds, the file exists and can be used. If it fails, check for:
- Typos in filename
- Wrong subdirectory
- Resource may not exist for this skill

## Practical Examples

### Example 1: Accessing User Skill Script

**Scenario:** The `dependency-management` skill mentions a script `check-deps.py`.

**Steps:**
1. Start at: `~/.claude/skills/dependency-management/`
2. Access script: `~/.claude/skills/dependency-management/scripts/check-deps.py`
3. Verify: `Read ~/.claude/skills/dependency-management/scripts/check-deps.py`
4. If successful, use the file

**If symlink:**
```bash
readlink -f ~/.claude/skills/dependency-management
# Result: /actual/location/dependency-management/
# Script is at: /actual/location/dependency-management/scripts/check-deps.py
# But ~/.claude/skills/dependency-management/scripts/check-deps.py also works
```

### Example 2: Accessing Project Skill Reference

**Scenario:** The `git-github-workflow` project skill references `code-reviewer-guide.md` in its `references/` directory.

**Steps:**
1. From project root, start at: `.claude/skills/git-github-workflow/`
2. Access reference: `.claude/skills/git-github-workflow/references/code-reviewer-guide.md`
3. Verify: `Read .claude/skills/git-github-workflow/references/code-reviewer-guide.md`
4. If successful, load the content

### Example 3: Multiple Symlink Levels

**Scenario:** Project has `.claude/skills/` as symlink, and individual skills are also symlinks.

**Symlink structure:**
```
project/.claude/skills/ -> /shared/location/skills/
/shared/location/skills/my-skill/ -> /storage/my-skill/
```

**Access:**
```
# Use the logical path (Claude follows symlinks)
Read project/.claude/skills/my-skill/scripts/tool.py

# Or resolve manually if needed
readlink -f project/.claude/skills/my-skill
# Result: /storage/my-skill/
# Access: Read /storage/my-skill/scripts/tool.py
```

## Troubleshooting

### Symlink Not Found

**Problem:** `~/.claude/skills/{skill-name}/` or `.claude/skills/{skill-name}/` does not exist.

**Solution:**
- Skill may not be installed
- Check parent directory: `ls ~/.claude/skills/` or `ls .claude/skills/`
- Verify skill name spelling
- User skills: Check if symlink was created in `~/.claude/skills/`
- Project skills: Check if `.claude/` directory exists in project root

### Subdirectory Missing

**Problem:** Skill directory exists but `scripts/`, `references/`, or `assets/` subdirectory is missing.

**Solution:**
- Not all skills have all subdirectories
- Check skill's SKILL.md for what resources it includes
- Verify you're in the correct skill directory: `ls -la {skill-directory}/`

### Permission Errors

**Problem:** Cannot read files even though path is correct.

**Solution:**
- Check file permissions: `ls -la {file-path}`
- Check permissions at symlink destination: `stat {path}`
- Ensure you have read access to all directories in the path

### Read Tool Fails

**Problem:** Read tool returns error when accessing bundled resource.

**Solution:**
- Verify path is correct: `ls {file-path}`
- Check for typos in filename
- Verify parent directories exist
- Try resolving symlinks manually: `readlink -f {path}`
- Use Bash to test: `cat {file-path}` (if error persists, file truly doesn't exist)

### Finding Skill Location (Last Resort)

**Problem:** Cannot determine where skill is located.

**Solution:**

Use Glob to search for the skill:
```bash
find ~ -type d -name "{skill-name}" 2>/dev/null | grep -E "(\.claude/skills|custom-claude-skills)"
```

This will show all locations where the skill directory exists. Look for paths containing:
- `.claude/skills/` (user or project skills)
- `custom-claude-skills/` (source location)

## Key Principles

1. **Standard structure:** All skills with bundled resources use `scripts/`, `references/`, `assets/` subdirectories
2. **Symlinks are transparent:** Use standard paths; tools like Read follow symlinks automatically
3. **Verify before use:** Always verify files exist with Read tool before attempting to execute or use them
4. **Start from standard locations:** User skills at `~/.claude/skills/`, project skills at `.claude/skills/`
5. **When in doubt:** List directory contents to see what's actually present

## When Not to Use This Skill

This skill is specifically for locating bundled resources (scripts, references, assets) within skill directories. Do not use this skill for:

- Finding project source code (use Glob or Grep)
- Locating configuration files outside of `.claude/` (use project-specific documentation)
- Searching for files in general (use Glob or Grep tools)
- Understanding what a skill does (read the skill's SKILL.md instead)
