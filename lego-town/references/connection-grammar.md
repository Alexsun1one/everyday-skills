# Connection Grammar / 连接语法

This is the heart of the skill. Every LEGO Town image encodes at least one relationship, and in bricks the relationship is **a physical connection**: how the parts snap together. The stud-and-tube system already means "joined"; your job is to render the *exact* connection — stacked, in a row, walled, geared, bridged — so the build *is* the relation, not a brick pile with arrows drawn on.

Choose the relationship before the build. Precision comes from the connection geometry, the direction, the condition, and the state.

## Relationship Families → Brick Connections

### Connection / 连接
Two things share a path, reference, or exchange.
Signals: "connects", "links", "between A and B", "把 A 和 B 连起来", "打通", "接口".
Brick rendering: a **road, rail, hose, or connector plate** physically joining two modules; a clear start, end, and a contact point (a coupling brick, a bridge span). The road has a direction marker (a road sign / arrow tile).
Build archetype: Bridge Span / 桥接, Road Link / 道路, Hose Coupling / 软管接驳.
Precision ladder: a brick laid between two builds → a labeled road with direction → an anchored road with source, target, the medium tile, and a "why" sign.
Degrades into: a random brick line touching two piles with no reason to exist.

### Sequence & Handoff / 顺序·交接
One stage passes material, ownership, or attention to the next.
Signals: "then", "step", "after", "handoff", "下一步", "交给", "流水线".
Brick rendering: **stations along a baseplate road or a conveyor of plates**, each a small build with a number tile; a minifig courier or a sloped chute shows the handoff; ownership changes via a different-colored minifig at each station.
Build archetype: Conveyor Line / 流水线, Relay Road / 接力道, Station Row / 工位排.
Precision ladder: left-to-right builds → numbered stations → a visible handoff object (parcel brick / chute) plus owner labels and a state change at each station.
Degrades into: a timeline of arrows with no ownership or state change.

### Dependency / 依赖
One module cannot stand without another beneath it.
Signals: "depends on", "requires", "built on", "without X", "前提", "底座", "支撑".
Brick rendering: **vertical stacking with a load-bearing foundation** — the dependent module physically sits on the one it needs; a foundation slab / pillar carries it; pull the base and it would topple. Show a missing-foundation failure twin (a module mid-collapse) when the article warns about it.
Build archetype: Load-Bearing Stack / 承重塔, Foundation Slab / 地基板, Pillar Brace / 立柱.
Precision ladder: stacked bricks → a labeled foundation layer → a visible load path + a "remove this and it falls" failure twin + a dependency-condition tile.
Degrades into: a tall stack that only means "higher/lower."

### Causality & Trigger / 因果·触发
One event activates or releases another.
Signals: "because", "leads to", "when X then", "触发", "导致", "一旦".
Brick rendering: a **Technic mechanism** — a lever, a falling domino of plates, a button on a 1×1 that drops a gate, a wound-up rubber-band catapult; the trigger visibly changes the next module's state (a light brick goes from clear to trans-red).
Build archetype: Lever & Gate / 杠杆闸, Domino Run / 多米诺, Trigger Button / 触发钮.
Precision ladder: an arrow from cause to effect → a real trigger part → a condition tile, the activation moment, a before/after pair, and the resulting state.
Degrades into: a causal arrow indistinguishable from a sequence arrow.

### Feedback Loop / 反馈环
An output returns to influence the input; the loop amplifies or stabilizes.
Signals: "feedback", "loop", "reinforces", "self-correcting", "越…越…", "闭环", "调节".
Brick rendering: **meshed gears or a closed conveyor loop** — a Technic gear train where turning one turns the next and back; a reinforcing loop adds a bigger gear / a growing stack each cycle; a balancing loop uses a governor, a valve, or a counterweight that damps it.
Build archetype: Gear Train / 齿轮组, Closed Conveyor / 环形传送, Governor / 调速器.
Precision ladder: a circle arrow → a gear mesh with a reading dial → a labeled loop type (reinforcing vs balancing), the signal value, the adjustment point, and the output state.
Degrades into: a decorative circle of bricks.

