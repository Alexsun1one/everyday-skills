---
name: busy-town
description: Generate or plan publish-grade images that turn a workflow, system, team, process, division of labor, or organization into a warm hand-painted busy town where anthropomorphic animal townsfolk are hard at work — a top-down town panorama, a cutaway building, a two-page spread comparison, or a trade close-up — in the watercolor / gouache storybook look of busy illustrated towns. Use when a user wants to explain or illustrate how a process runs end to end, how a team divides work, how parts of a system cooperate, a user journey, an org chart, an industry, a production line, a comparison of two ways of working, or a system's internal cooperation as cooperating animal characters inside a hand-painted town. Trigger words include 忙忙碌碌, 小镇, 忙碌镇, 动物干活, 剖面图, 全景镇, 谁在做什么, 分工, 协作, 流程, 旅程, 工序, "把流程画成镇子", "用动物讲清楚这个系统", "画出谁在忙什么". Especially good for making abstract cooperation feel warm, concrete, and full of simultaneous life: show the roles, show how they hand off and cooperate, show the whole thing turning. Do not use for: a single-quote card (use a card skill), a social click-cover (use a cover skill), realistic product renders, 3D-rendered towns, flat vector cartoons, claymation, voxel/Minecraft, or reproducing Richard Scarry's original characters, scenes, or copyrighted likenesses.
---

# Busy Town / 忙忙碌碌小镇

Busy Town turns an idea that has **cooperation** — roles, handoffs, a division of labor, a system running — into a warm hand-painted town scene where the townsfolk's work *is* the diagram.

默认面向中文图像/文档配图；用户使用英文时再切换英文输出。Use this skill when a concept is made of cooperating parts: a workflow, a team, a system, a user journey, an org, an industry, a process. **The town is the diagram. Animal characters are the verbs, the handoff between them is the grammar, the building is the container, and the street is the sequence.** If the idea is a single mood or one number with no "who works with whom / how does the whole thing turn", a town adds nothing — use a card or cover skill instead. The animals are never decoration; the way they hand off and cooperate must carry the meaning.

This skill exists because a flowchart of boxes and arrows, a sequence diagram, and a swimlane chart all lose something a busy town keeps: you can *see* who hands off to whom (one animal passes an object to the next), what the order is (animals line up along a street as one sequence of stations), how many roles there are (each window and each vehicle is a post), and that everything is happening *at once* (the whole page is busy). Division of labor, cooperation, sequence, and simultaneity become warm, visible life.

## Skill Boundaries — When to Use This, Not a Neighbor

Before anything else, confirm this is the right skill. The fastest failure is using a town for something a town can't do.

| The source is about… | Use | Why |
| --- | --- | --- |
| who hands off to whom / how does it run end to end / division of labor / simultaneity | **busy-town** | only a town can show cooperation + simultaneity warmly |
| a structure with parts that snap together / modules / dependencies / a prompt's anatomy | **lego-town** | bricks show *structural* assembly (snap/stack/wall), not character cooperation |
| one conceptual action performed on one object / a single paper-operator doing X to Y | **paper-operators** | one actor + one tool + one action, not a cooperating cast |
| one sentence / a quote / a number / one feeling | **quote-cards / cover-pop** | no cooperation to show |
| a realistic product render / a logo | neither | towns are explanatory, not photographic |

