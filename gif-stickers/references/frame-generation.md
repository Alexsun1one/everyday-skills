# Frame Generation (MODE A)

MODE A makes a short loop by **generating 2–8 consistent still frames** of one subject with an
image model, then handing them to the deterministic assembler. The frame-gen step needs an image
model; the assembly step does not (see `render-pipeline.md`). The hard problem here is NOT the
encoding — it is keeping the **same subject across frames** while changing **exactly one thing**.
Consistency is never assumed; it is *measured* before the frames ship (the drift gate, below).

Two sub-paths, decided by the Face-Truth Gate before any look work (see `SKILL.md (Face-Truth Gate)`):

- **A-theme** — invent the subject. You own the identity; cleanest loops, easiest to batch.
- **A-edit** — start from a user photo / avatar. Powerful, but it **alters and stylizes the
  real likeness** — the output is a *stylized version of them, not their actual face*. Say this
  before they upload. If the real face must be preserved pixel-for-pixel, this is the wrong mode —
  use MODE B (see `render-pipeline.md`, Mode B compositing), which never lets an image model touch
  the pixels — the text rides on top of the untouched photo via `scripts/kinetic_text.py`.

MODE A cannot do true talking-head or smooth facial animation — that needs a video model. This
makes a 2–8 frame loop, nothing more.

This is tool-neutral: the frame model can be any image-gen the host (Codex / Claude Code / Hermes)
can call; the assembler is plain code. Neither step is locked to a vendor.

## Identity-Lock Ladder (pick the highest rung the tool supports)

Strongest → weakest control. Stronger rungs lock identity by construction, so flicker and drift
*start* lower — but no rung is drift-free, so every rung still passes through the drift gate.

- **A1 — model-sheet crop (DEFAULT).** Generate ONE image that is a `1×N` / `2×N` grid of the
  same subject in N poses, then crop the cells into frames. All cells share one generation, so
  style / lighting / palette are locked from a single draw — this **lowers** cross-frame drift, it
  does not zero it: cells in one grid still vary in subject **scale, position, and crop framing**,
  which reads as flicker until registered. So A1 frames are NOT shippable raw — they MUST clear the
  drift gate (below). Prompt pattern: *"character model sheet, same character, 1×4 grid,
  white background, identical style and lighting, frame 1 neutral, frame 2 blinking, frame 3
  smiling, frame 4 waving."* Slice the sheet into `frames/f%04d.png` with a short inline Pillow
  crop (there is no slicing script — see the snippet below), then run it through the drift gate.
- **A2 — reference-edit from ONE base.** Feed the same base image + a per-frame instruction
  ("now raise the right hand"). Modern editors hold a subject across edits, but each edit re-noises
  position and background. **Always branch from the base, never chain edit→edit→edit** (drift trap,
  below). Drift-gate every output before stacking.
- **A3 — fixed-seed img2img (self-hosted SD / Flux).** Lock the seed, change one phrase. Numbers:
  denoise **0.35–0.5**, CFG **4–6**, IP-Adapter FaceID **0.65–0.8**, ControlNet OpenPose to drive
  the pose. These are starting values, not guarantees — the drift gate is what proves they held.
  Keep a fixed identity block; swap only the action line.
- **A4 — same-seed-only (fallback).** Lock the seed, change one word. Identity wobbles once the
  pose moves; the drift gate will fail it past 2 frames. Warn the user before authoring >2 frames.

### Slicing a model sheet (A1) — inline Pillow, no script

There is no shipped slicing script. A `1×N` sheet is sliced into the frame sequence with a few
lines of Pillow — write the cells straight into `out/<name>/frames/f%04d.png`:

```python
from PIL import Image
sheet = Image.open("sheet.png").convert("RGBA")
N, W, H = 4, sheet.width // 4, sheet.height          # 1×4 sheet → 4 equal cells
for i in range(N):
    cell = sheet.crop((i * W, 0, (i + 1) * W, H))
    cell.save(f"out/<name>/frames/f{i:04d}.png")     # the f%04d.png contract render-pipeline.md expects
```

