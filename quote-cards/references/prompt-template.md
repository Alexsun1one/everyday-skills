# Prompt Template

Generate one card at a time.

## Text rule (decide before generating)

A card is exact, multi-layer text — the hardest thing for an image model to render correctly.
**Default to text-last:** generate the card's field, grid, and layout with clean EMPTY text
zones, then set the exact hero / support / meta text in an editor where you control the font,
hierarchy, and correctness. Only let the model render text when it is one very short hero line
and a wrong glyph is survivable. Do not burn generations re-rolling broken Chinese — the
"Final Generation Prompt" below is for the in-image path; prefer the overlay path for anything
with a list, multiple lines, or exact wording.

## Planning Template

```text
Use $quote-cards. First plan, do not generate yet.

Source (quote / tip list / book note / number / steps / concept):
{paste}

Aspect ratio:
{1:1 square / 3:4 vertical}

Return:
- one idea
- card type
- who saves it & why
- hierarchy (1st / 2nd / 3rd)
- text content, exact
- alignment
- palette & fonts
- layout
- final generation prompt
- QA risks
```

## Final Generation Prompt

```text
Generate one typographic card in the Quote Cards style.

Aspect ratio:
{1:1 square / 3:4 vertical}

Card type:
{金句 / 干货清单 / 读书笔记 / 数据 / 步骤 / 概念}

Aesthetic register — routed by content (style-routing.md), applied to the whole card:
{e.g. 水墨·文人画 (rice paper + vertical 书法 hero + 印章) / Hara 留白 / Swiss·Vignelli 网格 / editorial / Rothko 色场}
- ground, palette, and type voice follow this register; 古诗词/国学 always route to ink
- the hierarchy (hero → support → meta) and the text rule below run inside it

One idea:
{the single thing this card carries}

Text — render this exact text, correct Chinese characters, no other text:
- hero (1st): "{the dominant line / number / term}"
- support (2nd): "{context / definition / list points / highlighted line}"
- meta (3rd): "{source / author / page / 来源, small}"

Hierarchy & type:
- hero is the dominant element, much larger and bolder than the rest — reads first
- support is a clear step down in size and weight
- meta is small and calm, a quiet footnote
- max two fonts: one strong font for the hero, one quieter for support
- do NOT set everything the same size

Alignment:
- {centered for a short quote/single hero line / left-aligned for lists, steps, definitions}
- one alignment held throughout the whole card

Layout:
- {archetype-specific layout from card-archetypes.md}
- generous, even margins on all four sides; the card breathes
- negative space is a feature; the hero sits in a calm field, not crammed to the edge

Palette:
- paper / off-white base, deep ink for text
- at most one accent color, on the {number / key word / a small block / a thin rule}
- optional subtle paper grain or a single flat accent block behind one line

Decoration:
- quiet only: a thin rule, a large faint quotation mark, a small accent block, or a numeral
- no clip art, stickers, emoji, mascots, gradient glow, sparkle, or title bar on everything

Style:
- typographic-led, restrained, collectable — something a person would screenshot and save
- no PPT slide look (equal-weight bullets, colored title bar, slide footer)
- no poster (no large imagery dominating the text)
- no 微商 (no gold-red glow, urgency badges, sticker pile, rainbow palette)
- no AI plastic: no melted text, no doubled or gibberish characters, no hallucinated watermark

Quality target:
save-worthy card, one idea, the eye lands on the hero first, clear hierarchy, generous space,
correct clean Chinese characters.
```

## Text-Fix Edit Prompt

Image models often mangle Chinese characters. When the composition is good but the text is
wrong or the hierarchy is flat:

```text
Use $quote-cards to edit this card.

Keep:
- the composition, layout, palette, and alignment

Fix:
- re-render the text as EXACTLY:
  - hero: "{correct hero text}"
  - support: "{correct support text}"
  - meta: "{correct meta text}"
- correct, clean Chinese characters, no melted/doubled/gibberish glyphs
- strengthen hierarchy: enlarge the hero, shrink the support and meta so the eye lands on
  the hero first
- remove any extra hallucinated text, watermark, or logo
```

If the model cannot render clean Chinese text, fall back to: generate the card layout with a
clean empty hero zone in the right place, then overlay the exact text in an editor.
