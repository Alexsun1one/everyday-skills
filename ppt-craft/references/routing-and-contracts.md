# Routing And Contracts

## Deck Brief

Freeze this before full generation:

```text
deck brief:
- source:
- audience:
- deck job: persuade / teach / report / sell / align / document / entertain
- setting: live talk / async reading / client proposal / social share / classroom
- language:
- density: low speaker-led / high reading-first
- route: html-first / editable-pptx / raster-image / existing-beautify
- final exports:
- assets: logo / product images / screenshots / charts / user images / none
- constraints:
- verification plan:
```

## Density Modes

**Low density / speaker-led**
- One idea per slide.
- 1-3 bullets max.
- Large type and strong visual beats.
- Prefer more slides over dense pages.

**High density / reading-first**
- Self-contained slides.
- Structured grids, tables, diagrams, captions.
- 4-8 bullets or 4-6 cards only when readable.
- Strong hierarchy, not document paste.

If unclear: live persuasion -> low; internal memo/report -> high.

## Route A: HTML-First Deck

Use when beauty, motion, browsing, PDF, or web sharing matters most.

Contract:
- Create `index.html` from `assets/deck_index.html`.
- Create one full HTML file per slide under `slides/`.
- Author each slide at 1920x1080.
- Use `shared/` for tokens, fonts, and reusable assets when the deck has more than 5 slides.
- Validate with `validate_deck_project.py --mode html`.
- Screenshot at least cover, one dense content slide, one visual slide, and closing slide.

## Route B: Editable PPTX

Use when PowerPoint editing is a hard requirement.

Contract:
- Decide this route **before** writing HTML.
- Read `references/editable-pptx-engine.md`.
- Use constrained HTML authored for the adapter, normally 960pt x 540pt or 1280px x 720px.
- Export with `scripts/html_to_editable_pptx.mjs` unless a heavier native PPTX engine is explicitly selected.
- Do not promise visual features that editable PPTX cannot preserve.
- Keep text in real text containers.
- Use solid color fills and `<img>` elements for pictures.
- Use native `<table>`, `data-pptx-chart`, and `data-pptx-connector` for basic editable tables, charts, and relationship lines.
- Validate with `validate_deck_project.py --mode editable`.
- Inspect the exported PPTX with `analyze_reference_deck.py --pptx`.

If both maximum beauty and editability are requested, state the fork:
- Beautiful HTML/PDF: highest fidelity, limited editability.
- Editable PPTX: lower visual freedom, editable text/shapes.

For serious editable decks, ImageGen is still recommended, but as an oracle and asset layer:
- generate full-page target plates to discover the visual system;
- generate cropped or transparent assets for planned `visual_slots`;
- keep meaning-critical copy, tables, charts, relationship graphs, and connectors in native HTML/PPTX objects.

Avoid making a full ImageGen slide the canonical source for editable PPTX unless the user accepts a raster or partially editable route. Reverse-engineering a generated page image back into editable HTML/PPTX is fragile.

## Route C: Raster Image Deck

Use for social-reading decks, cute/NPC/card styles, or when image generation is the desired output.

Contract:
- Save `outline.md`.
- Save each prompt as `prompts/NN-slide-slug.md` before generation.
- Generate images in consistent aspect ratio.
- Merge/export only after all images exist.
- Clearly state that slide text is baked into images.

## Route D: Existing Deck Beautify

If the source `.pptx` is finished and page split/order/wording should be preserved:
- Keep page count/order fixed.
- Preserve wording.
- Improve hierarchy, spacing, type, color, and assets.

If page count/order can change:
- Treat the deck as source material and reroute to HTML-first or editable-PPTX.

## Source Handling

Do:
- Convert PDFs/DOCX/PPTX/URLs to text or structured notes before writing slides.
- Extract images and charts into `assets/` or `images/`.
- Preserve speaker notes if they exist.
- Research current facts before slide claims.

Do not:
- Paste a long report into tiny slide text.
- Invent data, screenshots, logos, company facts, or product specs.
- Let a style route override the source's narrative.
