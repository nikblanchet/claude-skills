#!/bin/bash
# Create a new git worktree for the docimp project with all necessary symlinks
#
# Usage: create-worktree.sh <worktree-name> <branch-name>
# Example: create-worktree.sh issue-221 issue-221-improve-styleguides

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check arguments
if [ $# -lt 2 ]; then
    echo -e "${RED}Error: Missing required arguments${NC}"
    echo ""
    echo "Usage: $0 <worktree-name> <branch-name>"
    echo ""
    echo "Arguments:"
    echo "  worktree-name   Name of the worktree directory (e.g., issue-221)"
    echo "  branch-name     Name of the git branch (e.g., issue-221-improve-styleguides)"
    echo ""
    echo "Example:"
    echo "  $0 issue-221 issue-221-improve-styleguides"
    exit 1
fi

WORKTREE_NAME="$1"
BRANCH_NAME="$2"

# Validate we're in the docimp main repo
if [ ! -d ".git" ]; then
    echo -e "${RED}Error: Not in a git repository${NC}"
    echo "Please run this script from the docimp main repository directory"
    exit 1
fi

# Check if we're in the right repo (look for package.json or some docimp-specific file)
if [ ! -f "cli/package.json" ] && [ ! -f "analyzer/setup.py" ]; then
    echo -e "${YELLOW}Warning: This doesn't appear to be the docimp repository${NC}"
    echo "Are you in the correct directory?"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Ensure we're on main and up to date
echo -e "${BLUE}Ensuring main branch is up to date...${NC}"
git checkout main
git pull

# Create worktrees directory if it doesn't exist
WORKTREE_DIR="../.docimp-wt"
if [ ! -d "$WORKTREE_DIR" ]; then
    echo -e "${BLUE}Creating worktrees directory: $WORKTREE_DIR${NC}"
    mkdir -p "$WORKTREE_DIR"
fi

# Check if worktree already exists
WORKTREE_PATH="$WORKTREE_DIR/$WORKTREE_NAME"
if [ -d "$WORKTREE_PATH" ]; then
    echo -e "${RED}Error: Worktree already exists at $WORKTREE_PATH${NC}"
    exit 1
fi

# Check if branch already exists
if git show-ref --verify --quiet refs/heads/"$BRANCH_NAME"; then
    echo -e "${RED}Error: Branch '$BRANCH_NAME' already exists${NC}"
    echo "Use a different branch name or delete the existing branch first"
    exit 1
fi

# Create the worktree
echo -e "${BLUE}Creating worktree: $WORKTREE_PATH${NC}"
git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME"

# Change to worktree directory
cd "$WORKTREE_PATH"

echo -e "${BLUE}Creating symlinks to shared files...${NC}"

# Create symlinks for files in project root
ln -s ../../.docimp-shared/CLAUDE.md CLAUDE.md
echo -e "${GREEN}✓${NC} Created symlink: CLAUDE.md"

ln -s ../../.docimp-shared/CLAUDE_CONTEXT.md CLAUDE_CONTEXT.md
echo -e "${GREEN}✓${NC} Created symlink: CLAUDE_CONTEXT.md"

ln -s ../../.docimp-shared/.planning .planning
echo -e "${GREEN}✓${NC} Created symlink: .planning"

ln -s ../../.docimp-shared/.scratch .scratch
echo -e "${GREEN}✓${NC} Created symlink: .scratch"

# Create docs directory and symlink to patterns
mkdir -p docs
ln -s ../../../.docimp-shared/docs/patterns docs/patterns
echo -e "${GREEN}✓${NC} Created symlink: docs/patterns"

# Create .claude directory and symlinks
mkdir -p .claude
ln -s ../../../.docimp-shared/.claude/skills .claude/skills
echo -e "${GREEN}✓${NC} Created symlink: .claude/skills"

ln -s ../../../.docimp-shared/.claude/settings.local.json .claude/settings.local.json
echo -e "${GREEN}✓${NC} Created symlink: .claude/settings.local.json"

# Return to main repo
cd - > /dev/null

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ Worktree created successfully!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}Worktree details:${NC}"
echo "  Location: $WORKTREE_PATH"
echo "  Branch:   $BRANCH_NAME"
echo ""
echo -e "${BLUE}All symlinks created:${NC}"
echo "  ✓ CLAUDE.md → ../../.docimp-shared/CLAUDE.md"
echo "  ✓ CLAUDE_CONTEXT.md → ../../.docimp-shared/CLAUDE_CONTEXT.md"
echo "  ✓ .planning → ../../.docimp-shared/.planning"
echo "  ✓ .scratch → ../../.docimp-shared/.scratch"
echo "  ✓ docs/patterns → ../../../.docimp-shared/docs/patterns"
echo "  ✓ .claude/skills → ../../../.docimp-shared/.claude/skills"
echo "  ✓ .claude/settings.local.json → ../../../.docimp-shared/.claude/settings.local.json"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "  cd $WORKTREE_PATH"
echo "  # Open in Claude Code or your editor"
echo ""
echo -e "${BLUE}To view all worktrees:${NC}"
echo "  git worktree list"
echo ""
