---
name: rank-cards
description: Generate or plan professional ranking and tier cards (排名卡 / 段位卡 / tier list) for short-video covers and carousels — ranking football stars, basketball GOATs, writers, poets, musicians, directors, scientists, schools, universities, majors, cities, films, anime characters, or products into tiers with a stated, defensible basis. Use when a user wants a 球星排名卡, 历史地位卡, 段位卡, GOAT 金字塔, tier list, 顶级/普通 对比卡, top-10 排行, 大学排名卡, 专业排名, 诗人/作家排名, 城市排名, or a 谁更强/历史最强 card for 视频号 / 抖音 / 小红书 / YouTube. It ranks anything you can compare. The whole value is the harness: one unified subject-image pipeline (faces, logos, landmarks, or icons all treated identically), a stated ranking basis and scope, bounded warm→cool tiers, and clean typography — so it reads as designed, not a thrown-together collage. For real public figures, prefer compositing licensed/owned photos over photoreal impersonation, and never place a fabricated photoreal real person in a defamatory tier. Do not use for a plain single cover (use a cover skill), a typographic quote card (use a card skill), or content with no ranking/comparison.
---

# Rank Cards

Rank Cards turns a "who is better" question into a professional ranking card whose authority comes from a stated basis and whose polish comes from one unified portrait pipeline.

A ranking card is not a pile of portraits with labels. It makes a claim, and a claim needs two things to survive: a **defensible basis** (so it reads as judgment, not a random opinion that invites pile-ons) and **visual unity** (so every subject gets identical treatment and the card reads as designed, not a collage). The harness exists to force both. This skill works the same way across football, basketball, writers, musicians, directors, scientists, characters, or products — only three adapters change.

## Workflow

1. Read the ranking idea: who or what is being ranked, and the angle.
2. **Route the aesthetic register by subject** with `references/style-routing.md`: the subject picks the whole visual register — 古代诗人 → 水墨山水/文人画 with 神品/逸品 grades, 现代球星 → modern sports card, 西方作家 → 古典油画肖像. Never default everything to the sports look. This decides ground, portrait treatment, tier-label style, accents, and type before anything else.
3. Pin the scope: 现役/历史, position-only, club vs country, peak vs career. An unscoped ranking is the #1 cause of bad-faith arguments.
4. Choose the ranking basis from `references/tier-and-criteria.md`: 历史地位 / 巅峰统治力 / 荣誉 / 数据 / 影响力 / 时代调整. Pick one primary; optionally weight it. This goes ON the card.
5. Pick a tier system that fits the register: one vocabulary, 3–6 tiers, top tier scarce (sports → S/A/B/C or 球王/超巨; poets → 神品/逸品/妙品/能品).
6. List subjects and assign tiers; decide each subject's era / affiliation / source image.
7. Run the Ranking Integrity Test: is the register routed, the basis stated and scoped, and will every subject pass one pipeline?
8. Choose a layout archetype from `references/layout-archetypes.md` (cover → podium / versus / single-hero / pyramid; carousel → tier-row / grid).
9. Lock the subject-image pipeline with `references/portrait-pipeline.md`, INSIDE the routed register — same crop, same ground, one treatment, same edge, one art register.
10. Adapt props and criteria to the domain with `references/domain-adaptation.md`.
11. Build the final image prompt with `references/prompt-template.md`; generate one card at a time.
12. Run QA with `references/qa-checklist.md`; regenerate if the register is wrong for the subject, portraits drift into collage, the basis is missing, tiers sprawl, or names are unreadable.

## Ranking Integrity Test

Before generating, answer:

```text
rank card plan:
- domain: 足球 / 篮球 / 作家 / 诗人 / 音乐家 / 导演 / 科学家 / 学校 / 城市 / 角色 / 产品 / ...
- aesthetic register (routed by subject): 水墨山水 / 现代运动卡 / 古典油画肖像 / 编辑级肖像+网格 / 学院纹章 / ...
- ranking question: e.g. 历史最强后卫
- scope: 现役/历史 · 仅限{位置} · 俱乐部/国家队 · 巅峰 vs 生涯
- basis: primary criterion (+ optional weights), PRINTED on the card
- tier system: one vocabulary, 3-6 tiers, top tier scarce (1-3 names)
- subjects: name | tier | era/jersey/photo choice
- layout archetype:
- portrait pipeline: same crop / same background / one treatment / same edge / one art register
- forbidden drift: 拼贴感 / 无依据 / tier 太多 / 名字看不清 / 低清混搭 / 标签混形
```

