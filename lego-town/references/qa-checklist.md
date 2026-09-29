# QA Checklist / 验收清单

## Accept

- The source anchor is specific, and the idea has **buildable structure** (parts + how they connect).
- There is one reader takeaway, and the structure reads in three seconds.
- The **connection carries the relation**: stacked = dependency, in a row = sequence, walled = containment, geared = feedback, bridged = connection, seesaw = tradeoff, forked = divergence. Replacing it with a plain arrow would lose meaning.
- The build is the diagram — the bricks are load-bearing meaning, not decoration. Removing the bricks would lose the structure.
- The bricks look **real**: visible studs and tube/clutch geometry, honest brick proportions, ABS sheen, slight bevels. Not voxels, not Minecraft, not generic glossy 3D blocks, not clip-art bricks.
- The chosen **mode fits the job** (finished for a whole structure, instruction for a process/prompt, exploded for anatomy, box art for a cover) and shows its signature cues legibly.
- Minifigs are 0–3, **original**, each performing one live action; none just stands and waves.
- The domain is visible in the district, props, signage, and palette; engineering props are not pasted onto a life/learning topic.
- Labels are short, readable, and attached to printed tiles / signboards / road signs / plinths / step badges / call-out boxes — never floating, never garbled.
- State coding is disciplined: ≤ ~5 strong colors, exactly one focus accent, only the 1–2 encoders that carry the point active.
- One focal build module, generous quiet baseplate, real depth.
- It is **original brick art** — no real LEGO® set, no LEGO logo/wordmark, no licensed character or real-person minifig likeness.
- For a series: shared world / palette / minifig / label style; the build progresses image to image; a motif pays off.
- For README/showcase: at least one non-engineering build (knowledge town, life routine, research map) so the skill doesn't look software-only.
- Native label status is explicit: labels readable inside the image, intentionally omitted, or to be overlaid in post per the user's request.
- **Swap Test passes**: the build encodes THIS specific content — its real module names, real `×N` counts, real structure — and could NOT be relabeled onto an unrelated topic unchanged. It is not a default town stamped on any input.
- **Text is built/placed, not floating**: every label sits on a real carrier (printed tile / brick-built letters / studs-as-pixels / signboard / minifig placard / instruction page layer), the letterform matches the carrier, and Chinese is on tiles/signs or routed to overlay — never garbled (see `references/lettering-and-text.md`).
- **Native elements carry meaning**: where a real LEGO element already signals the idea (arrow road-plate, stop sign, striped barrier, gear, traffic light, trans-stud), it is used instead of a generic shape or drawn arrow (see `references/native-elements.md`); the element vocabulary varies across the user's images.
- **Asset routing & truth**: an asset role was chosen; text ownership respected (no stuffed headline when layout owns it); exact module names / `×N` / metrics match the contract; wrong-owner jobs were rerouted (`asset-routing-and-truth.md`, `text-strategy.md`, `layout-handoff.md`).
- **Failure pattern scan**: no hit from `failure-patterns.md` left unnamed (decorative bricks, brick-PPT, trademark drift, voxel drift, template lock, wrong owner, etc.).
- **Layout handoff** (when placed in another artifact): ratio/safe margin/caption-outside noted; focal module survives crop.

## Regenerate

