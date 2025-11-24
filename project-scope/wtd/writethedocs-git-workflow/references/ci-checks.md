# CI/CD Checks Reference

This document provides detailed information about the 6 automated CI/CD checks that must pass for all Write the Docs pull requests.

## 1. Ubuntu Build

**Workflow file**: `.github/workflows/ubuntu.yml`

**What it does**:
- Sets up Python 3.9 environment
- Installs dependencies from `requirements.txt`
- Builds documentation with `make html`
- Runs htmlproofer to validate internal links
- Archives built HTML as artifact

**Build command**:
```bash
cd docs
make html
```

**Link checking**:
```bash
bundle exec htmlproofer \
  --ignore-files "/404/,/2013/,/2014/,/2015/,/2016/,/2017/,/search\/index.html/,/archive\/tag\/index/" \
  --allow-hash-href=true \
  --enforce-https=false \
  --ignore-missing-alt=true \
  --disable-external=true \
  _build/html
```

**Common failures**:
- Sphinx build errors (syntax errors in RST, missing files)
- Broken internal links
- Missing images or assets
- Import errors in custom extensions

**How to fix**:
- Test build locally: `cd docs && make clean html`
- Check build output for specific errors
- Verify all referenced files exist
- Test custom extensions in `docs/_ext/`

## 2. Windows Build

**Workflow file**: `.github/workflows/windows.yml`

**What it does**:
- Sets up Python 3.9 on Windows
- Installs dependencies
- Builds documentation with `make.bat html`
- Ensures cross-platform compatibility

**Common failures**:
- Path separator issues (Windows uses `\` not `/`)
- UTF-8 encoding problems
- Line ending differences (CRLF vs LF)

**How to fix**:
- Check `docs/conf.py` for Windows-specific monkeypatch
- Ensure UTF-8 encoding specified in Python file operations
- Use `os.path.join()` for paths, not string concatenation

## 3. Spellcheck

**Workflow file**: `.github/workflows/spellcheck.yml`

**What it does**:
- Uses `codespell-project/actions-codespell`
- Checks `docs/` directory for spelling errors
- Skips: PDF, SVG, JS, CSS, SCSS files
- Skips: Legacy conference data (2015-2017)
- Custom ignore list in `codespell/ignore.txt`

**Common failures**:
- Actual typos in documentation
- Technical terms not in dictionary
- Brand names or proper nouns

**How to fix**:
1. Fix actual typos (preferred)
2. If word is correct but flagged:
   - Check if it's already in `codespell/ignore.txt`
   - Add to ignore list ONLY if it's a legitimate technical term/name
   - Don't add common words with typos

**Local testing**:
```bash
codespell docs/
```

## 4. Vale Linting

**Workflow file**: `.github/workflows/vale.yml`

**What it does**:
- Runs 3 separate Vale checks with different configurations
- Uses Vale 3.4.2
- Reports errors via reviewdog in PRs

**Three configurations**:

### 4a. General Content Check
- Config: `vale/vale.ini`
- Applies to: Most documentation
- Rules: WTD styles + proselint (many disabled for legacy content)
- Level: Warning minimum

### 4b. Guide Content Check
- Config: `vale/guide.ini`
- Applies to: `docs/guide/` directory
- Rules: Stricter enforcement
- Checks: Heading capitalization, inclusivity, gender bias
- Level: Error on violations

### 4c. Conference News Check
- Config: `vale/news.ini`
- Applies to: `docs/conf/**/news/*`
- Rules: Minimal (mainly `contents::` directive usage)
- Level: Error on violations

**Common failures**:

**Heading capitalization**:
- Must use sentence case: "This is a heading"
- Not title case: "This Is A Heading"
- Exceptions for proper nouns (API, Sphinx, Git, etc.)

**Branding**:
- "Write the Docs" (correct)
- "Write The Docs" (wrong)
- "Read the Docs" (correct)
- "Read The Docs" (wrong)

**Inclusivity**:
- Replace "tribe" with "people"
- Avoid gendered language

**Sentence length**:
- Suggested max 28 words per sentence
- Suggestion level only (not error)

**How to fix**:
```bash
# Test locally
vale --config=vale/vale.ini docs/

# Test guide content
vale --config=vale/guide.ini docs/guide/

# Test conference news
vale --config=vale/news.ini --glob=docs/conf/**/news/* docs
```

**Vale rule files**:
- `vale/WTD/headings.yml` - Heading capitalization
- `vale/WTD/Branding.yml` - Brand names
- `vale/WTD/inclusivity.yml` - Inclusive language
- `vale/WTD/SentenceLength.yml` - Sentence length
- `vale/WTD/contents.yml` - Newsletter TOC usage

## 5. YAML Validation

**Workflow file**: `.github/workflows/validate_yaml.yml`

**What it does**:
- Validates all conference YAML files against schemas
- Uses yamale and ruamel.yaml
- Runs `docs/_scripts/validate-yaml.sh`

**Validated files**:
- `docs/_data/*-config.yaml` against `schema-config.yaml`
- `docs/_data/*-sessions.yaml` against `schema-sessions.yaml`
- `docs/_data/*-schedule.yaml` against `schema-schedule.yaml`

**Common failures**:
- Missing required fields
- Wrong data types (string vs int)
- Invalid enum values
- Malformed YAML syntax

**How to fix**:
```bash
# Run validation locally
cd docs/_scripts
./validate-yaml.sh

# Check schemas
cat docs/_data/schema-config.yaml
cat docs/_data/schema-sessions.yaml
cat docs/_data/schema-schedule.yaml
```

**Schema requirements**:

**Config schema** (key fields):
```yaml
name: str()  # Conference name
shortcode: str()  # e.g., "berlin", "portland"
year: int()  # e.g., 2025
city: str()
tz: str()  # Timezone (e.g., "Europe/Berlin")
email: str()
time_format: enum('24h', '12h', required=False)
```

**Sessions schema** (key fields):
```yaml
slug: str()  # Unique identifier
title: str()  # Talk title
speakers: list()  # Speaker names
abstract: str()  # Talk description
```

**Schedule schema** (key fields):
```yaml
time: str()  # Time in format "HH:MM"
title: str()  # Event title
slug: str(required=False)  # Links to session
```

## 6. Read the Docs Preview

**Workflow file**: `.github/workflows/documentation-links.yml`

**What it does**:
- Automatic preview build for PRs
- Deploys to RTD preview environment
- Provides link to view changes
- Uses RTD's build configuration (`.readthedocs.yaml`)

**Build configuration**:
- OS: ubuntu-22.04
- Python: 3.9
- Builder: dirhtml (clean URLs)
- No PDF generation

**Common failures**:
- Sphinx build errors (same as Ubuntu build)
- RTD-specific issues (environment, dependencies)
- Resource limits (timeout, memory)

**How to fix**:
- Same as Ubuntu build fixes
- Check RTD build logs for specific errors
- Ensure `.readthedocs.yaml` is correctly configured

## Summary Checklist

Before creating a PR, verify locally:

- [ ] `cd docs && make clean html` succeeds
- [ ] No warnings in Sphinx output
- [ ] `codespell docs/` passes
- [ ] `vale --config=vale/vale.ini docs/` passes
- [ ] `cd docs/_scripts && ./validate-yaml.sh` passes
- [ ] Test live preview: `make livehtml`
- [ ] Check pages in browser at http://127.0.0.1:8888

All 6 CI checks must pass before merge.
