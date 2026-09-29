# Blueprint-Aware Asset Generation

Generated slide art must obey the layout blueprint. It is not a wallpaper that the deck later fights against.

Use this reference with image-generation skills such as `paper-operators`, hero image generation, product mockups, or raster slide backgrounds.

## Core Rule

Before generating any image, create an asset prompt plan:

```bash
python3 scripts/generate_asset_prompts.py deck --out deck/asset-prompts
```

The plan reads:

- `deck-brief.json`
- `layout-blueprint.json`
- `assets/layout-archetypes.json`
- `assets/slide-design-system.json`

It outputs:

- `asset-prompts/asset-prompts.json`
- one markdown prompt per slide

## What The Prompt Must Control

Every generated slide asset prompt must include:

- stage and aspect ratio;
- visual region coordinates;
- text-safe zones from claim/support/evidence/loop;
- no-go zones where the image subject cannot sit;
- foreground overlay objects that will be editable later;
- no-text policy for hybrid/editable routes;
- where blank plaques/tags may appear if useful;
- negative prompt banning fake text, logos, and busy texture in text zones;
- QA checklist.

For complex relationship slides, prefer planned `visual_slots[]` over full-slide backgrounds when the slide only needs a local metaphor, texture, icon, or evidence cue. A single generated image board may be cut into several named crops, including transparent PNG ornaments, as long as each crop has its own slot, box, fit, and no-text rule in the graph/view contract.

When a `relationship-graph.json` includes `visual_slots[]`, make the asset preparation reproducible:

```bash
python3 scripts/process_visual_slots.py deck
```

Each slot may declare `source` or `source_image`, `crop_box` or `source_crop`, `out` or `asset_out`, `output_size`, `transparent_threshold`, `transparent_chroma`, and `transparent_softness`. The script crops the source board, resizes the asset, optionally creates a transparent PNG, and writes `asset-prompts/visual-slots-report.json`. Treat report errors or pending slots as blockers before graph rendering.

When visual quality is the risk, do not stop at one candidate. Create a candidate prompt pack and score the outputs:

```bash
python3 scripts/score_visual_slot_candidates.py deck --write-prompts --write-imagegen-queue --candidates-per-slot 4 --plan-only
python3 scripts/score_visual_slot_candidates.py deck --select
```

The plan-only step writes `asset-prompts/builtin-imagegen-queue.json` for built-in ImageGen execution. The score report checks target resolution, aspect ratio, visible occupancy, border quietness, contrast, edge density, and transparency quality. It chooses the best local asset, then writes it into the slot output path.

## Text And Image Relationship

Route-specific rules:

- **HTML-first**: image may include text if the final output does not need editability, but it must still reserve or integrate text intentionally.
- **Editable PPTX**: generated image must not contain necessary text. Text, labels, tables, charts, connectors, badges, and callouts are external editable objects.
- **Hybrid**: generated image carries tactile atmosphere and objects; all important language is external editable overlay. Blank plaques may be generated for alignment, but not fake labels.
- **Raster image deck**: image can carry final typography, but font hierarchy and text positions still come from the design system.

## Paper Operators Integration

For `paper-operators`:

- the paper operator performs the conceptual action inside the visual region;
- reserved text zones are quiet off-white paper/tabletop;
- labels inside the image are omitted or replaced with blank plaques when the PPTX route needs editable labels;
- blue carrier ribbons avoid claim/support/evidence regions unless the slide explicitly reserves them for loop/path;
- generated props must leave enough space for editable number badges, tags, and captions.

## QA

Reject the image prompt before generation when:

- it does not mention reserved text-safe zones;
- it asks the model to freely compose the whole slide;
- it requests a full-slide image when a small crop, local plate, or transparent icon slot would preserve readability better;
- it declares planned visual slots but does not include reproducible source/crop/output fields or a clean visual slots report;
- it uses only the first generated slot image when the deck needs premium polish; use the candidate scoring loop instead;
- it places the focal object under a title/support/evidence area;
- it asks for fake text in a hybrid/editable route;
- it lacks a negative prompt for busy texture and accidental labels;
- it does not specify where editable foreground objects will be placed.

Reject the generated image after generation when:

- any key text-safe zone is visually busy;
- important subject matter collides with title/support/evidence/loop boxes;
- there is fake or unreadable text;
- the image forces a raw-text overlay with no plate;
- the slide cannot support at least one designed text backplate or callout object.
