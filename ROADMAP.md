# Everyday Skills — Build Loop Roadmap

This file is the backlog and coordination point for the autonomous improvement loop. Each
iteration: pick the next unchecked item, do it to publish-grade quality, adversarially
self-critique it ("左右脑互搏"), fix, QA, then check it off here. The loop is resumable —
anything checked is done; work the next unchecked item.

## Iteration recipe (every loop pass)

1. Read this roadmap; pick the next unchecked item (top to bottom).
2. **Make** — build or refine the skill following the house pattern: SKILL.md (trigger-rich
   description) + references (style-dna, core library, prompt-template, qa-checklist) +
   Chinese-first README. Give it a `style-routing.md` that AUTO-ROUTES the aesthetic by the
   user's subject/domain/mood into the right master register (poets → 水墨, footballers →
   sports card, knowledge → Swiss) — the user never names a style. Pull tokens from
   `master-styles` (the shared engine); do not make users invoke master-styles themselves.
3. **Critique (left brain vs right brain)** — adversarially review as a skeptical art
   director + skill reviewer: where would output still look generic / AI / amateur? what
   harness constraint is missing? is the decision gate real? Be harsh.
4. **Fix** — apply the top concrete findings.
5. **QA** — check against the skill's own qa-checklist; confirm house-style consistency.
6. **Test render** — if an image-generation tool is available in the session, generate 1–2
   sample images and judge them; if not, note that rendering is deferred to the user's image
   model. (Never substitute SVG/CSS for a real image.)
7. Check the item off; add any newly discovered follow-ups.

## Quality bar (non-negotiable)

- Every skill produces output that looks **designed by a top-tier designer**, not templated.
- A clear decision gate that rejects empty/generic work.
- A real harness: explicit anti-patterns (反微商/反PPT/反土味/反AI塑料/反拼贴/反套皮) + QA.
- `master-styles` tokens applied so the aesthetic is master-grade.
- Self-contained and open-source-ready; each skill liftable on its own.

## Done

- [x] `cover-pop` — 社交封面 (+ master-styles Elevation)
- [x] `sticker-set` — 表情包套图 (+ master-styles Elevation)
- [x] `quote-cards` — 金句/知识卡片 (+ master-styles Elevation)
- [x] `rank-cards` — 排名/段位卡 (generalized to schools/majors/poets/cities/films)
- [x] `master-styles` — 大师视觉语言 (aesthetic engine, 25 masters)
- [x] `gif-stickers` — 动图表情包 (two modes: A frame-gen → GIF, B photo + kinetic text; deterministic Pillow render, TESTED with real sample GIFs in examples/)

## Backlog — CURRENT PRIORITY (architectural correction, do these FIRST)

The master visual tokens are NOT a standalone skill users invoke — they are a shared engine
each content skill AUTO-ROUTES into by subject (poets → ink-wash, footballers → sports card).
master-styles is repositioned as that engine. Fuse auto-routing into every content skill
before building new ones.

- [x] `rank-cards`: add `style-routing.md` (subject → register) + wire into workflow/gate/default-look; add Chinese ink register (神品/逸品 + 水墨/印章).
- [x] `master-styles`: reframe as the internal AESTHETIC ENGINE (auto-routed by hosts, not a destination skill); add Chinese/East-Asian ink masters (宋元山水/文人画/书法/工笔).
- [x] `cover-pop`: replace the manual "Elevation" section with `style-routing.md` — auto-route the cover's aesthetic by niche/mood/subject (knowledge → Swiss; 国风/古风 → ink; product → Penn/Hockney; emotional → Hopper/Hara). User never picks a style. (done — routing table, wired into workflow/gate/default-look/prompt-template/references)
- [x] `quote-cards`: add `style-routing.md` — route by content (金句→Swiss/Hara; 古诗词/国学→水墨+书法; data→Vignelli; book note→editorial). Reframe Elevation as auto-routing. (done — routing table by content+culture, wired into workflow/gate/default-look/prompt-template/references)
- [x] `sticker-set`: add `style-routing.md` — route by character vibe (cute→Zagnoli; 国潮→ink/工笔; minimal→McFetridge; bold→Matisse). Reframe Elevation as auto-routing. (done — register LOCKED into character DNA + flows into model-sheet/per-sticker prompts)
- [x] Update README.md / README.en.md: master-styles described as the auto-routed engine, not a standalone skill; add the routing idea to the "Shared Workflow DNA". (done — added "按题材自动路由审美 / Subject-based aesthetic auto-routing" pillar to both READMEs)

## Backlog — new skills (priority order)

- [ ] `avatar-craft` — 头像/社交头像 (consistent, on-brand, non-uncanny; master-styles portrait tokens)
- [ ] `poster-pop` — 海报/活动海报/朋友圈海报 (one message, hierarchy, master-grade composition)
- [ ] `ecom-hero` — 电商主图/商品主图 (product hero, white-bg discipline, benefit callouts, no taobao clutter)
- [ ] `festival-cards` — 节日祝福图/贺卡 (warmth without 土味; restrained, premium)
- [ ] `wallpaper` — 手机壁纸/桌面壁纸 (safe-area, depth, master color fields)
- [ ] `ppt-visual` — PPT 单页视觉/单页配图 (one idea per slide, not icon soup)
- [ ] `nine-grid` — 朋友圈九宫格 (one image split into a coherent 3×3, or a unified set)
- [ ] `resume-card` — 个人介绍卡/作品集封面 (clean personal brand visual)

