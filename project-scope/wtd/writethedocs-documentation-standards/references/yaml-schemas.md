# YAML Schemas Reference

This document provides detailed information about the three YAML schemas used for Write the Docs conference data.

All conference YAML files must validate against these schemas using the `validate-yaml.sh` script.

## Schema Files

Located in `docs/_data/`:
- `schema-config.yaml` - Conference configuration
- `schema-sessions.yaml` - Speaker sessions and talks
- `schema-schedule.yaml` - Conference schedule/agenda

## Validation Tool

**Location**: `docs/_scripts/validate-yaml.sh`

**Usage**:
```bash
cd docs/_scripts
./validate-yaml.sh
```

**What it validates**:
- All `*-config.yaml` files against `schema-config.yaml`
- All `*-sessions.yaml` files against `schema-sessions.yaml`
- All `*-schedule.yaml` files against `schema-schedule.yaml`

## Config Schema (`schema-config.yaml`)

### Required Fields

```yaml
name: str()                    # Conference name (e.g., "Portland")
shortcode: str()               # Short identifier (e.g., "portland", "berlin")
year: int()                    # Conference year (e.g., 2025)
city: str()                    # City name
local_area: str()             # Neighborhood/area
area: str()                    # Country or region
tz: str()                      # Timezone (e.g., "America/Los_Angeles", "Europe/Berlin")
email: str()                   # Contact email
color: str()                   # Primary color for conference branding
```

### Optional Fields

```yaml
time_format: enum('24h', '12h')  # Time display format (default: varies by location)
tz2: str()                        # Second timezone for multi-TZ display
tz2_

color: str()                      # Second timezone color
cfp_url: str()                    # Call for Proposals URL
tickets_url: str()                # Ticket sales URL
livestream_url: str()             # Livestream link
```

### Feature Flags (boolean)

```yaml
flaglanding: bool()              # Show landing page
flagcfp: bool()                  # CFP is open
flagspeakersannounced: bool()    # Speakers have been announced
flaghasschedule: bool()          # Schedule is published
flagticketsonsale: bool()        # Tickets are on sale
flagsoldout: bool()              # Conference is sold out
flaghasshirts: bool()            # Shirts available
flaghasfood: bool()              # Food information available
flaglivestreaming: bool()        # Livestream is active
flagpostconf: bool()             # Post-conference mode
flagvideos: bool()               # Videos are published
```

### Sponsor Data

```yaml
sponsors:
  keystone:
    - name: str()
      link: str()
      brand: str()  # Filename in _static/img/sponsors/
  publisher:
    - name: str()
      link: str()
      brand: str()
  patron:
    - name: str()
      link: str()
      brand: str()
  # ... other sponsorship tiers
```

### Dates

```yaml
date:
  main: str()                    # Main conference dates (e.g., "May 4-6, 2025")
  cfp_ends: str()                # CFP deadline
  tickets_live: str()            # Ticket sales start
  unconf:
    - str()                      # Unconference dates (list)
  talks:
    - str()                      # Talk dates (list)
  job_fair: str()                # Job fair date
```

### Example Config YAML

```yaml
name: Portland
shortcode: portland
year: 2025
city: Portland
local_area: North Portland
area: Oregon, USA
tz: America/Los_Angeles
email: portland@writethedocs.org
color: green
time_format: 12h

flaglanding: false
flagcfp: false
flagspeakersannounced: true
flaghasschedule: true
flagticketsonsale: true
flagsoldout: false
flaghasshirts: true
flaghasfood: true
flaglivestreaming: false
flagpostconf: false
flagvideos: false

date:
  main: "**May 4-6, 2025**"
  talks:
    - "May 5-6"
  unconf:
    - "May 4"
  cfp_ends: "January 15, 2025"
  tickets_live: "February 1, 2025"

sponsors:
  keystone:
    - name: GitBook
      link: https://www.gitbook.com/
      brand: GitBook.png
  # ... more sponsors
```

## Sessions Schema (`schema-sessions.yaml`)

### Required Fields

```yaml
slug: str()                    # Unique identifier for session
title: str()                   # Talk title
speakers:                      # List of speakers
  - name: str()                # Speaker name
    slug: str()                # Speaker slug (for photo/bio)
    details: str()             # Speaker bio/details
abstract: str()                # Talk abstract/description
```

### Optional Fields

```yaml
youtubeId: str()              # YouTube video ID (post-conference)
```

### Speaker Photo Management

Speaker photos stored in `docs/_static/img/speakers/`:
- Filename: `{speaker_slug}.{jpg|jpeg|png}`
- Falls back to `missing.jpg` if not found
- Custom Jinja filter `speaker_photo()` locates photos

