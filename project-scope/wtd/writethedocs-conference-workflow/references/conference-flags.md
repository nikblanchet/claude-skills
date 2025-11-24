# Conference Flags Reference

Complete reference for all conference feature flags used in Write the Docs conference configurations.

## All Flags

All flags are boolean values in the config YAML (`{shortcode}-{year}-config.yaml`).

### flaglanding
**When to enable**: Early announcement phase, before detailed info available
**Controls**: Shows minimal landing page
**Typical timeline**: Initial setup → CFP open

### flagcfp
**When to enable**: Call for Proposals is open
**Controls**: CFP page displays submission form/link
**Related fields**: `cfp_url`, `date.cfp_ends`
**Typical timeline**: ~6 months before conference → speakers selected

### flagspeakersannounced
**When to enable**: Speaker lineup finalized and published
**Controls**: Speakers page displays
**Requirements**: Must have `{shortcode}-{year}-sessions.yaml` file
**Typical timeline**: ~3 months before conference

### flaghasschedule
**When to enable**: Full conference schedule published
**Controls**: Schedule page displays with times
**Requirements**: Must have `{shortcode}-{year}-schedule.yaml` file
**Typical timeline**: ~1-2 months before conference

### flagticketsonsale
**When to enable**: Tickets available for purchase
**Controls**: Ticket purchase button/link displays
**Related fields**: `tickets_url`, `date.tickets_live`
**Typical timeline**: ~4 months before → sold out

### flagsoldout
**When to enable**: All tickets sold
**Controls**: Shows sold-out notice, hides purchase link
**Interaction**: Turn off `flagticketsonsale` when enabling this
**Typical timeline**: When capacity reached

### flaghasshirts
**When to enable**: Conference shirts/swag available
**Controls**: Shows shirt information
**Typical timeline**: During ticket sales

### flaghasfood
**When to enable**: Food/venue information finalized
**Controls**: Shows food/dietary options
**Typical timeline**: ~1 month before conference

### flaglivestreaming
**When to enable**: During conference (livestream active)
**Controls**: Shows livestream link
**Related fields**: `livestream_url`
**Typical timeline**: ~1 week before → end of conference

### flagpostconf
**When to enable**: After conference ends
**Controls**: Switches to post-event mode
**Typical timeline**: Day after conference ends

### flagvideos
**When to enable**: Conference videos published
**Controls**: Video archive pages display
**Requirements**: YouTube IDs in sessions YAML
**Typical timeline**: ~2-4 weeks after conference

## Flag Lifecycle

Typical progression for a conference:

```
Setup Phase:
  flaglanding: true

CFP Phase:
  flaglanding: false
  flagcfp: true

CFP Closed:
  flagcfp: false

Speakers Announced:
  flagspeakersannounced: true
  flagticketsonsale: true  # Usually simultaneous

Schedule Published:
  flaghasschedule: true
  flaghasfood: true
  flaghasshirts: true

Sold Out (if applicable):
  flagticketsonsale: false
  flagsoldout: true

Pre-Conference:
  flaglivestreaming: true

During Conference:
  (flaglivestreaming remains true)

Post-Conference:
  flaglivestreaming: false
  flagpostconf: true

Videos Published:
  flagvideos: true
```

## Example Config

```yaml
# Portland 2026 at different stages

# Stage 1: Initial Setup
flaglanding: true
flagcfp: false
flagspeakersannounced: false
flag hasschedule: false
flagticketsonsale: false
flagsoldout: false
flaghasshirts: false
flaghasfood: false
flaglivestreaming: false
flagpostconf: false
flagvideos: false

# Stage 2: CFP Open
flaglanding: false
flagcfp: true
# ... rest false

# Stage 3: Speakers + Tickets
flagcfp: false
flagspeakersannounced: true
flagticketsonsale: true
# ... rest false

# Stage 4: Schedule Published
flagspeakersannounced: true
flaghasschedule: true
flagticketsonsale: true
flaghasshirts: true
flaghasfood: true
# ... rest false

# Stage 5: Post-Conference
flagspeakersannounced: true
flaghasschedule: true
flagsoldout: true  # or flagticketsonsale: true if not sold out
flaghasshirts: true
flaghasfood: true
flagpostconf: true
# ... livestreaming false, videos not yet

# Stage 6: Videos Published
flagspeakersannounced: true
flaghasschedule: true
flagsoldout: true
flaghasshirts: true
flaghasfood: true
flagpostconf: true
flagvideos: true
```

## Testing Flags Locally

Change flags in config YAML and rebuild:

```bash
# Edit config
vim docs/_data/portland-2026-config.yaml

# Validate
cd docs/_scripts
./validate-yaml.sh

# Build and preview
cd ../docs
make clean html
make livehtml
```

Check pages appear/disappear based on flags at http://127.0.0.1:8888
