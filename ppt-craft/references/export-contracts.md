# Export Contracts

## HTML Source

HTML-first route:
- `index.html` is the presenter shell.
- `slides/*.html` are source slides.
- Slides use 1920x1080 fixed canvas.
- The deck may export to PDF or screenshots.

Editable-PPTX route:
- Each slide uses 960pt x 540pt or another explicit PowerPoint physical size.
- Visual CSS is constrained from the first line.

## PDF

Use when:
- visual fidelity matters,
- recipient only needs to read/present,
- archive/print/share is the goal.

PDF preserves visual appearance better than editable PPTX. Treat it as a first-class export, not a failure.

## Editable PPTX Constraints

Use these if converting HTML to editable PowerPoint objects:

1. Body size matches PowerPoint layout, normally `960pt x 540pt`.
2. Text lives in `<p>` or `<h1>`-`<h6>`; do not put important text directly inside a bare `<div>`.
3. Backgrounds, borders, and shadows live on wrapper divs, not on text elements.
4. Pictures use `<img>`, not CSS `background-image`.
5. Tables use real `<table>` markup when they should remain editable.
6. Basic charts use `data-pptx-chart` plus JSON when they should remain editable.
7. Flow arrows and simple relationship lines use `data-pptx-connector` or `data-pptx-line`.
8. Avoid CSS gradients, web components, complex SVG decorations, and unsupported filters.

If these constraints conflict with visual ambition, split the deliverable: HTML/PDF for beauty, PPTX for editable collaborator copy.

Adapter:

```bash
python3 scripts/validate_deck_project.py deck --mode editable
node scripts/html_to_editable_pptx.mjs deck --out deck/exports/deck.pptx --report deck/reports/html2pptx-report.json
python3 scripts/analyze_reference_deck.py --pptx deck/exports/deck.pptx
```

The adapter emits native PowerPoint text boxes, shapes, images, tables, charts, and connectors for supported HTML. Explicit `data-pptx-raster="true"` regions become images and must be reported as partial editability.

Rendering note: QuickLook thumbnails are acceptable only as a smoke check for nonblank slides and simple objects. They are not a native chart regression test. For decks with editable charts, use PowerPoint or a working LibreOffice render before claiming visual verification.

## Image Deck PPTX

If slide pages are raster images:
- PPTX is a container of images.
- It is suitable for sharing and presenting.
- It is not editable as text.
- Say this explicitly.

## Export Note Template

```text
export note:
- source artifact:
- exports:
- editable in PowerPoint: yes/no/partial
- visual fidelity risk:
- verified:
- not verified:
```

## When To Use External Engines

- For full native editable PPTX from arbitrary documents, prefer a dedicated PPTX engine such as `ppt-master` if available.
- For HTML-to-editable-PPTX conversion, use `scripts/html_to_editable_pptx.mjs` only if the HTML was written under editable constraints.
- For raster image deck generation, use the runtime's native image generation when available and save prompts before rendering.
