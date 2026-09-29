# Prompt Template

Generate one cover at a time.

## Planning Template

```text
Use $cover-pop. First plan, do not generate yet.

Topic / title idea / note draft:
{paste}

Platform:
{小红书 3:4 / 公众号 2.35:1 / 视频 16:9}

Return:
- target reader
- core promise
- scroll moment
- archetype
- hook
- title line(s), exact text
- why not scrolled past
- layout & palette
- final generation prompt
- QA risks
```

## Text rule (decide before generating)

The title is a hero design element, so rendering a SHORT main line in-image is fine. But if
the title must be exactly correct, exceeds ~10 字, or has a sub-line, default to generating the
art with a clean empty title zone and overlaying the exact text in an editor — do not burn
generations re-rolling broken glyphs.

## Final Generation Prompt

```text
Generate one social cover image in the Cover Pop style.

Platform & aspect ratio:
{小红书 3:4 vertical / 公众号 2.35:1 / 视频 16:9}

Topic:
{one sentence}

Target reader:
{who is scrolling past, and in what moment}

Core promise:
{what they get if they tap}

Archetype:
{大字 / 反差 / 清单·数字 / 教程 / 情绪 / 实拍 / 盘点}

Aesthetic register — routed by subject (style-routing.md), applied to the whole cover:
{e.g. 瑞士网格 / 水墨·文人画 (rice paper + 书法 title + 印章) / 工作室静物 / Hopper 斜射光+留白 / 大胆极简编辑 / 圆润流行}
- ground, palette, light, and type voice all follow this register
- the title-legibility harness below runs inside it

Title — render this exact text, correct Chinese characters, no other text:
- main line: "{≤ 15 字}"
- sub line (optional): "{≤ 10 字}"

Title treatment:
- main line is the hero, heavy clean sans-serif (思源黑体 / 黑体 weight)
- readable at 200px-wide thumbnail, high contrast against its backdrop
- sits on a solid block / clean photo area / subtle highlight bar, not on busy texture
- at most one accent color or one highlight bar on the key word

Focal subject:
{one subject: the words themselves / a real object / a split before-after / a tidy grid / a quiet scene}

Layout:
- one focal subject, one promise, generous margins
- title placed in a calm zone with breathing room
- {archetype-specific layout from cover-archetypes.md}

Palette:
- follow the routed register's palette logic (ink+paper+seal-red for 水墨; two saturated flats for bold editorial; one base+one accent+one ink for grid/editorial)
- keep it restrained: avoid rainbow gradients regardless of register

Style:
- clean, premium, real — like a followable account in this niche
- real texture: clean photo / flat color block / paper grain / soft studio light
- no 微商 gold-red glow, scattered stickers, sparkle bursts, or fake urgency badges
- no 土味 WordArt, bevel, neon-on-neon, or double drop shadow
- no PPT title-slide look, no stock-photo-plus-color-bar
- no AI plastic: no melted text, no extra fingers, no waxy skin, no gibberish characters

Quality target:
publish-grade cover, title readable in one second, one real promise, would make the target reader stop scrolling.
```

## Text-Fix Edit Prompt

Image models often mangle Chinese characters. When the composition is good but the text is wrong:

```text
Use $cover-pop to edit this cover.

Keep:
- the composition, focal subject, palette, and layout

Fix:
- re-render the title as EXACTLY: "{correct text}"
- correct, clean Chinese characters, no melted/doubled/gibberish glyphs
- main line heavy and readable at thumbnail size
- remove any extra hallucinated text, watermark, or logo
```

If the model cannot render clean Chinese text, fall back to: generate the cover with a
clean empty title block in the right place, then overlay the exact title text in an editor.
