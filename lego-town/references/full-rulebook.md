---
name: lego-town
description: Generate or plan publish-grade images that turn a structure, system, relationship, process, prompt, or document into a tangible brick-built scene — a finished diorama, a step-by-step instruction sheet, or an exploded parts view — in the look of interlocking studded construction bricks. Use when a user wants to explain or illustrate an architecture, a workflow, a pipeline, a prompt's components, a system's parts and how they connect, a comparison, a concept's anatomy, a roadmap, an org or knowledge map, or a worked example as buildable brick modules, minifig actors, and a baseplate town. Trigger words include 乐高, 积木, 砖块, 搭建, 拼装, 零件图, 说明书图, 结构图, 模块图, 小镇地图, 爆炸图, brick build, instruction sheet / manual, exploded view, build a diagram out of bricks, "把这个结构搭出来", "用积木讲清楚这个系统/提示词/文档". Especially good for making abstract structure feel concrete and modular: show the parts, show how they snap together, show the assembled whole. Do not use for: a single-quote card (use a card skill), a social click-cover (use a cover skill), realistic product renders, voxel/Minecraft blocks, or reproducing trademarked LEGO® sets, the LEGO wordmark/logo, or licensed characters.
---

# LEGO Town / 乐高小镇

LEGO Town turns an idea that has **structure** — parts, relationships, an assembly — into a tangible brick-built scene where the build *is* the diagram.

默认面向中文图像/文档配图；用户使用英文时再切换英文输出。Use this skill when a concept is made of pieces that connect: a system, a workflow, a prompt, a document outline, an architecture, a comparison, a roadmap. **The build is the diagram. Bricks are the nouns, the stud-and-tube connection is the grammar, the minifig is the actor, and the baseplate is the world.** If the idea is a single mood or one sentence with no internal structure, bricks add nothing — use a card or cover skill instead. The bricks are never decoration; the way they connect must carry the meaning.

This skill exists because a pile of bullet points and a flat box-and-arrow chart both lose something a brick build keeps: you can *see* what depends on what (it sits on top), what is one module vs many (it clicks apart), what the steps are (the instruction sheet numbers them), and what is still missing (the empty studs). Modularity, dependency, and sequence become physical.

## Workflow

1. Read the source: the system, document, prompt, workflow, concept, comparison, or image-edit request. Classify the input (one-liner / article / existing image / comparison) — thin sources need particulars pulled from the user before building.
2. Find the **build anchor**: the one structure worth making tangible — the parts and how they fit. One image, one buildable structure. Before locking anything, **read the user's real intent** with `references/intent-reading.md` — infer the goal (impress / clarify / persuade / reassure / teach / document / sell / explore), audience, and tone, and fill the Intent Brief. Goal decides the mode, audience tunes density and labels, tone tunes the emotional coding. The same system is a persuade-Box-Art for an exec or a teach-Instruction-Sheet for a new hire.
3. **Route the asset** with `references/asset-routing-and-truth.md`: article figure / process-instruction / system town / exploded anatomy / comparison / box art / data status / reference-informed / center illustration. Record final container, display ratio, text ownership, exact truth constraints, and whether another tool should own the job (busy-town for cooperation casts; paper-operators for one conceptual action; native chart for strict axes).
4. Specialize when needed: metrics → `references/data-status-builds.md` (write the data contract first); real apparatus/protocol → `references/reference-informed-builds.md`. For long docs, pick 1–6 cognitive anchors — do not brick every paragraph.
5. Name the core **relationship** the build must show, using `references/connection-grammar.md`: connection, sequence, dependency, causality, feedback, contrast, tradeoff, hierarchy/containment, transformation, boundary, divergence/convergence, or tension. **Choose the relationship before the build** — precision comes from rendering the exact way the bricks connect, not from scattering generic arrows over a pile of blocks.
6. Choose the **domain and tone**: software/architecture, AI/prompt, product/strategy, data/process, org/team, education, research, personal/life, civic/city, or another field. The town's district, props, and signage come from the domain (`references/domain-adaptation.md`).
7. Choose the **mode** with `references/modes.md` — the single most LEGO-native decision:
   - **Finished Build / 成品** — the assembled diorama on a baseplate; the whole structure in one tangible hero shot.
   - **Instruction Sheet / 说明书** — numbered build steps + a parts call-out box; for processes, prompts, how-tos, document outlines.
   - **Exploded View / 爆炸图** — parts floating apart along connection lines; for anatomy, component breakdowns, "what's inside."
   - **Box Art / 盒面** — the front of a build's box; a title/cover image. (Original brand only — never the LEGO logo.)
