# Style Anchor Starter Library

## Purpose

The style anchor library used to be text-only. That is not enough for serious deck craft: an anchor must prove it can handle a cover, a proof slide, a system/mechanism slide, and a closing slide before it becomes a direction.

Files:

- `assets/style-anchor-starters.json`: machine-readable starter specs for every local anchor.
- `scripts/validate_style_anchor_starters.py`: verifies starter coverage and required fields.
- `scripts/render_style_anchor_starters.py`: renders starter previews as fixed 1280x720 HTML slides.

## Required Starter Set

Every anchor must have exactly four starters:

| Role | What It Proves | Typical Local Archetype |
| --- | --- | --- |
| `cover` | the visual thesis and first-viewport promise | `split-thesis`, `product-demo-workbench`, `metric-wall` |
| `proof` | evidence/data/table/metric handling | `proof-table-plus-signal`, `metric-wall`, `board-report-grid` |
| `system` | workflow, mechanism, path, loop, or before/after logic | `system-loop`, `demo-path`, `timeline`, `comparison-before-after` |
| `closing` | final rule, ask, decision, or memory object | `quote-evidence` |

If an anchor cannot produce a credible starter for all four roles, it is not mature enough to be a default style anchor.

## Commands

Validate the library:

```bash
python3 scripts/validate_style_anchor_starters.py
```

Render one anchor:

```bash
python3 scripts/render_style_anchor_starters.py --anchor dark-technical-investor --out /tmp/dark-technical-starter
node scripts/screenshot_deck.mjs /tmp/dark-technical-starter --out /tmp/dark-technical-starter/qa
python3 scripts/make_contact_sheet.py /tmp/dark-technical-starter/qa --out /tmp/dark-technical-starter/contact-sheet.png --thumb-width 520 --columns 2
python3 scripts/visual_qa_deck.py /tmp/dark-technical-starter --screenshots /tmp/dark-technical-starter/qa
```

Render all anchors:

```bash
python3 scripts/render_style_anchor_starters.py --anchor all --out /tmp/style-anchor-starters
node scripts/screenshot_deck.mjs /tmp/style-anchor-starters --out /tmp/style-anchor-starters/qa
python3 scripts/make_contact_sheet.py /tmp/style-anchor-starters/qa --out /tmp/style-anchor-starters/contact-sheet.png --thumb-width 360 --columns 4
python3 scripts/visual_qa_deck.py /tmp/style-anchor-starters --screenshots /tmp/style-anchor-starters/qa --fail-on error
```

## How To Use In A Deck

1. Run `select_style_anchors.py` from the Deck Brief.
2. Render starter previews for the top 2-4 anchors.
3. Inspect the contact sheet. Do not pick an anchor only because its cover looks good.
4. Choose or mix directions based on:
   - cover memorability,
   - proof readability,
   - system clarity,
   - closing strength,
   - fit to audience and source material.
5. Write the chosen direction into `style-anchors.md` and style lock.
6. Only then create the deck-specific layout blueprint and asset prompts.

## Bespoke Scene Kit Rule

The renderer must not be a color-swap template. Each anchor needs a recognizable scene kit:

- a distinct cover composition,
- a distinct proof mechanism,
- a distinct system/path mechanism,
- a distinct closing object,
- and enough object vocabulary to guide later image prompts and foreground PPTX objects.

If proof pages all use the same table, or system pages all use the same four-node loop, the library has failed even if the palette looks polished. The contact sheet should make the anchors distinguishable at thumbnail size.

## Acceptance Gates

- The four starters do not all have the same left/right or top/bottom relationship.
- Text sits on quiet fields, cards, strips, or high-contrast surfaces.
- The proof starter has a real table/metric/chart zone, not only decorative badges.
- The system starter has visible direction/order.
- The closing starter leaves one rule or ask, not a new topic.
- Proof/system/closing objects are anchor-specific, not one universal component reused across the library.
- The visual QA report has no overflow/text clipping errors; similarity warnings are inspected against the contact sheet.
- The starter can be adapted to user content without copying any proprietary template.

## Repair Rules

- If the cover is strong but proof is weak, do not use the anchor for dense reports.
- If proof is readable but cover is bland, use the anchor as a content-slide system and pair it with a stronger cover style.
- If the system starter is unclear, change archetype or object families before building user slides.
- If the closing starter feels generic, write a sharper final rule before visual polish.

## Important Boundary

Starter previews are internal design seeds. They may contain anchor names, role labels, and generic sample copy. Final user slides must replace them with real user content and must not expose internal labels such as "starter", "anchor", or "preview".
