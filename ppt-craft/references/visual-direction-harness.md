# Visual Direction Harness

## Three Visible Directions

For non-trivial decks, create 3 visible first-slide previews before building the full deck. If the user explicitly says "directly generate" or gives a strict brand/template, skip previews and state the assumption.

Before choosing directions, run the local anchor selector:

```bash
python3 scripts/select_style_anchors.py --query "<deck brief keywords>" --limit 3
```

Then render starter previews for the selected anchors:

```bash
python3 scripts/render_style_anchor_starters.py --anchor "<anchor-id-1>,<anchor-id-2>,<anchor-id-3>" --out /tmp/ppt-craft-selected-starters
```

Use anchor output and starter previews as design DNA, not as visible slide text.

For decks where visual quality is the main risk, generate ImageGen visual oracle plates before implementation. Read `references/imagegen-first-visual-oracle.md`, create a target plate with real slide copy, then extract `visual-tokens.json` with:

```bash
python3 scripts/extract_visual_tokens.py <oracle-or-reference-image.png> --out <deck>/visual-tokens.json
```

The oracle is the visual ceiling; the final deck still needs editable, blueprint-aligned HTML/PPTX layers unless the chosen route is raster.

Before drawing each direction, write a small composition blueprint. The preview should prove not only palette and typography, but also where the title, supporting copy, visual subject, proof object, and loop/path live. A beautiful image with text placed afterward is not a direction; it is a wallpaper test.

Each preview must:
- Look like a real first slide, not a diagnostic card.
- Use real deck content.
- Fit the final route's stage constraints.
- Show typography, palette, image policy, and one motion/atmosphere cue.
- Show a believable layout grammar for at least one content-heavy slide, not only a cinematic cover.
- Be consistent with a starter set that already proved cover, proof, system, and closing roles.
- Avoid internal text: no "Option A", "preview", "style preset", file names, prompt notes.

After previews, ask the user to pick, mix, or revise. If no structured input tool exists and the user is absent, pick the strongest direction and continue, noting the assumption.

## Style Registers

Use these as starting points, not templates:

| Register | Good for | Visual thesis |
| --- | --- | --- |
| Editorial Magazine | culture, research, narrative reports | Serif display, controlled image crops, captions, high contrast type scale |
| Swiss Grid | professional reports, architecture, consulting | Strict grid, red/blue accent, restrained type, visible alignment |
| Data Desk | finance, AI market, strategy | Dense but ordered charts, dark or light institutional palette, tabular numbers |
| Studio Keynote | product launches, vision decks | Large claims, cinematic full-slide moments, sparse copy |
| Paper System | education, knowledge, async reading | Warm paper, tabs, diagrams, annotations, gentle hierarchy |
| Technical Blueprint | engineering, systems, AI architecture | Grid, dimension lines, cool palette, precise labels |
| Bold Poster | manifesto, campaign, founder talk | Massive type, one accent color, few words, graphic confidence |
| Calm Trust | healthcare, public sector, compliance | Soft neutral surfaces, high legibility, restrained motion |
| Playful Learning | classroom, kids, lightweight training | Friendly shapes, simple metaphors, clear steps |
| Premium Minimal | luxury, executive, portfolio | Sparse composition, material texture, confident negative space |

## Anti-Slop Checks

Reject a direction when:
- It could fit any AI/SaaS deck after only changing the title.
- It uses purple gradients, emoji icons, generic rounded card walls, or stock bokeh as the main identity without source justification.
- Every slide has the same card grid.
- The cover is beautiful but the content slide system is undefined.
- The selected anchor has not shown proof/system/closing starter viability.
- No ImageGen oracle or reference-token pass was created for a high-polish/high-stakes deck.
- Text is placed on top of a busy background without a reserved quiet field, mask, or crop.
- The loop/path is decorative and does not explain the deck's argument.
- The style hides the user's actual assets or brand.

## Style Lock

After a direction is chosen, write a short style lock:

```text
style lock:
- visual thesis:
- palette:
- type system:
- layout grammar:
- image policy:
- motion tone:
- forbidden drift:
```

Carry the style lock through every slide. If context gets long, re-read it before continuing.