Generate only when both gates pass their falsifiable test (not just a stated plan):

- **Credibility gate (falsifiable)** — the printed basis + scope must (a) be specific enough that swapping it would change at least one tier placement, and (b) survive the fan test: read the basis, then name the ONE placement the target fanbase would scream about; if that placement contradicts the stated basis, the basis is decoration — fix the tier. A basis that changes no placement is not a basis. Good: "按巅峰统治力，仅限现役中后卫。" Weak: "就是我觉得他强。"
- **Unity gate (falsifiable)** — do not approve from the plan; approve from the blur-the-faces test in `references/qa-checklist.md`: heavy-blur the rendered card, and if any cell pops out by crop / tint / background / edge, the gate fails. Mixed crops, backgrounds, and art styles are the loudest amateur tell.
- **Basis-governs-tiers (falsifiable)** — run the basis-governs-tiers test in `references/tier-and-criteria.md`: for the 2 highest-ranked and the 1 most-debatable subject, write the one-line reason its tier follows from the printed criterion value; if you cannot, or the line contradicts the basis, move the subject, not the label.

If any gate fails, fix the plan or regenerate before accepting.

## Default Look

First route the register with `references/style-routing.md`, then read `references/portrait-pipeline.md` and `references/style-dna.md`. The DNA below is the **modern-sports register**; other registers replace the look accordingly (ink-wash uses rice paper + 书法 grades + 印章 instead of duotone + warm→cool, etc.) while keeping the same structural harness.

Core visual DNA (modern-sports register; swap per routed register):

- one unified portrait pipeline: identical crop, shared background, one color treatment (duotone is the default unifier), one edge/ring, one art register across ALL subjects
- the ranking basis and scope printed on the card — a small but present credibility line
- 3–6 tiers in parallel-form labels (all letters OR all nouns, never mixed), top tier scarce
- warm→cool color ramp top→bottom: red(S/神) · orange(A/天王) · yellow(B/一流) · green(C) · blue(D) — rank is legible before the labels are read
- clear typographic hierarchy: title → tier label → rank number → name → basis line → optional stat chips → source
- default 3:4 vertical (1080×1440) for 视频号/抖音/小红书 covers; 1:1 for grid carousels
- no collage of mismatched photos, no unstated arbitrary ranking, no 7+ tier sprawl, no clip-art tier-maker chrome, no low-res faces

## Domain Adaptation

The harness is domain-invariant. Only three adapters change — see `references/domain-adaptation.md`:

- **portrait**: peak-era player photo, a writer's painted portrait, a director's headshot — but unify the register (never mix oil painting + modern photo in one card).
- **prop / affiliation**: jersey & position glyph, instrument, book cover, film motif, company logo.
- **criteria**: trophies/数据 for sports; 影响力/开创性/流传度 for culture. The act of stating it is identical and always mandatory.

## Output Contract

For planning, return:

```text
domain:
ranking question:
scope:
basis (printed line):
tier system & tiers:
subjects (name | tier | era/jersey/photo):
layout archetype:
portrait pipeline (crop/background/treatment/edge/register):
typography plan:
final image prompt:
QA risks:
```

For generation, produce one card at a time and report:

- image path
- aspect ratio (3:4 / 1:1 / 16:9)
- the basis line and scope as printed
- whether all portraits share one pipeline
- whether it passes QA or needs regeneration

## References

- `references/style-routing.md`: route the aesthetic register by subject (poets → ink-wash, footballers → sports card) — read this FIRST.
- `references/style-dna.md`: the visual identity and anti-collage / anti-tier-maker rules.
- `references/portrait-pipeline.md`: the unified portrait harness — the core of this skill.
- `references/tier-and-criteria.md`: tier vocabularies, ranking basis, and the credibility line.
- `references/layout-archetypes.md`: podium, versus, pyramid, tier-row, grid, single-hero.
- `references/domain-adaptation.md`: how to map the harness onto sports, culture, characters, products.
- `references/prompt-template.md`: planning, final generation, and text-fix edit templates.
- `references/qa-checklist.md`: acceptance, regeneration, and repair rules.
