# PPT Craft System Architecture

This skill should not be a collection of prompts that "make slides prettier." It should be a slide production system with explicit intermediate representations, route contracts, and visual QA.

## Diagnosis

The failed approach was background-first:

```text
source -> nice background -> put text on top -> export -> patch collisions
```

That can make one screenshot look atmospheric, but it cannot reliably produce world-class decks because layout, contrast, editability, and narrative are not owned by the system.

The correct approach is layout-first and contract-driven:

```text
source
-> Deck Brief
-> Content IR
-> Narrative Spine
-> Style Anchors
-> Composition Blueprint
-> Slide Design System
-> Blueprint-Aware Asset Prompts
-> Asset Plan
-> Render Targets
-> QA Critic
-> Delivery
```

Each stage has a file artifact so the agent can inspect, revise, and test the deck instead of guessing.

## Upstream Lessons To Actually Keep

### PPT Master

Keep:

- Real native PPTX matters when the user needs PowerPoint editing.
- The harness is only a production line; model and operator quality still determine the ceiling.
- Examples should span distinct style families, not one house look.

Do not copy blindly:

- Native editability cannot be treated as the only goal. Extreme beauty sometimes requires HTML-first or raster/asset-assisted hybrid routes.

### Huashu Design

Keep:

- Show real visual directions instead of asking users to choose abstract style words.
- Bring in real assets before designing; do not decorate placeholders.
- Review design across philosophy, hierarchy, detail, function, and innovation.
- Support motion and cinematic moments as first-class output, not afterthoughts.

Do not copy blindly:

- HTML-native beauty does not automatically solve PowerPoint editability.

### Frontend Slides

Keep:

- Fixed 16:9 stage is non-negotiable.
- Ask about purpose, length, content readiness, and density.
- Design around text and images from the beginning.
- Three visual previews are useful because users react better to seeing than describing.

Do not copy blindly:

- Browser-first decks need a separate adapter contract before being called editable PPTX.

### Baoyu Slide Deck

Keep:

- Reading/share decks have different density and layout rules from live speaking decks.
- Prompt files, outline files, and image files are reproducibility records.
- Image generation should be batched only after prompts exist.

Do not copy blindly:

- Image-only slides are excellent for shareability but do not satisfy editable PPTX requirements.

## Required Artifacts

Every serious deck project should contain:

```text
deck/
  brief.md
  deck-brief.json
  content-ir.json
  narrative-spine.md
  style-anchors.md
  layout-blueprint.json
  asset-prompts/
  skeleton/
  slide-design-system.json (optional project override)
  asset-plan.md
  slides/
  assets/
  exports/
  reports/
  qa/
```

### 1. Deck Brief

Human-readable contract:

- audience
- situation
- deck job
- route target: HTML-first / editable PPTX / raster / hybrid
- density mode: live talk / async reading / board-room dense
- language and tone
- must-keep claims
- known assets
- unknowns and assumptions

Also create `deck-brief.json` so harnesses can validate the contract. It should record:

- audience
- deck_job
- route
- density
- page_count
- language
- style_direction
- user_decisions
- assumptions
- risks

Only ask the user questions that change route, story, style, or legal/brand constraints.

### 2. Content IR

Machine-readable content structure:

```json
{
  "claims": [],
  "evidence": [],
  "entities": [],
  "numbers": [],
  "quotes": [],
  "risks": [],
  "desired_action": "",
  "source_notes": []
}
```

This prevents the agent from designing before understanding.

### 3. Narrative Spine

Slide-by-slide story map:

```text
01 cover: thesis
02 tension: why current mental model fails
03 system: new model
04 proof: cases/numbers
05 loop: how it compounds
06 action: what to do next
```

Each slide has one job. If a slide has two jobs, split it.

### 4. Style Anchors

Style is not a phrase like "premium" or "tech." It is a concrete translation:

- anchor family
- palette
- type system
- image policy
- layout grammar
- component grammar
- forbidden drift

When the user gives a vague style request, show three visible directions. Each direction must include a content slide, not only a beautiful cover.

### 5. Composition Blueprint

The most important artifact.

For every slide, choose a layout archetype and reserve pixels before visual styling:

```json
{
  "id": "03-system",
  "archetype": "system-loop",
  "job": "show the operating loop",
  "claim": { "x": 72, "y": 84, "w": 500, "h": 180 },
  "support": { "x": 72, "y": 280, "w": 460, "h": 78 },
  "visual": { "x": 620, "y": 86, "w": 540, "h": 420 },
  "evidence": { "x": 72, "y": 400, "w": 500, "h": 156 },
  "loop": { "x": 72, "y": 596, "w": 520, "h": 54 },
  "mask": { "x": 0, "y": 0, "w": 620, "h": 720, "opacity": 0.72 },
  "empty": ["center gutter", "outer 56px safe margin"]
}
```

The background image must be generated or cropped to respect this blueprint. Important text never fights the image.

### 5.1 Slide Design System

The layout blueprint must be paired with a real design system. A rectangle map alone cannot produce a good PPT.

Use `assets/slide-design-system.json` or create a project-local override. It should define:

- font stack and type scale;
- roles for kicker, hero/title lines, body, caption, label, table, and micro text;
- color tokens;
- text backplates and plate rules;
- line, connector, badge, chip, callout, icon, and evidence-plate grammar;
- object richness expectations;
- image prompt contract for text-safe zones and no-text policy.

This is where the system decides how typography, boxes, lines, icons, and foreground richness work before a single final image is generated.

