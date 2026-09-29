---
name: ppt-craft
description: Create, redesign, or convert presentation decks with a world-class slide harness. Use when the user asks to make PPT/PPTX/slides/deck/演示文稿/幻灯片, convert source material into a deck, beautify an existing deck, create an HTML presentation, produce an editable PowerPoint, export PDF/PPTX/slide images, generate style directions for a presentation, or improve a deck's visual polish, motion, narrative, density, or shareability. Combines HTML-first deck craft, visual style discovery, editable-PPTX route boundaries, raster slide-image generation, and screenshot-backed QA. Trigger words include PPT, pptx, presentation, slide deck, keynote, pitch deck, report deck, 课件, 路演, 汇报, 提案, 生成PPT, 做PPT, 美化PPT, 转PPT, HTML slides, editable PPTX, 导出PDF, 视觉方向, 三版风格, 丝滑演示.
---

# PPT Craft / 幻灯片工坊

PPT Craft turns source material into a deck that is beautiful, easy to present, easy to share, and honest about editability. It is a **conductor skill**: use the light local harness for HTML preview, screenshots, and validation; use heavier PPTX/image engines only when their route is the right tradeoff.

Default response language follows the user. For Chinese users, write Chinese deck copy unless the source or user says otherwise.

## First Decision

Choose one route before designing. If the user did not specify a format, default to **Route A: HTML-first extreme beauty**, then offer PDF/PPTX/image exports after the first validated deck exists. Only let Route B override the default when native PowerPoint editability is a hard requirement.

| Route | Choose when | Main promise | Tradeoff |
| --- | --- | --- | --- |
| **A. HTML-first deck** | User wants maximum beauty, motion, browser presentation, web sharing, PDF export, or is still exploring style | Highest visual ceiling, smooth previews, screenshot QA | PPTX editability is not guaranteed |
| **B. Editable PPTX** | User says colleagues must edit text/shapes/tables/charts in PowerPoint, or asks for native editable PPTX | PowerPoint objects remain editable | Visual freedom is constrained from the first HTML/PPTX decision |
| **C. Raster image deck** | User wants social-sharing slides, NPC/cute/story cards, or image-first visual impact | Image quality and style freedom | Slides are pictures, not editable text |
| **D. Existing deck beautify** | User provides a finished `.pptx` and wants polish | Preserve or deliberately restructure based on one discriminator | Must clarify whether page count/order stays fixed |

If a source `.pptx` is provided, ask one discriminator only when ambiguous: **"Should the original page count/order and each slide's wording be preserved, or can I restructure it into a new story?"** Preserve -> Route D; restructure -> Route A/B.

## Core Workflow

