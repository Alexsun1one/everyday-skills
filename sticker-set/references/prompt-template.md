# Prompt Template

Generate the model sheet first to lock the character, then one sticker at a time.

## Planning Template

```text
Use $sticker-set. First plan, do not generate yet.

Character idea / mascot / pet photo / vibe:
{paste}

Set size:
{6-16}

Chat moments to cover:
{打招呼 / 赞同 / 摆烂 / 笑死 / 已读不回 / 催 / 夸人 / 晚安 / ...}

Delivery:
{grid sheet / individual stickers}

Return:
- character (one line)
- character DNA (3-5 fixed traits: silhouette, palette, head shape, line weight, signature accessory)
- per sticker: chat moment | emotion/action | caption (≤ 6 字)
- model sheet prompt
- QA risks
```

## Model Sheet Prompt (generate this FIRST)

```text
Generate one character model sheet in the Sticker Set style.

Square 1:1, clean white or flat single-color background.

Character:
{one original character — what it is, in one sentence}

Visual register — routed by character vibe (style-routing.md), LOCKED across the whole set:
{圆润流行 (Zagnoli) / 水墨·工笔 ink (国潮·古风) / 减法扁平 (McFetridge) / 剪纸纯色 (Matisse) / 大头卡通 (沙雕)}
- this register governs line, fill, palette feel, and ground for the model sheet and every sticker

Character DNA — keep these IDENTICAL in every later sticker:
- silhouette / body shape: {…}
- palette: {2-4 colors in fixed roles}
- head shape & face layout: {…}
- line weight & rendering: {clean even outline, flat fill / soft shading}
- one signature accessory: {hat / scarf / cheek blush / tail shape}

Layout:
- the character in one neutral front pose, plus a small grid of expressions
  (happy, tired, angry, crying, laughing, smug) — a 表情九宫格 / model sheet
- this sheet is the reference that locks the character's identity

Style:
- cute or funny, on-model, like a real chat sticker pack
- expressive but never creepy, melted, or uncanny
- ORIGINAL character — not Disney / 宝可梦 / LINE FRIENDS / 玲娜贝儿 / 蛋仔 or any existing IP

No caption text on the model sheet — this is identity reference only.
```

## Per-Sticker Generation Prompt

**Attach the model-sheet image as a reference/image input** (img2img / reference-image / same
seed where the tool supports it). A text description of a silhouette does not reproduce a
character — this image handle is what actually holds the set together. If the tool has no
reference-image input, crop one expression off the model sheet and inpaint a new pose rather
than text-prompting from scratch.

```text
Generate one chat sticker in the Sticker Set style, matching the locked character.

Same character as the ATTACHED model sheet — keep ALL fixed traits identical:
visual register, silhouette, palette, head shape, line weight, signature accessory.
Only change pose, expression, prop, and caption.

Square 1:1, clean white or flat single-color background, easy to cut out.

Chat moment:
{when the user sends it — e.g. 对方已读不回时}

Expression / action:
{e.g. 双手叉腰瞪眼 / 瘫倒在地}

Caption — render this exact text, correct Chinese characters, ≤ 6 字, no other text:
"{caption}"

Caption treatment:
- big and readable at small chat size
- placed top or bottom, off the character's face, with clean contrast
- 网络用语口吻

Style:
- on-model with the rest of the set, cute or funny, never creepy or uncanny
- the expression and the caption say the same thing
```

## Consistency / Text-Fix Edit Prompt

When a sticker drifts off-model OR the caption renders wrong:

```text
Use $sticker-set to edit this sticker.

Keep:
- the chat moment, pose, and caption intent

Fix (pull back on-model):
- match the model sheet exactly: same silhouette, palette, head shape, line weight, accessory
- this must be the SAME character as the rest of the set, not a lookalike

Fix (caption):
- re-render the caption as EXACTLY: "{correct text}"
- correct clean Chinese characters, ≤ 6 字, no melted/doubled/gibberish glyphs
- placed top or bottom, off the face, readable at small size
- remove any extra hallucinated text or watermark
```

## Fallbacks

- If the model drifts and a sticker stops looking like the character, regenerate it from the
  model sheet rather than nudging the bad output.
- If Chinese captions render badly, generate the sticker with a clean empty caption zone in
  the right place, then overlay the exact caption text in an editor.
