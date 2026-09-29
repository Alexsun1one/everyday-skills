# Collaboration Grammar / 协作语法

Every Busy Town image encodes at least one relationship. Choose the relationship before choosing the animals or the town. Precision comes from rendering the exact relation, direction, condition, and state, not from adding generic arrows over a cute diorama.

The grammar here differs from a "connection grammar" (bricks snapping together) on purpose: in a busy town the relation is **performed by cooperating characters**, not by the physical snap of parts. The same abstract relation (say, "dependency") is rendered differently — a brick sits *on* another brick, but a baker *waits for* the miller's flour. Always render the relation as **character cooperation first**, layout second.

## Relationship Families

### Handoff & Relay / 交接·接力
One role passes an object, message, or half-finished work to the next.
Article signals: "hands off", "passes to", "then", "relay", "交给", "下一步", "接力", "移交".
Visual encoding: an animal physically extending a parcel / crate / letter / loaf to the next animal down the street; a relay baton; a conveyor passing items between two shops. The handoff has a visible giver, receiver, object, and contact moment.
Role family: Courier / 邮递员, Porter / 搬运工, Relay Runner / 接力员.
Precision ladder: two animals near each other -> one extending an object to the other -> labeled object, giver's role, receiver's role, and a state tag (raw / checked / sealed).
Degrades into: a flowchart arrow labeled "next".

### Sequence & Assembly Line / 顺序·流水线
Roles line up so that work passes through each in order.
Article signals: "step", "stage", "pipeline", "assembly line", "then", "顺序", "工序", "流水线".
Visual encoding: a row of shop-stations along one street; each shop has an animal mid-task; the half-finished good moves left-to-right (or along the street) growing more complete. Numbered signposts or flags mark the order.
Role family: Assembly Line Workers / 流水线工, Station Keepers / 工位主.
Precision ladder: a row of shops -> numbered stations with state tags -> visible object transforming at each station, with owner labels and a "work in progress" tag that changes.
Degrades into: a timeline with arrows and no ownership change.

### Dependency & Waiting / 依赖·等待
One role cannot start, finish, or make sense without another's output.
Article signals: "depends on", "requires", "waits for", "blocked by", "前提是", "依赖", "等...交货".
Visual encoding: one animal idle or watching at its shop doorway, holding empty hands or an empty tray, while another shop upstream is still working; OR one shop's whole porch resting on / braced against another shop's wall. A "waiting" tag (an hourglass flag, a dozing helper) makes the stall visible.
Role family: Waiter / 等候员, Supplier / 供货员, Foundation Mason / 地基匠.
Precision ladder: two shops near each other -> one clearly idle waiting on the other -> labeled dependency, the missing input, the stalled station, and the condition ("等面粉到货").
Degrades into: a vertical stack that only means "higher/lower".

### Causality & Trigger / 因果·触发
One event activates, releases, or produces another.
Article signals: "because", "therefore", "leads to", "when X happens", "causes", "触发", "导致", "一旦".
Visual encoding: a bell rung by one animal that makes the next shop's animal leap into action; a lit fuse; a pulled lever; a dropped letter that releases a courier; a pulled rope that rings an alarm bell on the rooftop. The trigger moment is shown mid-action, and the resulting state change is visible at the next shop.
Role family: Bell-Ringer / 摇铃员, Trigger Keeper / 扳闸员, Signal Tower Operator / 信号员.
Precision ladder: arrow from cause to effect -> trigger object mid-pull -> condition label, activation moment, before/after pair, and resulting state tag.
Degrades into: a causal arrow that could also mean sequence.

### Feedback Loop / 反馈环
An output returns to influence the input; the loop may amplify or stabilize.
Article signals: "feedback", "loop", "reinforces", "self-correcting", "越...越...", "反过来", "闭环".
Visual encoding: a circular street or a roundabout where a courier carries a report back from the end shop to the start shop; reinforcing loops use a growing stack / a widening funnel of returning parcels; balancing loops use a scale, a damper, or a valve tap on the loop.
Role family: Inspector / 巡检员, Loop Courier / 回路信使, Valve Keeper / 阀门员.
Precision ladder: a circular street with arrows -> a courier visibly returning a report to the start -> labeled loop type (reinforcing/balancing), signal value, adjustment point, and output state.
Degrades into: a decorative circular arrow.

