# Upstream Synthesis

This skill borrows patterns, not code, from four strong public slide skills/repos.

## Sources

- `hugohe3/ppt-master`: https://github.com/hugohe3/ppt-master
- `alchaincyf/huashu-design`: https://github.com/alchaincyf/huashu-design
- `zarazhangrui/frontend-slides`: https://github.com/zarazhangrui/frontend-slides
- `JimLiu/baoyu-skills/skills/baoyu-slide-deck`: https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-slide-deck

## What To Borrow

### PPT Master

Borrow:
- Native-editability is a real product promise, not a decorative label.
- Source documents should be imported into a project folder with generated analysis and repeatable exports.
- Route existing `.pptx` by intent: preserve page split vs restructure the story.
- Use a spec lock for colors/fonts/layout decisions to reduce drift on long decks.
- Keep a live preview / quality check loop before final export.

Do not copy blindly:
- Strict serial per-page SVG generation is powerful but heavy. Use that depth only for decks that truly need native-editable PPTX or complex document conversion.
- The pipeline can feel slow. This skill should default to a lighter HTML-first route unless PPTX editability is required.

Adapter implementation in PPT Craft:
- `scripts/html_to_editable_pptx.mjs` is the lightweight native-PPTX adapter.
- It converts constrained HTML slides into PowerPoint text boxes, native shapes, and images.
- It writes a JSON report so the user can see text/shape/image/raster/table/chart/connector counts.
- It does not replace a full `ppt-master` document-ingestion engine; it covers the repeatable editable HTML route.

### Huashu Design

Borrow:
- HTML is the default source artifact; PDF/PPTX/video are derivatives.
- Vague design requests should become visible options, not abstract style questions.
- Brand assets and product facts must be verified before designing around real brands/products.
- Slide decks need a deck shell, not a long webpage.
- Editable PPTX must constrain HTML from the start; retrofitting is expensive.
- Screenshot and Playwright validation are part of the craft, not optional cleanup.
- HTML-to-PPTX must be a first-class adapter route with explicit supported CSS, not a hidden export button.

Do not copy blindly:
- The huge reference library is excellent but too heavy for default context. Keep PPT Craft's main entry small and load detailed refs only when needed.
- Subagents are useful for exploration, but local Codex may not always expose them. Support serial fallback.

### Frontend Slides

Borrow:
- Fixed 1920x1080 stage scaled to viewport is the cleanest browser-deck model.
- Style discovery works best through 3 visual previews.
- Progressive disclosure for template packs: read compact indexes first, then only the selected design recipe.
- Inline edit and PDF/web sharing are post-draft affordances; do not ask too early.

Do not copy blindly:
- Zero-dependency single HTML is elegant, but multi-file slide pages are easier to screenshot, debug, and export for larger decks.

### Baoyu Slide Deck

Borrow:
- Reading/share decks are different from live speaking decks.
- Preset style dimensions are easier to reason about than raw style names.
- Per-slide prompt files are the reproducibility record for raster decks.
- Batch image generation is valuable after all prompts are saved.
- Merge image slides to PPTX/PDF only after all slides exist.

Do not copy blindly:
- Raster decks are fast and beautiful, but not editable. They should be a clear route, not the default for every PPT request.

## Our Combined Shape

PPT Craft uses four layers:

1. **Conductor**: route by output promise and user intent.
2. **Design discovery**: three visible directions, brand facts, style registers, density.
3. **Artifact route**: HTML-first, editable PPTX, raster image deck, or existing-deck beautify.
4. **Harness**: local structure validation, screenshots, QA checklist, and explicit route note.

The key product decision: **HTML-first is the default source artifact**, but **editable PPTX is a separate route chosen early**. This gives the best balance of beauty, speed, and honest export semantics.

As of 2026-06-27, Route B has a local adapter:

```bash
python3 scripts/validate_deck_project.py deck --mode editable
node scripts/html_to_editable_pptx.mjs deck --out deck/exports/deck.pptx --report deck/reports/html2pptx-report.json
python3 scripts/analyze_reference_deck.py --pptx deck/exports/deck.pptx
```