## Backlog — refinement passes

- [x] Adversarial critique sweep across all existing skills; fix top issues per skill. (round 1 done — see Loop log)
- [ ] `master-styles`: add culturally-relevant masters (中国水墨/书法, 丰子恺, 几米, 包豪斯/孟菲斯, 草间弥生).
- [ ] `examples/`: add a curated final-prompt gallery per skill.
- [ ] Cross-skill consistency audit (voice, section rhythm, description trigger coverage).
- [ ] Once an image tool is available: add real sample renders to each skill's README.

## Loop log

- 2026-06-25 — Iteration 1: built `rank-cards` + `master-styles`; wired master-styles Elevation
  into cover-pop/sticker-set/quote-cards; generalized rank-cards to schools/majors/poets/cities/films.
- 2026-06-25 — Iteration 2 (adversarial critique round 1): applied 14 fixes. rank-cards now forks
  real-people (editor composite) vs generated (one-pass) + real-person likeness guard + no-face
  subject-image pipeline; Chinese-text overlay promoted to default for exact/multi-line text in
  rank-cards/quote-cards/cover-pop; cover-pop QA gets falsifiable 200px squint + real-account
  tests; rank-cards "stated basis must govern tiers" integrity rule + single-hue value ramp for
  no-face domains; sticker per-sticker prompt now attaches model-sheet as image reference +
  caption-voice rule + transparent-PNG deliverable; quote-cards Elevation mapped per archetype
  (void only for single-line heroes); master-styles "host restraint wins" precedence; README
  "都核实了" softened to a defensible claim. Open: #14 gate-name cosmetic (skipped).

- 2026-06-25 — Iteration 3 (direction correction): master tokens repositioned from a standalone
  skill into a shared AESTHETIC ENGINE that content skills AUTO-ROUTE into by subject. Built
  rank-cards/style-routing.md (poets → 水墨山水 + 神品/逸品 + 印章, footballers → sports card,
  etc.) and wired it into the workflow/gate/default-look. Reframed master-styles SKILL.md as the
  engine (not a destination skill) and added Chinese ink masters (宋元山水/文人画/书法/工笔). Next:
  add style-routing to cover-pop/quote-cards/sticker-set and reframe their Elevation sections.

- 2026-06-25 — Iteration 4: cover-pop auto-routing. Added cover-pop/references/style-routing.md
  (niche/mood → register: 知识→Swiss, 国风/国学→水墨+书法+印章, 产品→studio, 情绪→Hopper+留白,
  穿搭→Favre, 母婴→Zagnoli, 反差→Bass, 活动→Scher). Wired into workflow step 7, Stop Test gate
  (register field), reframed "Elevation" → "Aesthetic Routing (automatic)", added register block
  to the final-gen prompt + palette-by-register, references list. Self-critique fix: routed
  register now actually flows into the generation prompt (was decided but not expressed). Next:
  quote-cards style-routing (金句→Swiss/Hara, 古诗词/国学→水墨+书法, data→Vignelli).

- 2026-06-25 — Iteration 5: quote-cards auto-routing. Added quote-cards/references/style-routing.md
  (routes by card type + topic culture: 金句→Hara/Swiss, 古诗词/国学→水墨+书法+印章 [culture wins
  over type], 干货清单/步骤/数据/概念→Vignelli grid, 读书笔记→editorial, 治愈→Rothko). Wired into
  workflow step 8, Save Test gate (register field), reframed "Elevation" → "Aesthetic Routing",
  added register block to final-gen prompt, references list. Multi-line-content-needs-grid rule
  preserved. Next: sticker-set style-routing, then README update.

- 2026-06-25 — Iteration 6: sticker-set auto-routing. Added sticker-set/references/style-routing.md
  (route by character vibe: 萌系→Zagnoli, 国潮/古风→水墨/工笔, 极简→McFetridge, 撞色→Matisse,
  沙雕→大头卡通). Key: the routed register is LOCKED into the character DNA (one decision = routing
  + consistency) and flows into the model-sheet + per-sticker prompts. Wired into workflow step 7,
  Chat-Moment gate (register field), reframed "Elevation" → "Aesthetic Routing", references list.
  Ink register kept sticker-clean + transparent-keyable. Next: README.md/README.en.md update
  (master-styles as auto-routed engine; routing in Shared Workflow DNA) — last CURRENT PRIORITY item.

