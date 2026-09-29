# Busy Town Style DNA / 忙碌小镇风格 DNA

Use this reference before final image generation.

Busy Town is a hand-painted storybook illustration system for explaining cooperation. Its identity comes from anthropomorphic animal townsfolk working together inside a warm, dense, watercolor town.

## Chinese-First Default

When the user writes Chinese, plan and describe the image in Chinese. The default image must include readable Chinese labels on shop signs / banners / flags, not empty placeholders. For publish-critical wording, the model may use shorter labels and the final answer should note any text that may need manual overlay.

Default label rule:

- Use 3-6 short labels for simple towns.
- Use more labels when the process truly needs a multi-role, multi-step, comparison, or grouped diagram.
- Each Chinese label should usually be 2-6 characters.
- Attach labels to shop fronts, awnings, banners, vehicle sides, flags, signposts, crates, or chalkboards.
- A single readable sign strip / banner is allowed when it clarifies the takeaway; do not use dense paragraphs, tiny fake text, or empty labels as the default.
- Use blank sign containers only when the user explicitly asks for post-production overlay or editable text.

Good Chinese label containers (all hand-painted):

- shop signs above doorways (招牌)
- hanging banners / pennant strings (横幅/三角旗)
- awning edge text (篷布字)
- vehicle livery / side lettering (车身字)
- hand-lettered flags on poles (旗子)
- crate / barrel / sack stamps (木箱印章)
- chalkboard menus (小黑板)
- signposts at crossroads (路牌)

Avoid floating captions, dense fake Chinese, text-empty placeholder scenes, and any UI/HUD-style text overlays.

## Core Look

- 16:9 horizontal by default; 1:1 or 4:5 for cards/two-page spreads when asked.
- Warm cream / off-white paper background with visible paper grain.
- **Watercolor / gouache** as the medium: soft wet-on-wet washes, gentle color bleeds at edges, a faint pencil or ink under-drawing showing through, hand-mixed slightly desaturated colors. This is the tactile opposite of 3D render, flat vector, and clay.
- Hand-built imperfection: lines are not perfectly straight, colors overlap softly, brush texture is visible. Not messy doodle, not machine-clean.
- Small semantic color accents on top of the warm palette: a red flag (alert/risk), a green checkered flag (done), a golden bell (focus).
- Main palette: brick red, mustard yellow, sage green, dusty blue, terracotta, cream, warm brown wood, soft gray slate roofs. Restrained, never rainbow.
- Use one or a few lead animals; the rest of the cast is anonymous townsfolk.
- A lead animal is usually 10-20% of canvas height; townsfolk are smaller and scattered.
- The image should work inside an article column or as a standalone storybook page, not only as a poster.

## The Hand-Painted Town Rules

The image is a *town that explains*, not a cute diorama. Three things must all hold:

1. **It reads as a diagram.** A reader who has never seen a storybook should still be able to point at "the sequence", "the branch", "the gate", "the bottleneck", "the handoff" within three seconds.
2. **It reads as a town.** The same reader should also feel warmth, life, simultaneous busy-ness — shops, streets, vehicles, smoke, awnings, flags, multiple animals each doing something.
3. **The cooperation carries the meaning.** The way animals hand off, line up, branch, gate, weigh, or parallelize *is* the relationship. Arrows are a last resort and should be rare; the layout and the characters' actions do the work.

Reject if it becomes:

- a PPT flowchart with storybook texture pasted on
- equal-weight shop cards in a grid with no cooperation
- a cute animal village where nothing is being explained
- a 3D-rendered toy town
- a flat vector cartoon town
- a claymation / plasticine town
- a voxel/Minecraft town
- a pretty scene with no readable text

## Animal Character Rules

A townsfolk:

- is an anthropomorphic animal: cat, dog, rabbit, fox, bear, pig, mouse, owl, raccoon, badger, hedgehog, mole, frog, etc. (pick fresh, not only cats)
- stands upright, has rounded friendly proportions (big head, soft body), wears a trade outfit (apron, overalls, hat, scarf, uniform, vest)
- carries or operates one tool that matches the trade (baker = rolling pin, courier = parcel, inspector = clipboard, builder = trowel)
- has a calm or gently expressive face — small ink-dot or line eyes, a small mouth; **never** realistic eyes, never photoreal fur, never uncanny
- may show a simple expression that encodes its current STATE (effort, focus, strain, relief, satisfaction, worry, dozing). A calm plain face is the default.

