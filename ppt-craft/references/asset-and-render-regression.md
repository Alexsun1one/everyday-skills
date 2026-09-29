# Asset Candidates And Render Regression

Use this when a deck has planned visual slots, ImageGen/local image assets, or an editable PPTX export that must survive Office rendering.

## Visual Slot Candidate Loop

Do not accept the first generated local asset when visual quality matters. For each `visual_slots[]` entry, create several candidates and score them before rendering the deck.

For Codex/ChatGPT built-in ImageGen, first generate the agent queue:

```bash
python3 scripts/score_visual_slot_candidates.py deck --write-prompts --write-imagegen-queue --candidates-per-slot 4 --plan-only
```

The script creates:

- `asset-prompts/visual-slot-candidates/<view>/<slot>/prompt-01.md` etc.;
- `visual-slot-candidates-manifest.json`;
- `asset-prompts/builtin-imagegen-queue.json` and `.md`;
- candidate folders where ImageGen outputs should be placed as `candidate-01.png`, `candidate-02.png`, etc.

The queue is intentionally an agent contract, not an API wrapper. The executing agent calls the built-in ImageGen tool for each item, stores the generated PNG at `candidate_path`, then runs the scorer. Do not use `OPENAI_API_KEY` or an external image API for this queue route.

After candidate images exist, score and select:

```bash
python3 scripts/score_visual_slot_candidates.py deck --select
```

The report is:

```text
asset-prompts/visual-slot-candidate-scores.json
asset-prompts/visual-slot-candidate-scores.md
```

Default behavior fails on warnings. Selection normalizes the best candidate into the slot output path, applying the slot's fit, target size, and transparency policy.

Use `--seed-current` only for smoke tests or when turning an existing slot asset into candidate-01 for regression.

## What Candidate Scoring Checks

The scorer does not judge taste by itself. It blocks obvious asset failures before the human or agent judges taste:

- output resolution is high enough;
- aspect ratio matches the slot output size;
- transparent assets have meaningful visible occupancy, not empty or overcrowded pixels;
- transparent borders are quiet enough to sit near editable text and connectors;
- visible subject contrast is sufficient;
- edge density is neither blank nor noisy.

For true ImageGen production, still inspect a contact sheet. The scorer is a guardrail, not an art director.

## Browser vs LibreOffice Render Diff

Editable PPTX must be checked in an Office rendering engine, not only in browser screenshots.

After `html_to_editable_pptx.mjs` and `render_pptx_with_libreoffice.py`, compare browser screenshots with LibreOffice PNG pages:

```bash
python3 scripts/compare_render_regression.py deck --deck-type auto
```

The script reads:

- browser screenshots from `deck/qa/*.png`;
- LibreOffice pages from `deck/qa/libreoffice-render-script/*.png` or `deck/qa/libreoffice-render/*.png`.

It writes:

- `qa/render-diff/render-diff-report.json`;
- `qa/render-diff/render-diff-report.md`;
- `qa/render-diff/render-diff-01.png` etc.;
- `qa/render-diff/render-diff-contact-sheet.png`.

The contact sheet shows browser, LibreOffice, and heat-map diff side by side. Expected differences include font antialiasing, small line width differences, and minor text metric changes. Unexpected failures include missing images, shifted nodes, blank charts, broken connectors, clipped text, or page count mismatch.

`--deck-type auto` reads `deck-brief.json` and selects a threshold profile from `assets/render-diff-thresholds.json`. Current profiles are `default`, `investor`, `consulting`, `product`, `report`, `training`, and `raster`. You may pass `--deck-type investor` or another profile explicitly; direct numeric flags such as `--mean-warning` still override the profile. Do not loosen a profile just to pass a broken render; inspect the diff sheet first.

## Gates

For serious editable PPTX:

- visual slot candidate score report must have zero errors/warnings, unless a named waiver exists;
- LibreOffice render report must have `ok=true` and expected page count;
- render diff report must have zero errors/warnings;
- if render diff fails, inspect the diff sheet before changing thresholds.
