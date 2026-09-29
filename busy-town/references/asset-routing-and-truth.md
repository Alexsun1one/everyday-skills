# Asset Routing And Truth / 资产路由与事实约束

Use this reference before final prompt writing when the source is more than a vague "画个流程图": a process doc, org chart, report, metrics board, slide, screenshot, industry explainer, or social-card package.

Busy Town is a visual cooperation system, not only a style. The first question is not "what should the town look like?" but "what job must this image do in the final artifact?"

## Core Rule

Keep the busy town only when **character cooperation** clarifies the meaning.

If the final need is an exact chart, a full slide layout, a full social card, a logo, a structural assembly diagram, or a decorative village where no cooperation is needed, do not force Busy Town to own the whole job. Use Busy Town for the cooperation image, and let the surrounding layout, chart, PPT, lego-town, or card system do its own work.

## Asset Roles

Pick one role before choosing the mode.

### Article / Doc Figure

Use for one section, process, team, or system inside an essay or doc.

- Visual job: make one cooperation memorable.
- Best form: panorama, cutaway, or sequence street with 3–7 roles.
- Text ownership: short shop signs / flags inside; paragraph explanation stays outside.

### Process Town

Use for an end-to-end workflow, pipeline, order flow, or user journey with multiple stations.

- Visual job: show who hands off to whom and where it stalls.
- Best form: panorama or sequence street; cutaway if the process is layered.
- Truth rule: use the real step names and real count; do not invent stations.

### Org / System Cutaway

Use for departments, service layers, platform stacks, or "what's inside X".

- Visual job: show who sits where and what the hidden floor does.
- Best form: cutaway building with floor plaques and inter-floor connectors.
- Truth rule: floor names and ownership must match the source.

### Comparison Spread

Use for old vs new, plan A vs B, before vs after, team A vs team B.

- Visual job: make the single delta obvious.
- Best form: two-page spread — same town twice, only cooperation state differs.
- Truth rule: both sides must share the same layout template.

### Trade Close-up Card

Use for "what does a ___ do", onboarding one role, or zooming one station.

- Visual job: show tools, action, and output of one trade.
- Best form: trade close-up with labeled kit.
- Text ownership: tool labels inside; role bio / salary / long description outside.

### Data Status Town

Use when the source includes metrics, queues, SLAs, backlog, pass rates, or status boards — but the image should explain *operational meaning*, not replace a rigorous chart.

- Visual job: show what the numbers mean as town status (queue length, red flags, smoke, backlog piles).
- Best form: panorama or cutaway with state coding carrying the numbers.
- Truth rule: list every value that appears; do not invent counts, rates, or dates.
- If exact axes are the whole artifact, use a native chart; Busy Town can create the surrounding status town.

### Reference-Informed Town

Use for a real industry, harbor, hospital, school, factory, brand ops, or any place/process that is visually easy to get wrong.

- Visual job: make the world recognizable without copying a photo or Scarry page.
- Best form: domain-adapted town with stable cues translated into watercolor animals/shops.
- Reference rule: gather stable cues (parts, roles, vehicles, layout conventions), not style.

### Center Illustration For A Card Or Slide

Use when another system will handle title, subtitle, body copy, platform ratio, or slide layout.

- Visual job: be the central image well.
- Best form: no large title inside; leave safe margins; avoid dense edge labels.
- Text ownership: only shop/role labels needed to understand the cooperation. Outer layout owns headline and commentary.

## Routing Questions

Answer these before prompt writing:

```text
asset role:
final container: article / README / social card / slide / doc / knowledge base / other
display well or ratio:
text ownership: inside image / outside layout / both
truth constraints: exact role names / exact step count / exact metrics / industry cues / none
reference need: yes/no and why
cooperation necessity:
if not Busy Town, better owner:
```

## Cognitive Anchors For Long Sources

For a long process doc, org handbook, transcript, report, or deck, do not illustrate every paragraph.

Pick 1–6 cognitive anchors:

- the opening question ("who does what?")
- the main handoff chain
- the bottleneck or risk
- the hidden layer / forgotten role
- the evidence or metric turn
- the before/after change
- the closing payoff ("now it runs")

For each anchor, decide whether it becomes:

- one standalone town figure
- one page in a series
- a data status town
- a comparison spread
- no image because text explains it better

## Truth Handling

### Must Be Exact

- role / step / department names specified by the user
- station counts ("six stages", "four floors")
- metrics that appear in the image (queue=12, pass rate=98%)
- product / team / service names when recognition matters
- industry cues when the town claims to be a specific kind of place

Put exact requirements in the final prompt:

```text
Exact text: include only these labels: "接单", "拣货", "质检", "打包", "发货", "配送".
Exact counts: six stations along the river; no extra shops inventing steps.
Exact data: backlog pile shows 12 crates; do not invent other numbers.
Do not invent extra roles, stages, dates, legends, or labels.
```

### Can Be Symbolic

- animal species choice (as long as trade is clear)
- weather / time of day
- decorative townsfolk in the periphery
- metaphor world (bakery / harbor / mill) when it fits
- non-critical background props

## What To Refuse Or Reroute

Reroute away from Busy Town when:

- the user only needs a strict chart with exact axes and values
- a screenshot or table already explains the point better
- the animals would be decorative
- the asset is a complete social card or slide layout rather than the center illustration
- the topic is structural assembly (modules snapping together) → **lego-town**
- the topic is one conceptual action by one actor → **paper-operators**
- the topic is a single quote / number / feeling → **quote-cards / cover-pop**
- the topic requires photo-real documentary accuracy
- the user needs a logo, icon system, sticker, or brand mark

In these cases, say the better owner plainly.

## QA Additions

Before delivery, check:

- The chosen asset role is visible in the result.
- Text ownership is respected: no headline stuffed into the image when an outer layout should own it.
- Exact labels, counts, and metrics are not invented, misspelled, or swapped.
- Reference-informed cues are recognizable but not copied from a source image or Scarry page.
- The cooperation is still necessary after routing.
- The image remains readable at the intended display size.
