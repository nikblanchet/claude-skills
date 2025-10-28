# CI/CD Monitoring Guide

## Overview

GitHub Actions runs automated checks on every push to a pull request. Monitor these checks throughout the PR workflow to ensure code quality and catch issues early.

## When to Check CI/CD Status

Monitor CI/CD checks at these workflow points:

1. **After creating PR:** Initial checks run automatically
2. **After pushing commits:** New checks run for each push
3. **After addressing code review feedback:** Verify fixes don't break tests
4. **Before invoking teacher-mentor agent:** Ensure all checks pass
5. **After pushing documentation:** Verify docs don't break build

## Commands for Checking Status

### Quick Summary: Check All PR Checks

```bash
gh pr checks <pr-number>
```

**Output shows:**
- Check names (e.g., "Test", "Lint", "Type Check", "Build")
- Status: pass, fail, pending
- Conclusion: success, failure, neutral, cancelled, skipped

**Example output:**
```
Some checks were not successful
1 failing, 3 successful, and 0 pending checks

X   Test       CI       failed  2m45s ago  https://github.com/...
✓   Lint       CI       passed  2m30s ago  https://github.com/...
✓   Build      CI       passed  2m20s ago  https://github.com/...
✓   Type Check CI       passed  2m15s ago  https://github.com/...
```

### List Recent Workflow Runs

```bash
gh run list --limit 5
```

**Output shows:**
- Workflow name
- Status (completed, in_progress, queued)
- Conclusion (success, failure, cancelled)
- Branch name
- Run ID

**Example output:**
```
STATUS  TITLE        WORKFLOW  BRANCH              EVENT  ID          ELAPSED AGE
✓       CI           CI        feature/random-sel  push   6789012345  2m45s   3m
X       CI           CI        feature/random-sel  push   6789012344  2m30s   1h
✓       CI           CI        main                push   6789012343  2m20s   2h
```

### View Detailed Run Information

```bash
gh run view <run-id>
```

**Output shows:**
- Complete workflow execution details
- All jobs and their statuses
- Steps within each job
- Failure reasons
- Logs (can be accessed with additional flags)

**To see logs:**
```bash
gh run view <run-id> --log
```

**To see logs for failed jobs only:**
```bash
gh run view <run-id> --log-failed
```

### Watch Checks in Real-Time

```bash
gh pr checks <pr-number> --watch
```

Continuously updates check status until all checks complete.

## Interpreting Results

### Success Indicators

**All checks pass:**
```
All checks have passed
4 successful checks

✓   Test       CI  passed  2m45s ago
✓   Lint       CI  passed  2m30s ago
✓   Build      CI  passed  2m20s ago
✓   Type Check CI  passed  2m15s ago
```

**Next steps:**
- Proceed to next workflow step (code review, merge preparation, etc.)

### Failure Indicators

**One or more checks fail:**
```
Some checks were not successful
1 failing, 3 successful, and 0 pending checks

X   Test  CI  failed  2m45s ago
```

**Next steps:**
- Identify which check failed
- View detailed logs: `gh run view <run-id> --log-failed`
- Reproduce locally
- Fix the issue
- Commit and push fix

### Pending/In-Progress

**Checks still running:**
```
Some checks are pending
2 pending, 2 successful checks

●   Test       CI  in_progress  30s
●   Type Check CI  pending      -
✓   Lint       CI  passed       1m ago
✓   Build      CI  passed       45s ago
```

**Next steps:**
- Wait for checks to complete
- Use `--watch` flag to monitor in real-time
- Continue with other work while waiting

## Common Failure Patterns and Fixes

### Linting Errors

**Symptom:** Lint check fails

**Reproduce locally:**
```bash
npm run lint
```

**Common issues:**
- Code formatting violations (Prettier)
- ESLint rule violations
- Import order issues

**Fix:**
```bash
npm run lint:fix    # Auto-fix formatting issues
npm run lint        # Verify fixes
```

If auto-fix doesn't resolve all issues, manually fix remaining violations, then:
```bash
git add .
git commit -m "Fix linting errors"
git push
```

### Test Failures

**Symptom:** Test check fails

**Reproduce locally:**
```bash
npm test
# OR for more verbose output:
npm run test:unit
```

**Important:** Run tests in bbud conda environment:
```bash
/Users/nik/miniconda3/envs/bbud/bin/python -m pytest
```

**Common issues:**
- Test assertions fail (logic bugs)
- Coverage threshold not met (need more tests)
- Tests timeout (infinite loops, performance issues)
- Environment-specific failures

**Fix:**
1. Identify failing test from CI logs
2. Run that specific test locally
3. Debug and fix the issue
4. Verify all tests pass locally
5. Commit and push:
   ```bash
   git add .
   git commit -m "Fix failing tests in [component]"
   git push
   ```

### Type Errors

**Symptom:** Type check fails

**Reproduce locally:**
```bash
npx tsc
# OR
npm run type-check
```