8. Run the **Build Test** (below) to confirm the idea has buildable structure and that any minifig earns its place. Gate: if it fails, reroute.
9. Pick the **build archetype + minifig roles** from `references/brick-library.md` that can physically embody the relationship. For any non-trivial idea, first **diverge then converge** with `references/creative-divergence.md`: sketch 2–4 genuinely different concepts (different metaphor world / mode / archetype / minifig POV), then pick the freshest one that still passes the Build Test — never default to the obvious gray-blue town.
10. Assemble the scene from the kit in `references/primitives.md` — bricks, plates, tiles, slopes, technic, baseplate, signage, and the minifig kit — and **prefer a real native LEGO element that already carries the meaning** (arrow road-plate = flow, striped barrier = stop, gear mesh = coupled, trans-red stud = alarm) using `references/native-elements.md`, rather than a generic shape or a drawn arrow. Encode status, degree, and state precisely with `references/state-coding.md`. Reuse the same element for the same meaning so the build stays consistent.
11. Adapt the world, district, props, palette, and signage with `references/domain-adaptation.md`.
12. Place **text** with `references/lettering-and-text.md` + `references/text-strategy.md` — text is a *built/placed element*, not a free caption: choose the carrier and match its letterform. Tiles must carry **this content's real names and counts**. Move headline/explanation outside when the outer layout owns them (`references/layout-handoff.md`). Route exact/multi-line Chinese to the overlay path.
13. Put **exact truth constraints** into the final prompt (module names, `×N` counts, metrics). Do not let the model invent parts, steps, or the LEGO logo.
14. For artifacts entering README/social/slides/docs, return layout handoff fields from `references/layout-handoff.md`.
15. Build the final image prompt with `references/prompt-template.md`.
16. Generate or edit one image at a time. Apply `references/variation-engine.md` so each run varies the surface while the meaning stays invariant.
17. When the idea needs more than one image, plan the set with `references/series-and-chaining.md`.
18. For public/reusable assets, record with `references/prompt-records.md`.
19. Run QA with `references/qa-checklist.md`, plus asset-routing checks, `references/failure-patterns.md`, and the **Swap Test**. Regenerate if bricks are decorative, connection collapses into a generic arrow, voxel/Minecraft drift, labels wrong, trademark drift, or exact truth fails.
20. For README/showcase images, include at least one non-engineering domain when possible — a knowledge town, a life/learning build, a research map.

## Build Test

Before generating, answer:

```text
brick build:
- buildable structure: yes/no
- source anchor:
- domain & tone:
- relationship type:
- the parts (3-7 modules):
- how they connect (the stud grammar):
- the assembled meaning:
- mode (finished / instruction / exploded / box art):
- minifig: needed? role & what it adds (agency/scale/POV) — or none
- what breaks if flattened to a bullet list:
- forbidden drift:
```

Build only when **buildable structure = yes** and **what breaks if flattened** is concrete. Good answers:

- "Three modules depend on a shared foundation; stacked bricks show the load you can't see in a list."
- "The prompt has four parts that snap together in order; the instruction sheet shows assembly, not just a list."
- "Two designs differ by one swapped module; side-by-side builds make the single difference obvious."
- "The pipeline branches at a gate; the baseplate routes show where work splits and merges."

Weak answers (do not build — route to a card/cover/illustration skill):

