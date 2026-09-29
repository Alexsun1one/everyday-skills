# Visual QA Automation

Use automated visual QA after screenshots and before delivery. It does not replace human taste, but it catches the boring failures that repeatedly waste time: repeated layouts, low contrast, clipped text, visible overflow, and text that violates the layout blueprint.

## Scripts

- `scripts/visual_dom_metrics.mjs`: opens `slides/*.html` in Playwright and records DOM-level issues:
  - elements outside the slide stage,
  - text boxes that actually clip their text,
  - text contrast below the configured threshold,
  - stage-relative bounding boxes for real text nodes.
- `scripts/visual_qa_deck.py`: reads slide screenshots and the DOM report, then writes:
  - `qa/visual-qa-report.json`,
  - `qa/visual-qa-report.md`.
- `scripts/compare_render_regression.py`: after editable PPTX export and LibreOffice rendering, compares browser screenshots against LibreOffice PNG pages and writes:
  - `qa/render-diff/render-diff-report.json`,
  - `qa/render-diff/render-diff-contact-sheet.png`.

By default, `visual_qa_deck.py` fails on warnings as well as errors. A warning is a blocking issue unless the delivery note names a deliberate waiver.

## Required Order

```bash
python3 scripts/validate_deck_project.py <deck> --mode html
node scripts/screenshot_deck.mjs <deck> --out <deck>/qa
python3 scripts/make_contact_sheet.py <deck>/qa --out <deck>/qa/contact-sheet.png
python3 scripts/visual_qa_deck.py <deck> --screenshots <deck>/qa
```

If screenshots do not exist yet, the QA script can run the screenshot harness:

```bash
python3 scripts/visual_qa_deck.py <deck> --auto-screenshot
```

For serious decks, make missing blueprint zones a hard failure:

```bash
python3 scripts/visual_qa_deck.py <deck> --screenshots <deck>/qa --require-blueprint-zones
```

For editable PPTX, run the Office render regression after LibreOffice has produced PNG pages:

```bash
python3 scripts/compare_render_regression.py <deck> --deck-type auto
```

## What It Detects

### Layout Similarity

The screenshot layer computes luminance, edge, and occupied-block features for every slide pair. Similarity findings mean the deck may be relying on the same layout skeleton too often.

Repair:
- change archetype,
- move from left/right to path, spread, table, map, cutaway, object stage, or poster grammar,
- change the foreground object system before changing colors.

### Contrast

The DOM layer computes text color against the nearest visible background. Hard errors mean important text may not be readable on real screens or exports.

Repair:
- add a plate, strip, scrim, ticket, or quiet field,
- switch foreground/background tokens,
- avoid accent-on-accent or muted-on-light combinations.

### Overflow

The DOM layer checks slide-stage overflow and true text clipping. It ignores intentionally clipped decorative children inside a clipped parent, but text clipping remains a hard failure.

Repair:
- split the slide,
- enlarge the text box,
- move the object,
- shorten copy only when the narrative permits it.

### Blueprint Text-Safe Zones

When `layout-blueprint.json` or `asset-prompts/asset-prompts.json` exists, the QA layer treats these regions as the contract for readable editable text:

- `claim`,
- `support`,
- `evidence`,
- `loop`,
- explicit `text_safe_zones`.

The DOM layer reports each real text box in slide coordinates. The QA layer scales the blueprint to the rendered stage and fails any text box above the minimum font size that does not sit fully inside one declared zone.

Text inside declared relationship graph nodes or graph labels (`data-graph-node`, `data-graph-label`) is handled by `inspect_relationship_graph.mjs` instead of the generic text-safe-zone check. This prevents valid node labels on their own plates from being mistaken for random text pasted over an image.

Repair:
- move the text into its reserved region,
- expand the reserved zone in the blueprint and rerender the skeleton,
- add the missing zone to `asset-prompts/asset-prompts.json`,
- add a plate/ticket/scrim inside the zone when the background is visually busy.

### Edge Pressure

The screenshot layer scans high-detail pixels near the slide edge. This catches elements that visually feel cut off even when the DOM technically fits.

Repair:
- restore safe margins,
- crop intentionally,
- or add a full-bleed rationale.

## Pass Criteria

- `errors=0` is required before delivery.
- `warnings=0` is required before delivery unless the delivery note contains an explicit named waiver.
- Similarity warnings are not automatically conceptually wrong, but the default harness still blocks them. Fix the archetype/object grammar, or write a deliberate waiver.
- For non-trivial decks, `--require-blueprint-zones` should pass: every meaningful text box must land inside a declared text-safe zone.
- For editable PPTX, render diff should also pass with zero errors/warnings using the right deck-type profile when both browser screenshots and LibreOffice PNG pages exist. Browser QA passing alone does not prove Office render fidelity.

## Escape Hatches

Internal diagnostic text can be excluded with:

```html
<div data-visual-qa-ignore="true">...</div>
```

Use this only for internal starter metadata, not user-facing slide content.
