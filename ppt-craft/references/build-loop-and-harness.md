# Build Loop And Harness

The PPT Craft build process is a loop with gates. It is not "generate slides and look at screenshots at the end."

## Build Loop

```text
Digest
-> User Decisions
-> Content IR
-> Narrative Spine
-> Layout Blueprint
-> Slide Design System
-> Relationship Graph Contract (when needed)
-> Blueprint-Aware Asset Prompts
-> Style + Asset Plan
-> Skeleton Slides
-> Foreground Objects
-> Render/Export
-> QA Critic
-> Repair
-> Delivery
```

Each loop iteration should repair a specific failure, not randomly restyle the deck.

## Gate 1: Content Understanding

Pass when:

- content-ir exists
- core thesis is one sentence
- claims and evidence are separated
- numbers and source-sensitive facts are listed
- slide jobs are clear

Fail when:

- the deck starts from visual templates before thesis
- evidence is mixed into decorative copy
- the user would ask "what is this really saying?"

## Gate 2: User Decision Lock

Pass when:

- audience is known or reasonably assumed
- deck job is known
- route/editability is known
- density/page count target is known
- style direction is known
- assets/brand constraints are known

Fail when:

- the agent asks style before reading the material
- the user has not confirmed a decision that changes the route
- route is implied but not stated

## Gate 3: Layout Blueprint

Pass when every slide has:

- an archetype id or documented custom reason
- fixed stage size
- safe area
- claim box
- support box when needed
- visual/evidence box
- loop/path box when the story uses a loop
- contrast mask or quiet field
- intentional empty regions

Fail when:

- text is placed after the image is chosen
- a title can collide with visual subject
- a table/chart has no reserved region
- the loop floats randomly

## Gate 4: Skeleton Slides

Skeleton means layout without final visual polish:

- plain masks
- text boxes with type roles and font sizes
- mandatory text backplates / caption bands / plates
- tables/charts as simplified objects
- image placeholders with exact crop boxes and text-safe/no-go zones
- connectors and loop path
- foreground object families: badges, chips, callouts, evidence plates, leader lines

For line-heavy slides, the skeleton must also declare semantic graph nodes and edges. Read `references/web-rendered-relationship-graphs.md`.

For dense or multi-layer graph slides, add `relationship-graph.json` and pass:

```bash
python3 scripts/validate_relationship_graph.py deck/relationship-graph.json --require-native --require-active-path --min-layers 3
python3 scripts/render_relationship_graph.py deck
```

If the graph uses planned visual slots, prepare assets before rendering:

```bash
# Source-board crop route.
python3 scripts/process_visual_slots.py deck

# Multi-candidate ImageGen/local asset route.
python3 scripts/score_visual_slot_candidates.py deck --write-prompts --write-imagegen-queue --candidates-per-slot 4 --plan-only
# Run built-in ImageGen from asset-prompts/builtin-imagegen-queue.json, then:
python3 scripts/score_visual_slot_candidates.py deck --select
```

The renderer should emit layout diagnostics in `layout-blueprint.json`: `crossings_before`, `crossings_after`, `bundled_edges`, `edge_bundles`, `scored_labels`, `max_label_score`, `swimlanes`, `collapsed_subgraphs`, `node_crowding_score`, `node_overlaps`, `min_node_gap`, and `edge_density_peak`.

Pass when skeleton screenshots already read well in grayscale. If the skeleton is ugly or confusing, styling will not save it.

Required command:

```bash
python3 scripts/generate_asset_prompts.py deck --out deck/asset-prompts
python3 scripts/render_skeleton_deck.py deck --out deck/skeleton
python3 scripts/validate_deck_project.py deck/skeleton --mode html --require-brief --require-blueprint
node scripts/screenshot_deck.mjs deck/skeleton --out deck/qa/skeleton
python3 scripts/make_contact_sheet.py deck/qa/skeleton --out deck/qa/skeleton-contact-sheet.png
```

## Gate 5: Asset Fit

Pass when:

- images follow the asset plan
- image prompts were generated from `layout-blueprint.json` and list text-safe zones
- text-safe regions are quiet
- product/brand assets are real or marked placeholder
- no generated image contains accidental text/logos
- foreground overlays are planned before the image is generated
- planned visual slots have either a clean `visual-slots-report.json` or a clean `visual-slot-candidate-scores.json`

Fail when:

- background competes with claim
- image subject sits under a table/chart
- generated text appears in a non-raster route
- the prompt lets the model freely compose without reserved title/support/evidence/loop zones

