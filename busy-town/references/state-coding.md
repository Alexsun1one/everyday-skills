# State Coding / 状态编码

Show status, degree, and quality **without extra text**. The state is encoded in physical storybook things — smoke, flags, expressions, gate posture, color accents. Keep an **encoding budget**: pick the one or two encodings that carry the article's precision and let the rest stay neutral. Over-coding makes a town unreadable.

## Encoding Channels

| Channel | What it encodes | How |
| --- | --- | --- |
| **Chimney smoke** | is this station running? | smoke = busy/running; no smoke = idle/stopped |
| **Flag color** | state of a shop / role | red = alert/risk/blocked; green = done/healthy; gold = focus/active-now; gray = neutral; checkered = shipped |
| **Animal expression** | the role's current state | calm = neutral; furrowed = effort; eased = relief; tiny "z" = dozing/waiting |
| **Animal posture** | the role's state | mid-action = working; leaning idle = waiting; asleep = blocked/stalled |
| **Gate posture** | a boundary's state | gate up = open; gate down = closed; half-open = partial; a pile at the side = rejected |
| **Object state** | the state of the passed good | raw sack → milled flour → baked loaf = a transformation chain; a torn sack = broken; a patched sack = repaired |
| **Crate stamp** | state of a handoff item | "✓ 已检" green stamp; "✗ 退" red stamp; blank = pending |
| **Stack height** | degree / accumulation | a growing pile of returning parcels = reinforcing loop; a shrinking pile = balancing loop; a tall stack = backlog |
| **Awning state** | open/closed for business | awning rolled out = on-duty; rolled up = off-duty |
| **Light** | focus / activity | a lit lantern / golden window = active; a dark window = idle; a red lantern = alert |
| **Color accent** | the one to watch | a single gold bell / gold flag / gold window marks the focal station; everything else stays in the warm neutral palette |

## Status Encodings

### Running vs Idle
- **Running**: chimney smoke, awning out, animal mid-action, lit lantern, a queue at the door.
- **Idle / waiting**: no smoke, awning half-up, a dozing helper, an hourglass flag, an empty tray.
- **Stopped / broken**: no smoke + a red flag + a Repair animal approaching; a cold forge; a stalled cart.

### Done vs In-progress
- **Done**: a checkered flag on the rooftop; a green stamp on the output crate; a satisfied (eased) expression.
- **In-progress**: a half-finished loaf on the bench; a "加工中" tag; a furrowed effort expression; smoke rising.
- **Not started**: an empty shop with a closed sign; raw material still in sacks at the door.

### Pass vs Fail (at a gate)
- **Pass**: green stamp, the item proceeds to the next shop.
- **Fail**: red stamp, the item joins a pile at the side of the gate.
- **Partial / retry**: half-open gate, a Sorter animal re-routing the item.

### Healthy vs Risk
- **Healthy**: green flag, calm expression, smoke gently rising.
- **Risk / alert**: red pennant, a worried expression, a Firefighter animal approaching, smoke that is too dark/thick.

## Degree Encodings

When the article claims a *degree* (more / less / faster / heavier), encode it physically rather than with a number.

- **More / accumulation**: a taller stack, a thicker sack, more smoke, more animals on the job.
- **Less / drain**: a shorter stack, a thinner sack, a nearly-empty bin.
- **Faster**: more vehicles on the street, motion lines, leaning-forward animals.
- **Slower / bottleneck**: a queue piling up at one shop while the next shop's animal waits idle.
- **Heavier load**: a bigger crate, a Donkey leaning harder into its harness, a bowed shelf.

## Quality Encodings

- **High quality**: a golden bell / gold flag; a pristine output; an eased satisfied expression; a green checkered flag.
- **Low quality / error**: a red flag; a torn / dented output; a furrowed worried expression; a rejected pile.
- **Repaired / recovered**: a visible patch / seam on a mended object; a Repair animal's needle still in frame; a "修复后" tag.

## Encoding Budget

Don't encode everything. Pick **one or two channels** that carry the article's precision and let the rest stay neutral.

Examples:
- An article about a **bottleneck**: encode with *queue length* + *dozing next shop*. Everything else stays calm.
- An article about a **transformation**: encode with *object state chain* (wheat → flour → bread). Everything else stays neutral.
- An article about a **tradeoff**: encode with *scale tilt* + *removed vs kept tags*. Everything else stays balanced.
- An article about a **failure and recovery**: encode with *broken-then-mended object* + *Repair animal*. Everything else stays calm.

## Forbidden Encodings

Do not use:
- floating UI badges / progress bars / percentage dials / KPI tiles
- chart icons (pie / bar / line graph) pasted onto the town
- dense text annotations where a marker would do
- red/green stoplight icons that look like a dashboard
- rainbow color-coding (one accent color is enough)

The state must read as part of the **hand-painted storybook world** — smoke is smoke, a flag is a flag, a stamp is a stamp — not as a UI overlay on a painting.

## Accept / Regenerate

Accept if:
- The article's key state (running/idle, pass/fail, done/in-progress, healthy/risk) is readable from the painting alone.
- The encoding uses storybook-physical channels (smoke, flag, expression, gate, stamp), not UI overlays.
- The encoding budget is respected — one or two channels carry precision; the rest stay neutral.

Regenerate if:
- Every shop has every channel maxed out (over-coded clutter).
- The state markers look like dashboard UI pasted on a painting.
- The state is only readable from a tiny text label, not from the painting itself.