### Contrast & Opposition / 对比·对立
Two positions or states compared in one frame.
Signals: "but", "whereas", "A vs B", "before/after", "相比", "反而", "不是…而是".
Brick rendering: **two builds on a split baseplate sharing one reference line**, identical except for the one part that differs (a swapped colored module) so the difference is unmissable; mirrored layout, matched label tiles, a center divider plate.
Build archetype: A/B Split Plate / 对照板, Twin Builds / 双子build, Swapped Module / 换件对比.
Precision ladder: two separate builds → mirrored builds → same baseplate grid, matched labels, a highlighted single difference, and a verdict tile.
Degrades into: two unrelated builds on two unrelated plates.

### Tradeoff & Balance / 权衡·取舍
More of one value means less, cost, or risk elsewhere.
Signals: "tradeoff", "cost", "give up", "balance", "priority", "取舍", "代价", "两难".
Brick rendering: a **brick seesaw / balance beam** with weighted modules on each arm; the beam tilts toward the heavier side; removed-cost bricks sit in a discard bin; sliders show how much of each you keep.
Build archetype: Brick Seesaw / 跷跷板, Balance Beam / 天平梁, Slider Bank / 滑杆组.
Precision ladder: a level beam → weighted modules → named values on each side, a cost-bin tile, the chosen (lower) side, and a residual-risk part.
Degrades into: a level seesaw that says only "a decision exists."

### Hierarchy & Containment / 层级·包含
Parts live inside a whole, or smaller layers within larger ones.
Signals: "inside", "contains", "part of", "layer", "system", "包含", "层级", "母体".
Brick rendering: **walled plots / nested baseplates / a building with a cutaway wall** showing the rooms inside; smaller modules sit within a larger fenced district; one wall is removed (cutaway) so the reader sees the contained parts and their ownership tiles.
Build archetype: Walled District / 围合街区, Cutaway Building / 剖面楼, Nested Plates / 嵌套底板.
Precision ladder: stacked boxes → fenced plots → part-whole label tiles, boundary depth, ownership tags, and one open cutaway.
Degrades into: a pile of boxes or a brick org-tree.

### Transformation & State Change / 转化·状态迁移
Something becomes another state through a visible operation.
Signals: "becomes", "turns into", "from X to Y", "转化", "迁移", "重构后".
Brick rendering: a **build-station / a machine the part passes through**, or a **before-and-after twin** — raw bricks go in one side, an assembled module comes out the other; a color/material shift (gray rough → bright finished) marks the change; a minifig works the machine.
Build archetype: Build Machine / 加工机, Before/After Twin / 前后双子, Re-Brick Station / 重搭台.
Precision ladder: before & after → a conversion machine → input state, the operation, output state, leftover scrap bin, and state tiles.
Degrades into: a magic arrow between two builds.

### Boundary, Filter & Threshold / 边界·过滤·门槛
Some items pass an edge, others are held, softened, or transformed.
Signals: "boundary", "filter", "threshold", "approval", "门槛", "筛选", "准入".
Brick rendering: a **gate / fence / sieve plate / checkpoint** on the baseplate; passing items roll through on the road, rejected ones divert to a side bin; a barrier arm (Technic) is up/down; an inspector minifig stamps a tile. Pass/fail piles are visibly sorted.
Build archetype: Checkpoint Gate / 关卡, Sieve Plate / 筛板, Fence Line / 围栏.
Precision ladder: a wall between sides → a gate with pass/fail piles → the named rule tile, blocked items, admitted items, and the gate posture (up/down/locked).
Degrades into: a fence that doesn't explain the rule.

### Divergence & Convergence / 分流·汇聚
One source splits into paths, or many merge into one outcome.
Signals: "branches", "splits", "converges", "synthesizes", "分流", "汇聚", "归并".
Brick rendering: a **forking road / a junction plate / a funnel hopper** — one conveyor splits at a switch into labeled lanes (divergence), or several lanes feed a single hopper that outputs one module (convergence); a switch lever and criteria tile sit at the fork.
Build archetype: Road Fork / 岔路, Funnel Hopper / 漏斗, Merge Junction / 汇流口.
Precision ladder: branching arrows → a labeled road split → the criteria tile at the fork, each lane's state, the merged output, and grouped lane colors.
Degrades into: a brick tree with no rule for branching or merging.

