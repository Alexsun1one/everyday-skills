# Prompt Template

Two modes, one pipeline. Templates for both are below. Run the Face-Truth Gate first
(`SKILL.md (Face-Truth Gate)`) — it returns `MODE_A` or `MODE_B`, and you fill in only that
mode's template. Both modes emit the SAME frame contract — zero-padded `frames/f%04d.png` plus a
`manifest.json`, the contract documented in `render-pipeline.md` — then the SAME deterministic
assembler (`assemble.py`) turns those frames into bytes. The agent WRITES and RUNS the assembly
code; no image model touches the encode step.

- **MODE A** generates 2–8 consistent frames (theme-invented subject, OR by editing a reference
  photo) then loops them. Editing a real photo ALTERS/stylizes the face — the output is a stylized
  likeness, not the real person. Say this out loud (the honesty caveat from the Face-Truth Gate in
  SKILL.md).
- **MODE B** keeps the real photo EXACTLY and animates a composited caption deterministically with
  `kinetic_text.py`. No image model. The text is always crisp because it is drawn on RGB before
  quantization.

Neither mode does true talking-head or smooth facial animation — that needs a video model. This skill
makes a small looping sticker, not lip-sync.

## MODE A — Planning Template

```text
Use $gif-stickers, MODE A. First plan, do not generate yet.

Subject source:
{theme-only / user-photo / pet-photo / brand-mascot}   ← if user-photo, print the honesty caveat

Chat moment(s) this loop is for:
{笑死 / 赞同 / 摆烂 / 求饶 / 晚安 / 生气 / ...}

Target platform(s):
{wechat / line / telegram / discord / twitter / generic}

Return:
- subject (one line) + identity DNA (3-5 fixed traits: silhouette, palette, head shape, line, accessory)
- visual register (routed by vibe, style-routing.md), LOCKED across every frame
- identity-lock rung (frame-generation.md): A1 model-sheet / A2 reference-edit / A3 fixed-seed / A4 same-seed
- per loop: chat moment | the ONE element that varies per frame | motion_preset | loop_strategy (boomerang/cyclic/directional)
- frame_count (2-8) and fps ∈ {25,20,10,5,4,2}
- QA risks
```

## MODE A — Frame Generation Prompt (model-sheet first)

Generate ONE model sheet that locks identity by construction, then slice it into `frames/f%04d.png`
with a short inline Pillow crop (no dedicated script — `Image.open(sheet).crop(box)` per cell, saving
each as `f%04d.png` so it lands in the same frame contract `assemble.py` consumes). Vary EXACTLY ONE
element per frame; hold everything else identical (the register-before-stacking rule in
`frame-generation.md`).

```text
Generate ONE character model sheet for an animated chat sticker.

Square 1:1 per cell, clean transparent or flat single-color background, subject centered with margins.

Subject:
{one subject — what it is, in one sentence}

Visual register — routed by vibe (style-routing.md), LOCKED across every frame:
{圆润流行 (Zagnoli) / 水墨·工笔 ink (国潮·古风, 朱砂红+石青 accent, tiny 印章) / 减法扁平 / 剪纸纯色 / 大头卡通}

Identity DNA — keep IDENTICAL in every frame (drift = flicker):
- silhouette / body shape, palette (2-4 fixed roles), head shape & face layout, line weight, one signature accessory

Layout — a 1×N or 2×N grid of the SAME subject, one varied element per cell:
{e.g. 1×4: arm down → arm mid → arm up → arm mid  (a wave loop)}
- identical lighting, background, framing, and body across all cells
- ORIGINAL subject — not Disney / 宝可梦 / LINE FRIENDS / 玲娜贝儿 / 蛋仔 or any existing IP

No caption text on the sheet — identity reference only; captions are added later if needed.
```

After the sheet comes back, slice it inline — no separate splitter script:

```python
# inline Pillow slice of an N-cell model sheet into the frame contract
from PIL import Image
import os
sheet = Image.open("sheet.png").convert("RGBA")
W, H = sheet.size
cols = 4                                  # cells across (1×N here)
cw = W // cols
os.makedirs("out/wave/frames", exist_ok=True)
for i in range(cols):
    cell = sheet.crop((i * cw, 0, (i + 1) * cw, H))
    cell.save("out/wave/frames/f%04d.png" % i)
```

Then hand-write a `manifest.json` next to `frames/` (same shape as Mode B's — `fps`, `size`,
`frames`, `loop_kind`, `frame_glob: "frames/f%04d.png"`; the contract is in `render-pipeline.md`) and
the rest of the pipeline is identical to Mode B.

## MODE A — Edit-From-Photo Prompt (the honest branch)

When the subject is a user/pet photo and the user accepts AI-stylized frames. Print the caption
caveat verbatim FIRST. Branch every frame from the ONE base image — never chain edit→edit→edit (the
drift trap in `frame-generation.md`). Cap ~2–3 variants.

```text
Honesty caveat (surface to the user before generating):
"这会把你照片里的脸做成 AI 风格化版本，不是逐像素保留你本人的脸；动作越大，越像‘AI 版的你’。
要逐像素保留真实的脸，请改用 MODE B（只动文字，照片不变）。"

Generate ONE animated-sticker frame, edited from the ATTACHED base photo.

Same subject as the ATTACHED photo — keep recognizable likeness; this is a stylized sticker version.
Visual register (style-routing.md), LOCKED across all frames: {…}

Change ONLY this one element for this frame:
{e.g. eyes open → eyes closed  (a blink)}

Square 1:1, transparent or flat single-color background, subject centered with margins.
Keep lighting, framing, and background identical to the other frames.
```