1. **Digest before asking.** If the user provides a document, prompt, PPTX, PDF, or URL, first extract the story, audience clues, claims, assets, and density. If a reference deck is provided, run or manually follow `references/reference-deck-forensics.md`.
2. **Run the intake dialog.** Draft a Deck Brief v0, infer sensible defaults, then ask the few high-leverage questions that change audience, deck job, route, density/page count, style, or preservation constraints. When native UI dialog tools are available, use them for grouped choices; otherwise present concise options. Read `references/intent-intake-and-interview.md` and `references/intake-dialog-protocol.md`.
3. **Freeze a Deck Brief.** Write: audience, deck job, final format, density mode, narrative arc, assets, constraints, and verification plan. For branded decks, collect or fetch logo/product/UI assets before styling.
4. **Use the system architecture for serious decks.** For high-stakes or multi-slide work, create the required artifacts: `deck-brief.json`, `content-ir.json`, `narrative-spine.md`, `style-anchors.md`, `layout-blueprint.json`, and `asset-plan.md`. Treat final styling as a fidelity restore of the blueprint/skeleton, not a fresh generation. Read `references/system-architecture.md` and `references/design-practice-bridge.md`.
5. **Choose the world-class pattern.** Match the deck to a proven narrative and slide archetype set before designing pixels. Read `references/world-class-deck-patterns.md`.
6. **Find style/template anchors and starter previews.** For non-trivial decks, run the local anchor selector first, then render starter previews for the strongest anchors. Each candidate direction must prove cover, proof, system, and closing slides before full-deck work. For high-polish/high-stakes decks, generate ImageGen visual oracle plates and extract `visual-tokens.json` before implementation. Read `references/style-anchor-library.md`, `references/style-anchor-starter-library.md`, `references/template-style-library.md`, and `references/imagegen-first-visual-oracle.md`.
7. **Select layout archetypes and design composition before decoration.** Every serious slide must declare an archetype or a deliberate custom reason, then reserve pixel regions in `layout-blueprint.json`. Read `references/layout-archetype-library.md` and `references/layout-first-composition.md`.
8. **Lock the slide design system before generating images.** Define type roles, font scale, backplates, line/icon grammar, object richness, and image text-safe rules. For complex system maps or line-heavy slides, also define the web-rendered relationship graph contract before final styling. Read `references/slide-design-system.md` and `references/web-rendered-relationship-graphs.md`.
9. **Generate blueprint-aware asset prompts and planned visual slots.** Before image generation, run `scripts/generate_asset_prompts.py` so every image prompt knows visual region, text-safe zones, foreground overlays, no-go zones, and route-specific no-text policy. For relationship/system slides that use local generated ornaments or crops, declare `visual_slots[]` first. Use `scripts/process_visual_slots.py` for source-board crops, or `scripts/score_visual_slot_candidates.py` for multi-candidate ImageGen/local assets before rendering. Read `references/blueprint-aware-asset-generation.md` and `references/asset-and-render-regression.md`.
10. **Render and review the skeleton first.** Run `scripts/render_skeleton_deck.py`, screenshot it, and inspect a contact sheet. The skeleton must show geometry, type roles, plates/backplates, object families, and asset constraints. If it fails, repair the brief/spine/archetype/blueprint/design system before styling.
11. **Make visual direction visible.** Start from the local starter previews and ImageGen oracle when visual quality is the risk, then produce 3 real first-slide previews or 3 short direction cards using user content unless the user gave a strict brand/template or asked to proceed directly. Read `references/visual-direction-harness.md`.
12. **Lock the route contract.** For HTML-first/editable/raster/export decisions, read `references/routing-and-contracts.md` and the relevant section of `references/export-contracts.md`.
13. **Build the deck.** Use one source of truth:
   - HTML-first: copy `assets/deck_index.html`, create `slides/*.html`, and keep slide pages fixed at 1920x1080.
   - Editable PPTX: start with `assets/editable-slide-template.html`, follow `references/editable-pptx-engine.md`, then run `scripts/html_to_editable_pptx.mjs`.
   - Raster image deck: write outline -> per-slide prompts -> generate images -> merge/export.
14. **Run QA before delivery.** At minimum: validate structure with `scripts/validate_deck_project.py`, screenshot representative slides with `scripts/screenshot_deck.mjs` when Playwright is available, run `scripts/visual_qa_deck.py` for similarity/contrast/overflow checks, run `scripts/inspect_relationship_graph.mjs` when slides contain complex node/edge systems, and run the checklist in `references/qa-checklist.md`. For editable PPTX, render through LibreOffice and run `scripts/compare_render_regression.py` when both browser and LibreOffice PNGs exist.
15. **Deliver with a route note.** State file locations, chosen route, slide count, exports, what is editable, and what was verified.

## Style Rules

