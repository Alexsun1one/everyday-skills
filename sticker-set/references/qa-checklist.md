# QA Checklist

## Accept

- **Lineup squint test (falsifiable):** shrink every sticker to 120px wide, lay all of them in
  one row, and describe the character in one sentence using only the silhouette + palette + head
  shape + signature accessory. If your one-sentence description does not fit EVERY sticker — if
  any sticker forces a different silhouette, color, head shape, or makes the accessory vanish —
  that sticker is off-model. Name which stickers fail and regenerate them from the model sheet.
  Do not pass the set on a full-size glance.
- The signature accessory is present and unchanged across every sticker.
- Each sticker maps to a real chat moment someone would send it in.
- **Send test (falsifiable):** for each sticker, name the last real chat where YOU would have
  sent it instead of an existing pack (e.g. 微信默认 / LINE 熊大 / a popular meme). State who you
  send it to and what their last message was. If the honest answer is "I would just send 哈哈哈 /
  a default emoji instead," the sticker earns nothing — cut it or sharpen the expression+caption
  until it beats the default. A sticker that only survives because the grid needs filling fails
  the send test.
- Each caption is ≤ 6 字 and in the right 网络 tone.
- **Caption chat-size test (falsifiable):** render or shrink the sticker to 240×240 (微信 表情
  size) and read the caption aloud. If any stroke merges, any character is ambiguous, or the text
  loses contrast against the body, the caption fails at deployment size — re-render
  bigger/higher-contrast, or drop to an empty caption zone and overlay the exact text per
  prompt-template.md. Judging legibility on the full-res render is not a pass.
- The caption renders correct Chinese characters — no melted, doubled, or gibberish glyphs.
- The caption and the expression say the same thing.
- **Caption-specificity test:** could this exact caption sit on any random sticker? If yes, it
  is filler — rewrite it to sound like this character.
- Background is keyed to true alpha (open the PNG on a colored canvas and confirm no white halo /
  fringe around the character), exported at the platform's required size.
- The character is original — no copied or closely imitated IP.

## Regenerate

- The set drifts off-model: stickers look like several different characters.
- The head shape, proportion, palette, line weight, or accessory shifts between stickers.
- A sticker has no chat moment and exists only to fill the grid.
- A caption is unreadable, garbled, wrong characters, or stiff 书面语.
- The caption sits on the face or has no contrast to read against.
- It is creepy, melted, or uncanny — dead eyes, fused limbs, extra fingers.
- The background is busy and hard to cut out.
- The deliverable is a flat white/colored square, not a keyed transparent PNG at the platform
  size (微信 240×240) — a sticker that still needs manual cutting-out is NOT shipped.
- It copies or closely imitates an existing IP (Disney / 宝可梦 / LINE FRIENDS / 玲娜贝儿 / 蛋仔…).

## Repair Moves

If the sticker drifts off-model (most common):

```text
Pull back to the model sheet: same character, identical silhouette, palette, head shape,
line weight, and signature accessory. Change only pose, expression, prop, and caption. This
must be the SAME character as the rest of the set, not a lookalike. Regenerate from the
model sheet if needed.
```

If the caption text is wrong:

```text
Re-render the caption as EXACTLY "{correct text}" with clean correct Chinese characters,
≤ 6 字, placed top or bottom off the face, readable at small chat size. Keep the character
and pose. Remove any extra hallucinated text or watermark. If clean text is impossible,
leave an empty caption zone for overlay.
```

If the background is busy:

```text
Replace the background with clean white or one flat color so the sticker cuts out easily.
Keep the character on-model. Do not add scene clutter, props, or texture behind the figure.
```

If a sticker has no chat moment:

```text
Replace this decorative sticker with one that maps to a real chat moment (e.g. 已读不回 / 摆烂
/ 笑死 / 催 / 夸人). Name the moment, set the matching expression, and add a ≤ 6 字 caption
in 网络 tone — keep the same character.
```

If it is creepy or uncanny:

```text
Regenerate cute or funny and on-model: softer face, clear friendly eyes, exaggerated but
not realistic emotion. No photoreal human face, no melted features, no dead stare. Keep the
character's locked DNA.
```

If it copies an IP:

```text
Redesign the character as original: change silhouette, palette, and signature features so it
no longer resembles any licensed IP. Re-lock a new model sheet, then regenerate the set from it.
```
