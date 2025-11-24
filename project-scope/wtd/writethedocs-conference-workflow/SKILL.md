---
name: writethedocs-conference-workflow
description: Complete workflow for creating and managing Write the Docs conference websites with YAML-driven pages. Use when setting up conference pages, managing conference lifecycle stages, or updating conference data.
---

# Write the Docs Conference Workflow

This skill provides the complete workflow for creating, updating, and managing Write the Docs conference websites using YAML-driven data and flag-based feature toggles.

## When to Use This Skill

Use this skill when:
- Setting up a new conference website
- Updating conference through lifecycle stages (CFP → speakers → schedule → videos)
- Managing conference YAML data files
- Understanding flag-based feature toggles
- Debugging conference page rendering

## Conference Lifecycle Overview

Conferences progress through stages controlled by feature flags:

1. **Landing** (`flaglanding`) - Early announcement
2. **CFP Open** (`flagcfp`) - Call for proposals
3. **Speakers Announced** (`flagspeakersannounced`) - Speaker lineup published
4. **Schedule Published** (`flaghasschedule`) - Full agenda available
5. **Tickets On Sale** (`flagticketsonsale`) - Ticket sales active
6. **Sold Out** (`flagsoldout`) - No tickets remaining
7. **Livestreaming** (`flaglivestreaming`) - During conference
8. **Post-Conference** (`flagpostconf`) - After event
9. **Videos Published** (`flagvideos`) - Video archive available

## Conference Data Structure

Each conference requires 3 YAML files in `docs/_data/`:

1. **Config** (`{shortcode}-{year}-config.yaml`) - Metadata, flags, sponsors
2. **Sessions** (`{shortcode}-{year}-sessions.yaml`) - Speakers and talks
3. **Schedule** (`{shortcode}-{year}-schedule.yaml`) - Time-ordered agenda

Plus RST pages in `docs/conf/{shortcode}/{year}/`.

## Stage 1: Conference Setup

### Create Conference Directory

```bash
# Example for Portland 2026
mkdir -p docs/conf/portland/2026
cd docs/conf/portland/2026
```

### Copy from Previous Year

```bash
# Copy and update from previous year
cp -r ../2025/* .

# Update year references in all files
# Change 2025 → 2026 throughout
```

### Create Initial Config YAML

**File**: `docs/_data/portland-2026-config.yaml`

**Minimum required**:
```yaml
name: Portland
shortcode: portland
year: 2026
city: Portland
local_area: North Portland
area: Oregon, USA
tz: America/Los_Angeles
email: portland@writethedocs.org
color: green
time_format: 12h

# Initial flags (all false except landing)
flaglanding: true
flagcfp: false
flagspeakersannounced: false
flaghasschedule: false
flagticketsonsale: false
flagsoldout: false
flaghasshirts: false
flaghasfood: false
flaglivestreaming: false
flagpostconf: false
flagvideos: false

date:
  main: "**May 3-5, 2026**"
  cfp_ends: "TBA"
  tickets_live: "TBA"
```

See `references/conference-flags.md` for all flag definitions.

### Create Conference Pages

**Required pages in `docs/conf/{shortcode}/{year}/`**:

- `index.rst` - Homepage
- `cfp.rst` - Call for proposals (initially TBA)
- `tickets.rst` - Ticket information (initially TBA)
- `sponsors/prospectus.rst` - Sponsorship prospectus
- `code-of-conduct.rst` - Code of conduct

**Page template (`index.rst`)**:
```rst
:template: {{year}}/index.html
:banner: _static/conf/images/headers/portland-2026-small-group.jpg
:og:image: _static/conf/images/headers/portland-2026-opengraph.png
:orphan:

.. title:: Home | Write the docs Portland 2026

Welcome to Write the Docs Portland 2026
========================================

Write the Docs Portland 2026 will be held **May 3-5, 2026** in Portland, Oregon.

More details coming soon!
```

### Validate YAML

```bash
cd docs/_scripts
./validate-yaml.sh
```

## Stage 2: CFP Open

### Update Config Flags

```yaml
flaglanding: false  # No longer just landing
flagcfp: true       # CFP is open
```

### Update CFP Details

**In config YAML**:
```yaml
cfp_url: https://cfp.writethedocs.org/portland-2026
date:
  cfp_ends: "January 15, 2026"
```

**In `cfp.rst`**:
- Add submission guidelines
- Link to CFP system
- Deadline information
- Talk format details
- Selection criteria

### Announce CFP

Create announcement in `docs/conf/portland/2026/news/`:

