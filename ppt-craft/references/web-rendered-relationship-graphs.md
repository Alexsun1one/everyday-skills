# Web-Rendered Relationship Graphs

Use this for slides with complex lines, loops, system maps, process networks, investor evidence maps, architecture diagrams, flywheels, or causal graphs.

The principle: **compose the relationship graph in HTML first, with semantic nodes and edges, then keep core nodes/labels/connectors native-editable in PPTX.** Raster is allowed only for atmosphere, glow, texture, decorative mesh, or background context.

Default priority for serious decks:

```text
1. expression accuracy
2. PPTX-native editability for core graph objects
3. visual polish and depth
4. intentional raster only for atmosphere
```

## Why This Layer Exists

Image generation can create beautiful system-map atmosphere, but it is unreliable for exact text, line endpoints, editability, and repeated graph semantics.

HTML/SVG can do the opposite:

- exact coordinates,
- real text,
- inspectable node/edge topology,
- repeatable line styles,
- screenshot QA,
- export adapter handoff.

Therefore complex PPT slides should use the web renderer as the precision stage, not as a throwaway preview.

## Layer Stack

Use this order:

1. background atmosphere or image texture;
2. quiet fields, masks, and plates;
3. relationship graph rails/connectors;
4. nodes/cards/evidence objects;
5. labels, callouts, numbers, chips;
6. active highlight and final emphasis.

Connectors usually sit under nodes. Labels sit above connectors and must have a plate or quiet field.

## Pre-Render Graph Contract

Before HTML, serious relationship slides should have:

```text
relationship-graph.json
```

Validate it with:

```bash
python3 scripts/validate_relationship_graph.py relationship-graph.json --require-native --require-active-path --min-layers 3
```

If the graph declares planned image slots with `source` / `crop_box` / `out`, prepare those assets before rendering:

```bash
python3 scripts/process_visual_slots.py deck
```

If the deck does not need a hand-positioned bespoke graph, render the contract first:

```bash
python3 scripts/render_relationship_graph.py deck
```

The auto-layout renderer uses layer columns, node roles, priorities, active paths, connector anchors, route hints, and edge labels to create `slides/01-relationship-autolayout.html` plus `layout-blueprint.json`. It now also runs a deterministic layout optimizer:

- **swimlane grouping**: optional `swimlanes` plus node `swimlane` / `group` / `cluster` fields create horizontal business lanes so dense graphs read by domain, not only by layer;
- **subgraph collapse**: optional `subgraphs[].collapsed=true` rewrites repeated detail nodes into aggregate cards and merges duplicate collapsed edges before layout;
- **crossing minimization**: barycentric layer sweeps reorder nodes within each layer and records `crossings_before/after` in `layout-blueprint.json`;
- **node crowding scoring**: node gaps and overlaps are measured as `node_crowding_score`, `node_overlaps`, and `min_node_gap`;
- **edge density scoring**: routed segments are scored on an 8x5 grid as `edge_density_peak` and `edge_density_hot_cells`;
- **edge bundling**: parallel layer-to-layer edges are routed through bus lanes and exported as native multi-segment PPT lines;
- **label placement scoring**: edge labels test multiple positions/offsets and choose the lowest-overlap candidate, recording `data-graph-label-score`.

The graph contract records:

- graph purpose;
- optional `views[]` for multi-slide graph splits;
- optional view-level `visual_slots[]` for planned image crops, transparent icons, and metaphor blocks;
- optional swimlanes and collapsed subgraphs;
- layers and their visual treatment;
- node ids, roles, priority, coordinates;
- edge ids, endpoints, relation type, strength, active path, export policy;
- optional `layout_policy` for crossing minimization, edge bundling, and label placement;
- optional `layout_policy` for node crowding and edge density thresholds;
- which raster layers are allowed.

This is the relationship equivalent of `layout-blueprint.json`: it prevents beautiful but ambiguous diagrams.

## Planned Image Slots

Complex relationship slides can use generated images, but the image must be planned before generation or cropping.

Use view-level `visual_slots[]` when the slide needs:

- a small metaphor block instead of a full-slide background;
- a cropped piece from a larger generated image board;
- a transparent PNG ornament or icon-like cue;
- a quiet evidence texture that supports the graph without carrying critical text.

Each slot must declare the placement first and, when generated from a larger image board, the reproducible crop contract:

```json
{
  "id": "data-flywheel-ornament",
  "role": "flywheel texture",
  "box": { "x": 46, "y": 210, "w": 176, "h": 98 },
  "src": "assets/ornament-data-flywheel-transparent.png",
  "source": "assets/visual-ornaments-contact-sheet.png",
  "out": "assets/ornament-data-flywheel-transparent.png",
  "crop_box": { "x": 0.6663, "y": 0.119, "w": 0.2978, "h": 0.7598 },
  "output_size": { "w": 640, "h": 360 },
  "fit": "contain",
  "transparent": true,
  "transparent_threshold": 38,
  "transparent_chroma": 34,
  "transparent_softness": 20,
  "blend_mode": "screen",
  "opacity": 0.86,
  "crop": "right panel from generated ornament sheet",
  "prompt": "data moat flywheel ornament, no text, transparent background"
}
```

