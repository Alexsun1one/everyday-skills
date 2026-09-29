# Prompt Template

Generate one image at a time. Always write the prompt in token terms applied to the user's
subject — never "in the style of {artist}".

## Planning Template

```text
Use $master-styles. First plan, do not generate yet.

Subject / what we are making:
{a cover for X / a card about Y / a portrait of Z}

Desired feeling:
{elegance / punch / warmth / gravitas / narrative / opulence / loud}

Return:
- structure token (from which master / what it is)
- palette·light token (from which master / what it is)
- shared restraint (the one refusal both obey)
- anti-pastiche check (does NOT reproduce {famous work}; subject stays hero)
- how the tokens map onto this subject
- final generation prompt
- QA risks
```

## Final Generation Prompt

```text
Generate one image with a world-class, art-directed look. Apply these visual tokens to the
subject below. Do NOT reproduce any artist's actual famous work — borrow the rules only.

Subject:
{what the image is of, in plain terms}

Desired feeling:
{elegance / punch / warmth / gravitas / narrative / opulence / loud}

Structure token:
{e.g. asymmetric mathematical grid, content snapped to columns, large active whitespace}
{or: extreme tight face crop on a void, centered, frontal, slightly low angle}
{or: tiny faceless figure dwarfed by a vast environment, cinematic wide framing}

Palette · light token:
{e.g. two clashing flat saturated colors + black ground, no gradients}
{or: low raking light, long hard-edged shadows, muted palette + one warm accent}
{or: near-white field + one ink tone, flat diffuse shadowless light}

Shared restraint (keep strictly):
{e.g. no gradients, all flat / no environment, subject on a void / no decoration / no facial detail}

How the tokens serve the subject:
{one line — the style clarifies or elevates the subject, never buries it}

Composition & space:
- one clear focal element; the subject reads first, the style second
- {negative space / density value from the chosen masters}

Text & overlay (HARD — Chinese by default):
- If the subject is Chinese / ink-register, set any title, label, or tier mark as CORRECT
  Chinese — vertical 书法 for titles, a single red 印章 as the one warm accent, a quiet 宋体
  for body. Tier labels render as 神品/逸品/妙品/能品 in brush, never S/A/B/C.
- Every glyph must be a real, correct character. No melted, doubled, mirrored, or invented
  glyphs; no fake-Chinese-looking strokes. If clean text is impossible in-model, render the art
  with an empty calligraphy/seal zone for overlay rather than shipping garbled text.
- The seal (印章) is one small red mark, not a logo pile; the calligraphy column reads
  top-to-bottom, right-to-left.

Quality target:
gallery-grade, intentional, like a real designer made it; the rule is borrowed, the picture is original; the subject stays the hero.
```

## Layering on another skill

When elevating a cover, card, or ranking card: plan the CONTENT with that skill first, then add
one structure token + one palette/light token + one restraint from here. Example add-on line:

```text
Art direction (master-styles): Platon-style face-on-void portraits (tight crop, butterfly light,
neutral void) + a Müller-Brockmann grid for the layout. Restraint: no environment, no decoration.
Apply to the ranking card's portrait pipeline and grid. Do not imitate any actual Platon photo.
```

## Edit Prompt

```text
Use $master-styles to edit this image.

Keep:
- the subject and its focal hierarchy

Fix:
- apply the {structure} token more clearly: {specific change}
- enforce the restraint: remove {gradients / decoration / background clutter} that breaks it
- pull the palette to {token} so the look is intentional, not generic
- ensure the style serves the subject — if the style dominates, dial it back
```
