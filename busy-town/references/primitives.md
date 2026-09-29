# Primitives / 镇子零件套件

The composable kit of town elements, signage/label containers, and the animal-character construction kit. Build every scene from these so a set of images feels like one town. **One primitive carries one meaning; reuse the same primitive for the same meaning.**

## A. Buildings & Containers / 建筑容器

The "boxes" of the diagram — each holds a role or a stage.

| Primitive | Use for | Visual tell |
| --- | --- | --- |
| **Shop / 铺子** | one role / one station | a small storefront, awning, sign above door, one animal inside |
| **House / 小屋** | a single unit / one instance | a cottage, chimney, garden — for "one of something" |
| **Tower / 塔楼** | a layered system / hierarchy | tall, several floors, used in cutaway mode |
| **Warehouse / 仓库** | storage / buffer / persistence | big, low, full of crates, wide doors |
| **Workshop / 工坊** | a transformation station | in-door and out-door, machines inside, sparks/smoke |
| **Town Hall / 镇公所** | governance / oversight / central control | central, balcony, clock tower, mayor on the balcony |
| **Market Square / 集市广场** | exchange / convergence / focal handoff zone | open, central, many stalls, the meeting point |
| **Harbor / Dock / 港口** | external interface / import-export / boundary | edge of town, ships, cranes, customs gate |
| **Wall / Fence / 围墙** | boundary / enclosure / threshold | separates inside from outside, has a gate |
| **Garden / Field / 田园** | growth / organic / source | green, rows, a Farmer animal, used for "raw input" |

Rules: a **shop** = one role; a **tower** = a layered system (use cutaway); a **warehouse** = storage/buffer (not a role). Don't use a tower when you mean a single shop.

## B. Streets, Routes & Connections / 街道与连接

How parts of the cooperation are linked. **The street IS the relationship** — a row of shops along a street = sequence; streets meeting at a square = convergence; a street that loops back = feedback.

| Primitive | Use for | Visual tell |
| --- | --- | --- |
| **Main Street / 主街** | the spine / the primary sequence | runs through the town, shops line it in order |
| **Side Alley / 小巷** | secondary / quiet relation | small, behind the main street, less busy |
| **Crossroads / 岔路口** | divergence / branching | a signpost, a Guard animal, lanes splitting |
| **Roundabout / 环岛** | feedback loop | a circular street, a courier looping back |
| **Bridge / 桥** | connection over a gap / handoff between two sides | spans a river or a gap, two animals meeting mid-bridge |
| **River / 河** | the shared spine / the value stream | flows through, used in two-page spreads to tie pages |
| **Railway / 铁路** | high-throughput pipeline | ties stations in a fixed order |
| **Square / 广场** | convergence / focal meeting point | open, central, where handoffs happen |
| **Wall with Gate / 带门围墙** | boundary with a controlled threshold | a Gatekeeper animal, pass/fail tags |

Rules: use a **main street** for sequence (shops line up); a **crossroads** for branching; a **roundabout** for a loop; a **bridge** for connecting two distant sides. Don't draw arrows when a street does the job.

## C. Vehicles / 车船

Mobile actors that perform **handoff** and **transport** between fixed shops. Each vehicle is a labeled carrier.

| Primitive | Use for |
| --- | --- |
| **Cart / Wagon / 板车** | porter moving crates between shops |
| **Bicycle / 自行车** | courier carrying one letter/parcel fast |
| **Delivery Van / 货车** | bulk handoff between stages |
| **Train / 火车** | sequential pipeline (cars = ordered stages) |
| **Boat / Ship / 船** | crossing a boundary / import-export |
| **Hot-Air Balloon / 热气球** | the overview / top-down POV (often shown floating above a panorama) |
| **Fire Truck / 消防车** | incident response |
| **Ambulance / 救护车** | recovery / repair rush |

Rules: a vehicle is for **moving** something; if nothing is being moved, don't add a vehicle. The hot-air balloon is the signature "you are looking down at the whole town" marker in panorama mode.

## D. Tools & Props / 工具道具

The small hand-painted objects that animals use to perform their trade. Each tool is a labeled micro-detail. See `role-library.md` for each trade's canonical kit. Reuse the same tool for the same trade across a series.

Common labeled props: **parcel, crate, sack, barrel, letter, ledger, stamp, key, lantern, flag, banner, signpost, scale, anvil, rolling pin, clipboard, bell, megaphone.**

