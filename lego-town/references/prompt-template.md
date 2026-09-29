# Prompt Template / 提示词模板

Use one image at a time.

## Planning Template

```text
Use $lego-town. First plan, do not generate yet.

Source anchor:
{system / document / prompt / workflow / concept / comparison}

Return:
- reader takeaway
- domain & tone
- relationship type
- the parts (3-7 modules) and how they connect (the stud grammar)
- mode (finished / instruction / exploded / box art)
- build archetype
- minifig roles (or none, with reason)
- baseplate world / district
- elements & state coding
- composition
- label plan
- final generation prompt
- QA risks
```

## Final Generation Prompt

```text
Generate one standalone {16:9 horizontal / 1:1 / 4:5} illustration in the LEGO Town style: an ORIGINAL build of interlocking studded construction bricks (NOT a real LEGO® set, NOT the LEGO logo, NOT a licensed character; NOT Minecraft/voxel).

Context:
{one sentence — what this explains}

Source anchor:
{the specific structure, claim, or step}

Reader takeaway:
{one sentence}

Domain & tone:
{AI/prompt · software · product · data/process · org · education/research · life · civic; tone}

Relationship to show:
{connection / sequence / dependency / causality / feedback / contrast / tradeoff / hierarchy-containment / transformation / boundary-filter / divergence-convergence / tension}

Mode:
{Finished Build (studio set-photo) / Instruction Sheet (numbered steps + parts call-out box) / Exploded View (parts floating on drop-lines) / Box Art (original product box)}

The build (the diagram):
- build archetype: {Load-Bearing Stack / Conveyor Line / Brick Seesaw / Gear Train / A/B Split Plate / Checkpoint Gate / Walled District / Build Machine / Road Fork / Funnel Hopper / Tug Anchors / Baseplate Town / ...}
- the parts (modules): {3-7 named modules as buildings/bricks/tiles}
- how they connect: {stacked on a foundation / in a row on a road / walled in a plot / meshed by gears / bridged by a road / balanced on a seesaw / forked at a switch} — the physical connection MUST carry the relation, not a drawn arrow.
- native elements: {prefer REAL LEGO elements that already signal the meaning — arrow road-plate=flow, stop sign/striped barrier=stop, meshed gears=coupled, traffic light=gate, trans-red stud=alarm — instead of generic shapes or drawn arrows}.
- baseplate world / district: {service town / factory floor / planning site / knowledge town / cozy street / ...}

Minifig:
- {none} OR {1-3 ORIGINAL role-minifigs}: {Builder / Inspector / Courier / Operator / Mayor / Surveyor / Researcher / Guide / Maintainer}, each performing one live action {mid-snap / inspecting at a gate / carrying a parcel / at a lever / on a plinth}.
- appearance: classic minifig silhouette, ABS plastic, original printed torso + role accessory (hard hat / clipboard / wrench / goggles / chain), simple ORIGINAL expression (calm by default, or state-coded). No trademarked smiley, no licensed face, no real-person likeness.
- scale: 8-18% of canvas height; smaller than the build.

Material & light:
- real ABS bricks: visible studs and tube/clutch geometry, honest brick proportions, soft glossy specular highlight, slight bevels.
- Finished/Box: clean studio product light, soft key + fill, soft contact shadow, seamless sweep. Instruction/Exploded: flat even shadow-light vector/booklet render on an off-white page.

State coding:
- semantic colors (≤5 active, ONE focus accent): gray=structure/done, blue=live route, yellow=attention, green/mint=passed/gain, red=risk/failure, orange=in-progress, transparent=live signal.
- brick-native states: bare studs = to-build/open slot; smooth tile cap = done/sealed; cracked brick = broken; patch brick = repaired; gate arm up/half/down/locked = pass/hold/block/reject.
- pick only the 1-2 encoders that carry the precision; leave the rest neutral brick.

Composition:
- one focal build module; generous quiet baseplate; real depth (foreground build + action, mid modules, back skyline).
- clear start/change/result or before/action/after along one baseplate road if there's a process.
- Instruction mode: numbered step panels, an exploded "add these" arrow per step, a parts call-out box (e.g. 2×4 砖 ×3), a small finished preview in a corner.
- Exploded mode: parts aligned and floating on thin dashed drop-lines in assembly order; ghost of the whole optional.

Text (labels) — text is a BUILT/PLACED element, never a floating caption:
- choose a carrier per label and match its letterform: PRINTED TILE (friendly rounded sans, the workhorse) / BRICK-BUILT HERO LETTERS (blocky stud-grid, one big title or number) / STUDS-AS-PIXELS on a road / SIGNBOARD on posts / MINIFIG PLACARD / INSTRUCTION PAGE TYPE (neutral sans, step numbers + part counts) / BOX-ART BANNER (bold condensed display).
- the labels carry THIS content's REAL names and counts (real module names, real ×N), not placeholders.
- Chinese: on printed tiles/signs in a clean rounded sans; brick-build only 1-2 simple hero characters; route exact/multi-line Chinese to the overlay path (blank tiles, set text in an editor).
- RENDER ONLY THESE EXACT LABELS: {list the 3-6 exact glyph strings}. Do NOT invent extra Chinese sentences, captions, sub-text, or explanatory strips — unrequested text is exactly where the image model garbles glyphs. If a caption is truly needed, leave its tile blank for overlay.
- 3-6 short labels for a simple build; more when steps/modules/contrasts/groups need them; one hero text element max; attach every label to a real carrier; no floating text, no dense fake text, no garbled glyphs.

Quality target:
publish-grade explainer image; the structure reads in three seconds; tactile real bricks; original brick art; elegant, modular, not childish; not a voxel pile, not a PPT brick-icon grid, not a pretty cityscape that explains nothing.
```