- Make the deck feel made for **this topic**, not a template reskin.
- Use one visual thesis: a committed typography system, palette, spacing rhythm, image policy, and motion tone.
- Never put internal labels such as "Option A", "preview", "template", or prompt notes on slides unless the user asked for those words.
- Match density to use: live talk -> fewer words/more slides; async reading -> structured detail, tables, captions, and self-contained slides.
- Keep slide content inside a fixed 16:9 canvas; split overcrowded slides instead of shrinking text into mush.
- Do not use emoji as structural icons. Use SVG/icon fonts or text labels.
- For branded or product decks, official assets beat guessed colors. A recognizable brand/product name requires its logo/product/UI asset or an explicit placeholder.

## Route References

Read only what the task needs:

- `references/upstream-synthesis.md` — distilled lessons from `ppt-master`, `huashu-design`, `frontend-slides`, and `baoyu-slide-deck`.
- `references/routing-and-contracts.md` — route decision tree, deck brief, density modes, source handling.
- `references/intent-intake-and-interview.md` — digest-first intent understanding and the 0-3 question rule.
- `references/intake-dialog-protocol.md` — how to ask the user for confirmation after understanding the document, with recommended choices and agent judgment.
- `references/system-architecture.md` — full production architecture: Deck Brief, Content IR, Narrative Spine, Style Anchors, Layout Blueprint, Asset Plan, Render Targets, QA Critic.
- `references/design-practice-bridge.md` — borrow design-practice methodology: skeleton before skin, token discipline, restore fidelity, render-critique loop.
- `references/reference-deck-forensics.md` — how to study a supplied PPTX/PDF/template and borrow its system without copying it.
- `references/world-class-deck-patterns.md` — investor, keynote, consulting, report, training, and product-demo deck patterns.
- `references/style-anchor-library.md` — local world-class style/template anchor library and how to turn anchors into directions.
- `references/style-anchor-starter-library.md` — starter preview library: every anchor must prove cover/proof/system/closing before use.
- `references/template-style-library.md` — how to scout and map beautiful template/style anchors to a user's deck.
- `references/layout-archetype-library.md` — reusable page skeletons, archetype selection rules, and skeleton-first acceptance.
- `references/layout-first-composition.md` — pixel blueprint, safe regions, contrast planning, loop/path grammar, and editable-PPTX layout safeguards.
- `references/slide-design-system.md` — typography, font scale, text backplates, line/icon grammar, foreground object kit, and skeleton design-system requirements.
- `references/web-rendered-relationship-graphs.md` — HTML/SVG-first complex graph contract for nodes, connectors, labels, and PPTX handoff.
- `references/blueprint-aware-asset-generation.md` — image generation contract driven by layout blueprint, text-safe zones, and foreground overlay plan.
- `references/asset-and-render-regression.md` — visual slot multi-candidate scoring and browser-vs-LibreOffice render diff gates.
- `references/build-loop-and-harness.md` — gated build loop from skeleton to export, with layer-specific QA and repair rules.
- `references/editable-pptx-engine.md` — constrained HTML-to-native-editable PPTX adapter workflow, supported elements, and failure gates.
- `references/visual-direction-harness.md` — 3-preview style discovery, anti-slop checks, style registers.
- `references/imagegen-first-visual-oracle.md` — generate beautiful ImageGen target plates first, then extract visual tokens before building.
- `references/visual-qa-automation.md` — automated similarity, contrast, clipped text, overflow, and blueprint text-safe-zone checks after screenshots.
- `references/export-contracts.md` — HTML/PDF/PPTX/image export boundaries and editable-PPTX constraints.
- `references/qa-checklist.md` — pass/fail gates before delivery.

## Local Harness