Rules: a tool must be **in use** (mid-action), not lying idle, unless the idle state itself is the point (a dozing station).

## E. State Markers / 状态标记

Small physical objects that encode status without text. See `state-coding.md` for the full system. Quick list:

| Marker | Means |
| --- | --- |
| **Chimney smoke / 烟囱冒烟** | the shop is running / busy |
| **No smoke / 不冒烟** | idle / waiting / stopped |
| **Flag on rooftop / 屋顶旗** | the shop's state (red=alert, green=done, gold=focus) |
| **Awning rolled out / 篷布拉开** | open for business |
| **Awning rolled up / 篷布卷起** | closed / off-duty |
| **Dozing animal / 打瞌睡** | stalled / waiting on a dependency |
| **Pile of rejected crates / 退货堆** | gate rejected items |
| **Checkered flag / 格子旗** | done / shipped |
| **Red pennant / 红三角旗** | alert / risk / blocked |
| **Golden bell / 金铃** | focus / the one to watch |
| **Hourglass / 沙漏** | waiting / latency |

## F. Signage & Label Containers / 招牌与标签容器

Where the readable text lives. **All hand-painted.** Never floating UI text.

| Container | Use for | Visual tell |
| --- | --- | --- |
| **Shop Sign / 招牌** | role name above a shop door | a painted board or hanging sign |
| **Awning Text / 篷布字** | short label on an awning edge | a word or two painted on the fabric |
| **Banner / Pennant String / 横幅·三角旗串** | section / phase / page label | a cloth strip across the top |
| **Vehicle Livery / 车身字** | what a vehicle carries | painted on the side |
| **Crate Stamp / Barrel Stamp / 木箱印章** | state of a passed object | a stamped word on a crate |
| **Signpost / 路牌** | crossroads label / direction | a wooden post with arms |
| **Chalkboard / 小黑板** | conditional rule ("当...") | a small board at a gate |
| **Flag on a pole / 旗杆旗** | state signal | a colored flag |
| **Floor Plaque / 楼层牌** | floor label in a cutaway | a small plaque on each floor |
| **Banner over a page / 页眉横幅** | two-page spread page label | "旧做法" / "新做法" |

Rules: attach labels to **relationship objects** (the handoff parcel, the gate rule board, the scale crate, the floor plaque, the crossroads signpost), not to empty space. Use 3–6 short labels for simple towns; more when roles/steps/groups need them.

## G. Animal-Character Construction Kit / 角色构造件

How to build an original townsfolk. Combine one of each layer. **Never assemble a copyrighted likeness** (see `style-dna.md` Identity).

1. **Species** — pick from `role-library.md` Part 1 (cat, fox, bear, owl, mole, ...). Vary across the page.
2. **Body** — upright, rounded friendly proportions, soft watercolor body, big head. Never realistic, never uncanny.
3. **Trade outfit** — one signature garment: apron, overalls, uniform, vest, scarf, hat. **Original colors and shape** — do not copy any recognizable character's costume.
4. **Tool** — one handheld prop matching the trade (from Part 2's kit).
5. **Action pose** — mid-task (rolling, lifting, inspecting, driving), not posing at the reader.
6. **Face** — calm default, or a minimal ink-stroke expression that encodes state (effort / focus / strain / relief / dozing). See `style-dna.md` Simple Expressions.
7. **Scale tag (optional)** — a small role label on the apron or a sash if the role isn't obvious from species+outfit.

## Composing a Scene

1. Pick the **relationship** (from `collaboration-grammar.md`).
2. Pick the **mode** (from `modes.md`) — this fixes the macro layout (panorama / cutaway / two-page / close-up).
3. Pick the **buildings & streets** (this section A, B) that physically stage the relationship.
4. Pick the **roles** (from `role-library.md`) and assemble each with the **construction kit** (this section G).
5. Add **vehicles** (C) where handoff/transport is needed.
6. Add **tools & props** (D) in mid-use.
7. Add **state markers** (E) to encode status.
8. Add **signage** (F) with readable labels.
9. Keep the palette warm and the medium watercolor — see `style-dna.md`.

## Reuse Rule

Within a series, reuse the **same species+trade for the same role**, the **same shop for the same station**, the **same street for the same sequence**, the **same flag color for the same state**. This is what makes N images feel like one town rather than N unrelated paintings.