Rules:

- Plan the slot in the graph/view contract before generating the image.
- If one generated image contains several useful motifs, cut it into named assets and place each cut into its own slot.
- Prefer transparent PNGs for icon-like, symbolic, or edge-floating ornaments.
- Run `python3 scripts/process_visual_slots.py deck` before `render_relationship_graph.py` whenever slots declare `source` / `crop_box` / `out` fields.
- The generated `asset-prompts/visual-slots-report.json` must have `ok=true`, zero errors, and no pending slots unless the missing asset is intentionally waived.
- If the slot will be generated as several alternatives, run `python3 scripts/score_visual_slot_candidates.py deck --write-prompts --write-imagegen-queue --candidates-per-slot 4 --plan-only`, execute the built-in ImageGen queue, then run `python3 scripts/score_visual_slot_candidates.py deck --select` before graph rendering.
- Keep necessary text, labels, numbers, nodes, and connectors outside the image.
- Do not stretch a full image across the whole slide when the slide only needs a small local visual cue.
- The renderer writes `visual_assets` into `layout-blueprint.json`; QA should treat missing assets, wrong slot dimensions, or text overlap as build failures.

## Data Contract

Every serious graph element needs a stable semantic id.

```html
<div class="node" data-graph-node="signal" data-graph-role="input">...</div>

<div
  class="edge"
  data-graph-edge="signal-proof"
  data-graph-from="signal"
  data-graph-to="proof"
  data-graph-layer="evidence"
  data-graph-relation="proves"
  data-graph-strength="strong"
  data-graph-active="true"
  data-pptx-connector
  data-pptx-from="0,50%"
  data-pptx-to="100%,50%"
  data-pptx-anchor-from="right"
  data-pptx-anchor-to="left"
  data-pptx-route="orthogonal"
  data-pptx-label="proof path"
  data-pptx-arrow="end"
  data-pptx-color="#63CAFF"
  data-pptx-width="2">
</div>
```

Required:

- `data-graph-node`: stable node id.
- `data-graph-edge`: stable edge id.
- `data-graph-from` / `data-graph-to`: semantic endpoints.
- `data-graph-layer`: semantic layer such as `input`, `reasoning`, `evidence`, `risk`, `decision`, `feedback`.
- `data-graph-relation`: what the edge means, such as `feeds`, `transforms`, `proves`, `filters`, `blocks`, `triggers`, `loops`.
- `data-pptx-connector` or `data-pptx-line`: when the line must become native PPTX.
- `data-pptx-from` / `data-pptx-to`: explicit edge endpoints.
- `data-pptx-anchor-from` / `data-pptx-anchor-to`: `auto`, `left`, `right`, `top`, `bottom`, or `center` node anchors when the edge binds to `data-graph-from/to`.
- `data-pptx-route`: `straight`, `orthogonal`, `elbow`, `dogleg`, `avoid`, `curve`, `bezier`, or `cubic`.
- `data-pptx-bend` or graph `route_bend`: optional 0-1 bend control for orthogonal/dogleg routes when a connector must avoid a primary path.
- `data-pptx-waypoints`: semicolon-separated route points for explicit multi-segment lines.
- `data-pptx-avoid`: comma-separated node ids to route around for `avoid`.
- `data-pptx-label`: editable edge label text exported as a PPT text box with an optional native plate.
- `data-graph-bundle`: bundle id for edges that share a bus lane.
- `data-graph-label-score`: placement score emitted by the renderer; low score means clean placement, high score means the label likely fought nodes/edges.
- `data-graph-swimlane`: business swimlane id when the graph has multiple domains or audiences.
- `data-graph-collapsed="true"`: aggregate node that represents a collapsed subgraph.

Optional:

- `data-graph-role`: `input`, `operation`, `proof`, `risk`, `output`, `loop`, `actor`.
- `data-graph-label`: semantic label id.
- `data-graph-active="true"`: marks the current reading path.
- `data-graph-strength`: `weak`, `normal`, `strong`, or `critical`.
- `data-graph-priority`: visual weight 1-5 for nodes.
- `data-pptx-raster="true"`: intentional raster group for complex curved or decorative geometry.
- `data-pptx-label-position`, `data-pptx-label-offset`, `data-pptx-label-width`, `data-pptx-label-fill`: label placement and style controls.

## Export Modes

### Native Connector Mode

Default for serious decks and all core graph relationships.