- "It would look fun as LEGO."
- "Bricks add personality."
- "It's a single quote / one feeling / one number." → that's a card.
- "It's just a pretty cityscape." → no structure being explained.

**Minifig Test:** a minifig is justified only when it adds *agency, role, scale, or point of view* — a builder mid-assembly (the work is in progress), an inspector at a gate (a check is happening), a courier on a route (a handoff), a mayor on a plinth (ownership). A minifig standing beside a finished build, waving, is decoration — cut it. The build is the hero; minifigs are 0–3, never a cast.

## The Three+1 Modes

The mode is the LEGO-native equivalent of "what kind of picture." Choose it deliberately — see `references/modes.md`.

- **Finished Build / 成品模式** — the assembled scene on a baseplate, shot like an official set photo: clean studio light, glossy ABS, real stud geometry. Best for showing a *whole structure or relationship* at once — a system, a town, a comparison, an org.
- **Instruction Sheet / 说明书模式** — the iconic booklet look: numbered step panels, an exploded "add these parts" arrow, and a **parts call-out box** (e.g. `2×4 砖 ×3`). This is the signature mode for **documents, prompts, workflows, and how-tos**: it shows *assembly order*, not just a result. A prompt's system/context/instruction/format become four numbered build steps.
- **Exploded View / 爆炸图模式** — components separated along thin connection lines, hovering in assembly order. Best for **anatomy and breakdowns**: "what is this made of," "the parts of a good X," component architecture.
- **Box Art / 盒面模式** — the front of the set's box: hero build, an original product-name banner, an age/piece-count strip, a "minifig included" corner. A title/cover image. Use an **original or the user's own brand** — never the LEGO logo or wordmark.

One mode per image. A series may pair modes (box art opener → instruction-sheet middle → finished-build resolution).

## Default Style

Read `references/style-dna.md` before generating final images.

Core visual DNA:

- the look of **interlocking studded construction bricks** — authentic brick proportions, visible studs and tubes, ABS plastic with a soft glossy specular highlight, slight bevels
- **the build is the diagram**: every concept is a real brick element — brick, plate, tile, slope, baseplate, sign, gear, minifig — arranged so its *physical placement is the relationship* (stacked = depends on, in a row = sequence, walled = bounded, geared = coupled)
- clean **studio product-photography** light by default (soft key, gentle fill, contact shadows on a seamless sweep) — or a clean **instruction-vector** look in Instruction-Sheet mode
- authentic brick palette: bright red, yellow, blue, green, orange, plus warm tan, light/dark bluish gray, white, black, and **transparent** elements (clear, trans-blue, trans-neon) used semantically
- text is a **built/placed element, never a floating caption**: printed tiles (friendly rounded sans), brick-built hero letters (blocky stud-grid), studs-as-pixels, signboards, minifig placards, or the instruction page layer — match the letterform to the carrier; see `references/lettering-and-text.md`
- meaning carried by **real native LEGO elements** (arrow road-plates, stop signs, striped barriers, gears, traffic lights, trans-stud lights) wherever one already signals it — see `references/native-elements.md`; never a generic shape or drawn arrow where a real element exists
- **minifigs are original role-actors**, 0–3, smaller than the build; classic minifig silhouette with an *original* simple expression, defined by accessories and a printed torso, not by being a named/licensed character
- 16:9 horizontal by default for article/doc body images; 1:1 or 4:5 for cards/box art when asked
- one focal build module, generous quiet baseplate around it, clear depth (foreground build, mid action, back skyline)
- adaptive complexity: simplest sufficient build; allow a richer town when the system genuinely needs more modules, as long as routes, labels, and color coding stay legible
- **Original Bricks, not LEGO® sets** (see Identity below)
- no Minecraft/voxel cubes, no generic 3D-render blocks, no clip-art bricks, no PPT icon grid, no fake dense text, no rainbow clutter

## Identity: Original Bricks, Not LEGO® Sets

This skill uses the *visual language* of interlocking studded construction bricks. It must not trade on the LEGO® brand or copy protected content.