### Contrast & Opposition / 对比·对立
Two states, ways of working, or readings must be compared in one frame.
Article signals: "but", "whereas", "instead", "A vs B", "on the other hand", "相比", "反而", "不是...而是".
Visual encoding: **two-page spread** — left page and right page show the same town drawn twice with one thing different (one chaotic, one orderly; one old way, one new way). Both pages share the same buildings and street layout so the eye locks onto the single difference. A shared measuring axis (a river, a road) connects them.
Role family: Two Mayors / 双镇长, Mirror Shopkeepers / 镜像店主.
Precision ladder: two towns side by side -> same town drawn twice -> matched layout, contrast axis, labeled difference, and highlighted delta.
Degrades into: two unrelated panels.

### Tradeoff & Balance / 权衡·取舍
Choosing more of one value means less, delay, risk, or cost elsewhere.
Article signals: "tradeoff", "cost", "give up", "balance", "priority", "取舍", "代价", "两难".
Visual encoding: a playground seesaw / a market scale in the town square, two animals on opposite ends with labeled crates ("速度" vs "质量", "成本" vs "可靠"); a tilted platform with removed and kept tags.
Role family: Scale Keeper / 司秤员, Mediator / 调停员, Seesaw Pair / 跷跷板二人组.
Precision ladder: a scale with two sides -> weighted labeled crates -> named values, cost tag, chosen side, residual risk flag.
Degrades into: a balanced scale that says only "decision".

### Hierarchy & Containment / 层级·包含
Parts live inside a whole, or smaller layers sit within larger structures.
Article signals: "inside", "contains", "part of", "layer", "system", "belongs to", "包含", "层级", "母体".
Visual encoding: **cutaway building** — a tower with several floors, each floor a layer; nested rooms inside rooms; a town inside a region shown as a map-in-map. Ownership tags on each floor; one exposed cutaway wall shows the inside.
Role family: Tower Keeper / 塔楼管家, Floor Managers / 楼层主管, Town Planner / 规划员.
Precision ladder: stacked floors -> labeled layers with ownership -> part-whole tags, boundary depth, one exposed cutaway, and an org-tree flag.
Degrades into: an org chart or pile of floors with no meaning.

### Transformation & State Change / 转化·状态迁移
Something becomes another state through a visible operation.
Article signals: "becomes", "turns into", "before/after", "from X to Y", "转化", "迁移", "修复后".
Visual encoding: a workshop with a clear input door and output door — raw material goes in, finished good comes out (e.g. wheat in, bread out); a mill, a forge, a wash-house, a paint shop. Before/after twins on a shared conveyor; a color shift across the shop; a repair seam visible on a mended object.
Role family: Miller / 磨坊主, Forge Smith / 铁匠, Repair Tailor / 缝补匠, Color Painter / 漆匠.
Precision ladder: before and after objects -> a conversion workshop with in/out doors -> input state, operation, output state, residue/by-product, and state labels.
Degrades into: a magic arrow between two objects.

### Boundary, Filter & Threshold / 边界·过滤·门槛
Some items are allowed through, held back, softened, or transformed at an edge.
Article signals: "boundary", "filter", "threshold", "permission", "approval", "拒绝", "门槛", "筛选", "进入条件".
Visual encoding: a town-gate checkpoint with an inspector animal; a sieve or sorting screen at an orchard line; a stamp tray at a customs house; a quiet zone fence. Pass/fail tags on items; admitted items proceed, rejected items pile up at the side.
Role family: Gate Inspector / 闸门检查员, Customs Stamp Officer / 盖章官, Sieve Sorter / 筛选员.
Precision ladder: a wall between two zones -> a gate with pass/fail -> named rule, blocked items, admitted items, gate state (open/closed/half).
Degrades into: a barrier that does not explain the rule.

### Divergence & Convergence / 分流·汇聚
One source splits into paths, or many sources merge into one outcome.
Article signals: "branches", "splits", "many paths", "converges", "synthesizes", "分流", "汇聚", "归一".
Visual encoding: a crossroads where one cart splits into three lanes to three shops; a harbor where many ships dock at one quay; a funnel hopper at a mill where many sacks pour into one chute; braided streets that merge into one avenue.
Role family: Crossroads Guard / 岔口守卫, Harbor Master / 港务长, Funnel Miller / 漏斗磨坊主.
Precision ladder: branching streets -> labeled lane split -> criteria at fork, path states, merged output, grouped label set.
Degrades into: a tree diagram with no rule for branching or merging.

### Simultaneous Busy / 齐忙·并进
Many roles work at once, independently but together keeping the whole running.
Article signals: "meanwhile", "at the same time", "in parallel", "all going on", "同时", "并行", "到处都在忙".
Visual encoding: **the signature mode** — a top-down town panorama where every shop, street, and vehicle is busy at the same moment; smoke from every chimney; multiple animals each doing their own task; no single arrow, the simultaneity is the point. This is the relation that *only* a busy town can show well — a flowchart cannot.
Role family: The Whole Town / 全镇居民, Mayor on the Balcony / 阳台镇长 (oversight).
Precision ladder: many busy shops -> each labeled with its role and current task -> a focal cooperation zone in the middle, peripheral simultaneous work around it, and a mayor/overseer reading the whole.
Degrades into: a cluttered cute village with no focal point.