**File**: `cfp-open.rst`
```rst
:template: {{year}}/generic.html

.. post:: Oct 15, 2025
   :tags: portland-2026, cfp

CFP open for Portland 2026
===========================

The Call for Proposals for Write the Docs Portland 2026 is now open!

Submit your talk proposals by **January 15, 2026**.

More details: `/conf/portland/2026/cfp/`_
```

### Close CFP

When deadline passes:
```yaml
flagcfp: false  # CFP closed
```

## Stage 3: Speakers Announced

### Create Sessions YAML

**File**: `docs/_data/portland-2026-sessions.yaml`

Import from Pretalx:
```bash
cd docs/_scripts
export PRETALX_TOKEN=your-token
python pretalx2wtd.py
# Edit year/city at bottom of script
```

Or create manually:
```yaml
- title: Documentation as code
  slug: documentation-as-code
  speakers:
    - name: Jane Smith
      slug: jane-smith
      details: >
        Jane Smith is a technical writer at Example Corp,
        where she leads the docs-as-code initiative.
  abstract: >
    This talk explores treating documentation like code:
    version control, automated testing, and continuous deployment.

- title: Writing for developers
  slug: writing-for-developers
  speakers:
    - name: John Doe
      slug: john-doe
      details: >
        John Doe is a developer advocate with a passion
        for clear, concise technical writing.
  abstract: >
    Developers need different documentation than end users.
    Learn how to write effective API docs and getting started guides.
```

### Add Speaker Photos

Place photos in `docs/_static/img/speakers/`:
- Filename: `{speaker_slug}.jpg` (or .png)
- Falls back to `missing.jpg` if not found

Pretalx import script auto-downloads photos.

### Update Flag

```yaml
flagspeakersannounced: true
```

### Create Speakers Page

**File**: `docs/conf/portland/2026/speakers.rst`

Uses datatemplates directive to render from YAML:
```rst
:template: {{year}}/generic.html

Speakers
========

.. datatemplate::
   :source: /_data/portland-2026-sessions.yaml
   :template: {{year}}/speakers.html
```

### Announce Speakers

Create news post:
```rst
:template: {{year}}/generic.html

.. post:: Feb 1, 2026
   :tags: portland-2026, speakers

Announcing our Portland 2026 speakers
======================================

We're excited to announce the speaker lineup for Write the Docs Portland 2026!

View the full lineup: `/conf/portland/2026/speakers/`_
```

### Validate

```bash
cd docs/_scripts
./validate-yaml.sh

# Build to test
cd ../docs
make html
```

## Stage 4: Schedule Published

### Create Schedule YAML

**File**: `docs/_data/portland-2026-schedule.yaml`

```yaml
unconf:
  - time: "09:00"
    title: Doors Open
  - time: "10:00"
    title: Writing Day Introduction
  - time: "10:30"
    title: Writing Sessions
  - time: "12:00"
    title: Lunch
    icon: food
  - time: "13:00"
    title: Afternoon Writing Sessions
  - time: "17:00"
    title: Day 1 Wrap-Up

talks_day1:
  - time: "08:00"
    title: Doors Open
  - time: "09:00"
    title: Welcome and Orientation
  - time: "09:30"
    title: Opening Keynote
    slug: keynote-2026
  - time: "10:15"
    title: Morning Break
    icon: food
  - time: "10:45"
    title: Documentation as Code
    slug: documentation-as-code
  - time: "11:30"
    title: Writing for Developers
    slug: writing-for-developers
  - time: "12:15"
    title: Lunch
    icon: food
  # ... more events

talks_day2:
  - time: "08:00"
    title: Doors Open
  - time: "09:00"
    title: Day 2 Welcome
  # ... more events
```

**Important**:
- Times in 24-hour format (`"09:00"`, `"14:30"`)
- Slugs must match sessions YAML
- Use `icon: food` for meals/breaks

### Preview Schedule

```bash
cd docs/_scripts
python show-conf-schedule.py portland 2026
```

### Update Flag

```yaml
flaghasschedule: true
```

### Create Schedule Page

**File**: `docs/conf/portland/2026/schedule.rst`

```rst
:template: {{year}}/schedule.html

Schedule
========

Write the Docs Portland 2026 runs May 3-5, 2026.

.. datatemplate::
   :source: /_data/portland-2026-config.yaml
   :source: /_data/portland-2026-schedule.yaml
   :template: {{year}}/schedule.html
```

### Validate

```bash
cd docs/_scripts
./validate-yaml.sh
```

## Stage 5: Tickets On Sale

### Update Config

```yaml
flagticketsonsale: true
tickets_url: https://ti.to/writethedocs/portland-2026

date:
  tickets_live: "February 1, 2026"
```

### Update Tickets Page

**File**: `docs/conf/portland/2026/tickets.rst`

