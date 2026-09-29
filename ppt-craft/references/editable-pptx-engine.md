# Editable PPTX Engine

## What This Adds

Route B is now a real adapter path, not only a promise. It follows the practical `html2pptx` idea: author a constrained HTML slide, use the browser to read layout and computed styles, then emit native PowerPoint text boxes, shapes, images, tables, charts, and connector lines.

Use this route when the user values PowerPoint editability enough to accept visual constraints.

## Engine Command

```bash
node scripts/html_to_editable_pptx.mjs /path/to/deck --out /path/to/deck.pptx --report /path/to/report.json
python3 scripts/analyze_reference_deck.py --pptx /path/to/deck.pptx
```

Input can be:

- `/path/to/deck/slides/*.html`
- or `/path/to/deck/*.html`

The adapter writes:

- A native `.pptx`.
- A JSON report with object counts and warnings.

## Authoring Contract

Use `assets/editable-slide-template.html` as the starting point.

Required:

- Fixed 16:9 canvas, normally `960pt x 540pt` or `1280px x 720px`.
- Important text in `h1`-`h6`, `p`, `li`, `span`, `small`, `strong`, `em`, or elements marked `data-pptx-text="true"`.
- Wrapper backgrounds/borders/radius on `div`, `section`, `article`, or similar block elements.
- Images as `<img src="/img/example.png">`, not CSS `background-image`.
- Tables as real `<table>` markup with `tr`, `th`, and `td`.
- Charts as a positioned element with `data-pptx-chart` and a small JSON spec.
- Connectors as positioned elements with `data-pptx-connector` or `data-pptx-line`.
- Complex node/edge graphs should use semantic `data-graph-node`, `data-graph-edge`, `data-graph-from`, and `data-graph-to` attributes, then pass `scripts/inspect_relationship_graph.mjs`.
- Solid fills, solid borders, normal opacity.
- Leave extra vertical breathing room between text elements. Browser and PowerPoint font metrics differ; the adapter adds a small text-box safety height, but source HTML should not rely on tightly stacked flow.
- For large display headlines, prefer separate positioned text elements for each line. Do not rely on `<br>` or automatic wrapping for hero-scale Chinese/English titles.

Avoid:

- CSS gradients.
- Complex SVG decorations.
- CSS filters and blend modes.
- Shadow-dependent design.
- Web components and canvas-only visuals.
- Important bare text directly inside a `<div>`.

## Supported Output Objects

| HTML/CSS | PPTX output | Editable |
| --- | --- | --- |
| `h1`-`h6`, `p`, `li`, `span`, `[data-pptx-text]` | Text box | Yes |
| Block with solid background/border/radius | Rectangle or rounded rectangle | Yes |
| `<img>` | Image | Crop/stretch editable as picture |
| `<table>` or `[data-pptx-table="true"]` | Native table | Yes |
| `[data-pptx-chart]` | Native chart | Yes |
| `[data-pptx-connector]`, `[data-pptx-line]` | Native line with optional arrow | Yes |
| `data-pptx-raster="true"` | Screenshot image | Not text-editable |

## Data Attributes

- `data-pptx="ignore"`: skip this element and its visual output.
- `data-pptx-text="true"`: treat this element's text as a text box even if the tag is not normally text.
- `data-pptx-raster="true"` or `data-pptx-mode="raster"`: screenshot this element and insert it as one picture. Use for complex charts, maps, dense decorative groups, or effects PowerPoint cannot represent.
- `data-pptx-chart="bar|line|pie|doughnut"`: create a native chart. Put the data in a child `<script type="application/json">`.
- `data-pptx-chart-spec='{"type":"bar",...}'`: alternate chart spec attribute when a child script is inconvenient.
- `data-pptx-connector` or `data-pptx-line`: create native connector output.
- `data-pptx-from="0,50%"` / `data-pptx-to="100%,50%"`: explicit endpoints inside the connector element.
- `data-pptx-anchor-from="right"` / `data-pptx-anchor-to="left"`: anchor to graph node edges when `data-graph-from/to` points at real nodes.
- `data-pptx-route="straight|orthogonal|elbow|dogleg|avoid|curve"`: route strategy. Orthogonal/elbow/dogleg/avoid export as multiple native line segments; curve exports as native custom geometry with cubic Bezier XML.
- `data-pptx-bend` or graph `route_bend`: optional 0-1 bend control for orthogonal/dogleg routes.
- `data-pptx-waypoints="50%,0;50%,100%"`: explicit intermediate points inside the connector element; use `stage:x,y` for stage-relative points.
- `data-pptx-avoid="node-a,node-b"` and `data-pptx-avoid-gap="24"`: ask the adapter to route around graph nodes for `avoid`.
- `data-pptx-label="proof path"` plus optional `data-pptx-label-position`, `data-pptx-label-offset`, `data-pptx-label-width`, `data-pptx-label-fill`: export an editable line label text box with a native plate.
- `data-graph-bundle`: edge bundle id emitted by the auto-layout renderer for bus-routed parallel lines.
- `data-graph-label-score`: edge label placement score emitted by the auto-layout renderer.
- `data-graph-swimlane`: swimlane/group id emitted by the auto-layout renderer for dense business graphs.
- `data-graph-collapsed="true"`: aggregate node emitted when a repeated/detail subgraph is collapsed.
- Connector style attributes: `data-pptx-arrow="begin|end|both|none"`, `data-pptx-color="#0F766E"`, `data-pptx-width="2"`, `data-pptx-dash="dash"`.
- `data-graph-node="node-id"`: declare a semantic graph node.
- `data-graph-edge="edge-id"`: declare a semantic graph edge.
- `data-graph-from="node-id"` / `data-graph-to="node-id"`: bind a graph edge to semantic node endpoints.

