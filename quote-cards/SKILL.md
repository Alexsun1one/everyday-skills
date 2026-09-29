---
name: quote-cards
description: Generate or plan beautiful, collectable typographic cards that carry ONE idea — a quote, a tip, an insight, a book takeaway, a data point, or a definition. Use when a user wants a 金句卡, 知识卡片, 干货卡, 读书笔记卡, 语录卡, 卡片图, 文字卡, 收藏卡, quote card, knowledge card, or any single-idea card whose job is to be saved and shared (收藏 / 转发), not to bait a click. Especially useful for turning a sentence, a short list, a book note, a number, a workflow, or a term-and-definition into a clean, screenshot-worthy card with clear typographic hierarchy and generous space. Do not use for social cover/hero images that earn a tap (use a cover skill), dense infographics, posters dominated by imagery, logos, or stickers.
---

# Quote Cards

Quote Cards turns one idea into a beautiful, collectable typographic card — the kind of image a person screenshots and saves.

A card is not a click-bait cover and not a poster. Its job is 收藏 / 转发: someone reads it, feels the idea land, and keeps it. The whole quality moat is typographic discipline — clear hierarchy, restraint, generous negative space. The opposite of a crammed PPT slide or a 微商 poster. If the card said the same thing as plain copy-pasted text, the typography added nothing. Use this skill to plan and generate cards where the type builds hierarchy, makes the key point land faster, and makes the idea feel worth saving.

## Workflow

1. Read the quote, tip, insight, book takeaway, number, or definition.
2. Find the ONE idea the card will carry. One card, one idea.
3. Decide who would save it, and why.
4. Choose a card type from `references/card-archetypes.md`.
5. Run the Save Test: is there one idea worth a whole card, and would someone save it?
6. Set the hierarchy: what the eye hits 1st, 2nd, 3rd.
7. Lock the typography with `references/typography-system.md` — one dominant element, strong scale contrast, one alignment, generous margins.
8. Route the register by content with `references/style-routing.md` (金句 → Hara 留白/Swiss, 古诗词/国学 → 水墨+书法+印章, 干货清单/数据 → Vignelli 网格, 读书笔记 → editorial) — the content picks the look automatically — then apply `references/style-dna.md` inside it.
9. Build the final image prompt with `references/prompt-template.md`.
9b. Decide the text path (HARD): if the card has a list, steps, multiple lines, or any exact
    wording that must be correct, you MUST use the overlay path — generate the field / grid with
    EMPTY text zones and set the exact text in an editor. Let the model render text only for a
    single very short hero line where one wrong glyph is survivable. Do not send multi-line Chinese
    to the image model and hope.
10. Generate one card at a time.
11. Run QA with `references/qa-checklist.md`; regenerate if it looks like a PPT slide, has no hierarchy, is over-full, or the text is garbled.

## Save Test

Before generating, answer:

```text
card plan:
- one idea: the single thing this card carries
- card type: 金句 / 干货清单 / 读书笔记 / 数据 / 步骤 / 概念
- aesthetic register (routed by content): 水墨·书法 / Hara 留白 / Swiss·Vignelli 网格 / editorial / Rothko 色场
- who saves it & why:
- hierarchy: what the eye hits 1st / 2nd / 3rd
- text content: exact text
- forbidden drift: 信息过载 / 像 PPT / 像海报 / 排版没层级 / 配色花
```

Generate a card only when there is one savable idea and a clear 1st / 2nd / 3rd hierarchy. Good answers:

- "一句话金句做主角，署名小、留白大，一眼就想存。"
- "清单有标题 + 5 个短点，编号清楚，不是平权 PPT 项目符号。"
- "一个大数字当英雄，下面一行语境，角落一行小来源。"

Weak answers:

- "一张卡塞了 5 个观点。"
- "全部字一样大，没有焦点。"
- "排版跟正文一样，存它和复制文字没区别。"

A card that carries five ideas carries none, and a card with no focal line is just text in a frame. If the typography does not build hierarchy and make the point land faster, do not generate it.

