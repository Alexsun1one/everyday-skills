---
name: cover-pop
description: Generate or plan thumb-stopping social cover images for Xiaohongshu (小红书), WeChat Moments, public-account covers, Douyin/video thumbnails, and post headers. Use when a user wants a 封面图, 小红书封面, 公众号封面, 视频封面, 笔记首图, or any single hero image whose one job is to make the right reader stop scrolling and tap. Especially useful for turning a note topic, title idea, product, tutorial, list, or before/after into a clear, click-earning cover with a strong readable title and a clean, non-tacky look. Do not use for full article body illustrations (use an illustration skill), logos, stickers, or dense infographics.
---

# Cover Pop

Cover Pop turns a topic into a social cover image whose single job is to make the right reader stop scrolling and tap.

A cover is not decoration and not a poster. It is a one-second pitch. If the cover does not earn the tap, nothing else in the note matters. Use this skill to plan and generate covers with a strong readable title, a clear visual hook, one promise, and a clean look that does not read as 微商 spam, 土味 poster, or AI plastic.

## Workflow

1. Read the topic, title idea, note draft, product, or screenshot.
2. Identify the target reader and the one moment they are scrolling in.
3. Write the core promise: what the reader gets if they tap.
4. Choose a cover archetype from `references/cover-archetypes.md`.
5. Run the Stop Test: would this reader stop, and is the promise real?
6. Write the title line(s) using `references/title-formulas.md` — short, concrete, readable at thumbnail size.
7. Route the aesthetic register by niche/mood/subject with `references/style-routing.md` (知识/干货 → 瑞士网格, 国风/国学 → 水墨, 产品 → 工作室静物, 情绪 → Hopper+留白) — the subject picks the look automatically — then apply `references/style-dna.md` inside it.
8. Build the final image prompt with `references/prompt-template.md`.
9. Generate one cover at a time.
10. Run QA with `references/qa-checklist.md`; regenerate if the title is unreadable, the hook is empty, the look is tacky, or it is cluttered.

## Stop Test

Before generating, answer:

```text
cover plan:
- one job: make {target reader} stop and tap
- target reader:
- scroll moment: where/when they see it (信息流缩略图 / 搜索结果 / 推荐页)
- core promise: what they get if they tap
- hook: the visual or word that interrupts the scroll
- title line: ≤ 15 字 main line, optional ≤ 10 字 sub line
- archetype:
- aesthetic register (routed by subject): 瑞士网格 / 水墨 / 工作室静物 / Hopper+留白 / 大胆极简 / 圆润流行 …
- why not scrolled past:
- forbidden drift: 标题党空心 / 微商风 / 信息过载 / AI 塑料感
```

Generate a cover only when `why not scrolled past` is concrete and the promise is real. Good answers:

- "数字 + 具体收益让人想知道是哪几个。"
- "反差封面制造缺口：左边的错法是读者正在犯的。"
- "标题点名了目标人群，他们会对号入座。"

Weak answers:

- "颜色很好看。"
- "字很大。"
- "加了个 emoji。"

**Forward Test (run before generating).** State the answer as a competitor swap: write the ONE rival cover this reader is also seeing in the same feed, then finish this sentence with a concrete reason — "They tap THIS one instead of that one because ____." The blank must name a mechanism the image actually shows (a number, a named reader group, a visible ✗/✓ gap, a result), not a property of the cover ("颜色好看", "字大", "很高级"). If the blank could be pasted onto any other cover in the niche, it fails — rewrite the hook or reject the plan. Also write the literal payoff line: "Behind the tap is: ____" naming the specific thing the note delivers. If that line is empty or generic, the promise is clickbait — reject.

A pretty cover with an empty promise is clickbait; it loses the reader on the second screen and trains the algorithm against the account. Reject it.

## Default Look

Read `references/style-dna.md` before generating final covers.

Core visual DNA:

- title is the hero: one dominant line, readable at 200px thumbnail size, high contrast against its backdrop
- one promise, one focal subject — not a collage of everything
- restrained palette: one base, one accent, one ink; no rainbow gradients
- real texture over plastic gradients: clean photo, flat color block, paper, or soft studio light
- generous breathing room; the title is never crammed edge to edge
- platform-correct aspect ratio (default 小红书 3:4 vertical)
- no 微商-style gold-on-red, scattered stickers, glow bursts, fake "限时" badges
- no AI-plastic skin, melted text, six-finger hands, or gibberish characters
- no PPT title-slide look, no generic stock-photo-plus-watermark

## Archetype Adaptation

Covers are not one shape. Pick the archetype that matches the note's job — see `references/cover-archetypes.md`:

- 大字封面: the title IS the image; topic is opinion, declaration, or a strong single line.
- 反差/避坑封面: before/after or wrong/right; topic is a mistake, fix, or transformation.
- 清单/数字封面: "N 个…"; topic is a list, roundup, or resource pack.
- 教程/步骤封面: shows the end result + "手把手"; topic is a how-to.
- 情绪/共鸣封面: a feeling the reader is in right now; topic is an essay, mood, or relatable moment.
- 实拍/好物封面: a real object shot well; topic is a product, food, place, or haul.
- 盘点/合集封面: a tidy grid of items; topic is a collection or comparison.

Let the topic pick the archetype. Do not force a 大字 declaration onto a product haul, or a tidy grid onto a raw personal essay.

## Aesthetic Routing (automatic, by subject)

A great cover is clear AND looks designed. The visual register is **routed by the topic**, not
hand-picked — see `references/style-routing.md`. The skill reads the niche/mood and applies the
fitting master register automatically: 知识/干货 → Swiss grid, 国风/国学/古诗词 → 水墨/文人画 (rice
paper, 书法 title, 印章 accent — never a neon gradient), 产品/好物 → studio still-life (composite
the real product), 情绪/共鸣 → Hopper raking light + Hara emptiness, 穿搭/美妆 → bold editorial
(Malika Favre), 母婴/萌宠 → rounded pop (Zagnoli). The user does not name a style.

Rule: route to ONE register, apply its tokens, keep one restraint (e.g. "one accent, lots of
negative space"). The title and subject stay the hero; the register serves readability, never
buries it. Covers forbid clutter — never route a clean cover to a maximalist register.

## Output Contract

For planning, return:

```text
target reader:
core promise:
scroll moment:
archetype:
hook:
title line(s):
why not scrolled past:
layout & palette:
final image prompt:
QA risks:
```

For generation, produce one cover at a time and report:

- image path
- platform & aspect ratio
- the exact title text rendered
- one-line purpose
- whether it passes QA or needs regeneration

## References

- `references/style-routing.md`: route the aesthetic register by niche/mood/subject (国风 → ink, knowledge → Swiss…) — read this with style-dna.
- `references/style-dna.md`: the visual identity and anti-tacky rules.
- `references/cover-archetypes.md`: cover types, when to use each, layout and title pattern.
- `references/title-formulas.md`: how to write the title line that earns the tap.
- `references/prompt-template.md`: planning, final generation, and text-fix edit templates.
- `references/qa-checklist.md`: acceptance, regeneration, and repair rules.