- The idea has no structure (a single mood, one quote, one number) — it should have been a card/cover, not a build.
- The bricks are decorative; the meaning would survive without them.
- The connection collapses into a generic arrow over a brick pile; sequence, causality, and dependency look identical.
- The build is a flat brick-textured chart icon (a flat brick pyramid/funnel/venn/org-tree) instead of a real 3D assembly.
- It looks like Minecraft, a voxel field, a generic 3D block render, or a PPT brick-icon grid.
- It's a pretty cityscape that explains nothing — no focal module, no routes, no labels.
- A minifig only stands, waves, points vaguely, or presents; or there's a crowd of characters posing.
- The minifig has a **trademarked smiley, a licensed face, a brand print, or a real-person likeness**; or it's a blocky Minecraft figure / generic mannequin.
- It reproduces a **real LEGO® set, the LEGO logo/wordmark, or a licensed character/theme**.
- The mode fights the job (a process shown as a static finished build; an anatomy hidden inside box art).
- Labels float in empty space, are missing/blank by default, too tiny, unreadable, garbled, or meaningless filler.
- Two modules fight for the focus accent; too many encoders read as a dashboard.
- The output is charming but unclear, or accurate but visually lifeless.
- **Swap Test fails**: the build is a generic default town with placeholder labels that would fit any topic — a template, not THIS content.
- Text floats as a flat caption, uses a generic system font ignoring its carrier, or Chinese is garbled / brick-built into stroke-mush.
- The image model invented **extra unrequested Chinese** (a caption strip, signboard sub-text) that garbles — warning, not always fatal: keep it if every rendered glyph is correct and on-meaning; regenerate (or blank-for-overlay) if any invented text is broken or distracting.
- A generic shape or drawn arrow stands in where a real native element exists (a red cube for "stop", a painted arrow for "flow").
- Every build reduces to the same roads-and-gray-buildings vocabulary regardless of topic.
- Every showcase image is a software/engineering build by habit, making the skill look narrower than it is.

## Repair Moves

If the connection is just an arrow (the most common failure):
```text
Regenerate so the PHYSICAL CONNECTION carries the relation. Stack modules on a foundation for dependency; lay them in a row on a baseplate road for sequence; wall them in a plot for containment; mesh gears for feedback; bridge with a road for connection; balance on a seesaw for tradeoff; fork the road at a switch for divergence. Remove drawn arrows; let the bricks show how things relate.
```

If it looks like Minecraft / a voxel pile:
```text
Regenerate with REAL brick parts: visible studs and tube/clutch geometry, honest brick proportions (1×2, 2×4 bricks, plates, tiles, slopes, baseplate), ABS plastic sheen and slight bevels. No uniform cubes, no voxels, no generic 3D blocks.
```

If a minifig is decorative or branded:
```text
Regenerate the minifig as an ORIGINAL role-actor performing one live action (a builder mid-snap, an inspector stamping at a gate, a courier on a road). Original printed torso + role accessory only; no trademarked smiley, no licensed face, no brand print. Or remove the minifig and let the build tell it.
```

If it explains nothing (pretty city, no argument):
```text
Regenerate around ONE focal build module that embodies the named relationship. Quiet the rest of the baseplate, add a clear route/connection, and attach short readable labels to printed tiles or signboards. The reader must see the parts and how they connect in three seconds.
```

If a process is shown statically:
```text
Regenerate in Instruction-Sheet mode: numbered step panels showing the build after each step, the newly-added parts hovering on drop-lines, a parts call-out box (e.g. 2×4 砖 ×3), and a small finished preview. Show assembly ORDER, not just the result.
```

If it reproduces a real set / logo / licensed character:
```text
Regenerate as an ORIGINAL build conveying the same idea. Remove the LEGO logo/wordmark, any real set, and any licensed character. Use an original product name in Box-Art mode.
```

If it feels like a template (the "every image looks the same" failure):
```text
Regenerate against the Swap Test. Put THIS content's real names on the tiles, the real count in the ×N call-out, and the real structure in the connection geometry. Pick the native elements the domain actually implies (signage for routing, gears for feedback, screens for data), rotate the text carrier and camera per `references/variation-engine.md`, and confirm the build could NOT be relabeled onto a different topic unchanged.
```

If exact truth is wrong (invented modules, wrong ×N, fake metrics):
```text
Reject. Rewrite the exact-text / exact-data block from the source, regenerate, or blank tiles for overlay. Do not ship invented structure.
```

If the job belongs to another skill:
```text
Reroute plainly: cooperation cast → busy-town; one conceptual action → paper-operators; strict chart → native chart; quote/cover → card skills.
```
