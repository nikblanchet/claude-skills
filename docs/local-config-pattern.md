# Local Configuration Pattern

This document explains the `.local/` directory pattern used in this repository for machine-specific configuration.

## Overview

To maintain portability while supporting local customization, this repository uses:
1. **Placeholders** in committed files (e.g., `<python-path>`, `<project-root>`)
2. **SessionStart Hook** for automatic detection (recommended)
3. **`.local/` directory** for manual overrides (gitignored, fallback)

## Why This Pattern?

**The Problem:**
- Skills need machine-specific paths (e.g., conda environment paths)
- Hardcoding paths makes repository non-portable and exposes local machine details
- Generic placeholders alone reduce automation and require manual substitution

**The Solution:**
- Committed files use placeholders
- SessionStart hook auto-detects project context and provides actual paths
- `.local/` directory provides manual fallback when hook detection isn't available

## Using .local/ Directory

### When to Use

Use the `.local/` directory when:
- Your SessionStart hook doesn't support project-specific detection
- You need to override auto-detected values
- You're working in a non-standard location
- You want explicit control over environment configuration

### Structure

```
project-root/
├── .local/                  # Gitignored directory
│   ├── README.md           # This file (not committed, template provided)
│   └── env-config.md       # Your local environment paths
├── .gitignore              # Includes .local/
└── ... (rest of project)
```

### Setup Instructions

1. **Create .local/ directory:**
```bash
mkdir .local
```

2. **Create env-config.md:**
```bash
cat > .local/env-config.md << 'EOF'
# Local Environment Configuration

## Python Paths

### BroteinBuddy
BBUD_PYTHON=/Users/nik/miniconda3/envs/bbud/bin/python

### DocImp
DOCIMP_PYTHON=/Users/nik/miniconda3/bin/python

## Project Roots

BROTEIN_BUDDY_ROOT=~/Documents/Code/BroteinBuddy
DOCIMP_ROOT=~/Documents/Code/Polygot/docimp

## Usage

When skills reference:
- `<python-path>` in BroteinBuddy → use BBUD_PYTHON value
- `<python-path>` in DocImp → use DOCIMP_PYTHON value
- `<project-root>` in DocImp → use DOCIMP_ROOT value
EOF
```

3. **Verify .gitignore includes .local/:**
The repository `.gitignore` should already include `.local/`, but verify:
```bash
grep -q "^\.local/" .gitignore || echo ".local/" >> .gitignore
```

### Using Local Config

When Claude Code reads a skill that references `<python-path>`, you can tell it:
> "Check `.local/env-config.md` for the local Python path"

Claude will read the file and use your configured value.

## Recommended: SessionStart Hook

While `.local/` works as a fallback, the **recommended approach** is to use an enhanced SessionStart hook that automatically detects project context.

### Advantages of SessionStart Hook over .local/

| Feature | SessionStart Hook | .local/ Directory |
|---------|-------------------|-------------------|
| Automatic | Yes - zero manual intervention | No - must reference manually |
| Project-aware | Yes - detects based on PWD | No - static configuration |
| Seamless integration | Yes - always available | Requires explicit reference |
| Setup complexity | One-time hook enhancement | Per-project directory setup |
| Use case | Primary solution (95% of cases) | Fallback/override (5% of cases) |

### Hook Setup

See `project-scope/brotein-buddy/git-github-workflow/README.md` for complete SessionStart hook setup instructions with example code.

## Best Practice: Hybrid Approach

**Use both:**
1. **Primary:** Enhanced SessionStart hook for automatic operation
2. **Fallback:** `.local/` directory for edge cases and overrides

This provides the best of both worlds:
- Automatic convenience most of the time
- Manual control when needed
- Graceful degradation if hook isn't configured

## Example: Working with BroteinBuddy

### With SessionStart Hook (Automatic):
```bash
cd ~/Documents/Code/BroteinBuddy/wt/main
claude

# Hook automatically detects:
# - Project: BroteinBuddy
# - Python: /Users/nik/miniconda3/envs/bbud/bin/python
# Skills using <python-path> just work!
```

### With .local/ Directory (Manual):
```bash
cd ~/Documents/Code/BroteinBuddy/wt/main
claude

# When skill says: "<python-path> .claude/skills/git-github-workflow/scripts/setup-worktree.py"
# You tell Claude: "Check .local/env-config.md for python-path"
# Claude reads BBUD_PYTHON and uses the correct path
```

## Summary

- **Committed files**: Use placeholders (portable, shareable)
- **SessionStart hook**: Auto-detect and provide actual paths (seamless, automatic)
- **`.local/` directory**: Manual overrides and fallback (explicit control)
- **Best practice**: Use hook as primary, `.local/` as fallback
