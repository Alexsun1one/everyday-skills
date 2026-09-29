# ImageGen-First Visual Oracle

Use this when the deck needs a strong visual ceiling, when the user says the current deck looks ugly, or when supplied references show a level the harness is not yet matching.

The goal is to create one or more **beautiful target plates first**, then extract design tokens and layout rules before building HTML or PPTX. Do not generate a random background and place text afterward.

## Route Judgment

Do not choose between "all native HTML/PPTX" and "all ImageGen pages" at deck level. Use a layered route:

1. **ImageGen as visual oracle**: generate beautiful target plates to discover composition, contrast devices, texture, object richness, and emotional register.
2. **ImageGen as asset factory**: generate local assets for planned slots, crops, transparent PNG ornaments, metaphors, textures, product shots, or evidence visuals.
3. **Semantic HTML/native PPTX as source of truth**: keep important copy, tables, charts, relationship nodes, connectors, labels, and business logic in editable objects.
4. **Full-page raster only by exception**: use a whole ImageGen page as the final slide only for raster-image decks, social cards, poster-like pages, or when the user accepts baked text and limited editability.

The fragile route is: generate a full slide image -> ask HTML to reverse-engineer it -> convert to editable PPTX. It may look good for a screenshot, but it makes exact text, graph semantics, chart accuracy, connector endpoints, accessibility, and PowerPoint editability brittle. Use full-page images as targets or references, not as the canonical editable deck layer.

## Required Order

1. Digest the source and references.
   - Run `references/reference-deck-forensics.md` for supplied PPTX/PDF samples.
   - Identify what makes the sample good: stage composition, text-safe fields, contrast devices, typography scale, object grammar, and slide-to-slide rhythm.
2. Freeze the pixel contract.
   - `deck-brief.json`
   - `content-ir.json`
   - `layout-blueprint.json`
   - `asset-prompts/asset-prompts.json`
   - slide design system roles
3. Generate visual oracle plates with Image Gen.
   - Use real or representative deck copy.
   - Include text in the image when the goal is visual exploration.
   - Ask for explicit text-safe areas, plates, strips, tickets, masks, and foreground objects.
   - Produce at least a cover/proof/system sample for serious decks, or explain why one target plate is enough.
4. Inspect the oracle plates.
   - Reject if text is illegible, fake text appears, the layout is only left/right or top/bottom, or the sample has no content-heavy system.
   - Reject if text would not survive conversion into editable HTML/PPTX roles.
5. Extract visual tokens.
   - Run `scripts/extract_visual_tokens.py <image> --out <deck>/visual-tokens.json`.
   - Add semantic notes that the script cannot infer: type intent, backplate grammar, line/icon language, asset policy, forbidden drift.
6. Build from tokens.
   - Convert the oracle into a style lock and slide design system.
   - Do not copy the image directly unless the route is raster.
   - For HTML/PPTX, reproduce the token system with editable type, native shapes, plates, masks, connectors, charts, and image regions.
   - For relationship/system slides, turn visual motifs into `visual_slots[]`, declare `source` / `crop_box` / `out` when cutting from an ImageGen board, run `scripts/process_visual_slots.py`, and keep graph nodes/edges native.
   - When a local visual slot affects perceived quality, generate 2-4 candidates from the built-in ImageGen queue created by `scripts/score_visual_slot_candidates.py --write-imagegen-queue --plan-only`, then run `scripts/score_visual_slot_candidates.py --select` before rendering.
7. QA against the blueprint.
   - `visual_qa_deck.py` must pass with warning-blocking behavior.
   - For serious decks, `--require-blueprint-zones` must pass.
   - For editable PPTX, LibreOffice render must pass and `scripts/compare_render_regression.py --deck-type auto` should have zero errors/warnings when browser screenshots and LibreOffice PNGs are available.

## Oracle Prompt Contract

Every oracle prompt must contain:

- final stage ratio and approximate resolution;
- real slide title/support copy, kept short enough for accurate rendering;
- desired audience and deck job;
- exact layout regions or at least relative composition;
- text-safe zones and no-go zones;
- foreground devices: plates, strips, cards, chips, badges, connectors, callouts, charts, tables;
- typography intent: title scale, body scale, weight contrast, letter spacing, line height;
- contrast policy: where dark/light fields sit and how text is made readable;
- visual richness beyond simple split layouts;
- negative prompt: no fake UI labels, no random tiny text, no busy texture under text, no generic card wall.

## Token Extraction Checklist

The final `visual-tokens.json` should include:

- `palette`: dominant colors and accent candidates;
- `tonal_bands`: dark, mid, light surfaces and their usage;
- `type_system`: title/body/caption/numeric roles;
- `layout_grammar`: stage grid, major zones, negative space, rhythm;
- `text_backplates`: plaques, strips, scrims, cards, tags, and when to use them;
- `object_grammar`: charts, tables, lines, icons, props, evidence plates;
- `image_policy`: where generated imagery lives, where it must stay quiet, and where it may contain baked text;
- `qa_rules`: contrast, overflow, safe-zone, repetition, and fake-text checks;
- `forbidden_drift`: styles or habits that would make the deck generic or ugly.

## Reference Sample Borrowing

Borrow systems, not skins:

- If a sample is excellent because the text has reserved quiet bands, extract that as `text_backplates` and `layout_grammar`.
- If the sample is excellent because dense charts stay editable, extract that as `object_grammar`.
- If the sample is excellent because every slide has a different spatial job, extract archetype distribution.
- Do not copy proprietary slide copy, logos, or exact compositions unless the user owns the deck and asks for direct continuation.