The Save Test is FAIL by default. It PASSES only when ALL of these are concretely answerable: (1) the ONE idea fits in a single hero line / number / term — if it needs two clauses joined by 而且/and, it is two ideas, cut one; (2) "who saves it & why" names a specific person and a specific reason to save THIS card rather than re-read the source text (e.g. "准备面试的人存来背" — not "对内容感兴趣的人"); (3) the 1st / 2nd / 3rd hierarchy lists three DIFFERENT elements at clearly different sizes, not the same line described three ways. If any answer is generic or the idea won't fit one hero line, do NOT generate.

## Default Look

Read `references/typography-system.md` and `references/style-dna.md` before generating final cards.

Core visual DNA:

- one dominant text element — the hero line — with strong scale contrast against everything else
- typographic-led, restrained, collectable; the card reads as something worth saving
- square 1:1 by default (1080×1080); 3:4 vertical for longer cards (lists, steps)
- one alignment, held throughout; left-align for lists, centered only for short quotes
- generous, consistent margins; the card breathes; negative space is a feature
- paper/ink base + at most one accent color; max two fonts
- quiet decoration only: a thin rule, a large quotation mark, a small accent block, a number
- correct, clean Chinese characters — no melted, doubled, or gibberish glyphs
- no equal-weight PPT bullets, no title bar slapped on everything
- no big imagery drowning the words, no clip art, stickers, or gradient glow
- no rainbow palette, no 微商 gold-red urgency, no AI-plastic text

## Card-Type Adaptation

Cards are not one shape. Pick the type that matches the source — see `references/card-archetypes.md`:

- 金句卡: one quote dominant, attribution small, lots of negative space; source is a quote or line.
- 干货清单卡: a title + 3–7 short numbered points; source is a list of tips.
- 读书笔记卡: book + author header, one takeaway as the hero; source is a book note.
- 数据卡: one big number is the hero, a context label, a tiny source line; source is a stat.
- 步骤卡: numbered steps in a clean vertical flow, one verb each; source is a how-to.
- 概念卡: a term + a one-line plain-language definition + a tiny example; source is a concept.

Let the source pick the type. Never stack two types on one card, and never force a quote layout onto a list or a number.

## Aesthetic Routing (automatic, by content)

A collectable card is typographic design, not text dropped on a color. The register is
**routed by the content** — the card type and the topic's culture — not hand-picked. See
`references/style-routing.md`. The skill reads what the card carries and applies the fitting
register automatically:

- 金句/语录 (single modern quote) → Kenya Hara emptiness or Swiss: near-white field, one ink tone, big 留白.
- 古诗词/国学/国风/古文 (any type) → 水墨/文人画: rice paper, vertical 书法 hero, 留白, one red 印章 accent — culture wins over card type.
- 干货清单/步骤/数据/概念 → Müller-Brockmann/Vignelli grid: a real grid, numbered rail in one accent, flat color as a coding system. Multi-line content needs the grid, NOT a maximal void.
- 读书笔记 → editorial: refined serif, a quiet rule, book+author header.
- 治愈/情绪金句 → Rothko color field behind the short quote.

Restraint for every card: one accent, max two fonts, generous even margins, no decoration that
doesn't serve hierarchy. The routed register elevates the field and type; the hierarchy (hero →
support → meta) still leads. Cards forbid clutter — never route to a maximalist register.

## Output Contract

For planning, return:

```text
one idea:
card type:
who saves it & why:
hierarchy (1st / 2nd / 3rd):
text content (exact):
alignment:
palette & fonts:
layout:
final image prompt:
QA risks:
```

For generation, produce one card at a time and report:

- image path
- aspect ratio (1:1 / 3:4)
- the exact text rendered, by hierarchy level
- one-line purpose
- whether it passes QA or needs regeneration

## References

- `references/style-routing.md`: route the register by content (古诗词 → ink, data → Vignelli, 金句 → Hara) — read this with typography-system.
- `references/style-dna.md`: the visual identity, the collectable bar, and anti-PPT / anti-poster rules.
- `references/card-archetypes.md`: card types, when to use each, layout and a Chinese example.
- `references/typography-system.md`: the heart — hierarchy, type scale, alignment, spacing, palette, decoration restraint.
- `references/prompt-template.md`: planning, final generation, and text-fix edit templates.
- `references/qa-checklist.md`: acceptance, regeneration, and repair rules.