- `assets/deck_index.html` — multi-slide HTML shell with overview, keyboard navigation, iframe stage fitting, and manifest.
- `assets/editable-slide-template.html` — constrained 960pt x 540pt slide skeleton for editable-PPTX-oriented HTML.
- `assets/complex-relationship-slide-template.html` — constrained HTML template for semantic relationship graphs with PPTX-native connectors.
- `assets/multilayer-relationship-slide-template.html` — richer native-editable multi-layer relationship graph template.
- `assets/style-anchor-library.json` — local curated style/template anchor library for HTML-first deck directions.
- `assets/style-anchor-starters.json` — starter specs for cover/proof/system/closing previews for every local style anchor.
- `assets/layout-archetypes.json` — local curated layout archetype library for skeleton-first deck planning.
- `assets/slide-design-system.json` — default machine-readable type scale, color tokens, foreground object kit, and image prompt contract.
- `assets/deck-brief.schema.json` — machine-readable deck brief schema.
- `assets/layout-blueprint.schema.json` — machine-readable layout blueprint schema.
- `assets/asset-prompt.schema.json` — machine-readable schema for blueprint-aware image prompts.
- `assets/visual-tokens.schema.json` — machine-readable schema for oracle/reference visual tokens.
- `assets/relationship-graph.schema.json` — machine-readable contract for layered relationship graphs, nodes, edges, relation types, active paths, and export policy.
- `assets/render-diff-thresholds.json` — deck-type render regression profiles for investor, consulting, product, report, training, and raster decks.
- `scripts/analyze_reference_deck.py` — quick PPTX/PDF forensics: slide/page count, text density, fonts, colors, media, chart/table counts, and representative titles.
- `scripts/select_style_anchors.py` — choose local style anchors from deck type, industry, and style keywords.
- `scripts/render_style_anchor_starters.py` — render HTML starter previews for one or all style anchors.
- `scripts/validate_style_anchor_starters.py` — validate that every style anchor has cover/proof/system/closing starter specs.
- `scripts/validate_deck_brief.py` — validate `deck-brief.json`.
- `scripts/validate_layout_blueprint.py` — validate `layout-blueprint.json`.
- `scripts/render_skeleton_deck.py` — render a low-fidelity HTML skeleton deck from `deck-brief.json` and `layout-blueprint.json`.
- `scripts/render_relationship_graph.py` — render `relationship-graph.json` into editable-oriented auto-layout HTML slide(s) with optional `views[]` multi-slide splits, planned `visual_slots[]` image/crop/transparent asset placements, graph semantics, swimlane bands, collapsed subgraphs, crossing minimization, node crowding / edge density diagnostics, edge bundling, label placement scoring, and native connector attributes.
- `scripts/generate_asset_prompts.py` — generate blueprint-aware image prompts with text-safe zones, foreground overlays, no-go zones, and QA.
- `scripts/process_visual_slots.py` — prepare planned `visual_slots[]` assets from a graph contract: crop source image boards, resize to slot asset dimensions, optionally create transparent PNGs, and write a report before graph rendering.
- `scripts/score_visual_slot_candidates.py` — create ImageGen/local candidate prompt folders and a built-in ImageGen queue for each planned visual slot, score candidate images, and optionally select the best candidate into the slot output path.
- `scripts/extract_visual_tokens.py` — extract palette, tonal bands, image metrics, and token scaffolding from ImageGen oracle or reference slide images.
- `scripts/validate_relationship_graph.py` — validate a pre-render relationship graph contract JSON for layers, node/edge ids, relation types, active paths, and native export policy.
- `scripts/inspect_relationship_graph.mjs` — inspect semantic graph nodes/edges, SVG/native connector export readiness, and relationship graph issues.
- `scripts/make_contact_sheet.py` — build contact sheets from screenshot folders.
- `scripts/html_to_editable_pptx.mjs` — Playwright + pptxgenjs adapter from constrained HTML slides to native PPTX text/shape/image/table/chart/connector objects.
- `scripts/render_pptx_with_libreoffice.py` — render PPTX through LibreOffice headless into PDF and PNG pages for actual Office-engine visual regression.
- `scripts/compare_render_regression.py` — compare browser screenshots against LibreOffice-rendered PNG pages and produce diff heat maps plus a blocking report.
- `scripts/validate_deck_project.py` — deterministic structure/route validation.
- `scripts/screenshot_deck.mjs` — Playwright screenshot helper for `index.html` and `slides/*.html`.
- `scripts/visual_dom_metrics.mjs` — Playwright DOM inspection for slide overflow, clipped text, and text contrast.
- `scripts/visual_qa_deck.py` — screenshot-backed visual QA for repeated layouts, low contrast, and edge/overflow risk.