### Simple Expressions (state, not decoration)

The animal may have a minimal hand-drawn face when it helps the reader read its STATE — effort, focus, strain, relief, satisfaction, worry, dozing, or alert. The animal's whole job is state and cooperation, so a small expression is a legitimate state-coding device, not mascot cuteness. A calm plain face is still the default when no state needs reading.

Rules for expressions:

- Draw the face as a few hand-made ink strokes: two dots or short arcs for eyes, one short stroke for the mouth — flat (neutral), small upward curve (satisfied), downward curve (strain), tiny "z" near a dozing head (idle/asleep).
- Keep it abstract and sparse. No realistic eyes with pupils, no teeth, no detailed snouts. The simplicity is exactly what avoids the uncanny valley and what keeps it from copying any specific copyrighted character.
- Prefer profile or three-quarter views, with the animal looking at its work, not staring at the reader. A face turned toward its task reads as state; a face turned flat at the camera reads as a mascot.
- One expression per animal, matched to its station's beat. Across a series, let the expression progress with the throughline (e.g. furrowed during 加工, eased at 交付).
- Expression must serve the state or relation. If removing the face changes nothing about the meaning, keep it calm and plain.

## Not 3D, Not Flat-Vector, Not Clay

This skill's medium is watercolor/gouache on paper. That single choice is what separates it from neighboring styles and is non-negotiable.

Do not use:

- 3D-rendered town / plastic / vinyl toy look
- flat geometric vector cartoon (Corporate Memphis, modern flat illustration)
- claymation / plasticine / stop-motion clay
- voxel/Minecraft cubes
- AI-glossy hyper-detailed illustration
- isometric-low-poly game art
- sticker / kawaii mascot style

The watercolor look means: visible paper grain, soft color bleeds, hand-mixed desaturated warm palette, pencil/ink under-drawing showing through, brush texture, gentle imperfection.

## Not Mascot, Not Decoration

Do not make the animals:

- cute-first
- expressive for charm rather than for state (a grin that says nothing about the work)
- waving, presenting, or smiling at the reader
- standing beside the diagram doing nothing
- a branded character set
- a generic office worker / robot / avatar

Expression and action are allowed only as state/cooperation signals (see Simple Expressions). The line between "state" and "mascot" is simple: a furrowed brow while inspecting a crate is state; a cute grin aimed at the reader is mascot.

## Cooperation As Scenes, Not Chart Icons

Busy Town carries a deep vocabulary of relationships (see `references/collaboration-grammar.md`, `references/role-library.md`, and `references/primitives.md`). That vocabulary is a list of relations to EXPRESS, not a set of chart icons to paint a storybook skin onto.

Do not flatten a relationship into a small painted chart symbol — a painted flowchart, a painted org tree, a painted funnel — sitting flat on the page. That is just a flowchart with watercolor grain.

Instead, stage the relation as a deep, living town scene:

- arrange the animals, shops, and props so their **physical placement and their cooperation IS the relation**: lined along a street for sequence, stacked in floors for layers, gathered at a crossroads for branching, paired at a checkpoint for filtering, on a seesaw for tradeoff.
- let a street, a river, a conveyor, or a procession of handing-off animals **guide the eye** through the relation.
- let the animals' **actions and expressions perform and feel** the relation.
- use real depth: foreground action, mid shops, back skyline; raised scaffold for active work, dozing corners for idle stations.

This is why the style is loved: it carries flowchart-level information density, but in a warm, busy, hand-painted world that is eye-catching and readable in one glance. A painted flowchart loses exactly that. Use the chart vocabulary to decide WHAT relation to show; use the town, the animals, the street guidance, and the state coding to decide HOW to show it.

## World-Class Quality Bar

Accept only if:

- the cooperation reads in three seconds
- the animals physically hand off, line up, branch, gate, weigh, or parallelize something
- the composition has a clear focal cooperation zone and generous busy detail around it
- labels are short and attached to shop signs, banners, flags, awnings, vehicles, or crates
- the domain feels specific, not engineering props pasted onto every article
- the medium reads clearly as hand-painted watercolor/gouache on paper
- the image feels warm, editorial, and publishable

Reject if:

- the animals are decorative
- the image looks like a PPT infographic with storybook texture
- it uses stock icons
- it has fake dense text
- it is charming but unclear
- it is accurate but visually lifeless
- it looks 3D / flat-vector / clay / voxel