For a `2×N` grid, walk rows then columns; the only contract is that the cells land in
`frames/f%04d.png` in play order. `scripts/assemble.py` loads them in sorted filename order, so the
numbering *is* the timeline.

## Harness Invariants (QA-verifiable)

1. **Vary exactly ONE element per frame** — eyes, OR hand height, OR vertical bounce — never
   several at once. One variable is what makes 4 frames read as deliberate animation, not jitter.
2. **Hold background, body, framing, and lighting identical.** Generate on flat white / a flat
   color / transparent so the cut-out stays clean; busy backgrounds re-noise every frame and
   flicker hardest.
3. **Branch, never chain.** Every frame comes off the same base image / seed. Chained edits let
   facial embeddings wander until frame 8 no longer matches frame 1.
4. **Register, then PROVE it, before stacking.** Re-center every frame to one subject bbox with a
   short inline Pillow crop, then run the drift gate (below) and **fail the set if it is still out
   of spec** — eyeballing is the last resort, not the first. A 3px subject jump reads as flicker,
   so 3px is the line.
5. **Same identity block + same seed pack-wide** — locks style frame-to-frame *and* sticker-to-
   sticker across the whole set.

## The Drift Gate (measured, not eyeballed)

A1's single-grid draw lowers drift; it does not remove it. "Near-zero drift" is a lie by omission —
so MODE A *measures*. There is no drift-measurement script; the gate is a short inline Pillow/numpy
pass you run on every set after slicing (A1) or after each branch render (A2–A4). It emits the same
three numbers the QA `>3px` and `flicker` rules assert against — write them to
`out/<name>/drift.json` so QA reads a verdict, not your gut:

```python
# inline drift gate — runs over out/<name>/frames/, writes out/<name>/drift.json
# 1. SEGMENT subject vs background per frame (alpha if RGBA, else luma threshold on the flat bg).
# 2. REGISTER: re-center every frame's subject centroid bbox to the median bbox with a Pillow
#    crop/paste — translate only (no warp, no scale of the real subject).
# 3. MEASURE drift against the reference (frame 0 for cyclic, the median for boomerang):
#      subject_shift_px = max per-frame centroid displacement AFTER registration
#      bg_delta         = mean abs background-region delta (0..1) between consecutive frames
#      id_drift         = 1 - mean SSIM over the subject bbox between consecutive frames
# 4. VERDICT in drift.json — PASS only if ALL hold:
#      subject_shift_px <= 3          (else: registration failure → flicker)
#      bg_delta         <= 0.04       (else: background re-noising → flicker)
#      id_drift         <= 0.12       (else: off-model drift → Regenerate, not Repair)
```

```json
{
  "mode": "A",
  "rung": "A1",
  "frames": 4,
  "subject_shift_px": 1.6,
  "bg_delta": 0.018,
  "id_drift": 0.07,
  "verdict": "PASS",
  "fail_reason": null
}
```

Routing the verdict (QA reads `drift.json`, does not re-judge by eye):

- **subject_shift / bg_delta over budget** → a *registration / encode-input* failure. Re-run the
  inline re-center pass; only if it still fails are the frames themselves bad.
- **id_drift over budget** → an *off-model* failure registration cannot fix. **Regenerate** the
  offending frame FROM the model sheet / base — never chain-edit it (Invariant 3).
- A4 past 2 frames almost always trips `id_drift`; that is the gate telling you the rung is too
  weak for this motion. Drop frames or escalate the rung — do not ship and hope.

The thresholds (`3px`, `0.04`, `0.12`) are the contract: tune them in the manifest if a register is
genuinely looser (撞色纯色 tolerates more bg_delta than a photo edit), but the verdict is always a
number QA can re-derive, never a feeling.

## A-theme vs A-edit (honesty)

```text
A-theme: invented subject → define a one-line identity block once, reuse VERBATIM every frame,
         vary only the action. Cleanest path; the default. Still goes through the drift gate.
A-edit:  user photo/avatar → NOT face-preserving. Generative editing re-synthesizes eye shape,
         cheekbones, skin; the more the pose/expression changes, the more it drifts — and id_drift
         in the gate is exactly that drift, made measurable. Cap ~2-3 variants off one selfie;
         beyond that it reads as "AI version of you" and the gate will say so.
```