Run validation from the skill folder or project folder:

```bash
python3 /path/to/ppt-craft/scripts/analyze_reference_deck.py --pptx /path/to/reference.pptx --pdf /path/to/reference.pdf
python3 /path/to/ppt-craft/scripts/select_style_anchors.py --query "AI investor pitch dark technical" --limit 3
python3 /path/to/ppt-craft/scripts/validate_style_anchor_starters.py
python3 /path/to/ppt-craft/scripts/render_style_anchor_starters.py --anchor dark-technical-investor --out /path/to/anchor-starter-preview
python3 /path/to/ppt-craft/scripts/validate_deck_brief.py /path/to/deck/deck-brief.json
python3 /path/to/ppt-craft/scripts/validate_layout_blueprint.py /path/to/deck/layout-blueprint.json --archetypes /path/to/ppt-craft/assets/layout-archetypes.json
python3 /path/to/ppt-craft/scripts/generate_asset_prompts.py /path/to/deck --out /path/to/deck/asset-prompts
python3 /path/to/ppt-craft/scripts/extract_visual_tokens.py /path/to/oracle-slide.png --out /path/to/deck/visual-tokens.json
python3 /path/to/ppt-craft/scripts/validate_relationship_graph.py /path/to/deck/relationship-graph.json --require-native --require-active-path --min-layers 3
python3 /path/to/ppt-craft/scripts/process_visual_slots.py /path/to/deck
python3 /path/to/ppt-craft/scripts/score_visual_slot_candidates.py /path/to/deck --write-prompts --write-imagegen-queue --candidates-per-slot 4 --plan-only
python3 /path/to/ppt-craft/scripts/score_visual_slot_candidates.py /path/to/deck --select
python3 /path/to/ppt-craft/scripts/render_relationship_graph.py /path/to/deck
python3 /path/to/ppt-craft/scripts/render_skeleton_deck.py /path/to/deck --out /path/to/deck/skeleton
python3 /path/to/ppt-craft/scripts/validate_deck_project.py /path/to/deck --mode html --require-brief --require-blueprint --require-asset-prompts
node /path/to/ppt-craft/scripts/html_to_editable_pptx.mjs /path/to/deck --out /path/to/deck/exports/deck.pptx --report /path/to/deck/reports/html2pptx-report.json
python3 /path/to/ppt-craft/scripts/render_pptx_with_libreoffice.py /path/to/deck/exports/deck.pptx --out-dir /path/to/deck/qa/libreoffice-render
node /path/to/ppt-craft/scripts/screenshot_deck.mjs /path/to/deck --out /path/to/deck/qa
python3 /path/to/ppt-craft/scripts/compare_render_regression.py /path/to/deck --deck-type auto
node /path/to/ppt-craft/scripts/inspect_relationship_graph.mjs /path/to/deck --out /path/to/deck/qa/relationship-graph-report.json --require-pptx-native --require-layering --require-relation-types --require-active-path --require-connector-anchors --require-connector-labels --require-edge-bundling --require-label-scores --require-swimlanes --require-subgraph-collapse --max-edge-crossings 0 --max-label-overlaps 0 --max-node-crowding 2 --max-edge-density 14 --min-layers 3
python3 /path/to/ppt-craft/scripts/make_contact_sheet.py /path/to/deck/qa --out /path/to/deck/qa/contact-sheet.png
python3 /path/to/ppt-craft/scripts/visual_qa_deck.py /path/to/deck --screenshots /path/to/deck/qa --require-blueprint-zones
```