Borderline calls:
- "A microservice architecture" → if the article is about **how services cooperate** (handoffs, routing, the gateway), use **busy-town**; if it's about **how the system is structured** (layers, modules, dependencies), use **lego-town**. Read the source's verb: *cooperate* → town; *assemble* → bricks.
- "A user journey" → if it's about **roles the user passes through** (a customer meets 4 employees), use **busy-town**; if it's about **the path itself** (one traveler crossing terrain), use **paper-operators**.
- "A single concept's anatomy" (what's inside a good X) → **lego-town** exploded view, not a town.

If you cannot point at cooperation in the source, do not use this skill.

## Workflow

The workflow is not a checklist — each step has a **why** and a **failure mode**. Skip a step only if you can name why it doesn't apply.

### 1. Read the source — and classify the input
Read the source material. First **classify what kind of input** you have, because each is read differently:
- **A one-liner** ("画一下我们的订单流程"): the source is thin — you must **pull particulars from the user** (how many steps? who owns each? where does it hurt?) before drawing. A one-liner cannot drive a precise town; ask the one short question.
- **A paragraph / article / doc**: the source is rich — mine it for the real role names, the real step count, the real bottleneck, the real tradeoff. These particulars are what lock the image to this document (see Swap Test).
- **An existing image** ("改一下这张图"): the source is a picture — describe what's there, name what must stay invariant vs what changes. Use the image-edit template, not a fresh prompt.
- **Meeting notes / a transcript**: the source is noisy — extract the *decisions* and the *open questions*; a town of "what we agreed" beats a town of "everything that was said".
- **A comparison request** ("对比一下 A 和 B"): the source is two-headed — both sides must be drawn from the **same** town template or the comparison dies.

**Why:** the input type fixes how much you must invent vs extract. **Failure mode:** treating a one-liner like an article and inventing generic roles that fail the Swap Test.

### 2. Find the cooperation anchor — the one running whole
Find the **one** running whole worth making tangible: the roles and how they cooperate. One image, one running town. Before locking it, **read the user's real intent** with `references/intent-reading.md` — infer the goal (impress / clarify / persuade / reassure / teach / document / sell / explore), audience, and tone, and fill the Intent Brief. Goal decides the mode, audience tunes density and labels, tone tunes the emotional coding. The same process is a persuade-Two-Page-Spread for an exec or a teach-Cutaway-Building for a new hire.

**Why:** a town that tries to show two running wholes reads as clutter. **Failure mode:** "show everything our team does" → no focal cooperation → cluttered village → fails the three-second read.

### 3. Route the asset — role, container, text ownership, truth
Route the asset with `references/asset-routing-and-truth.md`: decide whether this is an article/doc figure, process town, org/system cutaway, comparison spread, trade close-up, data status town, reference-informed town, or center illustration for a card/slide. Record final container, display ratio, text ownership, exact truth constraints, and whether another tool should own the job.

**Why:** the first question is not "what should the town look like?" but "what job must this image do in the final artifact?" **Failure mode:** forcing Busy Town to own a strict chart, full social card, structural assembly (→ lego-town), or single-operator concept (→ paper-operators).

### 4. Specialize when the source demands it
- For **metrics, queues, SLAs, backlog, status boards**, read `references/data-status-towns.md` and write the exact data contract before prompting.
- For **real industries / harbors / hospitals / schools / factories / brand ops**, read `references/reference-informed-towns.md` and gather stable visual/factual cues before prompting when accuracy matters.
- For long docs, pick 1–6 cognitive anchors (see asset-routing) — do not illustrate every paragraph.

**Why:** invented numbers and wrong industry cues are silent failures that look "pretty." **Failure mode:** fake data beauty; reference hallucination.

### 5. Name the relationship BEFORE the town
Name the core **relationship** the town must show, using `references/collaboration-grammar.md`: handoff, sequence, dependency, causality, feedback, contrast, tradeoff, hierarchy/containment, transformation, boundary/filter, divergence/convergence, or simultaneous-busy. **Choose the relationship before choosing any animal or shop.**

**Why:** precision comes from rendering the exact way animals cooperate, not from scattering generic arrows over a cute diorama. A "sequence" town and a "feedback loop" town look completely different — but only if you named the relation first.

**Falsifiable test:** can you state the relationship in one sentence with a direction? ("A hands to B", "A waits for B", "A and B pull against each other".) If you can only say "they're related", you don't have a relationship yet — go back to the source.

**Failure mode:** skipping this step and drawing "a busy town about X" → the cooperation collapses into left-to-right arrows → fails QA.

### 6. Choose the domain and tone
Choose the **domain and tone**: software/architecture, AI/prompt, product/strategy, data/process, org/team, education, research, personal/life, civic/city, or another field. The town's district, shops, props, and signage come from the domain (`references/domain-adaptation.md`).

**Why:** the shops and vehicles must belong to the source's world — server racks pasted onto a bakery article is the loudest tell of a lazy skill. **Failure mode:** defaulting to engineering gray + server village for every topic.

### 7. Choose the mode — see the Mode Decision Tree below
Choose the **mode** with `references/modes.md` — the single most Busy-Town-native decision. This choice is important enough to get its own decision tree (next section). Asset role often implies mode (process town → panorama/sequence; org/system → cutaway; comparison → two-page; one role → close-up), but intent can override.

### 8. Run the Collaboration Test (below)
Confirm the idea has cooperative roles and that any animal character earns its place. The Test is the **gate** — do not proceed to step 9 if it fails; route the user to a neighbor skill instead.

### 9. Diverge 2–4 concepts, then converge
For any non-trivial idea, first **diverge then converge** with `references/creative-divergence.md`: sketch 2–4 genuinely different concepts (different town world / mode / role POV), then pick the freshest one that still passes the Collaboration Test. Pick the **animal role + trade** from `references/role-library.md` that can physically embody the relationship.

**Why:** the biggest failure mode of this skill is auto-defaulting to the bakery-street. Divergence is the cure. **Failure mode:** "I'll just use a bakery street again" → every image looks the same → the skill dies.

### 10. Assemble the scene + encode state
Assemble from the kit in `references/primitives.md` — buildings, shops, vehicles, tools, signage, props, and the animal-character construction kit — and encode status, degree, and state precisely with `references/state-coding.md`. Reuse the same element for the same meaning so the town stays consistent.

**Why:** state coding (smoke, flags, dozing) is what lets a town carry *status* without text — the thing a flowchart can't do. **Failure mode:** over-coding (every channel maxed) → clutter; under-coding (no state markers) → a pretty village that says nothing about health/risk/done.

### 11. Adapt the world
Adapt the world, district, props, palette, and signage with `references/domain-adaptation.md`.

### 12. Write labels — text strategy + relationship objects
Write readable **labels** with `references/text-strategy.md`. Use 3–6 short labels for a simple town; more when roles, steps, contrasts, or groups need them. **Attach labels to relationship objects** (the handoff parcel, the gate rule board, the scale crate, the floor plaque, the crossroads signpost), not to empty space. Move headline / explanation / citations outside the image when the outer layout should own them (`references/layout-handoff.md`).

**Why:** labels on relationship objects double as state; labels on empty space are decoration; titles stuffed into the town fight the outer layout. **Failure mode:** floating captions, text-empty scene, or text overload.

### 13. Put exact truth into the prompt
For exact labels, step counts, metrics, industry cues, or proper names, put **exact truth constraints** into the final prompt. Do not let the image model invent stations, roles, numbers, dates, or reference-specific details.

### 14. Layout handoff (when the image enters another artifact)
For final artifacts that will enter README, social cards, slides, docs, or article packages, read `references/layout-handoff.md` and return caption, crop guidance, safe margin, and handoff owner.

### 15. Build the final prompt
Build the final image prompt with `references/prompt-template.md`.

### 16. Generate one image, vary the surface
Generate or edit one image at a time. Apply `references/variation-engine.md` so each run varies the surface (camera, town layout, focus accent, lead animal, weather/time of day) while the meaning stays invariant — two runs of the same request must look visibly different yet read as the same cooperation.

### 17. Chain if more than one image
When the idea needs more than one image, plan the set with `references/series-and-chaining.md` so the images share one town world, palette, animal identity, and a progressing story.

### 18. Record public / reusable assets
For public examples or reusable packages, record the source anchor, asset role, truth constraints, reference cues, final prompt, output path, rejected attempt reason, and QA result using `references/prompt-records.md`.

### 19. Run QA — Swap Test + failure scan + asset routing
Run QA with `references/qa-checklist.md`. Include the asset-routing checks from `references/asset-routing-and-truth.md`, the failure scan from `references/failure-patterns.md`, and the **Swap Test** from `references/variation-engine.md`: if the image could move to a different article on the same topic without anyone noticing, it has failed — regenerate with more content-specific particulars. Regenerate if animals are decorative, the medium drifts, the cooperation collapses into a generic arrow, labels are missing/wrong, exact truth is wrong, or the idea is unclear.

### 20. Include a non-engineering domain in showcase sets
For README/showcase images, include at least one non-engineering domain — a bakery, school, hospital, market town — so the skill does not look like it only draws software flowcharts.

## Mode Decision Tree

The mode is the single most Busy-Town-native decision. Do not pick a mode by habit. Ask the questions in order:

```text
Q1. Is the article about the WHOLE thing turning at once ( simultaneity, end-to-end, "a day in the life", "launch day" )?
    yes → TOWN PANORAMA. (A flowchart cannot show simultaneity; only a panorama can.)
    no  → Q2.

Q2. Is it about what's INSIDE one thing ( a system's layers, an org's departments, "what happens inside X" )?
    yes → CUTAWAY BUILDING.
    no  → Q3.

Q3. Is it about a DIFFERENCE between two states / two ways / before-after?
    yes → TWO-PAGE SPREAD.
    no  → Q4.

Q4. Is it about ONE role in depth ( "what does a ___ do", zooming in on one station )?
    yes → TRADE CLOSE-UP.
    no  → you probably don't have a busy-town problem. Re-check Skill Boundaries.
```

### Goal → Mode shortcut (when intent is clear)

| If the real goal is… | lean toward… |
| --- | --- |
| impress / sell (exec, customer) | Panorama hero, or Two-Page Spread |
| clarify / teach (new hire, learner) | Cutaway or Sequence street |
| persuade (advocate a change) | Two-Page Spread (old vs new) |
| reassure ("it's under control") | Panorama, calm, green flags |
| document (reference) | Cutaway with full labels |
| explore ("here's the map") | Panorama with a focal "?" flag |

### Falsifiable mode test

State the mode choice as a sentence with a *because*:

> "I chose **Cutaway** *because* the article is about the hidden infrastructure layer, and only a cutaway can reveal a hidden floor."

If you cannot finish the *because* with a structural reason, you picked by habit — go back to the tree.

## Collaboration Test — the Gate

Before generating, answer every field. **The Test is a gate**: if `cooperative structure = no` or `what breaks if flattened` is vague, do NOT proceed — route the user to a neighbor skill (card / cover / lego-town / paper-operators).

```text
busy town:
- cooperative structure: yes/no
- source anchor:
- domain & tone:
- relationship type:
- the roles (3-7 animal jobs):
- how they cooperate (the handoff grammar):
- the running meaning:
- mode (panorama / cutaway / two-page / close-up):
- lead animal: needed? role & what it adds (agency/scale/POV/focus) — or none
- what breaks if flattened to a flowchart:
- forbidden drift:
```

### Three-tier answer key (per field)

For the trickiest fields, here is what good / borderline / bad answers look like.

**`what breaks if flattened to a flowchart`**
- **Good (proceed):** "Five roles hand an object down a line; the street layout shows the sequence you can't see in a list." / "The system has a hidden floor everyone forgets; the cutaway makes it visible." / "Two ways of working differ only in cooperation; same-town-twice makes the delta obvious."
- **Borderline (tighten before proceeding):** "It's a process with several steps." → too generic; ask *which* step is the interesting one and make that the focal zone.
- **Bad (do not draw):** "It would look cute as animals." / "Animals add personality." / "It's a single quote / one number." → route to a card.

**`lead animal: needed?`**
- **Good:** "Yes — a Cat Inspector at the gate; removing it loses the *check-is-happening-now*." / "No — the cooperation is the cast; no single lead; the town is the hero."
- **Borderline:** "Yes, a baker, because bakers are nice." → weak; the baker must add agency (work-in-progress) or POV, not charm.
- **Bad:** "Yes, a mascot waving at the reader." → decoration; cut it.

**`how they cooperate (the handoff grammar)`**
- **Good:** "A Goose at intake hands the slip to a Mouse who files it; the Mouse hands the file to a Cat who stamps it; rejected files pile at the Cat's gate."
- **Borderline:** "They work together as a team." → name the *physical* cooperation (who passes what to whom, where).
- **Bad:** "They collaborate." → no grammar; you don't have a town yet.

**Lead-Animal Test:** a lead animal is justified only when it adds *agency, role, scale, or point of view* — a baker rolling dough (work in progress), a cat inspector at a checkpoint (a check is happening), a courier driving a delivery van (a handoff in motion), a mayor on a balcony (oversight). An animal waving at the reader beside a finished town is decoration — cut it. The town is the hero; named lead animals are 1–2, the rest of the cast is anonymous townsfolk, never a branded character set.

## The Four Modes

The mode is the Busy-Town-native equivalent of "what kind of picture." Choose it deliberately — see `references/modes.md`.

- **Town Panorama / 全景镇模式** — a top-down or high-angle view of an entire town: shops, streets, vehicles, squares, all busy at once, no perspective vanishing point, encyclopedic even layout. Best for showing a *whole system or value chain* at once — a process end to end, an org as a town, an industry, a journey across a map. The **only mode that can show simultaneity**.
- **Cutaway Building / 剖面楼模式** — the iconic look: a building cut open, each floor and each window a work station with one animal on the job, interior detail visible (pipes, shelves, ladders). The signature mode for **systems, orgs, and "what happens inside X"**: a microservice stack becomes a tower, an order flow becomes a multi-floor workshop, a team becomes an office building.
- **Two-Page Spread / 对照页模式** — left page and right page, same town drawn twice, two ways of working / before vs after / plan A vs plan B. Best for **comparisons and change**: the cooperation is shown by *what differs* between the two otherwise-identical towns.
- **Trade Close-up / 职业特写模式** — one animal, one trade, in focus: its tools laid out, its action mid-motion, its output labeled. Best for **"what does a ___ do"** and zooming in on one station of a larger town.

One mode per image. A series may pair modes (panorama opener → cutaway middle → close-up detail → two-page resolution).

## Precision Tiers — How Dense Should the Town Be?

Not every image needs the same information density. Match the tier to the audience and goal. Over-dense for an exec is clutter; under-dense for a reference doc is useless.

| Tier | Reads in… | Audience / goal | Town density | Labels |
| --- | --- | --- | --- | --- |
| **T1 — Glance** | 3 seconds | exec / customer / "wow" | one focal cooperation zone + warm busy periphery | 3–4 short labels |
| **T2 — Study** | 30 seconds | peer / engineer / "now I get it" | focal zone + 4–6 stations with handoffs | 5–8 labels, one sign strip allowed |
| **T3 — Reference** | repeated reading | new hire / docs / "look it up" | full panorama or rich cutaway, every station labeled, state coding on | 8+ labels, full signage, allowed a chalkboard rule |

Rules:
- Pick the tier **from the intent brief**, not from the source length. A long article can still want T1 if the goal is "impress".
- The three-second read (QA) must pass at *every* tier — even T3 must have a recognizable focal zone on first glance; the detail rewards the second look, it doesn't gate the first.
- Do not silently upgrade to T3 because the source is rich. Density is a choice; justify it.

## Composition — When the Article Nests Relations

Most articles nest 2–3 relationships (e.g. a process *that branches at a gate* *and has a feedback loop*). Rendering every relation at equal weight produces diagram soup. Layer them:

| Layer | What it carries | Visual weight |
| --- | --- | --- |
| **Primary** | the one relationship the article is *about* | the main street / focal cooperation zone / the gold bell |
| **Secondary** | a relation that qualifies the primary | state coding (a red flag at the gate, smoke at the bottleneck) |
| **Tertiary** | a relation that's context | a quiet side alley, a grouped label set, a small inset |

Rules:
- Name the primary before drawing. If you can't name it, the article isn't ready for a town.
- The secondary is **encoded**, not re-drawn — don't give the feedback loop its own arrow system; show it as a returning courier on the same street.
- The tertiary is **grouped**, not scattered — a side alley labeled "反馈" with one tiny courier is enough.
- One focal module. If two zones fight for the eye, neither wins.

**Accept:** primary reads in 3 seconds; secondary and tertiary reward a second look without competing.
**Regenerate:** every relation has its own arrow system; the eye doesn't know where to land.

## Failure Mode Library

Every image dies in one of a few recognizable ways. Diagnose, then apply the fix.

| # | Failure | Symptom | Fix |
| --- | --- | --- | --- |
| 1 | **Decorative animals** | removing the animals changes nothing | cut them, or give them agency (a handoff / a check / a wait) |
| 2 | **Arrow collapse** | the cooperation reads as left-to-right arrows | re-render the relation as physical cooperation (handoff / lineup / gate / seesaw); remove arrows |
| 3 | **Medium drift** | the town looks 3D / flat-vector / clay / voxel | regenerate with the HARD NEGATIVES block; lead the prompt with "手绘水彩" |
| 4 | **Copyright drift** | a character resembles Huckle / Lowly / Mr. Frumble | swap species + outfit; state "original equivalent" in the output |
| 5 | **Template lock** | same bakery street as last time | run creative-divergence with ≥3 concepts; pick a fresh metaphor |
| 6 | **Over-coding** | every shop has every state channel maxed | encoding budget: 1–2 channels carry precision; neutralize the rest |
| 7 | **Under-coding** | no state markers; a pretty village that says nothing | add smoke (running) + one flag (alert/done) on the focal shop |
| 8 | **Swap-Test fail** | could illustrate any article on this topic | inject one content-specific particular (real role name / real count / real bottleneck) |
| 9 | **Clutter panorama** | "everything at once" with no focal zone | name one focal square; demote the rest to periphery |
| 10 | **Two-page delta loss** | left and right look unrelated | redraw right page from the *same* template as left; change only the cooperation state |
| 11 | **Cutaway-as-orgchart** | a stack of flat labeled boxes, no interior | add inter-floor connectors (ladder/chute/pipe), visible interior detail, one animal per window |
| 12 | **Close-up-as-portrait** | an animal posing, no tools, no action | put it mid-action; lay out the labeled tool kit around it |

When QA fails, look up the symptom here before regenerating blind.

## Default Style

Read `references/style-dna.md` before generating final images.

Core visual DNA:

- the look of **hand-painted watercolor / gouache storybook illustration** — visible paper grain, soft wet-on-wet washes, gentle pencil or ink under-drawing showing through, warm muted palette, hand-lettered signs. The tactile opposite of 3D render, flat vector cartoon, claymation, and voxel.
- **the town is the diagram**: every concept is a real storybook element — shop, house, vehicle, tool, sign, awning, flag, streetlight — arranged so its *placement and the animals' cooperation is the relationship* (along a street = sequence, cut into floors = layers, at a crossroads = branching, passing an object = handoff)
- warm storybook palette: brick red, mustard yellow, sage green, dusty blue, terracotta, cream, soft brown wood, with small semantic accents (a red flag for alert, a green checkmark flag for done)
- readable labels as **hand-painted shop signs, banners, awning text, vehicle livery, poster bills, or hand-lettered flags** — never floating UI text, never garbled glyphs
- **anthropomorphic animal townsfolk are original role-actors**, many of them (a town is busy), each defined by species + trade outfit + action, not by being a named/copyrighted character; classic round-friendly proportions, calm or gently expressive faces
- 16:9 horizontal by default for article/doc body images; 1:1 or 4:5 for cards/two-page spreads when asked
- one focal cooperation zone, generous busy detail around it, clear depth (foreground action, mid shops, back skyline)
- adaptive complexity: simplest sufficient town; allow a richer panorama when the system genuinely needs more roles, as long as handoffs, labels, and color coding stay legible
- **Original Characters, not Scarry's** (see Identity below)
- no 3D-rendered town, no flat vector cartoon, no clay/plasticine, no Minecraft/voxel cubes, no AI-glossy illustration, no rainbow clutter, no cute-animals-doing-nothing diorama

## Identity: Original Characters, Not Scarry's

This skill uses the *visual language* of a hand-painted busy illustrated town. It must not trade on Richard Scarry's work or copy protected content.

Do:

- generate **original** animal characters and **original** town scenes in the generic busy-storybook aesthetic
- treat "忙忙碌碌小镇 / Busytown" as internal shorthand for the look and the *method* (encyclopedic panorama, cutaway building, anthropomorphic division of labor, warm hand-painting); the **output is original art in that tradition, never a copy of his books**
- in Two-Page mode, draw an **original** comparison, not a recreation of any spread from his books

Do not:

- reproduce any of Scarry's **named characters** (Huckle Cat, Sally Cat, Lowly Worm, Mr. Frumble, Bananas Gorilla, Sergeant Murphy, Miss Honey, etc.) or their specific outfits/colors/likenesses
- reproduce a **specific scene or spread** from his books (the famous bakery page, the fire station page, the ship page, the road page, etc.)
- render any **publisher logo, series logo, or trademark** (Golden Books, Busy World, etc.)
- imply official endorsement

If the user asks for a named Scarry character or a specific scene, paint an **original equivalent** that conveys the same idea (a different animal in a different trade outfit, a different shop layout) and say so.

## Domain Adaptation

Busy towns are not only for software diagrams.

- **AI / prompt**: a prompt assembled from cooperating animal workers — the planner rabbit hands the brief to the researcher fox, who hands context to the writer bear, who hands the draft to the editor owl; shown as a cutaway workshop so the reader sees the order and the handoffs.
- **Software / architecture**: a service town — microservices as shops connected by streets, the database as a warehouse everyone delivers to, the API gateway as a town-square post office routing parcels.
- **Product / strategy**: a roadmap built block by block along a main street, a tradeoff as two animals on a seesaw, a comparison as two parallel streets.
- **Data / process**: a conveyor of shop-stations, crossroads where records are routed, a funnel hopper at a mill.
- **Org / team**: a town of departments connected by streets, ownership shown by which animal runs which shop and which flag flies over it.
- **Education / research**: a knowledge town where concepts are districts, prerequisites are foundations, and a learning path is a road with numbered stops.
- **Personal / life**: a cozy small town — a home, a garden, a daily-routine street — warm cream and sage, not engineering blue.

Let the source choose the district, shops, props, and signage. Do not force a server-rack town onto a life or learning topic.

## Depth Layers

Four references give the skill its depth. Reach for them in this order.

- **Relationship first** (`references/collaboration-grammar.md`): name the exact relationship, then render its *cooperation* — animals passing an object along a street for handoff, a building cut into floors for layering, a crossroads for branching, a checkpoint gate for filtering, a seesaw for tradeoff. This is what stops every image from collapsing into a cute diorama with arrows. Express the relation as a real hand-painted scene whose *character cooperation is* the relation, not as a flat flowchart with storybook texture.
- **Roles & town as the kit** (`references/role-library.md` + `references/primitives.md`): build every scene from a known set of animal roles + trade outfits + town parts. One element carries one meaning; reuse it for that meaning so a set of images feels like one town.
- **State coding for precision** (`references/state-coding.md`): show status, degree, and quality without extra text — chimney smoke (running) vs no smoke (idle), a dozing animal (a stalled station), a checkered flag (done), a red flag (alert), a half-open gate (partial). Keep an encoding budget: pick the one or two encodings that carry the precision and let the rest stay neutral.
- **Series for chaining** (`references/series-and-chaining.md`): when the idea needs several images, chain them into one storybook. Keep the town world, palette, and lead animal constant; advance one throughline — the town wakes up, gets busier, and resolves — and pay off a recurring element at the end.

These compose: pick the relationship, render it with roles/town and state coding, and when there are multiple images, chain them across one growing storybook.

## Flexibility & Intent — Don't Be Rigid

Three layers keep this skill from producing the same picture every time and from missing what the user actually wants. They are not optional polish — they are how the skill stays alive instead of stamping a template.

- **Read intent first** (`references/intent-reading.md`): infer the goal, audience, and tone behind a vague ask ("画个流程图" / "做得好看点") and let the *intent* pick the mode and tone — not the bare fact that "it's a process." Fill the Intent Brief before the Collaboration Test. A wrong mode usually means the intent was never read.
- **Diverge then converge** (`references/creative-divergence.md`): for any non-trivial idea, consider 2–4 genuinely different town concepts and reach for a fresh-but-apt town metaphor (an orchard sorting line for filtering, a fire station for incident response, a harbor for import/export, a bakery street for a pipeline) before committing. Never auto-default to the bakery-street.
- **Vary the surface, hold the meaning** (`references/variation-engine.md`): every generation rotates camera, town layout, focus accent, lead animal, and weather/time of day while the relationship, focal cooperation, and label meanings stay invariant. Re-runs look visibly different yet stay correct; this is what answers "每次出来的图都一样."

Together: **read what the user means → explore several ways to paint it → render it fresh every time, without ever corrupting the cooperation.** Variety is the sugar; the relationship is the medicine — never change the medicine to add sugar.

## Output Contract

For planning, return:

```text
cooperation anchor:
reader takeaway:
intent (audience · feeling · author stance · the one sentence to keep):
asset role:
final container and display ratio:
text ownership:
truth constraints and reference needs:
data contract (if relevant):
layout handoff:
tier (T1 glance / T2 study / T3 reference):
domain & tone:
relationship type (primary / secondary / tertiary):
the roles (animal jobs):
how they cooperate (handoff grammar):
mode (panorama / cutaway / two-page / close-up) + because:
lead animal (or none, with reason):
town world / district (after divergence; why this beats the default):
elements & state coding (budget: 1-2 channels):
composition (focal zone + layering):
labels (shop signs / banners / flags / livery; attached to relationship objects; exact-text block):
series plan (only when planning more than one image):
final image prompt:
prompt record (for public/reusable assets):
QA risks (asset routing + failure patterns + Swap Test):
```

For generation, produce one image at a time and report:

- image path
- intended placement
- one-line purpose
- mode used + tier + asset role
- native label status: confirm whether labels are rendered inside the image, intentionally omitted, or to be overlaid in post because the user requested editable text / Chinese was unstable
- layout handoff notes (caption outside, crop warnings, safe for small display?)
- QA verdict: which failure modes were watched for, whether exact truth holds, whether the Swap Test passes, whether it ships / regenerates / reroutes

## References

- `references/style-dna.md`: the visual identity, the watercolor material/palette/light, the Original-Characters rules, and anti-3D/anti-flat-vector/anti-clay rules.
- `references/intent-reading.md`: read the user's real goal, audience, and tone behind a vague ask, and let intent pick the mode — the anti-template layer.
- `references/asset-routing-and-truth.md`: decide asset role, final container, text ownership, truth constraints, reference needs, and when another tool should own the job.
- `references/data-status-towns.md`: preserve exact numbers while turning metrics, queues, and status boards into town status scenes.
- `references/reference-informed-towns.md`: gather stable factual and visual cues for real industries/places; never copy Scarry pages.
- `references/collaboration-grammar.md`: the 12 relationship families and how each is rendered as a specific cooperation between animals, not a generic arrow.
- `references/modes.md`: Town Panorama, Cutaway Building, Two-Page Spread, and Trade Close-up — when to use each and how to compose it.
- `references/role-library.md`: animal role species + trade families — the verbs and actors that physically perform a relationship.
- `references/creative-divergence.md`: diverge into 2–4 distinct town concepts and fresh town metaphors, then converge — so the skill is inventive, not rigid.
- `references/primitives.md`: the composable kit of town elements, signage/label containers, and the animal-character construction kit.
- `references/state-coding.md`: the precise visual encoding system for status, degree, and quality (smoke, dozing, flags, gate posture, color accents).
- `references/domain-adaptation.md`: how to adapt the town and its districts to AI/prompt, software, product, data, org, education, research, and life topics.
- `references/text-strategy.md`: decide which text belongs inside the image, which belongs outside, and how to repair label failures.
- `references/layout-handoff.md`: hand a generated town to README, social-card, slide, article, or knowledge-base layouts without stuffing the image with outer-layout text.
- `references/series-and-chaining.md`: how to chain a set of images into one growing town or one storybook with a shared throughline.
- `references/variation-engine.md`: vary the surface while holding the meaning invariant; the Swap Test.
- `references/prompt-records.md`: record public/reusable prompts, truth constraints, output paths, rejected attempts, and QA results.
- `references/failure-patterns.md`: name and repair common failures such as decorative animals, fake data beauty, text overload, template lock, and wrong-owner tasks.
- `references/prompt-template.md`: planning and final generation prompt templates, plus an image-edit template.
- `references/qa-checklist.md`: acceptance, regeneration, and repair rules.
