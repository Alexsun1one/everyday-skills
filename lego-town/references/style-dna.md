# LEGO Town Style DNA / 乐高小镇风格 DNA

Read this before final image generation.

LEGO Town is a tactile brick-build illustration system for explaining structure. Its identity comes from authentic interlocking studded bricks, assembled so the build itself *is* the diagram. The quality moat is twofold: the bricks look real (ABS plastic, studs, tubes, honest proportions) **and** the way they connect carries the meaning.

## Chinese-First Default

When the user writes Chinese, plan and describe the image in Chinese, and render readable Chinese labels — never empty placeholders or fake dense text. Labels live as **printed tiles, brick-built letters, signboards, route signs, or instruction call-out numbers**, attached to objects.

Default label rule:

- 3–6 short labels for a simple build; more when steps, modules, contrasts, or groups need them.
- Each Chinese label is usually 2–6 characters; an instruction call-out can be `2×4 砖 ×3`-style.
- Attach labels to tiles, signs, baseplate roads, plinths, step panels, or a printed brick.
- One readable sign strip is allowed when it sharpens the takeaway; no dense paragraphs, no tiny fake text.
- Use blank label zones only when the user explicitly asks for post-production overlay or editable text.
- For exact/critical wording (multi-line, lists, legal), prefer the **overlay path**: render empty printed tiles/signs and set the text in an editor. Let the model render text only for one very short hero line where a wrong glyph survives.

Good label containers: a printed 1×2 / 2×2 **tile**, a **signboard** on two stud-posts, **brick-built letters**, a **road sign**, a **plinth plaque**, an **instruction-step number** in a circle, a **parts call-out box**.

Avoid: floating captions, melted/doubled glyphs, dense fake Chinese, text-empty placeholder scenes.

## Core Look

- 16:9 horizontal by default (doc/article body). 1:1 or 4:5 for cards/box art when asked.
- **Material**: real ABS plastic — soft glossy specular highlight, slight edge bevel, visible **studs** on top and **tube/clutch** geometry where it reads; honest brick proportions (a 1×1 is a cube-ish unit, studs are cylinders, minifig is the classic silhouette). Tiny mold-line realism is welcome; perfect chrome is not.
- **Light**: clean studio product photography — soft key light, gentle fill, a seamless paper sweep or a subtle baseplate ground, soft contact shadows. In Instruction-Sheet mode, switch to a clean flat vector/booklet render instead.
- **Palette**: authentic brick colors — bright red, bright yellow, bright blue, bright green, orange; warm tan and dark tan; light bluish gray, dark bluish gray, white, black; and **transparent** elements (clear, trans-light-blue, trans-neon-green, trans-red) used *semantically*, not as glitter. Keep ≤ ~5 strong colors active; let gray/tan/white carry the neutral mass.
- One focal build module; generous quiet baseplate; real depth (foreground build, mid action, back skyline of simpler bricks).
- The build is the hero. Minifigs are 0–3 and smaller than the build.
- The image should work inside a doc column or a slide, not only as a poster.

## The Build Is The Diagram (not bricks pasted on a chart)

LEGO Town carries a deep vocabulary of relationships (see `connection-grammar.md`) and elements (`primitives.md`). That vocabulary is a list of relations to **build**, not a set of chart icons to brick-texture.

Do **not** flatten a relationship into a brick-textured chart symbol — a flat brick pyramid, a brick funnel, a brick venn, a brick org-tree — lying flat on the page. A reference board of brick-ified icons is fine as a catalog; as an explainer image it is just a chart with plastic grain.

Instead, **stage the relation as a real 3D build** where the physical assembly carries the relation:

- arrange modules so their placement *is* the relation: stacked (dependency), in a row on a baseplate (sequence), nested in a walled plot (containment), meshed by gears (feedback), bridged by a road (connection), balanced on a seesaw (tradeoff).
- let a baseplate **road / rail / conveyor** guide the eye through a process.
- let a **minifig** perform the live action: building, inspecting, carrying, gating.
- use real depth: raised modules for what's active, recessed/built-down for what's done, an empty studded plate for what's not built yet.

This is why the style lands: it carries chart-level information density inside a tangible toy world that is eye-catching, uncrowded, and readable in one glance. Use the relationship vocabulary to decide **what** to show; use the bricks, the baseplate routes, the connection geometry, and the minifig's action to decide **how**.

## Reject If It Becomes

- a Minecraft / voxel cube field (uniform cubes, no studs, no real brick parts)
- a generic glossy 3D-render of blocks with no clutch/stud honesty
- a PPT icon grid or equal-weight dashboard of brick cards
- a busy brick city with no visual argument (a pretty cityscape that explains nothing)
- a flat chart with brick texture pasted on
- a poster with brick decoration but no readable structure or labels
- a reproduction of a real LEGO® set, the LEGO logo, or a licensed character

## Minifig Rules (original role-actors, not a cast)

The minifig:

- uses the **classic minifig silhouette** — cylindrical head, trapezoidal torso, C-curve legs, claw hands — rendered in ABS plastic.
- is **original**: defined by **role accessories** (hard hat, clipboard, wrench, satchel, mayor's chain, lab goggles) and a simple **printed torso**, not by being a named or licensed character.
- carries one role tool that matches the domain and performs one action (build, inspect, carry, gate, present-a-sign).
- is secondary to the build but, when present, essential to the *action* (it shows work happening, ownership, scale, or POV).
- may have a **simple original expression** when it encodes state — calm dots-and-line by default; angled brows for effort/focus; a small frown near a risk-coral part. Keep it abstract and original; never copy a trademarked smiley print or a licensed face.

Minifig count: 0 when the build alone tells it; 1 for an actor; 2 for a handoff/comparison/negotiation; 3 max. Never a crowd of characters posing.

### Minifig Test (state, not decoration)

A minifig earns its place only if removing it loses *agency, role, scale, or POV*:

- a builder **mid-assembly** (snapping a brick on) → the work is in progress, not finished.
- an inspector **at a gate** with a clipboard → a check is happening.
- a courier **on the road** with a parcel → a handoff/route.
- a mayor **on a plinth** → ownership of a module.

If the minifig only stands beside a finished build and waves at the camera, it is a mascot — cut it.

## World-Class Quality Bar

Accept only if:

- the structure reads in three seconds: you can see the parts and how they connect
- the bricks are real (studs, tubes, honest proportions, ABS sheen), not voxels or generic blocks
- the connection is specific: stacked/row/walled/geared/bridged — replacing it with a plain arrow would lose meaning
- there is one focal build module and generous quiet baseplate
- labels are short, readable, and on tiles/signs/call-outs
- the domain is specific (the district, props, signage fit the topic)
- it is **original** brick art — no trademarked set, logo, or licensed character
- it feels like a real, photographable build — tactile, premium, publishable

Reject if:

- the bricks are decorative and the meaning would survive without them
- it looks like Minecraft, a voxel render, or a PPT brick-icon grid
- it's a pretty cityscape that explains nothing
- it has fake dense text or garbled glyphs
- it reproduces a real set / the LEGO logo / a licensed character
- it is charming but unclear, or accurate but visually lifeless