Do:

- generate **original** brick builds and **original** minifigs in the generic studded-brick aesthetic
- treat "LEGO" as internal shorthand for the look; the **output is original brick art**
- in Box-Art mode, use an **original product name** or the **user's own brand**

Do not:

- reproduce a specific official LEGO® set, named model, or its box
- render the **LEGO logo / wordmark** or the stud-top brand stamp
- depict **licensed characters or themes** (Star Wars, Marvel, Harry Potter, Ninjago-specific characters, Friends-specific characters, etc.) or recognizable real-person minifig likenesses
- imply official endorsement

If the user asks for a trademarked set or licensed character, build an **original equivalent** that conveys the same idea and say so.

## Domain Adaptation

Brick builds are not only for software diagrams.

- **AI / prompt**: a prompt assembled from snap-together modules — system tile, context bricks, instruction beam, format plate — shown as an instruction sheet so the reader sees the order and the optional parts.
- **Software / architecture**: a service town — modules as buildings, APIs as roads, the database as a foundation slab, the load-bearing dependency visible because everything sits on it.
- **Product / strategy**: a roadmap built lane by lane, a tradeoff on a brick seesaw, a comparison as two builds sharing one swapped module.
- **Data / process**: a conveyor of brick stations, gates where records pass or divert, a funnel hopper.
- **Org / team**: a baseplate town of departments connected by roads, ownership shown by which minifig stands on which plinth.
- **Education / research**: a knowledge town where concepts are districts, prerequisites are foundations, and a learning path is a road with numbered stops.
- **Personal / life**: a cozy small build — a single house, a garden plot, a daily-routine instruction sheet — warm tan and soft colors, not engineering gray.

Let the source choose the district, props, and signage. Do not force a server-rack town onto a life or learning topic.

## Depth Layers

Four references give the skill its depth. Reach for them in this order.

- **Relationship first** (`references/connection-grammar.md`): name the exact relationship, then render its *connection* — stacked for dependency, in-line for sequence, geared for feedback, walled for boundary, hinged for conditional. This is what stops every image from collapsing into a brick pile with arrows. Express the relation as a real 3D build whose physical assembly *is* the relation, not as a flat chart with brick texture.
- **Bricks & minifigs as the kit** (`references/brick-library.md` + `references/primitives.md`): build every scene from a known set of elements and minifig roles. One element carries one meaning; reuse it for that meaning so a set of images feels like one town.
- **State coding for precision** (`references/state-coding.md`): show status, degree, and quality without extra text — color semantics, stud-exposure (done vs to-build), elevation, transparency, gate posture, edge condition, light. Keep an encoding budget: pick the one or two encodings that carry the precision and let the rest stay neutral brick.
- **Series for chaining** (`references/series-and-chaining.md`): when the idea needs several images, chain them into one build. Keep the baseplate world, palette, and minifig constant; advance one throughline — the town gets built up, or the instruction booklet steps forward — and pay off a recurring element at the end.

These compose: pick the relationship, render it with bricks/minifigs and state coding, and when there are multiple images, chain them across one growing build.

## Precision & Anti-Template — Don't Be Rigid

The failure mode this skill is built to avoid: the first image feels amazing, then every later one feels the same and the magic dies. That happens when the skill stamps a default town onto any content. The cure is **precision first, variety second** — and four layers that keep it alive instead of templated.