### Tension & Equilibrium / 张力·均衡
Forces hold each other in place; unresolved but stable.
Signals: "tension", "held together", "not resolved", "dynamic balance", "拉扯", "僵持", "均衡".
Brick rendering: **two builds pulling on a shared part** — rubber bands / chains / a suspended module held between two anchored towers; the part stays centered because both sides pull; if one tower were removed it would swing. Counterweight bricks and force-direction arrow tiles.
Build archetype: Tug Anchors / 张拉锚, Suspended Span / 悬索, Counterweight Pair / 配重对.
Precision ladder: opposing builds → visible pull members (bands/chains) → force label tiles, the anchor point, the equilibrium state, and a "what breaks if one side wins" note.
Degrades into: two builds with arrows pointing at each other.

## Relationship × Build Quick Map

| Relation | Build archetype | Key element |
| --- | --- | --- |
| Connection / 连接 | Bridge Span / Road Link | road / connector plate |
| Sequence & Handoff / 顺序·交接 | Conveyor Line / Station Row | numbered stations + chute |
| Dependency / 依赖 | Load-Bearing Stack | foundation slab |
| Causality & Trigger / 因果·触发 | Lever & Gate / Domino Run | Technic lever / trigger |
| Feedback Loop / 反馈环 | Gear Train / Governor | meshed gears |
| Contrast & Opposition / 对比·对立 | A/B Split Plate | split baseplate + swapped module |
| Tradeoff & Balance / 权衡·取舍 | Brick Seesaw | balance beam + weights |
| Hierarchy & Containment / 层级·包含 | Walled District / Cutaway | fenced plots / cutaway wall |
| Transformation / 转化 | Build Machine / Before-After Twin | processing machine |
| Boundary & Filter / 边界·过滤 | Checkpoint Gate / Sieve | gate + pass/fail piles |
| Divergence & Convergence / 分流·汇聚 | Road Fork / Funnel Hopper | switch + lanes / hopper |
| Tension & Equilibrium / 张力·均衡 | Tug Anchors / Suspended Span | rubber bands + anchors |

## Precision Moves

- **Direction**: road signs, arrow tiles, conveyor-belt cleats, a minifig facing travel direction — never one giant floating arrow.
- **Condition tags**: attach "若 / 除非 / 完成后 / if / unless" tiles to gates, levers, and forks.
- **Before/after twins**: build both states when the claim is transformation, repair, or growth.
- **Counterweights**: make tradeoffs physical with weight bricks, a discard bin, a tilted beam.
- **Broken vs fixed**: a collapsed/cracked module vs a re-built one on the same baseplate for recovery claims.
- **Gate posture**: barrier arm up (pass), down (block), half (hold), locked (reject) — see `state-coding.md`.
- **Reinforcing vs balancing loop**: growing gears/stacks for reinforcing; a governor/valve/counterweight for balancing.
- **Primary vs secondary**: put the main relation on the lit baseplate road; demote side relations to quiet gray modules, amber evidence tiles, coral risk parts, or mint growth parts.

## Composing Multiple Relations

When a system nests 2–3 relations, render the **primary** as the main baseplate build/route, the **secondary** as state coding (color, elevation, stud-exposure), and the **tertiary** as a grouped label set on tiles. Keep one focal module. Do not give every relation its own road system, or the town becomes a diagram dump.

Use `state-coding.md` for pass/fail, before/after, done/active, missing/built, and risk/reward. Use `primitives.md` for the elements; use `brick-library.md` for the build archetype and minifig action.

## Accept / Regenerate

Accept if:

- The primary relation is named before the build is chosen.
- The connection geometry is specific (stacked / row / walled / geared / bridged / seesaw / forked), and replacing it with a plain arrow would lose meaning.
- Direction, condition, and state are visible in the bricks, not only in labels.
- A minifig (if present) physically performs the relation: builds, inspects, carries, gates, weighs, or anchors.
- Secondary relations are coded quietly and don't compete with the focal module.
- Labels sit on tiles, signs, road markers, plinths, or step numbers.

Regenerate if:

- The relationship collapses into a left-to-right arrow over a brick pile.
- Sequence, causality, and dependency look identical.
- Contrast becomes two unrelated builds with no shared reference.
- Feedback becomes a decorative ring of bricks.
- Tension resolves into a winner when the claim says it's held in balance.
- The build is a flat brick-textured chart icon instead of a real 3D assembly.