Chart JSON:

```json
{
  "type": "bar",
  "title": "Native object coverage",
  "labels": ["Text", "Shape", "Table", "Chart", "Connector"],
  "series": [
    { "name": "Coverage", "values": [6, 2, 1, 1, 2] }
  ],
  "colors": ["0F766E"],
  "axisColor": "64748B",
  "showLegend": false,
  "yMin": 0
}
```

Supported chart types are `bar`, `line`, `pie`, and `doughnut`. Use raster fallback for complex dashboards, bespoke infographics, maps, charts that depend on custom annotations, or any chart whose visual polish matters more than editability.

Relationship graph contract and inspection:

```bash
python3 scripts/validate_relationship_graph.py deck/relationship-graph.json --require-native --require-active-path --min-layers 3
python3 scripts/render_relationship_graph.py deck
node scripts/inspect_relationship_graph.mjs deck --out deck/qa/relationship-graph-report.json --require-pptx-native --require-layering --require-relation-types --require-active-path --require-connector-anchors --require-connector-labels --require-edge-bundling --require-label-scores --require-swimlanes --require-subgraph-collapse --max-edge-crossings 0 --max-label-overlaps 0 --max-node-crowding 2 --max-edge-density 14 --min-layers 3
```

Use this when a slide contains system maps, loops, architecture diagrams, flywheels, or multiple connector lines. It catches missing node/edge ids, unknown endpoints, missing relation types/layers, missing active paths, SVG paths that would rasterize unexpectedly, native connectors without stable endpoint coordinates/anchors/labels, excess edge crossings, label overlaps, missing edge bundles, missing swimlanes, missing collapsed subgraphs, node crowding, and edge density spikes.

## PPT-Master / HTML2PPTX Lessons

Borrowed ideas:

- Keep a project folder with source, assets, exports, and reports.
- Do not convert arbitrary fancy HTML after the fact; author for PPTX constraints from the first slide.
- Separate native-editable elements from raster fallback regions.
- Generate a report so users know what is editable and what is baked.
- Verify the final PPTX object structure rather than trusting a successful export.
- Do not rely on macOS QuickLook as a chart render test. QuickLook can show tables and connector lines while leaving native Office charts blank. For chart visual regression, use PowerPoint or a working LibreOffice install; otherwise report object-structure evidence only.
- Use HTML as the precision stage for complex relationship diagrams. If the graph must remain editable, author core edges as native connectors with anchors/routes/labels. If the graph is too visually complex, rasterize the atmosphere intentionally and keep foreground labels/nodes/key connectors editable.

Do not vendor upstream code into this skill. Use the local adapter as the stable minimum and route to heavier external engines only when a task needs their full capabilities.

## Workflow For Route B

1. Read `references/intent-intake-and-interview.md` and freeze the route as `editable-pptx`.
2. Create a deck folder:

```text
deck/
  slides/
    01-cover.html
    02-problem.html
  assets/
  exports/
  reports/
```

3. Validate before export:

```bash
python3 scripts/validate_deck_project.py deck --mode editable
node scripts/inspect_relationship_graph.mjs deck --require-pptx-native
```

4. Export:

```bash
node scripts/html_to_editable_pptx.mjs deck --out deck/exports/deck.pptx --report deck/reports/html2pptx-report.json
```

5. Inspect object structure:

```bash
python3 scripts/analyze_reference_deck.py --pptx deck/exports/deck.pptx
```

6. Render with LibreOffice when available:

```bash
python3 scripts/render_pptx_with_libreoffice.py deck/exports/deck.pptx --out-dir deck/qa/libreoffice-render
python3 scripts/make_contact_sheet.py deck/qa/libreoffice-render --out deck/qa/libreoffice-render/contact-sheet.png
python3 scripts/compare_render_regression.py deck --deck-type auto --lo-dir deck/qa/libreoffice-render
```

If LibreOffice is unavailable, report that visual render was not available and provide object-count evidence.

## Quality Gates

Pass only when:

- Export succeeds.
- Report has at least one text box for every text slide.
- Report shows expected `tables`, `charts`, and `connectors` counts when those objects are authored.
- Relationship graph exports with rich connectors should report expected `connector_groups`, expanded `connectors`, and `connector_labels`.
- Relationship graph report has `errors=0` and `warnings=0` for line-heavy slides unless a raster waiver is documented; dense editable graphs should normally show `edge_crossings=0`, `label_overlaps=0`, nonzero `bundled_edges`, nonzero `label_scored_edges`, nonzero `swimlanes`, nonzero `collapsed_nodes` when repeated detail clusters exist, low `node_crowding_score`, and bounded `edge_density_peak`.
- Raster count is intentional and documented.
- Warnings are either zero or explicitly accepted.
- Generated PPTX has expected slide count.
- `analyze_reference_deck.py --pptx` confirms expected slide count and, when used, `chart_count`, per-slide `tables`, and per-slide `charts`.
- LibreOffice render report is `ok=true` and the PDF/PNG contact sheet was inspected when LibreOffice is installed.
- Browser screenshot vs LibreOffice render diff has `errors=0` and `warnings=0` under the appropriate deck-type profile when both render sets are available.
- No crucial text is baked into an image unless the user accepted partial editability.

Fail and revise when:

- A slide exports as mostly raster by accident.
- Important text was bare in a `div` and omitted.
- Gradients/background images are central to the design.
- Text boxes are too small and likely to wrap.
- A hero title wraps or overlaps differently in PPTX than in the HTML screenshot.
- The deck needs visual fidelity that Route B cannot preserve.
