# Design Practice Bridge

This reference borrows the useful parts of design-practice 技能 and maps them into PPT Craft.

The important lesson is not "make slides look like web pages." The important lesson is **skeleton before skin, restore before invention, render evidence before claiming quality**.

## Method Mapping

| Design Practice | PPT Craft Equivalent | What Changes |
| --- | --- | --- |
| Intent Brief | Deck Brief | Audience, deck job, route, density, style, and editability constraints are frozen before design. |
| Anti-Plastic Test | Anti-Ugly/Anti-Wallpaper Test | Name what would break if we only made a pretty slide image: unreadable text, fake labels, repeated layouts, missing proof, export drift. |
| Five-Layer Blade | Slide Five-Layer Blade | Task = slide job; Structure = archetype/sequence; State = density/export/fallback states; System = tokens/components/objects; Tradeoff = what not to show. |
| Stage 1 Drafts | Narrative spine + layout blueprint + skeleton deck | Low fidelity is not optional. It decides geometry, hierarchy, and safe zones. |
| Stage 2 Fidelity Restore | Final HTML/PPTX restore | Final styling must map 1:1 to the skeleton/blueprint. No surprise blocks, charts, or decorative loops. |
| Render-Critique Loop | Screenshot/DOM/visual QA loop | Browser screenshots and reports are evidence. Fix the weakest layer, rerun, repeat. |
| Design Tokens | Slide Design Tokens | Primitive -> semantic -> component tokens for type, color, spacing, radius, line, chart, plate, and connector grammar. |
| QA Restore Fidelity | Slide Restore Fidelity Diff | Compare blueprint/skeleton vs final HTML/PPTX. Detect added, missing, moved, or rasterized objects. |

## PPT Ten-Step Flow

Use this as the default serious-deck workflow:

1. Compress the source into one deck thesis.
2. Name audience, scene, and success standard.
3. Split content into slide jobs, not template pages.
4. Choose deck IA: sequence, sections, proof order, and call-to-action.
5. List failure states: missing asset, dense slide, low contrast, editability demand, chart/table route, export target.
6. Freeze slide tokens: typography, spacing, plates, line grammar, chart/table style, connector style.
7. Generate with constraints: HTML skeleton, ImageGen oracle, then final HTML/PPTX restore.
8. Self-review with reports: visual QA, relationship graph inspection, restore fidelity diff.
9. Human visual acceptance: contact sheet, key slides, PPTX smoke render when available.
10. Sediment useful tokens/archetypes/tests back into the skill.

## Slide Five-Layer Blade

### 1. Task

Every slide answers one job:

- what the audience must understand,
- what evidence supports it,
- what action or belief changes after the slide.

If the slide has two jobs, split it.

### 2. Structure

Structure is not left/right by default. Pick a real archetype:

- thesis rail,
- proof table,
- system map,
- loop,
- route path,
- comparison,
- staged reveal,
- data wall,
- editorial spread,
- quote/evidence card.

Write coordinates before styling.

### 3. State

Slides have states too:

- live-talk vs async-readable density,
- HTML-first vs editable-PPTX vs raster/hybrid,
- missing/placeholder assets,
- dense data vs summary,
- dark/light projection environment,
- PDF/PPTX/PNG export risks.

State decisions determine whether text, charts, connectors, and labels must remain editable.

### 4. System

Use token tiers:

- primitive: raw palette, typeface, spacing, radius, line widths;
- semantic: claim text, support text, evidence surface, danger note, accent, quiet field;
- component: title plate, proof card, loop chip, metric badge, connector, callout leader, chart axis, table row.

No hardcoded one-off accent or radius inside a slide.

### 5. Tradeoff

Every deck needs a cut list:

- what will not be shown,
- what will be split into another slide,
- what will be rasterized,
- what will stay native editable,
- which visual effect is intentionally sacrificed for PPTX editability.

If everything is included, the deck is not designed.

## Restore Contract

Final HTML/PPTX is a restore of the chosen skeleton, not a fresh generation.

Mandatory restore table for serious decks:

```text
SLIDE RESTORE FIDELITY
======================
Blueprint slide:
Skeleton screenshot:
Final slide:

| Blueprint/skeleton element | Final implementation | Verdict |
| --- | --- | --- |
| claim box | h1 + support p inside claim plate | MATCH |
| evidence region | native table with 4 rows | MATCH |
| loop region | 3 chips + 2 native connectors | MATCH |
| visual region | generated image, no baked text | MATCH |
| not in blueprint | extra decorative chart | ADDED - FAIL |
```

Verdicts:

- `MATCH`: faithful restore.
- `ADDED`: final slide invented something.
- `MISSING`: final slide skipped something.
- `MOVED`: final slide violated the blueprint coordinates.
- `RASTERIZED`: object became an image; acceptable only when route says so.
- `FAIL`: permission/editability/text-safe/contrast contract violated.

Any non-`MATCH` verdict needs either a blueprint update or a repair.

## Render-Critique Discipline

Borrowed from design-practice Stage 3:

1. Render real screenshots.
2. Read objective report and contact sheet.
3. Score the deck on story, hierarchy, typography, contrast, layout variety, token discipline, object richness, export integrity, and originality.
4. Fix the single weakest dimension first.
5. Rerun the harness.

Do not random-restyle after a QA failure. A contrast failure needs plates/tokens. A layout failure needs blueprint repair. A graph failure needs relationship grammar repair.

## Anti-Patterns Imported From Web Work

- Card tiling: repeated equal cards that hide hierarchy.
- Skin without skeleton: beautiful cover, no proof/system slide.
- Stage drift: final slide adds charts/callouts that skeleton never planned.
- Token drift: each slide invents a new blue, radius, shadow, or line width.
- Happy-path-only: no plan for dense data, long Chinese text, missing assets, export drift.
- No render evidence: claiming quality without screenshots/reports.

## What PPT Adds Beyond Web

PPT has fixed pixels and export routes. Therefore the web method must be stricter:

- coordinate-level blueprint is mandatory for serious slides;
- text-safe zones must be machine-checked;
- PPTX route must decide native vs raster before styling;
- complex SVG/canvas must either become native objects or be declared intentional raster;
- PowerPoint font metrics require larger text boxes than browser rendering.