- Use absolutely positioned line elements with `data-pptx-connector`.
- Multi-segment paths may be authored as several connectors or as one connector with `data-pptx-route` / `data-pptx-waypoints`; the adapter exports them as native PPT line segments.
- Curved paths may use `data-pptx-route="curve"` and are exported as native custom geometry with cubic Bezier XML when supported by `pptxgenjs`.
- Use native node cards and labels as text/shape objects.
- Put labels on connector chips/tickets; avoid labeling very short edges where the chip will collide with node plates.
- For dense technical/consulting diagrams, require label placement scoring and zero label/node overlaps.
- Keep connector styles purposeful: width, color, dash, arrow must map to relation type or layer.
- Dense graphs need a visible active path.

### Hybrid Graph Mode

Best for premium visual polish while preserving editability of the meaning layer.

- Rasterize background graph atmosphere, glow, mesh, or dense decorative lines.
- Keep foreground nodes, labels, chips, charts, and key connectors editable.
- Delivery note states what is raster and what is native.

### Raster Graph Mode

Best only when the final deck is image-first or the graph is pure visual art.

- Entire graph can be baked into an image.
- Important text still needs intentional typography and no fake labels.
- Do not claim PPTX editability for baked text or lines.

## Composition Rules

- Every line must explain a relationship, not decorate empty space.
- Avoid more than three line styles per slide.
- Do not let connectors cross primary title/support text-safe zones.
- Bundle parallel lines into rails when there are more than four edges, or whenever multiple edges share the same source/target layer pair.
- Use swimlanes when a graph mixes audiences or domains such as demand, engine, proof, economics, privacy, or operations.
- Collapse repeated detail subgraphs before layout; do not show seven similar ROI cases or three security primitives as separate full nodes unless the slide is specifically about them.
- Treat node crowding and edge density as first-class readability failures, not cosmetic warnings.
- Push backward/feedback paths around the graph perimeter instead of drawing diagonals through the system.
- Put arrowheads only where direction matters.
- Use node size and position to express hierarchy; do not make all nodes equal.
- Reserve one active path per slide when the graph is dense; complex graphs are read by guided path, not by showing every relationship at equal weight.
- Multi-layer graphs should show layer lanes, bands, depth, or explicit label chips.
- Do not exceed six visual edge styles unless the style map is documented in the graph contract; semantic relation types may be richer than visual styles.
- If labels are small, put them on chips/tickets, not bare on texture.

## Inspection Command

```bash
node scripts/inspect_relationship_graph.mjs <deck> --out <deck>/qa/relationship-graph-report.json --require-pptx-native --require-layering --require-relation-types --require-active-path --require-connector-anchors --require-connector-labels --require-edge-bundling --require-label-scores --require-swimlanes --require-subgraph-collapse --max-edge-crossings 0 --max-label-overlaps 0 --max-node-crowding 2 --max-edge-density 14 --min-layers 3
```

Default behavior fails on warnings. Use this before editable PPTX export and after major graph edits.

The inspector checks:

- graph nodes have stable ids;
- edges have stable ids and semantic endpoints;
- native PPTX connectors declare explicit coordinates;
- native connectors declare anchors/routes/labels when the graph route requires them;
- dense graph routes expose bundles when parallel edge groups exist;
- scored edge labels avoid node and label overlaps;
- routed native edge segments stay under the configured crossing threshold;
- swimlanes exist when the graph mixes multiple business domains;
- collapsed subgraphs exist when the source contains repeated detail clusters;
- node crowding stays under the configured score threshold;
- edge density stays under the configured peak threshold;
- endpoints reference existing nodes;
- SVG edges are either intentionally rasterized or flagged;
- dense graphs have layers and active paths;
- every edge declares a relation type;
- graph objects remain inside the slide stage.

## Relationship With Visual QA

Run both:

```bash
node scripts/inspect_relationship_graph.mjs <deck> --require-pptx-native
python3 scripts/visual_qa_deck.py <deck> --screenshots <deck>/qa --require-blueprint-zones
```

The graph inspector checks semantic/export readiness. Visual QA checks rendered readability, contrast, overflow, repeated layouts, and text-safe-zone obedience.

For editable PPTX relationship graphs, also compare browser and LibreOffice render output after export:

```bash
python3 scripts/compare_render_regression.py <deck> --deck-type auto
```

This catches Office-specific shifts such as missing slot images, broken connector groups, text metric drift that clips labels, or page count mismatch.

## PPTX Handoff Rules

- Native connectors are exported by `scripts/html_to_editable_pptx.mjs`.
- SVG paths are not automatically converted into editable PPTX geometry. Mark as raster intentionally or rewrite as native connector segments.
- Complex Bezier paths can now export through `data-pptx-route="curve"` as native custom geometry; use it deliberately and verify the PPTX XML/object report.
- If a graph contains charts/tables, use native `data-pptx-chart` and real `<table>` markup for the proof layer.

## Smoke Template

Start from:

```text
assets/complex-relationship-slide-template.html
assets/multilayer-relationship-slide-template.html
```

They demonstrate:

- semantic graph nodes;
- semantic graph edges;
- semantic layers and relation types;
- native PPTX connector attributes;
- readable node labels;
- a bottom loop chip rail.