Print the verbatim caveat before any A-edit run (the QA fails an A-edit delivery that omits it):
*"这是把你照片风格化后的形象，不是你真实的脸；生成会改变五官细节。要逐像素保留真实的脸，请改用 MODE B。"*

## Frame Count & Loop Design (2–8 is a feature)

Stickers loop forever and play tiny. **Target 2–8 frames.**

- **2 frames** — on/off: 眨眼 / 张嘴。Reads as a blink or talk.
- **3–4 frames** — a gesture: 挥手 / 点头 / 比心。Maps perfectly to a `1×4` model sheet.
- **6–8 frames** — a small cycle: bounce / breathing / hair sway.

**Ping-pong (boomerang) doubles frames for free** — play forward then reverse; the loop is
automatically seamless because the end equals the start. Use it for there-and-back motion
(blink / bob / nod). **NEVER ping-pong directional motion** — a one-way 挥手 that rewinds looks
broken; author a true cyclic loop instead. Record the choice as `loop_strategy`
(`directional | cyclic | boomerang`) in `manifest.json` (the frames + manifest contract is
documented in `render-pipeline.md`). Loop length 0.6–1.8s; keep motion in the first 70%, hold a
readable rest pose in the last 30% (the frame people screenshot). Pick the motion preset from the
chat moment with `motion-library.md` (Bank B is MODE A's home turf).

## Batch a Themed SET

A pack is many small loops — script it, do not hand-make each one. Declare the identity block
ONCE, reuse it pack-wide, drive a manifest, and run the drift gate on each loop:

```text
IDENTITY = "chubby orange tabby, big eyes, tiny red scarf, flat style, white bg"
SEED     = 4242                                  # same seed across the whole pack
stickers = {                                     # name → ONE varied element per frame
  "wave":   ["arm down", "arm mid", "arm up", "arm mid"],   # directional → cyclic, no pingpong
  "blink":  ["eyes open", "eyes closed"],                   # there-and-back → pingpong
  "bounce": ["low", "mid", "high", "mid"],
}
# per loop: inline Pillow slice → drift gate (drift.json must PASS) → scripts/assemble.py
```

The model-sheet route can put a whole pack on one or two grid images and crop everything in one
pass — but each loop still clears its own drift gate before assembly. Mind the set-count
guardrails when batching (WeChat 16/24 all-animated-or-all-static; LINE 8/16/24 — see
`platform-specs.md`) — a pack is a SET, not 8 random loops.

## Hand-Off

Every A run emits the shared frame contract documented in `render-pipeline.md` —
`out/<name>/frames/f%04d.png` (RGBA, square, subject-centered, safe margins) + `drift.json`
(PASS required) + `manifest.json` with `mode: "A"`, `loop_strategy`, and `text_baked: false`.
Then encode and verify:

```bash
python3 scripts/assemble.py --in out/<name> --out out/<name>/wechat.gif --flatten FFFFFF
python3 scripts/verify_output.py --file out/<name>/wechat.gif --platform wechat
```

Use `--flatten RRGGBB` for platforms that drop alpha (WeChat / X); omit it to keep transparency
(Telegram / Discord). If a loop is over the platform byte cap, re-run `assemble.py` at a lower
`--fps` or a smaller `--size` until it clears `verify_output.py`. The scripts are Pillow-only — no
ffmpeg required; if `gifsicle` happens to be on PATH, `assemble.py` uses it to shrink further. The
assembler never knows how the frames were made; MODE A and MODE B converge on the exact same
pipeline.

If the agent can generate frames but cannot run a shell, it can produce the PNG sequence but
**cannot register, gate, encode, or batch** — it cannot prove the loop is on-model. Hand the
frames off for manual assembly (note the gate was not run) rather than faking a finished loop
(see the capability note in `SKILL.md`).
