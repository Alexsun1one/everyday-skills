# Series & Chaining / 系列串联

When an idea needs more than one image, chain them into **one storybook** — a shared town world, a shared cast, a shared palette, and a progressing throughline. The reader should feel they are turning the pages of one book, not looking at N unrelated paintings.

## What Makes a Series a Storybook

Three things tie a set of images together:

1. **One town world.** The same geography, the same shops, the same streets appear across the set. The harbor in image 1 is the same harbor in image 4.
2. **One cast.** The Fox Researcher is always the Fox Researcher; the Bear Miller is always the Bear Miller. Reuse species+trade for the same role. Background townsfolk can vary.
3. **One throughline.** A single thread advances across the set: the town wakes up, gets busy, hits a snag, recovers, ships. Or the booklet drills deeper: panorama → cutaway → close-up → resolution.

## Series Patterns

### Pattern A — The Waking Town (a day in the life)
A town across time. The throughline is the **time of day** and the **rising/falling busyness**.

- Page 1 (dawn): quiet town, only the Baker's chimney smokes; a Courier gears up.
- Page 2 (morning): main street fills, every shop open, handoffs flowing.
- Page 3 (noon): peak busy — a panorama, smoke from every chimney, the square is full.
- Page 4 (afternoon): a snag — one shop's flag goes red, a queue backs up, a Firefighter approaches.
- Page 5 (evening): resolved — green flags, the output ships, a checkered flag on the rooftop.

Best for: a day-in-the-life, a launch day, a process that runs over time.

### Pattern B — The Drill-Down (zooming in)
The throughline is **depth**: each page zooms one level deeper.

- Page 1 (panorama): the whole town — the system at a glance.
- Page 2 (cutaway): one tower in the town, cut open — the system's layers.
- Page 3 (close-up): one role in one floor — "what does the ___ actually do."
- Page 4 (two-page spread): a comparison — old way vs new way of doing that role's job.

Best for: onboarding, "how does our system work," explainers.

### Pattern B' — The Build-Up (zooming out)
Inverse of B. The throughline is **scope**: each page widens.

- Page 1 (close-up): one role's tools and action.
- Page 2 (cutaway): the role's place in its building.
- Page 3 (panorama): the building's place in the whole town.
- Page 4 (two-page spread): this town vs a rival town / old town.

Best for: establishing context, "why this matters," building up to a comparison.

### Pattern C — The Same Town, Different Question
Each page revisits the **same** town and answers a different question about it.

- Page 1: "who hands off to whom?" (handoff street)
- Page 2: "where's the bottleneck?" (a red flag, a queue)
- Page 3: "what happens when it fails?" (a red flag, a Firefighter, a recovery)
- Page 4: "how does it look when it's healthy?" (green flags, smoke rising calmly)

Best for: a multi-angle analysis of one system.

### Pattern D — The Comparison Book
A two-page-spread series. Each spread compares a different axis.

- Spread 1: old process vs new process.
- Spread 2: team A's workflow vs team B's workflow.
- Spread 3: small scale vs large scale.

Best for: a benchmark / state-of-play article.

## Throughline Motifs

A motif is a small recurring element that pays off at the end. Plant it early, pay it off late.

- a **golden bell** on one shop that finally rings at the climax
- a **parcel** that one animal starts carrying in page 1 and finally delivers in the last page
- a **red flag** that appears in page 2 (foreshadowing a snag) and goes green in the last page
- a **dozing helper** who finally wakes up when needed
- a **hot-air balloon** that drifts across every page, higher each time, until it lands at the climax

Motifs give a series the feeling of a story, not a deck.

## Consistency Rules

Across a series, hold these constant:

- **Town world**: same geography, same shops in the same places (a role's shop is always the corner bakery, not sometimes a dock).
- **Cast**: same species+trade for the same role. The Fox Researcher is always a fox in a green vest.
- **Palette & medium**: same warm watercolor palette, same paper grain, same hand-lettering.
- **Signage style**: same shop-sign lettering, same flag shapes.
- **State coding semantics**: smoke always means running; a red flag always means alert.

Vary these:

- **time of day / weather** (across a "day in the life")
- **which shop is the focal zone** (each page can focus a different shop)
- **the throughline state** (the town gets busier, snags, recovers)

## Mode Pairs Across a Series

A series often pairs modes. Common pairings:

- **Panorama opener → Cutaway middle → Close-up detail → Two-Page resolution.** The classic explainer arc.
- **Two-Page problem → Cutaway diagnosis → Close-up fix → Panorama healthy state.** The classic incident arc.
- **Close-up role → Cutaway team → Panorama org.** The classic "zoom out" arc.

## Series QA

A series passes if:

- A reader flipping through feels one town, one cast, one story.
- Each page adds new information (a new role, a new depth, a new question) — not a rehash.
- The throughline state visibly advances (busyness rises/falls, a snag appears/resolves, a parcel moves).
- The payoff motif pays off.

A series fails if:

- The pages could be shuffled without losing meaning (no throughline).
- The cast or palette drifts between pages.
- Every page shows the same zoom and the same focal zone.

## Output for a Series

When planning a series, return:

```text
series plan:
- pattern (waking town / drill-down / build-up / same-town-different-question / comparison book):
- page count:
- per-page: mode · focal zone · throughline state · new content
- throughline motif:
- consistency held (world, cast, palette, signage, state semantics):
- varied (time, focal, state):
```

Then generate one page at a time, in order, reusing the held invariants.