- 2026-06-25 — Iteration 7: built `gif-stickers` (two-mode animated sticker skill) via a 27-agent
  Workflow (research → design panel → per-file build → adversarial verify → harden). 10 reference
  files + a REAL tested `scripts/` (kinetic_text.py / assemble.py / verify_output.py, Pillow-only,
  no ffmpeg needed). Produced + verified real sample GIFs (examples/demo-xiaosi-240.gif passes
  WeChat 240px/<500KB/loop; demo-zantong-transparent.gif). Adversarial verify caught the build's
  doc↔reality drift (phantom reference/script names, "vaporware" scripts) — fixed SKILL.md
  References, README workflow + scripts section, added scripts/README.md.
  FOLLOW-UP (next loop pass): reconcile render-pipeline.md's remaining mentions of unbuilt helpers
  (budget.py / export_platform.py / probe_tools.sh) — either build minimal versions or reframe to
  the 3 shipped scripts; verify platform-specs Discord figures (flagged uncertain); add gif-stickers
  to the top-level README skills table (advanced line).

- 2026-06-25 — gif-stickers HARNESS UPGRADES (from user product feedback — implement these):
  - **Mode C — code-rendered (火柴人/simple vector + name/word) → GIF.** First-class CHEAP path,
    no image model, set-oriented, runs anywhere with a shell. Reference impl shipped + tested:
    `scripts/stickman.py` (+ examples/set-*.gif: a 4-sticker pack, 172KB total, passes WeChat).
  - **Economy is a HARD constraint, not精致.** GIF stickers must be deliberately low-res (≤240px),
    few frames (2–12), few colors, small files. Harness must CONSTRAIN cost (Codex can't gen many
    big/crisp images per run = token burn). Add an "economy budget" to the gate; reject over-spec.
  - **SET is the DEFAULT deliverable** (e.g. 9 / platform set-counts), not a single sticker. Plan a
    coherent set; the gate already has a SET field — make set-first the default flow.
  - **颜值 + 传播度 gate (shareability).** Stickers exist to be SPREAD. Add a shareability/meme test
    to the decision gate + QA: is it funny OR beautiful, does it have a hook, would someone forward
    it? Both aesthetics AND virality must be maxed — this is the core harness, make it strong.
  - **Real-photo-REQUIRED case → mark Codex-only.** When the user hard-requires their real face
    animated, it needs strong image-gen (Codex/Image 2.0); state this档 is Codex-only, not for
    sessions without image-gen. The cheap/code paths (B kinetic-text, C stickman) work anywhere.
  - Pending: bake the above into SKILL.md (add Mode C + economy gate + set-default + shareability
    test), references (a code-render.md + motion/qa updates), and the README.

- 2026-06-25 — gif-stickers cleanup RESOLVED: ran a focused cleanup workflow (10 doc agents) +
  grep-verified — ZERO phantom tokens, every references/*.md and scripts/* resolves, no shipped-font
  claims. The "phantom helpers (budget.py/export_platform.py/probe_tools.sh)" follow-up is DONE
  (those names no longer appear). Also finished the CURRENT-PRIORITY README routing item.
  Shipped a tested Mode-C reference impl: `scripts/stickman.py` (code-rendered 火柴人 + name → GIF;
  examples/set-*.gif, a 4-sticker pack ~172KB, passes WeChat) + examples/gallery.html viewer.
- 2026-06-25 — LOOP PARKED (autonomous loop disabled; in-session wakeup NOT rescheduled). Reason:
  user is actively steering gif-stickers and there is a pending question to them (stickman style:
  tweak cuter vs lock as-is). Next real work is the gif-stickers HARNESS UPGRADES block above
  (Mode C / economy gate / set-default / 颜值+传播度 test / Codex-only photo case), to be done WITH
  the user — NOT avatar-craft. Resume the loop only when the user says so.

- 2026-06-25 — gif-stickers FINALIZED (user decision: focus on Codex / strong image-gen):
  Repositioned to **Codex-first**. SKILL.md now has THREE modes — A image-gen frames (PRIMARY,
  best on Codex; where 颜值 + DIFFERENT STYLES live), B photo+kinetic (face-preserving, runs
  anywhere), C code-render mascot (cheapest floor: scripts/cutie.py polished 团子 8 emotions +
  scripts/stickman.py). Added the 5 harness upgrades: economy budget (≤240px/2-12 frames/few
  colors; don't over-spec image gen = token burn), SET-default deliverable, 颜值+传播度
  shareability gate (cute OR funny + a hook + a real chat moment, else cut), real-face-required =
  Codex-only. Added a STYLE MENU to style-routing.md (3D盲盒/像素/手绘/水墨/厚涂/扁平/日系/美式/
  photo-real — variety lives in Mode A on Codex; Mode C only covers the 团子 look). cutie.py
  tested: examples/cutie/*.gif (6-emotion cute set, ~100-150KB each, passes WeChat) +
  examples/cutie-gallery.html. The everyday-skills core line + master-styles + gif-stickers are
  done; remaining backlog (avatar-craft etc.) is untouched and the loop stays PARKED until the
  user resumes it.

## Coordination

- The loop reads this file's checkboxes and the on-disk file tree to know what is done.
- Do NOT push to a remote. Commits are optional checkpoints only if the user asks.
- Keep each skill folder self-contained so it can be open-sourced alone.
