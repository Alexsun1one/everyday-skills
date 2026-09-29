# Domain Adaptation / 题材适配

Busy Town is not only for software flowcharts. The town's district, shops, vehicles, props, and signage must come from the **source's own domain** — otherwise every image looks like the same engineering village. Let the source choose the town.

When the source is engineering-y, use engineering-appropriate shops (forge = build, warehouse = DB). When the source is about life / food / art / education, force the town away from server-rack clichés into warm domain-specific shops.

## Domain → Town Cheat Sheet

### AI / Prompt
- The town is a **workshop town** where a multi-step craft happens.
- Planner Rabbit → Researcher Fox → Writer Bear → Editor Owl, each in their own shop, handing a manuscript/parcel down a street.
- A prompt's system/context/instruction/format become four workshops along a lane.
- Mode: **Cutaway** (a workshop building, each floor a prompt layer) or **Sequence street**.

### Software / Architecture
- The town is a **service town**: microservices as shops, the database as a **warehouse** everyone delivers to, the API gateway as a **town-square post office** routing parcels.
- A Mole runs the underground pipes (infrastructure / hidden layers).
- Mode: **Panorama** (the whole system) or **Cutaway** (a service tower).

### Product / Strategy
- The town is a **roadmap town**: blocks built along a main street, one quarter per block.
- A tradeoff is a **seesaw** in the town square with two animals and labeled crates.
- A comparison is a **two-page spread**: two parallel streets, same buildings, different flow.
- Mode: **Panorama** or **Two-Page Spread**.

### Data / Process
- The town is a **mill / factory town**: a conveyor of shop-stations, a funnel hopper at a mill, a crossroads where records route, a sieve at an orchard sorting line.
- Mode: **Sequence street** or **Cutaway mill**.

### Org / Team
- The town is an **office / civic town**: a town hall with a mayor on the balcony, each department a shop flying its own flag.
- A cutaway office tower = the org chart.
- Mode: **Cutaway office tower** or **Panorama civic town**.

### Education / Research
- The town is a **knowledge town**: concepts are districts, prerequisites are foundations (a shop can't open until its upstream shop delivers), a learning path is a road with numbered stops.
- A library tower = the knowledge base; an Owl Librarian runs it.
- Mode: **Panorama map** or **Cutaway library tower**.

### Personal / Life
- The town is a **cozy small town**: a home, a garden, a market, a daily-routine street. Warm cream and sage palette, not engineering blue.
- A morning routine is a street of small shops (kitchen → bathroom → study).
- Mode: **Panorama small town** or **Sequence street**.

### Civic / City
- The town is a **real civic town**: a harbor, a market square, a town hall, a fire station, a customs gate.
- Use for: public services, governance, urban systems.
- Mode: **Panorama** or **Cutaway civic building**.

### Art / Culture / History
- The town is a **crafts / heritage town**: a gallery street, an atelier, a museum tower, a restoration workshop.
- A culture article's "the parts of a good ___" becomes a cutaway of an atelier with each station a part of the craft.
- Mode: **Cutaway atelier** or **Panorama gallery street**.

### Food / Cooking
- The town is a **food town**: a bakery street, a mill, a market, a harbor for imported ingredients.
- A recipe is a sequence street; a cuisine is a panorama food town.
- Mode: **Sequence street** or **Panorama food town**.

### Finance / Business
- The town is a **market / trading town**: a customs house, a scale in the square, a bank tower, a harbor.
- A tradeoff is a scale; a flow of value is a street of traders handing off coins/ledgers.
- Mode: **Panorama market town** or **Two-Page Spread**.

### Health / Medicine
- The town is a **care town**: a hospital tower (cutaway), a pharmacy shop, a harbor for incoming patients, a repair workshop for recovery.
- Mode: **Cutaway hospital tower** or **Panorama care town**.

## Choosing the Palette by Domain

Engineering / data / AI: keep the warm palette but allow a touch more blue/gray for the "system" feel. Never full-corporate-blue.

Life / food / education / art / personal: full warm palette — brick red, mustard, sage, terracotta, cream. This is where the skill shines; don't drain the warmth.

Civic / finance: warm with a dignified accent — slate roofs, brass scales, a navy banner.

## Adaptation Rules

1. Read the source's domain first.
2. Pick the **town type** from the cheat sheet (or invent a fresh one — see `creative-divergence.md`).
3. Pick the **shops, vehicles, props** that belong to that domain (don't paste server racks into a bakery article).
4. Pick the **animals + trades** that fit the domain (a Mole for hidden infra; an Owl for oversight; a Beaver for building).
5. Pick the **palette accent** (warm for life/food/art; cooler for engineering; slate/brass for civic).
6. Pick the **signage style** (chalkboard for kitchen; blueprint for architecture; ledger for finance; placard for gallery).

## Anti-Patterns

- **Server-rack town everywhere**: don't default to a data-center village for every topic. A life / food / art article wants its own town.
- **Generic office town everywhere**: don't default to cubicle animals for every process. A craft article wants an atelier, not a cubicle.
- **Engineering gray everywhere**: don't drain the warmth from a life / culture / education topic.
- **Same animal everywhere**: don't use only cats or only the same species. Match species to trade nature.

## When the Domain Is Unclear

If the source doesn't name a domain, infer it from the topic:
- talks about systems/code/data → engineering town
- talks about people/feelings/daily life → cozy town
- talks about craft/art/history → heritage town
- talks about money/markets → trading town

When truly unclear, default to a **warm generic storybook town** (market square + main street + a few craft shops) and let the cooperation define the layout, not the domain.
