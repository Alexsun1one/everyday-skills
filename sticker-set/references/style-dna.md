# Sticker Set Style DNA

Use this reference before final sticker generation.

Sticker Set makes chat sticker packs whose identity comes from one original character
repeated consistently across the whole set, a clean cuttable background, and a big readable
≤ 6 字 caption — like a real sticker pack a person would actually send, not a pretty
one-off drawing and never a copy of an existing IP.

## Core Look

- Square 1:1 (e.g. 1024×1024). The character fills the frame with a little margin to breathe.
- Clean flat single-color or white background — easy to cut out, easy to drop into any chat.
- One original character, drawn the SAME way in every sticker of the set.
- Big readable caption ≤ 6 字, placed top or bottom, never crammed across the character's face.
- Expressive pose and face — exaggerated emotion is good — but never creepy or uncanny.
- Consistent line weight, palette, head shape, and proportions across ALL stickers.
- Cute or funny and on-model. The personality is in the expression, not in five new colors.

## Platform deliverable

A white background is NOT send-ready — it still needs cutting out. For a real platform pack
(微信 / LINE / Telegram), the deliverable is a **transparent PNG** at the platform's required
size (微信 表情 are 240×240; 主图/封面 have their own sizes). So: generate on a flat, removable
background, then key it out to alpha. Don't call a sticker finished until it is transparent and
correctly sized. GIF packs follow the platform's frame/size limits too.

## Character Consistency Rules

The pack must read as one character. Lock these and keep them frozen:

- silhouette / body shape
- palette (the same few colors in the same roles)
- head shape and face layout
- line weight and rendering style
- one signature accessory (a hat, a scarf, a cheek blush, a tail shape)

Only these may change between stickers:

- pose and gesture
- facial expression
- the prop being held or reacted to
- the caption

Recommended technique: generate a MODEL SHEET first (角色三视图 / 表情九宫格 reference),
then derive every sticker from it. The model sheet is the source of truth. If a sticker
drifts, regenerate it from the model sheet — never let a good pose justify a wrong character.

## Caption Rules

The caption is part of the sticker, not an afterthought. It must:

- be ≤ 6 Chinese characters, big and readable at small chat size
- sit cleanly at top or bottom, off the face, with enough contrast to read
- use 网络用语口吻 — how people actually type (笑死 / 摆烂 / 在吗 / 蚌埠住了), not 书面语
- render exact, correct Chinese characters — no melted, doubled, or gibberish glyphs
- match the chat moment exactly; the words and the expression say the same thing

If the model cannot render clean Chinese, leave the caption zone empty and overlay text later.

## Not Off-Model

Do not let the set fall apart into different characters:

- no shifting head shape, body proportion, or color from sticker to sticker
- no swapping the signature accessory in and out
- no changing line weight or rendering style mid-set
- no "same vibe, different creature" — it must be the literal same character

## Not Creepy

Do not cross into uncanny valley:

- no photoreal human faces forced into a cartoon body
- no melted faces, fused limbs, extra fingers, dead staring eyes
- no over-detailed realism that makes a cute character unsettling
- exaggeration is fine; horror is not

## Not an IP Copy

The character must be original. Do not copy or trace existing IP:

- no Disney, 宝可梦/Pokémon, 三丽鸥/Sanrio, LINE FRIENDS characters
- no 玲娜贝儿, 蛋仔, Loopy, capybara-brand mascots, or any recognizable licensed face
- no "looks 95% like X but renamed" — design a genuinely new character

## World-Class Quality Bar

Accept only if:

- the whole set reads as one character — same silhouette, palette, head, line weight
- every sticker maps to a real chat moment someone would send it in
- each caption is ≤ 6 字, readable, correct, and in the right 网络 tone
- the background is keyed to true alpha (open the PNG on a colored canvas and confirm no white
  halo / fringe around the character), exported at the platform's required size
- it is genuinely funny or useful, not just pretty — and the character is original

Reject if:

- the set drifts off-model and looks like several different characters
- a sticker has no chat moment and is there to fill the grid
- a caption is unreadable, garbled, wrong characters, or stiff 书面语
- it is creepy, melted, or uncanny
- the background is busy and hard to cut out
- the deliverable is a flat white/colored square, not a keyed transparent PNG at the platform
  size (微信 240×240) — a sticker that still needs manual cutting-out is NOT shipped
- it copies or closely imitates an existing IP
