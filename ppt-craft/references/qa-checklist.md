# QA Checklist

Run this before saying a deck is done.

## Narrative

- [ ] Cover says the deck's real offer or claim, not a vague topic.
- [ ] Deck brief records audience, deck job, route, density/page count, style direction, user decisions, and assumptions.
- [ ] Each slide has one job.
- [ ] Slide order forms an arc: context -> tension -> insight -> proof -> action.
- [ ] Dense slides have captions or annotations that explain the insight.
- [ ] No invented facts, logos, charts, or product specs.

## Visual

- [ ] Fixed 16:9 stage; no scroll inside slides.
- [ ] No text or cards overflow the slide.
- [ ] Non-trivial decks selected 2-4 local style anchors or documented why a strict brand/template overrode them.
- [ ] Candidate style anchors have starter previews for cover/proof/system/closing, or a strict brand/template override is documented.
- [ ] Non-trivial decks have a composition blueprint: safe area, text boxes, visual regions, contrast masks, loop/path region, and intentional empty space.
- [ ] Non-trivial slides declare layout archetypes or documented custom reasons.
- [ ] Slide design system is locked: font stack, type scale, backplates, line/icon grammar, and foreground object kit.
- [ ] Blueprint-aware asset prompts exist before image generation; each prompt lists visual region, text-safe zones, no-go zones, foreground overlays, and no-text policy.
- [ ] Skeleton deck was rendered, screenshot-reviewed, and repaired before final styling; skeleton shows type roles, plates/backplates, and asset constraints, not only boxes.
- [ ] At least cover + one dense slide + one visual slide + closing slide were screenshot-reviewed.
- [ ] `visual_qa_deck.py` was run after screenshots with default warning-blocking behavior; errors and warnings are fixed or explicitly waived in the delivery note.
- [ ] For non-trivial decks, `visual_qa_deck.py --require-blueprint-zones` passes: meaningful text boxes land inside declared text-safe zones from `layout-blueprint.json` or `asset-prompts/asset-prompts.json`.
- [ ] Typography scale is consistent across the deck.
- [ ] Palette has one clear system; no accidental rainbow.
- [ ] Visual style is source-specific enough to fail the "relabel to any topic" test.
- [ ] No important text sits directly on image texture without a plate, strip, plaque, ticket, or quiet field.
- [ ] Contact sheet does not read as repeated left/right or top/bottom layouts only.
- [ ] Each slide uses enough meaningful foreground objects: badges, chips, lines, evidence plates, callouts, tables, charts, or icons where relevant.
- [ ] Line-heavy/system-map slides have a `relationship-graph.json` or equivalent graph contract; graph layers, node ids, edge ids, relation types, active path, and native/raster export intent are explicit.
- [ ] Line-heavy/system-map slides ran `inspect_relationship_graph.mjs --require-pptx-native --require-layering --require-relation-types --require-active-path`; for dense native-editable graphs, also require connector anchors and labels unless a named route waiver exists.

## Assets

- [ ] Brand/product logos are real or marked as placeholders.
- [ ] Images are relevant and high enough resolution.
- [ ] Generated images obey reserved text-safe zones and keep subject matter out of title/support/evidence/loop regions.
- [ ] If `visual_slots[]` are used, `process_visual_slots.py` was run before rendering; `asset-prompts/visual-slots-report.json` has `ok=true`, zero errors, and no pending slots unless a named waiver exists.
- [ ] If local ImageGen/asset quality matters, `score_visual_slot_candidates.py --write-prompts --write-imagegen-queue --plan-only` produced prompt files plus `asset-prompts/builtin-imagegen-queue.json`, built-in ImageGen candidates were generated, candidate images were scored, and `asset-prompts/visual-slot-candidate-scores.json` has zero errors/warnings unless a named waiver exists.
- [ ] Charts/data have source notes or are clearly illustrative.
- [ ] Local assets use relative paths.

## Interaction And Motion

- [ ] Keyboard navigation works.
- [ ] Motion supports the message and can be reduced.
- [ ] Presenter shell opens to the right first view.
- [ ] Overview/grid does not make slides unreadable.

## Route-Specific

**HTML-first**
- [ ] `index.html` exists.
- [ ] `slides/*.html` exist and open independently.
- [ ] `validate_deck_project.py --mode html` passes.

**Editable PPTX**
- [ ] Editable constraints were applied before generation.
- [ ] `deck-brief.json` and `layout-blueprint.json` pass their validators when present.
- [ ] Large multiline headlines are separate positioned text boxes, not one tight text box relying on browser line breaks.
- [ ] `validate_deck_project.py --mode editable` passes.
- [ ] `html_to_editable_pptx.mjs` writes a `.pptx` and JSON report.
- [ ] Export report shows expected text/shape/image counts.
- [ ] If native tables, charts, or connectors are used, export report shows expected `tables`, `charts`, and `connectors` counts.
- [ ] If rich native connectors are used, export report shows expected `connector_groups`, expanded `connectors`, and `connector_labels`, with `raster=0` unless a raster atmosphere waiver exists.
- [ ] If relationship graphs are used, `relationship-graph-report.json` has zero errors/warnings or a named raster/editability waiver.
- [ ] If relationship graphs include visual slots, the final PPTX export has the expected image count and `raster=0` for core graph objects.
- [ ] If auto-layout relationship graphs are used, require `edge_crossings=0`, `label_overlaps=0`, nonzero `bundled_edges` when parallel layer-to-layer edges exist, and nonzero `label_scored_edges` for edge labels.
- [ ] If dense business relationship graphs mix domains/audiences, require nonzero `swimlanes`; if repeated detail clusters exist, require nonzero `collapsed_nodes`.
- [ ] If auto-layout relationship graphs are used, require bounded node crowding and edge density, such as `node_crowding_score<=2` and `edge_density_peak<=14` unless a named waiver exists.
- [ ] If graph labels are important, inspect `data-graph-label-score` outliers; high scores mean the label likely needs a new route, offset, or shorter copy.
- [ ] Rasterized regions are intentional and listed in the delivery note.
- [ ] `analyze_reference_deck.py --pptx` confirms final slide count, text runs, and chart/table counts when relevant.
- [ ] If LibreOffice is available, `render_pptx_with_libreoffice.py deck/exports/deck.pptx --out-dir deck/qa/libreoffice-render` produces a PDF plus PNG pages, and the generated contact sheet is visually inspected.
- [ ] If both browser screenshots and LibreOffice PNG pages exist, `compare_render_regression.py deck --deck-type auto` selected the right render profile, has zero errors/warnings, and its diff contact sheet was inspected for structure shifts, missing images, broken connectors, and clipped labels.
- [ ] If visual render via LibreOffice/PowerPoint is unavailable, say so; do not imply it was visually inspected. macOS QuickLook is not enough for native chart render regression because it may leave charts blank.
- [ ] Export note clearly states editability limitations.

**Raster image deck**
- [ ] `outline.md` exists.
- [ ] `prompts/*.md` exist for every generated slide.
- [ ] Final images all share aspect ratio.
- [ ] User is told text is baked into images.

## Repair Rules

If QA fails:
- Overflow -> split slide or redesign layout; do not shrink below readable size.
- Low contrast -> add a plate/strip/scrim, move text to a quiet field, or change foreground/background tokens; do not rely on "looks okay on my screen".
- Repeated layout -> change archetype/object grammar before tweaking colors.
- Generic style -> rerun visual direction with a stronger source-specific thesis.
- Bad logos/assets -> fetch official assets or mark honest placeholders.
- Editable-PPTX violation -> rewrite constrained HTML, mark explicit raster fallback, or switch to PDF/HTML-first.