## MODE A — Batch Template (a whole themed SET)

A pack is a SET, not random loops. Declare the identity/register ONCE and a fixed seed pack-wide (the
batch/SET section of `frame-generation.md`); platform set-counts are guardrails (WeChat 16/24
all-animated-or-all-static; LINE 8/16/24). The agent loops generation, then runs the shared assembler
per loop.

```text
Use $gif-stickers, MODE A, batch a SET.

Identity DNA (declared ONCE, frozen pack-wide): {…}
Visual register (LOCKED): {…}      Fixed seed (pack-wide): {seed}
Platform + set count: {wechat 16 / line 24 / ...}   ← refuse non-allowed counts

Set manifest — one row per sticker:
[ (label, chat_moment, the ONE varied element, motion_preset, loop_strategy) , ... ]

Per sticker: generate frames (model-sheet inline-crop or edit-branch) → land frames/ + manifest.json
(the render-pipeline.md contract) → assemble.py → assemble.py --flatten RRGGBB if the platform drops
alpha (WeChat/X) → verify_output.py --platform X.
Return one report per sticker: path | chat moment | rendered caption (if any) | on-model? | pass/regenerate.
```

## MODE B — Build Spec (real photo, deterministic, text always crisp)

No image model. The photo pixels are kept byte-for-byte; only the composited caption is animated by
`kinetic_text.py` (Mode B compositing — see `render-pipeline.md`, with the caption/stroke rules in
`text-and-layout.md`). The agent WRITES and RUNS the render commands.

```text
Use $gif-stickers, MODE B. Real photo preserved exactly.

photo path:        {/abs/path/to/photo.png}
caption text:      "{exact text, ≤ 6 字, correct Chinese characters}"
chat moment:       {笑死 / 已读不回 / 摆烂 / ...}
routed register:   {text system from style-routing.md — font role, palette, WeChat white-stroke flag}
motion preset:     {routed from the chat moment, motion-library.md → one of pop|bounce|shake|flash|hold}
loop_strategy:     {boomerang / cyclic / directional}
fps:               {∈ 25,20,10,5,4,2}     frame_count: {N, e.g. 12; held frames merge to ~8 effective}
position:          {top / bottom}
platform(s):       {wechat / line / telegram / discord / twitter / generic}
```

## MODE B — Deterministic Render Invocation

`kinetic_text.py` draws the caption programmatically on RGB BEFORE quantization with a stroke auto-sized
to the canvas (~8px @240) — that is why Mode B text never muddies. There is NO shipped font folder: pass
your own bold CJK face with `--font /path/to/bold-CJK.ttf`, or omit `--font` and let the script auto-detect
a system CJK font (STHeiti / Hiragino / PingFang / Noto). Pipeline order, encoders, and the byte-budget
ladder live in `render-pipeline.md`.

```text
# 1. Bake the crisp caption on the untouched photo into RGBA frames + manifest.json
#    (Pillow-only; auto-detects a system CJK font, or pass --font /path/to/bold-CJK.ttf):
python3 scripts/kinetic_text.py --base photo.png --text 笑死 --preset bounce \
    --frames 12 --fps 10 --size 240 --pos bottom --loop cyclic --out out/xiaosi

# 2. Assemble frames + manifest into a small looping GIF (Pillow-only; uses gifsicle if on PATH).
#    --flatten RRGGBB for platforms that drop alpha (WeChat/X); omit to keep transparency:
python3 scripts/assemble.py --in out/xiaosi --flatten FFFFFF --out out/xiaosi/wechat.gif

# 3. Refuse non-compliant output — asserts dims/size/frames/loop, exits nonzero on breach:
python3 scripts/verify_output.py --file out/xiaosi/wechat.gif --platform wechat
```

Transparent variant (no photo, flat ground, kept transparent through assembly):

```text
python3 scripts/kinetic_text.py --base "" --text 赞同 --preset pop --frames 10 --fps 10 --size 240 --out out/zantong
python3 scripts/assemble.py --in out/zantong --out out/zantong/sticker.gif   # keeps transparency
python3 scripts/verify_output.py --file out/zantong/sticker.gif --platform generic
```

Optional cheap photo motion (Ken-Burns / bounce) is NOT a separate script — if you want the still photo
itself to drift, bake that motion into the frames with a short inline Pillow loop (resize/crop the base
per frame into `frames/f%04d.png`) BEFORE you run `assemble.py`. Most stickers skip it; the caption
motion alone reads as alive.

## Fallbacks

- **No encoder needed:** the scripts are Pillow-only — there is NO ffmpeg/gifski/probe step to run.
  If `gifsicle` happens to be on PATH, `assemble.py` uses it to shrink the file further; otherwise it
  falls back to Pillow's own optimizer. Never claim a probe script or fake a finished GIF.
- **Over the platform byte cap:** re-run `assemble.py` at a lower `--fps` (re-bake with a smaller
  `kinetic_text.py --fps`) or a smaller `--size` until `verify_output.py` passes. That down-ladder
  is the whole budget story — no separate budget script.
- **Image-only agent (no shell):** Mode A can produce frames but cannot encode or batch; hand off the
  `frames/` for manual ezgif assembly, or decline. Mode B needs only a shell (no image model).
- **Mode A drift:** if a frame goes off-model, regenerate it FROM the model sheet, do not chain-edit
  the bad output. On rung A4 only, warn that loops over 2 frames will wobble.
- **Caption renders wrong in Mode A:** leave a clean empty caption zone and bake the exact text in
  Mode B instead — Mode B text is always crisp.
