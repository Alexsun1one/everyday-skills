---
name: sticker-set
description: Generate or plan a consistent set of chat stickers (表情包套图) from one original character, each with a short Chinese meme caption. Use when a user wants a 表情包, 表情包套图, 微信表情, 聊天表情, 斗图表情, 沙雕表情, 自制表情包, IP 表情, or says 做个表情 / 做套表情 / 整套斗图 / 把我家猫狗做成表情 / 给我的 IP / 品牌吉祥物做表情包 (make a sticker pack of my pet / character / mascot, turn this into stickers) — a pack of reaction stickers built around one mascot/character with captions like 在吗 / 笑死 / 摆烂 / 已读不回. Especially useful for turning a character idea, a mascot, a pet photo, or a vibe into 6–16 send-ready stickers that all look like the SAME character and each map to a real chat moment. Do not use for a single cover image (use a cover skill), logos, full illustrations, dense infographics, or copying an existing IP (Disney, 宝可梦/Pokémon, LINE FRIENDS, 玲娜贝儿, 蛋仔, etc.).
---

# Sticker Set

Sticker Set turns one original character into a consistent pack of chat stickers, where every sticker is something a person would actually send mid-conversation.

A sticker is not a cute drawing. It is a reply. The whole pack has two jobs: every sticker must look like the SAME character (consistency), and every sticker must map to a real chat moment someone would send it in (usefulness). A set of pretty but off-model, sceneless stickers is a failed set. Use this skill to plan and generate sticker packs that read as one character and earn their place in a chat.

## Workflow

1. Read the character idea, mascot, pet photo, vibe, or edit request.
2. Lock the character DNA: 3–5 fixed traits that stay identical across the whole set.
3. List the chat moments to cover from `references/expression-library.md` (打招呼 / 赞同 / 拒绝 / 摆烂 / 打工累 / 委屈 / 生气 / 求饶 / 笑死 / 已读不回 / 催 / 夸人 / emo / 吃瓜 / 晚安 / 谢谢…).
4. Set the size: usually 6–16 stickers.
5. Run the Chat-Moment Test on every sticker: 用户在什么聊天瞬间会发这张？ Cut any sticker that maps to no real send-moment.
6. Write each caption: ≤ 6 字, 网络口吻, correct Chinese characters.
7. Route the visual register by character vibe/theme with `references/style-routing.md` (萌系 → 圆润流行, 国潮/古风 → 水墨/工笔, 极简 → 减法扁平, 撞色 → 剪纸纯色, 沙雕 → 大头卡通) — the character picks the look automatically — and LOCK that register into the character DNA; then apply `references/style-dna.md` inside it.
8. Generate the MODEL SHEET first to lock identity, then derive each sticker from it (`references/prompt-template.md`).
9. Generate one sticker at a time, referencing the locked DNA.
10. Run QA with `references/qa-checklist.md`; regenerate if the set drifts off-model, a sticker has no chat moment, a caption is garbled, or it copies an IP.

## Chat-Moment Test

Before generating, answer:

```text
sticker plan:
- character: one line — what it is
- visual register (routed by vibe): 圆润流行 / 水墨·工笔 / 减法扁平 / 剪纸纯色 / 大头卡通 …
- character DNA: 3-5 fixed traits identical across the whole set (silhouette, color, head shape, one signature accessory) — the routed register is locked in too
- set size: usually 6-16
- per sticker:
  - chat moment: when the user sends it
  - emotion / action:
  - caption: ≤ 6 字, 网络口吻
- forbidden drift: off-model / 文字看不清 / 没使用场景 / 恐怖谷 / 抄袭已有 IP
```

Keep a sticker only when its `chat moment` is concrete. Good answers:

- "对方已读不回时甩这张。"
- "同事甩活过来，回一张摆烂。"
- "群里有瓜，发这张围观。"

Weak answers:

- "很可爱。"
- "凑数。"
- "画得挺好看的。"

A sticker with no send-moment is decoration, not a sticker. Cut it or replace it with a real chat moment.

## Default Look

Read `references/style-dna.md` before generating final stickers.

Core visual DNA:

- one original character, consistent across every sticker in the set
- square 1:1; clean flat single-color or white background that is easy to cut out
- big readable caption ≤ 6 字, placed top or bottom, 网络用语口吻
- expressive pose and face — but never creepy, melted, or uncanny
- identical line weight, palette, head shape, and proportions across ALL stickers
- only pose / expression / prop / caption change between stickers — never the character
- cute or funny and on-model, like a real sticker pack a person would actually use
- no photoreal humans, no off-model drift, no tiny unreadable text
- no copying existing IP (Disney, 宝可梦, LINE FRIENDS, 玲娜贝儿, 蛋仔…); the character is original

## Set Consistency

The hardest part of a sticker pack is that all of it must look like one character. Lock the silhouette, palette, head shape, line weight, and one signature accessory, then keep them frozen. Generate a model sheet first (角色三视图 / 表情九宫格) and derive every sticker from it. If a sticker drifts off-model, do not keep it because the pose is nice — pull it back to the model sheet and regenerate. One consistent character beats a dozen prettier strangers.

## Aesthetic Routing (automatic, by character vibe — locked across the set)

A sticker set lives or dies on charm + consistency. The visual register is **routed by the
character vibe/theme**, not hand-picked — see `references/style-routing.md` — then LOCKED into
the character DNA so every sticker shares it. Routing and consistency are one decision:

- 可爱/萌系/治愈 → Olimpia Zagnoli rounded pop: soft rounded silhouettes, tested high-saturation palette, flat and buoyant.
- 国潮/古风/古装/武侠/仙侠/神兽 → 水墨/工笔 ink: confident ink-line or fine 工笔 contour, warm/rice-paper ground, mineral accents, optional 印章 — sticker-clean, not a full painting. (theme wins over cuteness.)
- 极简/高级/品牌 IP → Geoff McFetridge reductive: matte muted palette, clean contour, one signature shape.
- 大胆/撞色/潮玩 → Matisse cut-outs: pure flat color shapes, bold contrasting blocks.
- 沙雕/搞怪/梗 → bold flat cartoon: oversized head, thick outline, exaggerated emotion, punchy palette.

Once routed, the register is one of the frozen DNA traits — applied identically to the model
sheet and every sticker. Restraint for every set: flat, no gradients, one bold readable
silhouette, register and palette held identical across all stickers. The register + the five
consistency locks keep the set on-model; only pose/expression/prop/caption change.

## Output Contract

For planning, return:

```text
character:
character DNA (3-5 fixed traits):
set size:
chat moments covered:
per sticker:
  - chat moment | emotion/action | caption (≤ 6 字)
delivery: grid sheet / individual stickers
model sheet prompt:
QA risks:
```

For generation, produce the model sheet first, then one sticker at a time, and report:

- image path
- the exact caption text rendered
- the chat moment it is for
- whether it stays on-model with the rest of the set
- whether it passes QA or needs regeneration

## References

- `references/style-routing.md`: route the visual register by character vibe/theme (国潮 → ink, 萌系 → rounded pop…), locked across the set — read this with style-dna.
- `references/style-dna.md`: the visual identity, consistency rules, and anti-IP-copy rules.
- `references/expression-library.md`: the chat-moment taxonomy, consistency technique, and caption rules — the main reference.
- `references/prompt-template.md`: planning, model-sheet, per-sticker, and consistency-fix prompt templates.
- `references/qa-checklist.md`: acceptance, regeneration, and repair rules.