## Mode Add-Ons

Append the matching block.

**Instruction Sheet:**
```text
Render as a build-instruction booklet page: 2-6 numbered step panels in a clean grid/flow, each showing the build AFTER that step with the newly-added bricks highlighted and hovering on a thin drop-line into their slot; a parts call-out box per step (small part icons + counts like 2×4 砖 ×3, 印字片 ×1); a step-number badge in a circle; a small finished preview thumbnail in a corner; flat even booklet light on an off-white page. This shows ASSEMBLY ORDER, not just a result.
```

**Exploded View:**
```text
Render as a technical exploded diagram in bricks: the build pulled apart along one axis, each of the ≤7 modules floating at its station aligned to its socket, connected by thin dashed vertical drop-lines in assembly order; a label tile or leader-line caption naming each module's job; an optional faint ghost of the assembled whole to one side; clean even light, light ground.
```

**Box Art:**
```text
Render as the front of an ORIGINAL build's box: hero build at a dynamic 3/4 angle on a themed backdrop; a bold readable ORIGINAL product-name banner (the topic's name, NOT a real set name, NOT the LEGO logo); a small spec strip (age-style badge, a "piece count" mapping to the topic's scope, a "minifig ×N included" corner); one accent color from the build; premium box-photography light.
```

## Text-Path Decision (HARD)

If the image has a list, multiple lines, exact wording, or any text that must be correct: use the **overlay path** — generate the build with **empty printed tiles / blank signboards** in the right spots, then set the exact text in an editor. Let the model render text only for a single very short hero word/title where one wrong glyph survives. Do not send multi-line Chinese to the image model and hope.

## Image-Edit Prompt

```text
Use $lego-town to edit this image.

Keep:
- the core structure and what it explains
- the real ABS brick material (studs, tubes, honest proportions)
- the original minifig identity (no licensed/branded faces)

Fix:
- make the CONNECTION carry the relation (stack for dependency, row for sequence, wall for containment, gears for feedback) instead of a drawn arrow
- remove any minifig that only stands/waves; make the remaining minifig perform a live action
- make labels short, readable, and attached to printed tiles / signs / call-outs
- remove voxel/Minecraft cubes, generic 3D blocks, the LEGO logo, or any licensed character; rebuild as original bricks
- strengthen one focal module and quiet the rest of the baseplate
```