## Gate 6: Route-Specific Assembly

### HTML-first

- Use full visual freedom.
- Keep stage fixed.
- Screenshot every slide.
- Export PDF/images only after screenshot QA.

### Editable PPTX

- Use native text/shape/table/chart/connector where possible.
- Large title lines are separate boxes.
- Avoid CSS effects that PPTX cannot represent.
- Use image assets only where editability is not required.

### Hybrid

- Background/image atmosphere may be non-editable.
- Foreground claims, labels, tables, charts, and connectors should stay editable.
- Delivery note must state what is editable.

## Gate 7: QA Critic

Minimum harness:

```bash
python3 scripts/validate_deck_brief.py deck/deck-brief.json
python3 scripts/validate_layout_blueprint.py deck/layout-blueprint.json
python3 scripts/generate_asset_prompts.py deck --out deck/asset-prompts
python3 scripts/render_skeleton_deck.py deck --out deck/skeleton
python3 scripts/validate_deck_project.py deck/skeleton --mode html --require-brief --require-blueprint
node scripts/screenshot_deck.mjs deck/skeleton --out deck/qa/skeleton
python3 scripts/make_contact_sheet.py deck/qa/skeleton --out deck/qa/skeleton-contact-sheet.png
python3 scripts/validate_deck_project.py deck --mode editable --require-brief --require-blueprint --require-asset-prompts
node scripts/screenshot_deck.mjs deck --out deck/qa/html
node scripts/html_to_editable_pptx.mjs deck --out deck/exports/deck.pptx --report deck/reports/html2pptx-report.json
python3 scripts/analyze_reference_deck.py --pptx deck/exports/deck.pptx > deck/reports/pptx-forensics.json
python3 scripts/render_pptx_with_libreoffice.py deck/exports/deck.pptx --out-dir deck/qa/libreoffice-render
python3 scripts/compare_render_regression.py deck --deck-type auto --html-dir deck/qa/html --lo-dir deck/qa/libreoffice-render
node scripts/inspect_relationship_graph.mjs deck --out deck/qa/relationship-graph-report.json --require-pptx-native --require-layering --require-relation-types --require-active-path --require-connector-anchors --require-connector-labels --require-edge-bundling --require-label-scores --require-swimlanes --require-subgraph-collapse --max-edge-crossings 0 --max-label-overlaps 0 --max-node-crowding 2 --max-edge-density 14 --min-layers 3
```

Final decks should also have a polished contact sheet, not only the skeleton contact sheet.

## Visual QA Checks

Check these on screenshots/contact sheet:

- title never collides with image subject
- every text-on-image area has a backplate, strip, ticket, or quiet field
- contact sheet does not collapse into repeated left/right or top/bottom templates
- paragraph line length is readable
- no text is too close to panel edge
- every slide has one dominant idea
- dense tables/charts have enough breathing room
- loop/path is legible and meaningful
- relationship graph nodes, edges, labels, and active path are semantically declared when the slide depends on complex line relationships
- active state is clear if a repeated loop is used
- style is consistent but not monotonous

## PPTX QA Checks

Check these in reports and smoke render:

- expected slide count
- expected text count
- expected table/chart/connector count
- visual slot source/candidate reports pass when generated assets are used
- relationship graph report passes for line-heavy slides
- auto-layout relationship graphs report zero edge crossings and zero label overlaps unless a named waiver exists
- dense business graphs report swimlanes, collapsed subgraphs when repeated detail clusters exist, low node crowding, and bounded edge density
- `raster=0` unless intentional
- warnings are zero or explained
- top fonts are suitable for the deck language
- LibreOffice render report and browser-vs-LibreOffice diff report pass; QuickLook/PowerPoint smoke does not show title wrap collisions

QuickLook is a smoke test, not a full chart regression. Native chart visuals need PowerPoint or LibreOffice.

## Repair Strategy

When QA fails, repair in the correct layer:

| Failure | Repair layer |
| --- | --- |
| Story unclear | Narrative Spine |
| Too many ideas on one slide | Content IR / slide split |
| Text collides | Layout Blueprint |
| Image too busy | Asset Plan / crop / mask |
| Image did not leave text space | Asset prompt plan / regenerate image |
| All slides feel left-right only | Layout archetypes / foreground object kit |
| Complex line graph is hard to edit/export | Web relationship graph contract / native connector grammar |
| PPTX wraps differently | Editable object assembly |
| Style generic | Style Anchors |
| Chart/table unreadable | Layout + density |

Do not repair a layout failure by changing colors. Do not repair a story failure by adding animation.