**Common issues:**
- TypeScript type mismatches
- Missing type annotations
- Incorrect return types
- Unused variables or imports

**Fix:**
1. Review type errors from local run
2. Add missing types or fix type mismatches
3. Verify: `npx tsc`
4. Commit and push:
   ```bash
   git add .
   git commit -m "Fix type errors in [component]"
   git push
   ```

### Build Failures

**Symptom:** Build check fails

**Reproduce locally:**
```bash
npm run build
```

**Common issues:**
- Import errors (missing dependencies)
- Syntax errors
- Asset loading problems
- Environment variable issues

**Fix:**
1. Review build error from CI logs or local run
2. Fix the underlying issue (install missing deps, fix imports, etc.)
3. Verify: `npm run build`
4. Commit and push:
   ```bash
   git add .
   git commit -m "Fix build errors: [description]"
   git push
   ```

## When to Re-run Checks vs Fix Issues First

### Re-run Without Changes (Rare)

Re-run checks without making code changes only when:
- Transient network/infrastructure failures (very rare)
- GitHub Actions service issues (check status.github.com)
- Random flaky test that consistently passes locally

**How to trigger re-run:**
```bash
gh run rerun <run-id>
```

### Fix Issues First (Standard Practice)

In most cases:
1. Reproduce failure locally
2. Fix the issue
3. Verify locally (run tests, linting, build, type-check)
4. Commit fix
5. Push to branch
6. Checks run automatically on push

**Don't:**
- Re-run checks hoping they pass without fixing the issue
- Push multiple "fix CI" commits without testing locally first

**Do:**
- Reproduce and fix locally before pushing
- Make focused commits for each type of fix
- Verify all checks pass locally before pushing

## Reading Logs for Specific Errors

### Accessing Full Logs

```bash
gh run view <run-id> --log
```

### Searching Logs for Errors

```bash
gh run view <run-id> --log | grep -i error
gh run view <run-id> --log | grep -i failed
gh run view <run-id> --log | grep -A 10 "FAIL"  # Show 10 lines after "FAIL"
```

### Understanding Log Output

Logs typically show:
1. **Setup steps:** Installing dependencies, setting up environment
2. **Test/check execution:** Running the actual checks
3. **Failure details:** Specific errors, stack traces, failed assertions
4. **Teardown:** Cleanup steps

**Focus on:**
- Lines marked with `Error:`, `FAIL:`, `✗`, or `X`
- Stack traces showing where failures occurred
- Assertion messages explaining what was expected vs actual

## Workflow Integration

### Standard CI/CD Checkpoint Pattern

1. **Make changes and commit**
2. **Push to feature branch**
3. **Check status:**
   ```bash
   gh pr checks <pr-number>
   ```
4. **If checks fail:**
   - View logs: `gh run view <run-id> --log-failed`
   - Reproduce locally
   - Fix issue
   - Commit and push
   - Return to step 3
5. **If checks pass:**
   - Proceed to next workflow step

### Before Major Workflow Steps

**Before code review:**
```bash
gh pr checks <pr-number>
```
All checks must pass before invoking code-reviewer agent.

**Before teacher-mentor:**
```bash
gh pr checks <pr-number>
```
All checks must pass before invoking teacher-mentor agent.

**Before merge:**
```bash
gh pr checks <pr-number>
```
Final verification that all checks pass before merging.

## Troubleshooting

### Checks Not Running

**Problem:** PR created but no checks appear.

**Solutions:**
- Wait a few moments (checks may be queued)
- Verify GitHub Actions is enabled for the repo
- Check `.github/workflows/` directory has workflow files
- Verify branch protection rules aren't blocking checks

### Checks Stuck in Pending

**Problem:** Checks show "pending" or "in_progress" for long time.

**Solutions:**
- Check GitHub Actions status: status.github.com
- View run details: `gh run view <run-id>`
- If truly stuck (>30 minutes), cancel and re-run:
  ```bash
  gh run cancel <run-id>
  gh run rerun <run-id>
  ```

### Different Results Local vs CI

**Problem:** Tests pass locally but fail in CI (or vice versa).

**Possible causes:**
- Environment differences (Node version, Python version)
- Missing or different dependencies
- Environment variables not set in CI
- Timezone or locale differences
- File path differences (case sensitivity on different OS)

**Solutions:**
- Check workflow file for environment setup
- Verify dependency versions match local
- Ensure environment variables are set in GitHub repository settings
- Run tests in isolated environment locally (clean install)

## Best Practices

1. **Check early, check often:** Monitor CI/CD after every push
2. **Fix locally first:** Always reproduce and fix issues locally before pushing
3. **Read the logs:** Don't guess what's wrong; check the actual error messages
4. **One issue at a time:** Fix and commit each type of issue separately
5. **Use bbud environment:** For BroteinBuddy, always run tests in bbud conda environment
6. **Don't merge on red:** Never merge a PR with failing checks
7. **Watch patterns:** If certain checks consistently fail, improve local verification before pushing