### Example Sessions YAML

```yaml
- title: Documentation as code
  slug: documentation-as-code
  speakers:
    - name: Jane Smith
      slug: jane-smith
      details: >
        Jane Smith is a technical writer at Example Corp,
        where she leads the docs-as-code initiative.
        She has 10 years of experience in developer documentation.
  abstract: >
    This talk explores treating documentation like code:
    version control, automated testing, and continuous deployment.
    Learn how to build a docs-as-code workflow that scales.
  youtubeId: abc123xyz

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
    This talk covers how to write effective API docs,
    code samples, and getting started guides.
```

## Schedule Schema (`schema-schedule.yaml`)

### Required Fields

```yaml
time: str()                    # Time in format "HH:MM" (24-hour)
title: str()                   # Event title
```

### Optional Fields

```yaml
slug: str()                    # Links to session in sessions YAML
icon: str()                    # Icon type (food, talk, etc.)
```

### Time Format

- Always use 24-hour format in YAML: `"09:00"`, `"14:30"`
- Display format (12h/24h) controlled by config `time_format`
- Timezone conversion automatic based on conference `tz`

### Schedule Event Types

**Talk** (has slug):
```yaml
- time: "10:00"
  title: Documentation as code
  slug: documentation-as-code
```

**Break** (no slug):
```yaml
- time: "10:30"
  title: Morning break
  icon: food
```

**Meal**:
```yaml
- time: "12:00"
  title: Lunch
  icon: food
```

**Social Event**:
```yaml
- time: "18:00"
  title: Reception
  icon: social
```

### Multi-Day Schedules

Organized by day using YAML structure:

```yaml
unconf:
  - time: "09:00"
    title: Unconference Kickoff
  - time: "10:00"
    title: Unconference Sessions
  # ... more events

talks_day1:
  - time: "09:00"
    title: Registration
  - time: "10:00"
    title: Opening Remarks
  - time: "10:15"
    title: Keynote
    slug: keynote-speaker
  # ... more events

talks_day2:
  - time: "09:00"
    title: Doors Open
  - time: "10:00"
    title: Morning Session
    slug: morning-talk
  # ... more events
```

### Example Schedule YAML

```yaml
unconf:
  - time: "09:00"
    title: Doors Open
    icon: door
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
    slug: keynote-2025
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
  - time: "14:00"
    title: Afternoon Session 1
    slug: afternoon-talk-1
  - time: "14:45"
    title: Lightning Talks
  - time: "15:30"
    title: Afternoon Break
    icon: food
  - time: "16:00"
    title: Afternoon Session 2
    slug: afternoon-talk-2
  - time: "16:45"
    title: Unconference Reports
  - time: "17:30"
    title: Day 1 Closing
  - time: "18:00"
    title: Reception
    icon: social

talks_day2:
  - time: "08:00"
    title: Doors Open
  - time: "09:00"
    title: Day 2 Welcome
  - time: "09:15"
    title: Morning Keynote
    slug: day2-keynote
  # ... similar structure to day 1
```

## Common Validation Errors

### Missing Required Fields

```
Error: Required field 'name' missing in config
```

**Fix**: Add all required fields from schema

### Wrong Data Type

```
Error: Expected int for 'year', got string
```

**Fix**: Remove quotes from integers
```yaml
# Wrong
year: "2025"

# Correct
year: 2025
```

### Invalid Enum Value

```
Error: 'time_format' must be '12h' or '24h', got '24-hour'
```

**Fix**: Use exact enum values from schema
```yaml
# Wrong
time_format: 24-hour

# Correct
time_format: 24h
```

### Malformed YAML Syntax

```
Error: YAML parse error - tabs not allowed
```

**Fix**: Use spaces, not tabs for indentation

### Orphaned Schedule Slugs

```
Warning: Schedule slug 'talk-foo' not found in sessions YAML
```

**Fix**: Ensure all schedule slugs reference valid sessions

## Validation Workflow

1. **Create/Edit YAML files**
2. **Run validation**:
   ```bash
   cd docs/_scripts
   ./validate-yaml.sh
   ```
3. **Fix any errors** reported
4. **Re-run** until all pass
5. **Commit** changes

**Always validate before creating a PR** - YAML validation is a required CI check.

## Schema Updates

If schemas need updating (rare):
1. Edit `docs/_data/schema-*.yaml`
2. Update all affected conference YAML files
3. Test validation script
4. Document changes in PR

Schemas are intentionally strict to maintain data quality across all conferences.
