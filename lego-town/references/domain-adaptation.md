# Domain Adaptation / 领域适配

A LEGO Town must fit the topic's world. The bricks are universal, but the **district, props, signage, palette, and minifig role** come from the domain. Do not force a server-rack town onto a life or learning topic, or a cozy cottage onto a security pipeline.

## Decision Order

1. Identify the domain.
2. Identify the tone: analytical, instructional, strategic, playful, warm, urgent, rigorous, or reflective.
3. Choose the minifig role and tool from that domain (`brick-library.md`).
4. Choose the district / world and its signature props.
5. Choose labels and palette that fit the topic's seriousness.

## Domain Map

### AI / Prompt / LLM
World: a **prompt assembly bench** or a small "prompt factory."
Props: a **System baseplate**, **Context bricks**, an **Instruction beam**, a **Format/Output tile**, optional **example bricks**, a **tool/function port**, a token meter gauge.
Best mode: **Instruction Sheet** — show the prompt assembled in order, with optional parts in the call-out box.
Good builds: a prompt snapped together step by step; a RAG pipeline as a conveyor (retrieve → rank → stuff → generate); an agent loop as a gear train (think → act → observe → back).
Minifig: Operator / Builder.
Avoid: glowing-brain bricks, generic robot heads, circuit wallpaper.

### Software / Architecture / Systems
World: a **service town** on a baseplate.
Props: modules as **buildings**, APIs as **roads**, the database as a **foundation slab**, a queue as a **conveyor**, a load balancer as a **road fork**, a cache as a nearby small store, auth as a **checkpoint gate**.
Best mode: **Finished Build** (the whole system) or **Exploded View** (a service's internals).
Good builds: dependency as a load-bearing stack; a request path as a lit blue road through the town; a failure as a cracked module with traffic diverting.
Minifig: Operator, Maintainer, Inspector (security/QA).
Avoid: a pretty city with no routes or labels; equal-weight building grid with no focal module.

### Product / Strategy / Business
World: a **planning table town** or a **roadmap site**.
Props: **roadmap lanes** with milestone flags, a **brick seesaw** for tradeoffs, an **A/B split plate** for options, a funnel for a pipeline, a plinth for a bet you own.
Best mode: Finished Build or Instruction Sheet (a rollout in phases).
Good builds: a tradeoff weighed on a seesaw; two strategies as twin builds with one swapped module; a roadmap as parallel lanes climbing a ramp.
Minifig: Mayor (ownership), Surveyor (planning).
Avoid: soulless dashboard of equal brick cards; KPI clip-art.

### Data / Process / Pipeline
World: a **factory floor / conveyor hall**.
Props: a **conveyor** of plates, **stations** with numbers, **gates** that pass/divert records, a **sieve plate** for filtering, **bins** for outputs and rejects, a **hopper** for aggregation.
Best mode: Instruction Sheet (the steps) or Finished Build (the whole line).
Good builds: ETL as a conveyor with a transform machine mid-line; a filter as a checkpoint with sorted pass/fail piles; a fan-in/fan-out at a fork+hopper.
Minifig: Operator, Inspector.
Avoid: abstract arrow soup; a belt with no stations or state changes.

### Org / Team / People
World: a **town hall + departments** baseplate.
Props: departments as **walled districts**, reporting lines as **roads**, ownership as **minifig-on-plinth**, a cross-team project as a **bridge** between districts.
Best mode: Finished Build.
Good builds: an org as districts joined by roads; a RACI as minifigs placed on/around a module; a handoff between teams as a courier on a bridge.
Minifig: Mayor (lead), Courier (handoff), several role-figs by district.
Avoid: a literal org-tree of stacked boxes; a crowd of identical figures.

### Education / Research / Knowledge
World: a **knowledge town** or a **research lab district**.
Props: concepts as **districts**, prerequisites as **foundation slabs**, a curriculum as a **learning road** with numbered stops, a hypothesis→experiment→result as a **build machine**, citations as **signboards**.
Best mode: Finished Build (the map) or Exploded View (anatomy of a concept / a paper).
Good builds: a field map where you can't reach the advanced district without crossing the basics; the "parts of a good X" exploded into labeled modules; an experiment as raw-in / result-out.
Dependency in a learning town must be PHYSICAL, not just adjacency: the advanced district should visibly rest ON the foundation — pillars, a load-bearing slab, or stacked layers carrying it — so "you can't do 实战 without 基础" reads as structure, not two buildings placed near a road. (A learning road alone shows sequence, not dependency; add the load path when the claim is "built on".)
Minifig: Guide (teaching), Researcher (lab), Surveyor (mapping the field).
Avoid: classroom clip-art; a checkmark under every step.

### Personal / Life / Habits
World: a **cozy small build** — a single house, a garden plot, a daily-route street.
Props: warm tan and soft colors, a small home, a garden, a daily-routine **instruction sheet**, a calendar baseplate, a tiny park.
Best mode: Instruction Sheet (a routine/recipe) or a small Finished Build.
Good builds: a morning routine as a 4-step instruction sheet; a habit stack as a load-bearing stack (each habit rests on the prior); a balanced life as a seesaw of brick modules.
Minifig: one warm everyday figure performing the routine.
Avoid: cold engineering gray; over-charting a feeling; a dashboard of life metrics.

### Civic / City / Infrastructure
World: a literal **brick town** (the home turf).
Props: roads, zones, utilities as foundation slabs, traffic as a conveyor, a checkpoint at the edge.
Best mode: Finished Build (the map).
Good builds: a city system as the town it literally is; infrastructure dependency as what sits on the utility slab.
Minifig: Mayor, Surveyor, Maintainer.
Avoid: a generic cityscape with no explained structure.

## Label Strategy

Use model-rendered short labels by default; a LEGO Town image should not feel wordless. Attach to tiles, signboards, road signs, plinths, step numbers, or call-out boxes.

Default: 3–6 short labels for a simple build; more for multi-step/multi-module/comparison/grouped builds; 2–6 Chinese characters per label; one sign strip allowed when it sharpens the takeaway; no dense paragraphs; no tiny fake background text.

Use blank label zones (overlay path) for: explicit post-production overlay, dense/exact Chinese, legal/financial/client-critical wording, titles, anything that must be editable, or any multi-line list.

## District Choices (Finished Build mode)

Before prompting, choose one district form and hold it:

- **Service town**: buildings + roads + a foundation slab (software/systems).
- **Factory floor**: a conveyor + stations + gates + bins (data/process).
- **Planning site**: roadmap lanes + seesaw + A/B plates (product/strategy).
- **Knowledge town**: concept districts + learning road + prerequisites (education/research).
- **Cozy street**: a home/garden/routine in warm tones (life/personal).

One district per image. Keep the main road visible and the focal module clear.
