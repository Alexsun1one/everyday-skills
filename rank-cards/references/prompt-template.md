# Prompt Template

Generate one card at a time.

## Planning Template

```text
Use $rank-cards. First plan, do not generate yet.

Ranking idea:
{who/what is ranked, and the angle}

Platform:
{视频号/抖音/小红书 3:4 / grid 1:1 / YouTube 16:9}

Return:
- domain
- ranking question
- scope (现役/历史 · 位置 · 俱乐部/国家队 · 巅峰/生涯)
- basis (printed line, optional weights)
- tier system & tiers
- subjects: name | tier | era/jersey/photo choice
- layout archetype
- portrait pipeline (crop/background/treatment/edge/register)
- typography plan
- final generation prompt
- QA risks
```

## Production path (decide first)

- **Path A — real people**: render the EMPTY card (frame, tier bands, chrome, empty name
  plates) with the prompt below, then composite editor-cutout portraits and overlay names in
  an editor. Do not ask the model to assemble real likenesses.
- **Path B — generated/illustrated subjects**: use the full prompt below and render every
  subject in one pass.

Text rule (both paths): names and the basis line are exact and usually multi-line — default
to overlaying them in an editor on empty plates. Only let the model render text when it is one
short headline and a wrong glyph is survivable.

## Final Generation Prompt

```text
Generate one professional ranking / tier card in the Rank Cards style.

Aspect ratio:
{3:4 vertical 1080×1440 / 1:1 / 16:9}

Title:
"{headline, e.g. 历史最强后卫 · 段位排名}"

Basis line — render this exact text:
"{e.g. 按巅峰统治力排名 · 仅限现役中后卫 · 个人向}"

Domain:
{足球 / 篮球 / 作家 / 音乐家 / 导演 / 科学家 / 角色 / 产品}

Layout archetype:
{podium / versus / pyramid / single-hero / tier-row / grid}

Tiers (parallel-form labels, warm→cool, top tier scarce):
- {S / 神}: {subject(s)} — red
- {A / 天王}: {subjects} — orange
- {B / 一流}: {subjects} — yellow
- {C / 二流}: {subjects} — green
{3-6 tiers}

Portrait pipeline — apply IDENTICALLY to every subject (faces):
- crop: all {head-and-shoulders / chest-up}, eyelines aligned, faces same scale
- background: one shared {solid / single gradient}, every subject knocked out onto it
- treatment: one {duotone (shadows→{colorA}, highlights→{colorB}) / matched key light} for all
- edge: all {clean cutout / same tier-colored ring}
- art register: all {photographic-realistic / illustrated} — never mixed
- era/affiliation: {peak-era / current}; {peak-club jersey / national}; held for everyone

Subject-image pipeline — for NO-FACE domains (schools / cities / majors / products):
- same subject-image type: all {crests / skylines / icons / product renders}
- same frame size, same backdrop, same treatment, one art register
- the five locks on a logo/landmark/icon instead of a face — no eyelines, no face scale

Typography:
- title heaviest, top
- tier labels bold in colored caps
- every subject name same size and baseline, high-contrast plate, legible at thumbnail
- big rank numerals outlined to read on portraits
- basis/scope line small but present
- optional 2-4 stat chips per subject ({金球×8} etc.)
- tiny source/disclaimer in a corner

Style:
- unified, designed, authoritative — not a collage of scraped photos
- consistent saturation; the tier ramp carries the color
- one focal structure; generous spacing
- no mismatched crops/backgrounds/art styles, no default tier-maker chrome, no low-res faces
- correct, clean Chinese characters — no melted, doubled, or gibberish glyphs

Quality target:
publish-grade ranking card; every portrait looks shot in one studio; basis stated; readable at a 2cm thumbnail.
```

## Text-Fix Edit Prompt

When the composition is good but text or a portrait is off:

```text
Use $rank-cards to edit this card.

Keep:
- the layout, tier structure, and color ramp

Fix:
- re-render the title and basis line as EXACTLY: "{title}" / "{basis}", clean Chinese characters
- make every subject name the same size and baseline, high-contrast, readable at thumbnail
- pull {subject} back through the portrait pipeline: same crop / background / duotone / edge as the rest
- remove any leftover original photo background or hallucinated watermark/logo
```

If the model cannot render clean Chinese text, generate the card with empty name/title plates
in place and overlay the exact text in an editor.