### 5.2 Blueprint-Aware Asset Prompts

Before image generation, create prompts from the blueprint:

```bash
python3 scripts/generate_asset_prompts.py deck --out deck/asset-prompts
```

Each prompt must include:

- visual region coordinates;
- claim/support/evidence/loop text-safe zones;
- no-go zones for focal objects, busy texture, and fake labels;
- external editable foreground overlay plan;
- route-specific no-text policy;
- negative prompt and QA checklist.

Generated images are rejected if they do not leave room for the planned typography and foreground objects.

### 5.5 Skeleton Renderer

Before final styling, render the skeleton:

```bash
python3 scripts/generate_asset_prompts.py deck --out deck/asset-prompts
python3 scripts/render_skeleton_deck.py deck --out deck/skeleton
node scripts/screenshot_deck.mjs deck/skeleton --out deck/qa/skeleton
python3 scripts/make_contact_sheet.py deck/qa/skeleton --out deck/qa/skeleton-contact-sheet.png
```

The skeleton contact sheet should already prove hierarchy, region fit, loop/path clarity, typography roles, plate/backplate placement, image text-safe zones, and layout variety. If it does not, fix the archetype, blueprint, design system, or asset prompt plan before visual styling.

### 6. Asset Plan

Before generating or placing images:

- which slides need images
- what region must stay empty for text
- whether the image can include text
- whether image is decorative, evidentiary, metaphorical, or product-real
- crop policy
- fallback if the asset fails

Asset Plan is not a substitute for `asset-prompts/`. The asset plan says what is needed; asset prompts translate the layout blueprint and design system into generation instructions.

For deck backgrounds, prompt for quiet fields explicitly:

```text
left 45% has clean dark negative space for headline, no faces, no icons, no text;
right 45% contains the subject; center gutter remains low contrast
```

### 7. Render Targets

Render is a route, not an afterthought:

- HTML-first: highest visual ceiling, browser presentation, PDF/image export.
- Editable PPTX: native text/shape/table/chart/connector objects, constrained visual language.
- Raster deck: image-first shareability, text is baked.
- Hybrid: generated/cropped image assets plus editable foreground objects.

The route note must say exactly what is editable and what is not.

### 8. QA Critic

QA needs more than "the file exists."

Required checks:

- layout blueprint exists and matches slides
- HTML screenshots for all slides
- asset prompts exist and reserve text-safe zones
- contact sheet review
- PPTX object report
- PPTX smoke render via PowerPoint/LibreOffice/QuickLook where available
- overlap / overflow scan for text boxes
- style-specific anti-template test
- route-specific editability report

Failures should produce repair tasks, not vague taste comments.

## Routing Policy

Default route for "world-class, beautiful, smooth" is HTML-first.

Use editable PPTX only when:

- user explicitly needs colleagues to edit in PowerPoint
- or deck will live inside a PowerPoint workflow
- or the task is testing the editable engine

Use hybrid when:

- the user wants beauty and editability
- but the visual identity depends on images, atmosphere, product shots, or generated scenes

In hybrid, background and major images may be non-editable, but foreground claims, labels, tables, charts, and connectors should be editable.

## Interaction Policy

Do not ask many questions up front. Ask after digesting.

Ask when the answer changes:

- audience / purpose
- density
- route
- visual direction
- brand/legal constraints
- whether original PPT order must be preserved

For serious decks, the better interaction is:

1. digest source
2. produce Deck Brief v0 and 3 visual/layout directions
3. ask user to pick/mix
4. build the full deck
5. QA and repair

## Engineering Roadmap

### Phase 1: System Spec And Hard Gates

- `deck-brief.json` schema.
- `layout-blueprint.json` schema.
- validator checks for deck brief existence.
- validator checks for blueprint existence.
- no hero-scale `<br>` in editable route.
- no content slide without reserved title/body/visual/evidence regions.
- skeleton renderer and contact-sheet review before styling.

### Phase 2: Layout Archetype Library

Create reusable archetypes:

- split-thesis
- system-loop
- proof-table-plus-signal
- before-after
- timeline
- metric-wall
- quote-evidence
- product-demo
- board-report-grid

Each archetype has coordinates, density limits, and route compatibility.

### Phase 3: Style Anchor Starters

Each anchor gets a starter:

- cover
- dense proof slide
- system/process slide
- closing slide

This avoids style anchors being only text labels.

### Phase 4: Asset-Aware Generation

Image prompts are derived from blueprint regions. The asset generator must reserve quiet fields and avoid text inside images unless the route is raster.

### Phase 5: Render Regression

Add automated checks:

- HTML screenshot contact sheet.
- PPTX object inventory.
- PowerPoint/LibreOffice render when available.
- image diff against expected screenshot class.
- overlap detector from PPTX XML or rendered screenshot.

### Phase 6: Real Forward Tests

Maintain test decks from real materials:

- InnerScan investor deck style reverse-engineering.
- 阿彬 AI developer share.
- one dense consulting/report deck.
- one product keynote.
- one reading/share image deck.

Each forward test should declare what route it exercises and what visual defects are unacceptable.

## Acceptance Definition

The skill is good only when it can repeatedly do this:

- understand a document before asking
- pick or show suitable style directions
- reserve layout before choosing imagery
- generate or use assets that leave space for type
- preserve route honesty
- pass visual and structural QA
- produce a contact sheet the user would not call generic

Anything less is not a world-class PPT skill; it is a demo.