- **Precision is the deepest anti-sameness weapon — the Swap Test.** Build *this specific* document/idea: its real module names on the tiles, its real part-count in the `×N` call-out, its real structure in the connection geometry, the native element its domain actually implies. Ask: *could this exact build be relabeled onto a completely different topic without changing anything?* If yes, it's a template — regenerate. A build derived from the real content is inherently unique because the content is unique. Generic placeholder labels and a one-size town are the tells.
- **Read intent first** (`references/intent-reading.md`): infer the goal, audience, and tone behind a vague ask ("做好看点" / "搭个图") and let the *intent* pick the mode and tone — not the bare fact that "it's a system." Fill the Intent Brief before the Build Test.
- **Diverge then converge** (`references/creative-divergence.md`): for any non-trivial idea, consider 2–4 genuinely different build concepts and reach for a fresh-but-apt native element or metaphor (a canal-lock for backpressure, a claw-crane for selection, a tug-of-war for contention) before committing. Never auto-default to the gray-blue service town.
- **Vary the surface, hold the meaning** (`references/variation-engine.md`): rotate camera, baseplate layout, focus accent, minifig, **text carrier** (`references/lettering-and-text.md`), and **which native elements** appear (`references/native-elements.md`) while the relationship, focal module, and label *meanings* stay invariant. A mechanism build (gears, levers) and a signage build (signs, barriers, lights) look nothing alike even for related topics.

Together: **build THIS content precisely → read what the user means → explore several ways to build it → render it fresh every time, without ever corrupting the structure.** Precision makes each image inherently its own; variety keeps the surface fresh; the relationship is the medicine — never change the medicine to add sugar.

## Skill Boundaries — Neighbors

| Source is about… | Use |
| --- | --- |
| parts snap together / modules / dependencies / prompt anatomy | **lego-town** |
| who hands off to whom / simultaneity / division of labor | **busy-town** |
| one actor performs one conceptual action | **paper-operators** |
| one quote / feeling / number | quote-cards / cover-pop |

## Output Contract

For planning, return:

```text
build anchor:
reader takeaway:
intent (audience · feeling · author stance · the one sentence to keep):
asset role:
final container and display ratio:
text ownership:
truth constraints and reference needs:
data contract (if relevant):
layout handoff:
domain & tone:
relationship type:
the parts (modules) + exact ×N where relevant:
how they connect (stud grammar):
mode (finished / instruction / exploded / box art) + because:
build archetype:
minifig roles (or none, with reason):
baseplate world / district (after divergence; why this beats the default):
native elements & state coding:
composition:
labels (carriers + exact-text block):
series plan (only when planning more than one image):
final image prompt:
prompt record (for public/reusable assets):
QA risks (asset routing + failure patterns + Swap Test):
```

For generation, produce one image at a time and report:

- image path
- intended placement
- one-line purpose
- mode used + asset role
- native label status: inside image / intentionally omitted / post-overlay
- layout handoff notes
- QA verdict: failure modes watched, exact truth, Swap Test, ship / regenerate / reroute

## References

- `references/style-dna.md`: visual identity, Original-Bricks rules, anti-voxel rules.
- `references/intent-reading.md`: goal/audience/tone → mode.
- `references/asset-routing-and-truth.md`: asset role, container, text ownership, truth, reroute.
- `references/data-status-builds.md`: metrics as brick status without fake dashboards.
- `references/reference-informed-builds.md`: real systems/apparatus cues; never copy official sets.
- `references/connection-grammar.md`: 12 relationships as brick connections.
- `references/modes.md`: Finished / Instruction / Exploded / Box Art.
- `references/brick-library.md`: archetypes + minifig roles.
- `references/creative-divergence.md`: 2–4 concepts then converge.
- `references/primitives.md`: brick kit + minifig construction.
- `references/native-elements.md`: real element vocabulary that already signals meaning.
- `references/lettering-and-text.md`: text as built/placed carriers.
- `references/text-strategy.md`: what text the image owns vs the layout.
- `references/layout-handoff.md`: handoff to README/social/slide.
- `references/state-coding.md`: status/degree/quality encoders.
- `references/domain-adaptation.md`: district/props by topic.
- `references/variation-engine.md`: surface varies, meaning holds; Swap Test.
- `references/series-and-chaining.md`: growing build / instruction booklet.
- `references/prompt-records.md`: public/reusable audit trail.
- `references/failure-patterns.md`: name and repair common failures.
- `references/prompt-template.md`: planning + generation + edit templates.
- `references/qa-checklist.md`: acceptance, regeneration, repair.