- Ticket types and prices
- Link to ticket platform
- Refund policy
- Financial assistance info

## Stage 6: Sold Out (if applicable)

```yaml
flagticketsonsale: false
flagsoldout: true
```

Update tickets page with sold-out notice.

## Stage 7: During Conference

### Enable Livestreaming

About a week before:
```yaml
flaglivestreaming: true
livestream_url: https://hopin.to/events/wtd-portland-2026
```

### During Event

- Monitor livestream
- Post updates to news
- Engage with attendees

### After Event Ends

```yaml
flaglivestreaming: false
```

## Stage 8: Post-Conference

### Update Flag

```yaml
flagpostconf: true
```

### Add Thank You Post

**File**: `docs/conf/portland/2026/news/thanks.rst`

```rst
:template: {{year}}/generic.html

.. post:: May 10, 2026
   :tags: portland-2026, recap

Thank you Portland 2026!
=========================

Thank you to everyone who joined us for Write the Docs Portland 2026!

Photos, videos, and talk summaries coming soon.
```

## Stage 9: Videos Published

### Add YouTube IDs to Sessions

Update `docs/_data/portland-2026-sessions.yaml`:
```yaml
- title: Documentation as code
  slug: documentation-as-code
  youtubeId: abc123xyz  # Add this
  speakers:
    # ... rest of session data
```

Or use script:
```bash
cd docs/_scripts
python insert-video-ids.py
```

### Enable Video Flag

```yaml
flagvideos: true
```

### Build with Videos

```bash
cd docs
BUILD_VIDEOS=True make html
```

This generates individual video pages in `docs/conf/portland/2026/videos/`.

### Create Video Index

**File**: `docs/conf/portland/2026/videos/index.rst`

```rst
:template: {{year}}/generic.html

Videos
======

.. datatemplate::
   :source: /_data/portland-2026-sessions.yaml
   :template: {{year}}/video-listing.html
```

## Conference Flag Reference

See `references/conference-flags.md` for complete flag definitions and usage.

**Quick reference**:
- `flaglanding` - Show landing page
- `flagcfp` - CFP is open
- `flagspeakersannounced` - Speakers published
- `flaghasschedule` - Schedule available
- `flagticketsonsale` - Tickets for sale
- `flagsoldout` - Sold out
- `flaghasshirts` - Shirts available
- `flaghasfood` - Food info available
- `flaglivestreaming` - Livestream active
- `flagpostconf` - Post-conference mode
- `flagvideos` - Videos published

## Multi-Timezone Support

For conferences with international audiences:

```yaml
tz: America/Los_Angeles
tz2: Europe/Berlin
tz2_color: blue
time_format: 12h
```

Schedule automatically shows times in both timezones.

## Testing Workflow

**Before every change**:

1. **Validate YAML**:
   ```bash
   cd docs/_scripts
   ./validate-yaml.sh
   ```

2. **Build locally**:
   ```bash
   cd docs
   make clean html
   ```

3. **Preview**:
   ```bash
   make livehtml
   # http://127.0.0.1:8888
   ```

4. **Check conference pages**:
   - Homepage
   - Speakers (if flagspeakersannounced)
   - Schedule (if flaghasschedule)
   - Tickets

## Common Issues

### Schedule Slugs Don't Match

**Error**: Slug in schedule.yaml not found in sessions.yaml

**Fix**: Ensure exact match
```yaml
# sessions.yaml
- slug: documentation-as-code

# schedule.yaml
- slug: documentation-as-code  # Must match exactly
```

### Photos Not Displaying

**Issue**: Speaker photos show placeholder

**Fix**: Check filename matches slug
```
docs/_static/img/speakers/jane-smith.jpg  # Filename
slug: jane-smith  # In sessions YAML
```

### Time Format Issues

**Issue**: Times showing wrong

**Fix**: Always use 24-hour in YAML
```yaml
# In schedule YAML
time: "14:30"  # Always 24-hour

# In config YAML
time_format: 12h  # Controls display only
```

### Video Build Slow

**Issue**: `BUILD_VIDEOS=True` takes forever

**Expected**: Videos generate ~100+ pages, this is normal

**Solution**: Skip videos during development
```bash
make html  # Fast, no videos
BUILD_VIDEOS=True make html  # Slow, with videos
```

## Additional Resources

- See `references/conference-flags.md` for all flag definitions
- See `references/yaml-templates.md` for complete YAML examples
- Conference website guide: https://www.writethedocs.org/organizer-guide/confs/website/
- Validation script: `docs/_scripts/validate-yaml.sh`
- Schedule preview: `docs/_scripts/show-conf-schedule.py`
