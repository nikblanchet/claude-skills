---
name: brotein-buddy-standards
description: BroteinBuddy project-specific development standards including testing requirements (90% coverage, 100% critical paths), code quality tooling (ESLint, Prettier, Husky), documentation structure (README, DEVELOPING, ADRs, teaching docs), and tech stack conventions. Use when working on BroteinBuddy to ensure consistency with project standards.
---

# BroteinBuddy Development Standards

Project-specific standards for BroteinBuddy. These complement the global `development-standards` skill (no emoji, modern features, thorough docs) and the `git-github-workflow` skill (git/GitHub operations).

## Testing Requirements

### Coverage Targets

**Overall Coverage: 90%**
- Enforced by CI/CD pipeline
- Measured using Vitest with coverage-v8

**Critical Paths: 100% Coverage**

Critical paths requiring 100% coverage:
- Random selection algorithm (`src/lib/random-selection.ts`)
- Box priority sorting (`src/lib/box-selection.ts`)
- Inventory state mutations (`src/lib/stores.ts`)
- LocalStorage operations (`src/lib/storage.ts`)

### Test Types

**Unit Tests** (`tests/unit/`):
- Test individual functions and components in isolation
- Mock external dependencies
- Fast execution
- Run with: `npm run test:unit`

**Integration Tests** (`tests/integration/`):
- Test component interactions
- Test state management integration
- Test LocalStorage integration
- Run with: `npm run test:integration`
- Note: Currently disabled due to @testing-library/svelte v5 compatibility with Svelte 5 runes. See issue #3.

**End-to-End Tests** (`tests/e2e/`):
- Test complete user workflows using Playwright
- Test in real browser environment
- Run with: `npm run test:e2e`
- UI mode: `npm run test:e2e:ui`

### Before Creating PRs

All of these must pass:
```bash
npm test              # All unit tests pass
npm run test:coverage # Coverage thresholds met
npm run test:e2e      # E2E tests pass
npm run lint          # No linting errors
npm run check         # TypeScript checks pass
npm run build         # Production build succeeds
```

## Code Quality Tools

### ESLint Configuration

**Plugins:**
- `@typescript-eslint/eslint-plugin` - TypeScript linting
- `eslint-plugin-svelte` - Svelte-specific rules
- `eslint-config-prettier` - Prevents conflicts with Prettier

**Running ESLint:**
```bash
npm run lint          # Check for issues
npm run lint:fix      # Auto-fix issues
```

### Prettier Configuration

**Plugins:**
- `prettier-plugin-svelte` - Format Svelte files

**Running Prettier:**
```bash
npm run format        # Format all files
npm run format:check  # Check formatting without changes
```

### Pre-commit Hooks (Husky + lint-staged)

**Automatically runs on git commit:**
- ESLint with auto-fix on `.js`, `.ts`, `.svelte` files
- Prettier formatting on all supported files
- Prevents commits with linting errors

**Configuration:** See `lint-staged` section in `package.json`

### TypeScript Strict Mode

**Enabled** - See `tsconfig.json` and `tsconfig.app.json`
- Strict null checks
- Strict property initialization
- No implicit any
- All strict flags enabled

## Documentation Structure

### File Types

**README.md** (User-facing):
- What the app does
- How to install and use
- Screenshots and demo
- No technical implementation details
- Target audience: End users

**DEVELOPING.md** (Developer-facing):
- Setup instructions
- Development workflow
- Architecture overview
- Testing strategy
- Deployment process
- Target audience: Contributors and maintainers

**CONTRIBUTING.md** (Process documentation):
- Git worktree workflow
- Code review structure
- PR requirements
- Development methodology
- Target audience: Contributors

### Architecture Decision Records (ADRs)

**Location:** `docs/adr/`

**Template:** `docs/adr/000-template.md`

**Format:**
- Title: `NNN-descriptive-title.md` (e.g., `002-data-model-design.md`)
- Sections: Context, Decision, Consequences, Alternatives Considered
- Written when making significant architectural decisions
- Updated if decisions change

**Existing ADRs:**
- Will be created as needed during implementation

### Teaching Documents

**Location:** `.shared/.planning/teaching/` (gitignored, in shared directory)

**Purpose:**
- One teaching document per deliverable
- Explain concepts and design decisions
- Educational resource for learning
- Demonstrate technical writing skills

**Naming:** `X.Y-topic-name.md` (e.g., `0.2-testing-philosophy.md`)

**Examples:**
- `0.1-git-worktrees-parallel-development.md`
- `0.2-testing-philosophy.md`

## Tech Stack Specifics

### Framework and Build

**Svelte 5** with TypeScript:
- Use modern Svelte 5 features (runes: `$state`, `$derived`, `$effect`)
- Component-first architecture
- Reactive state management

**Vite**:
- Build tool and dev server
- Fast HMR for development
- Optimized production builds

### Testing Stack

**Vitest**:
- Unit and integration tests
- Coverage reporting with coverage-v8
- Fast, Vite-native test runner

**Playwright**:
- E2E testing in real browsers
- Cross-browser testing support
- Visual regression capabilities

**@testing-library/svelte**:
- Component testing utilities
- User-centric testing approach
- Currently v5.2.8 (limited Svelte 5 support - see issue #3)

### State Management

**Svelte Stores**:
- Writable stores for application state
- LocalStorage persistence
- Reactive updates across components

**LocalStorage**:
- Primary data persistence layer
- Schema validation with Zod (or similar)
- Migration support for data format changes

### Code Quality

**Pre-commit checks:**
- Linting and formatting enforced via Husky
- Prevents broken code from being committed
- Auto-fixes when possible

**CI/CD Pipeline:**
- GitHub Actions for automated testing
- Vercel for deployment
- Status checks required for PR merge

## Development Workflow Integration

### Starting a New Feature

1. Create worktree using `git-github-workflow` skill
2. Review acceptance criteria in `.planning/PLAN.md`
3. Write tests first (TDD approach encouraged)
4. Implement feature
5. Run full test suite before committing
6. Make many small commits (not one big commit after-the-fact)
7. Ensure all quality checks pass
8. Create PR using `git-github-workflow` skill

### Code Review Standards

Follow structure in CONTRIBUTING.md:
- tl;dr verdict (Approved / Fix X things / etc.)
- Optional summary (8-128 words)
- Findings with categories:
  - Blockers (must fix before merge)
  - Important (must fix immediately after merge)
  - Minor (can address later)
  - Enhancement ideas (by impact/effort matrix)
  - Nits (small improvements)

### Merge Requirements

**All PRs must:**
- Pass all tests (unit, integration, E2E)
- Meet coverage thresholds (90% overall, 100% critical paths)
- Pass linting and formatting checks
- Pass TypeScript compilation
- Build successfully
- Be reviewed and approved
- Use squash merge to main

## Quick Reference

**Test everything:**
```bash
npm test && npm run test:coverage && npm run test:e2e && npm run lint && npm run check && npm run build
```

**Coverage targets:**
- 90% overall (enforced)
- 100% critical paths (random selection, box sorting, inventory mutations, LocalStorage)

**Documentation:**
- README.md - user-facing
- DEVELOPING.md - developer-facing
- CONTRIBUTING.md - process and workflow
- docs/adr/ - architecture decisions
- Teaching docs - educational explanations

**Quality tools:**
- ESLint + Prettier (auto-run on commit)
- Husky + lint-staged (pre-commit hooks)
- TypeScript strict mode
- Vitest coverage reporting
