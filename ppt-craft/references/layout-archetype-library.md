# Layout Archetype Library

Layout archetypes are the reusable skeletons that stop PPT Craft from improvising every slide. They sit between the narrative spine and the final HTML/PPTX rendering.

Use them after `deck-brief.json`, `content-ir.json`, and `narrative-spine.md`, before visual styling or image generation.

## Core Rule

Every serious slide should declare an archetype in `layout-blueprint.json`:

```json
{
  "id": "04-proof",
  "archetype": "proof-table-plus-signal",
  "job": "prove that value hides in backstage operating work",
  "claim": { "x": 72, "y": 84, "w": 700, "h": 150 },
  "support": { "x": 72, "y": 248, "w": 650, "h": 54 },
  "evidence": { "x": 72, "y": 328, "w": 760, "h": 290 },
  "visual": { "x": 880, "y": 350, "w": 270, "h": 220 }
}
```

If a box is omitted, the skeleton renderer can use the archetype default. If a box is present, the slide override wins.

## Available Archetypes

The machine-readable library is `assets/layout-archetypes.json`.

| Archetype | Use When | Core Slots |
| --- | --- | --- |
| `split-thesis` | cover, thesis, section opener | claim, support, visual |
| `system-loop` | flywheel, workflow, operating model | claim, support, visual, loop |
| `proof-table-plus-signal` | cases, traction, dense evidence | claim, support, evidence, visual |
| `demo-path` | first action, validation path, go-to-market | claim, support, visual, evidence |
| `productization-ladder` | service to product, maturity, compounding | claim, support, evidence, visual |
| `timeline` | history, roadmap, project sequence | claim, support, visual |
| `metric-wall` | traction, benchmarks, board summary | claim, support, evidence |
| `quote-evidence` | closing rule, principle, memorable quote | claim, support, visual/loop |
| `product-demo-workbench` | software/product walkthrough | claim, support, visual, evidence |
| `board-report-grid` | report, consulting, board update | claim, evidence, visual |
| `comparison-before-after` | tension, transformation, before/after | claim, support, visual, evidence |

## Selection Guidance

Choose by slide job, not by taste:

- "Name the thesis" -> `split-thesis`.
- "Explain a repeatable system" -> `system-loop`.
- "Prove with cases" -> `proof-table-plus-signal`.
- "Show how to begin" -> `demo-path`.
- "Show compounding" -> `productization-ladder`.
- "Show sequence over time" -> `timeline`.
- "Make numbers dominate" -> `metric-wall`.
- "Leave one rule" -> `quote-evidence`.
- "Show the product" -> `product-demo-workbench`.
- "Report status and decisions" -> `board-report-grid`.
- "Show wrong model vs right model" -> `comparison-before-after`.

## Skeleton First

After assigning archetypes, run:

```bash
python3 scripts/generate_asset_prompts.py /path/to/deck --out /path/to/deck/asset-prompts
python3 scripts/render_skeleton_deck.py /path/to/deck --out /path/to/deck/skeleton
python3 scripts/validate_deck_project.py /path/to/deck/skeleton --mode html --require-brief --require-blueprint
node scripts/screenshot_deck.mjs /path/to/deck/skeleton --out /path/to/deck/qa/skeleton
python3 scripts/make_contact_sheet.py /path/to/deck/qa/skeleton --out /path/to/deck/qa/skeleton-contact-sheet.png
```

The skeleton must pass before final visual styling. If a skeleton is confusing, the finished slide will still be wrong after adding images and polish.

The skeleton is not only a rectangle map. It must expose:

- type role and expected size for each text region;
- required text backplates or quiet fields;
- foreground object family per region;
- image visual region;
- text-safe/no-go zones that image generation must respect.

## Acceptance

Pass:

- every slide has an archetype or a deliberate custom reason;
- every important element sits inside a reserved box;
- every text region has a type role and plate/backplate plan;
- every generated image has reserved text-safe zones and foreground overlay plan;
- the contact sheet shows varied but coherent layouts;
- dense slides have enough room before visual styling;
- loop/path slides reserve a path region and direction.

Fail:

- multiple slides use the same generic card grid without narrative reason;
- text regions are defined after background images;
- image prompts are written before the blueprint/design system;
- skeleton is only boxes and cannot guide typography or image composition;
- a proof table or chart appears without an evidence box;
- a loop is decorative and not tied to the deck's argument;
- skeleton labels already feel cramped.