## Relationship × Role Quick Map

| Relation | Recommended role family | Key prop / scene |
| --- | --- | --- |
| Handoff & Relay / 交接·接力 | Courier / 邮递员 | a parcel passed between two animals |
| Sequence & Assembly Line / 顺序·流水线 | Assembly Line Workers / 流水线工 | a row of shop-stations along a street |
| Dependency & Waiting / 依赖·等待 | Waiter / 等候员 | an idle animal + an upstream shop still working |
| Causality & Trigger / 因果·触发 | Bell-Ringer / 摇铃员 | a bell rung, the next shop leaping into action |
| Feedback Loop / 反馈环 | Loop Courier / 回路信使 | a circular street, a returning courier |
| Contrast & Opposition / 对比·对立 | Two Mayors / 双镇长 | two-page spread, same town twice |
| Tradeoff & Balance / 权衡·取舍 | Scale Keeper / 司秤员 | a town-square scale / seesaw |
| Hierarchy & Containment / 层级·包含 | Tower Keeper / 塔楼管家 | a cutaway tower, floors = layers |
| Transformation & State Change / 转化·状态迁移 | Miller / 磨坊主 | a workshop with in/out doors |
| Boundary, Filter & Threshold / 边界·过滤·门槛 | Gate Inspector / 闸门检查员 | a checkpoint gate with pass/fail |
| Divergence & Convergence / 分流·汇聚 | Crossroads Guard / 岔口守卫 | a crossroads or harbor |
| Simultaneous Busy / 齐忙·并进 | The Whole Town / 全镇居民 | a top-down panorama, everything busy |

## Precision Moves

- Direction markers: use small pennant flags along a street, vehicle headings, animal gazes, or a procession of passed objects; avoid giant arrows.
- Condition tags: attach "if / unless / after / except / 当..." tags as small chalkboards or signposts at gates, triggers, or thresholds.
- Before/after twins: show both states when the article claims transformation, repair, loss, or maturity — use a workshop with an in-door and an out-door.
- Counterweights: make tradeoffs physical with crates on a scale, removed tags on a tilted platform.
- Broken-vs-mended: show failure and repair on the same object when the claim is about recovery.
- Gate states: mark open (gate up), closed (gate down), half-open, rejected (pile at side), filtered, converted.
- Reinforcing-vs-balancing loops: a growing stack of returning parcels for reinforcing; a damper / valve / scale for balancing.
- Primary/secondary layering: keep the main relation on the central street / focal shop; put side relations in quieter side alleys, amber evidence flags, coral risk flags, mint growth flags.
- **Simultaneity is the special power**: when the article is about "everything happening at once" (a busy morning, a launch day, a live system), lean into the panorama and let multiple unconnected-but-simultaneous tasks fill the page — a flowchart cannot show this, a town can.

## Composing Multiple Relations

When an article nests 2-3 relations, render the primary relation as the main street / focal cooperation, the secondary as state coding (flags, smoke, expressions), and the tertiary as a grouped label set on a side alley. Keep one focal module.

Use `references/state-coding.md` for pass/fail, before/after, stable/unstable, hidden/visible, idle/busy, and risk/reward states. Use `references/primitives.md` for street, gate, scale, scaffold, chimney, flag, awning, vehicle, and sign primitives.

Do not give every relation equal visual weight. If every relation gets its own arrow system, the image becomes a diagram dump.

## Accept / Regenerate

Accept if:

- The primary relation is named before the animals are chosen.
- Direction, condition, and state are visible in the characters' cooperation, not only in labels.
- The animals physically perform the relation: hand off, line up, branch, gate, weigh, wait, transform, or parallelize.
- The visual encoding is specific enough that replacing it with a plain arrow would lose meaning.
- Secondary relations are coded quietly and do not compete with the focal cooperation.
- Labels are attached to relationship objects: shop signs, handoff parcels, gate rule boards, scale crates, floor plaques, crossroads signposts, or signal flags.

Regenerate if:

- The relationship collapses into a left-to-right arrow.
- Sequence, causality, and dependency are visually indistinguishable.
- Contrast becomes two unrelated panels.
- Feedback becomes a decorative circle.
- Tension resolves into a winner when the article says it is held in balance.
- The animals stand beside the relationship instead of handing off, lining up, gating, or weighing it.
- A "simultaneous busy" scene has no focal zone and reads as clutter.
