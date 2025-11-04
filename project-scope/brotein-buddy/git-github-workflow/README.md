# Git & GitHub Workflow Skill for BroteinBuddy

This skill defines the complete git and GitHub workflow for the BroteinBuddy project, including worktree management, branch naming conventions, commit standards, PR workflow, and merge strategy.

## Path Placeholders in Documentation

Throughout this skill's documentation, you'll see `<python-path>` used as a placeholder. This represents the path to your Python interpreter.

### Local Setup

My local environment uses:
- **Conda environments** for Python dependency management
- **pip** as a fallback for packages not available in conda
- Specific conda environment for BroteinBuddy: `bbud`

In my setup, `<python-path>` resolves to: `/Users/nik/miniconda3/envs/bbud/bin/python`

### Customizing for Your Environment

You have several options for using this skill with your own setup:

#### Option 1: Enhanced SessionStart Hook (Recommended for Seamless Operation)

The best approach is to enhance your Claude Code SessionStart hook to automatically detect project-specific Python paths. This provides zero-friction usage - skills just work without you thinking about placeholders.

**Setup Instructions:**

1. **Locate or create your SessionStart hook:**
   - Default location: `~/.claude/detect-python-env.sh` (or similar)
   - If you don't have one, create it and register it in `~/.claude/settings.json`

2. **Add project detection logic:**

```bash
#!/bin/bash
# Detect active Python environment and communicate it to Claude Code
# Enhanced with project-specific detection

# Get current working directory for project detection
CURRENT_DIR="$PWD"

# Default Python detection
PYTHON_PATH=$(which python || which python3)
# ... (your existing detection logic)

# Project-specific Python path detection
PROJECT_PYTHON_PATH=""
PROJECT_CONTEXT=""

# Check if we're in BroteinBuddy project
if [[ "$CURRENT_DIR" == *"BroteinBuddy"* ]]; then
    # BroteinBuddy uses the bbud conda environment
    BBUD_PYTHON="/path/to/your/conda/envs/bbud/bin/python"
    if [ -f "$BBUD_PYTHON" ]; then
        PROJECT_PYTHON_PATH="$BBUD_PYTHON"
        PROJECT_CONTEXT="BroteinBuddy"
        PLACEHOLDER_GUIDANCE="When you see <python-path> in skills, use: $BBUD_PYTHON"
    fi
fi

# Add to your hook output
if [ -n "$PROJECT_CONTEXT" ]; then
    echo "PROJECT-SPECIFIC CONTEXT DETECTED:"
    echo "- Project: $PROJECT_CONTEXT"
    echo "- Python for this project: $PROJECT_PYTHON_PATH"
    echo ""
    echo "$PLACEHOLDER_GUIDANCE"
fi
```

3. **Benefits:**
   - Completely automatic - skills work seamlessly
   - No manual path substitution needed
   - Project-aware - correct Python path for each project
   - Graceful fallback if hook isn't configured

**See also:** For a complete working example, check the enhanced hook at `~/.claude/detect-python-env.sh` in my setup.

#### Option 2: Manual .local/ Configuration (Fallback)

Create a `.local/` directory in your project root with environment-specific configuration:

```bash
# Create .local/ directory (gitignored)
mkdir .local

# Create env-config.md
cat > .local/env-config.md << 'EOF'
# Local Environment Configuration

## Python Paths
BBUD_PYTHON=/your/path/to/conda/envs/bbud/bin/python

## Usage
When you see <python-path> in skills, use: /your/path/to/conda/envs/bbud/bin/python
EOF
```

Add to `.gitignore`:
```
.local/
```

#### Option 3: Direct Substitution (Last Resort)

Simply replace `<python-path>` with your actual path wherever you see it in the documentation. This works but requires manual effort each time.

### Why Placeholders?

Using placeholders makes this skill:
- **Portable**: Can be shared across different machines and setups
- **Flexible**: Works with any Python environment (conda, virtualenv, system Python, etc.)
- **Privacy-preserving**: Doesn't expose local machine details in committed files

## Getting Started

See [SKILL.md](SKILL.md) for the complete workflow documentation.

## Resources

- `scripts/setup-worktree.py` - Interactive worktree creation script
- `references/code-reviewer-guide.md` - How to invoke the code-reviewer agent
- `references/teacher-mentor-guide.md` - How to invoke the teacher-mentor agent
- `references/skill-dependencies.md` - When to invoke related skills
- `references/ci-cd-monitoring.md` - Monitoring GitHub Actions checks
