# QA Checklist / 验收清单

Run every generated image through this checklist. Regenerate or repair anything that fails. QA is not optional polish — it is what separates a publish-grade illustration from a cute doodle.

## The Three-Second Read

The first test. Show the image to someone (or imagine showing it) for three seconds.

- [ ] Can they point at the **cooperation** (the handoff, the sequence, the branch, the gate)?
- [ ] Can they name **3+ roles** and what each is doing?
- [ ] Does the image feel **warm, busy, alive** — like a town, not a chart?

If any answer is no, regenerate. The three-second read is the harshest test; everything below is detail.

## Cooperation QA

- [ ] The **relationship** was named before the animals were chosen.
- [ ] The animals **physically perform** the relationship (hand off / line up / branch / gate / weigh / wait / transform / parallelize) — they are not standing beside it.
- [ ] The cooperation is readable from the **layout and actions**, not only from labels or arrows.
- [ ] Direction, condition, and state are **visible in the scene**, not only in text.
- [ ] There is **one focal cooperation zone**; secondary relations are coded quietly and don't compete.
- [ ] If the relationship is "simultaneous busy," there is still a focal zone — not undifferentiated clutter.

## Mode QA

- [ ] The chosen **mode** fits the article's goal (panorama for breadth / cutaway for depth / two-page for comparison / close-up for one role).
- [ ] If **Panorama**: top-down, encyclopedic, multiple busy zones, one focal square, smoke from chimneys, no perspective vanishing point.
- [ ] If **Cutaway**: front wall opened, each floor labeled, **physical connections between floors** (ladder / chute / pipe / dumbwaiter), visible interior detail.
- [ ] If **Two-Page Spread**: same town drawn twice, one delta, shared spine across the gutter, banner over each page.
- [ ] If **Close-up**: one animal mid-action, labeled tool kit around it, simplified workshop background.

## Style QA (the medium is non-negotiable)

- [ ] Reads clearly as **hand-painted watercolor / gouache on paper**: paper grain, soft washes, color bleeds, pencil/ink under-drawing showing through.
- [ ] **NOT** 3D-rendered, NOT flat vector cartoon, NOT clay/plasticine, NOT voxel/Minecraft, NOT AI-glossy.
- [ ] Warm muted palette (brick red, mustard, sage, dusty blue, terracotta, cream, warm brown) with at most 1–2 semantic accents.
- [ ] Hand-lettered signs; **no floating UI text, no garbled glyphs, no fake dense text**.

## Character QA

- [ ] All animals are **original** — no copyrighted likeness (no Huckle, Sally, Lowly Worm, Mr. Frumble, Bananas Gorilla, Sergeant Murphy, etc., and no copied outfits/likenesses).
- [ ] **Species vary** across the page (not all cats); species match trade nature (Owl = oversight, Mole = hidden, Beaver = builder).
- [ ] Each animal has an **original trade outfit** (apron/hat/scarf color and shape are invented, not copied).
- [ ] Faces are **calm or minimal hand-drawn expression** encoding state — not realistic, not uncanny, not mascot-cute.
- [ ] Animals are **mid-action**, not posing at the reader; no waving/grinning at the camera.
- [ ] The **Lead-Animal Test** passes: each named lead adds agency/role/scale/POV; decorative leads cut.

## Label QA

- [ ] **3–6 short labels** for a simple town; more only when roles/steps/groups need them.
- [ ] Labels are attached to **relationship objects** (shop signs, handoff parcels, gate rule boards, scale crates, floor plaques, crossroads signposts, flags).
- [ ] Chinese labels are 2–6 chars each, hand-lettered, readable (or noted as needing post-overlay).
- [ ] **No empty placeholder scene** unless the user explicitly asked for editable text in post.
- [ ] The image is not text-empty and not text-cluttered.

## State-Coding QA

- [ ] The article's key state (running/idle, pass/fail, done/in-progress, healthy/risk) is **readable from the painting alone**.
- [ ] State uses **storybook-physical channels** (smoke, flag, expression, gate posture, stamp) — not UI overlays (badges, bars, dials, KPI tiles).
- [ ] **Encoding budget respected**: 1–2 channels carry precision; the rest stay neutral.
- [ ] No rainbow color-coding; one accent color is enough.

## Intent & Precision QA

- [ ] The **Intent Brief** was filled before drawing; goal picked the mode, audience tuned density, tone tuned state coding.
- [ ] **Content-specific particulars** from this document (real role names, real step count, the actual bottleneck/tradeoff/example) appear in the image.
- [ ] **The Swap Test**: the image could NOT be moved to a different article on the same topic without someone noticing. If it could, add a missing particular and regenerate.

## Asset Routing & Truth QA

- [ ] An **asset role** was chosen (article figure / process town / cutaway / comparison / close-up / data status / reference-informed / center illustration).
- [ ] **Text ownership** is respected: no headline/paragraph stuffed into the town when an outer layout should own it (`text-strategy.md`, `layout-handoff.md`).
- [ ] **Exact truth** holds: no invented stations, roles, metrics, dates, or labels; exact-text / exact-data blocks in the prompt were honored.
- [ ] If metrics were involved, the **data contract** matches what appears (`data-status-towns.md`).
- [ ] If a real industry/place was claimed, **reference cues** are recognizable and not hallucinated (`reference-informed-towns.md`).
- [ ] If Busy Town was the wrong owner, the job was **rerouted** (chart / lego-town / paper-operators / card / slide) instead of forced.

## Layout Handoff QA

- [ ] Final container and ratio fit the placement (16:9 article, safe margins for social, text-safe zones for slides).
- [ ] Focal cooperation zone sits in the central ~70%; edge labels won't die in a crop.
- [ ] Caption / title / CTA that belong outside are noted in the handoff, not painted into the town.
- [ ] Image is usable at the intended display size (including phone/thumbnail if relevant).

## Domain QA

- [ ] The town's **district, shops, vehicles, props, signage** come from the source's domain — not server-rack clichés pasted onto every topic.
- [ ] For life / food / art / education topics, the palette and town are **warm and domain-specific**, not engineering gray.
- [ ] At least one non-engineering domain in a README/showcase set.

## IP Red-Line QA

- [ ] No reproduction of any **named Scarry character** or its likeness/outfit.
- [ ] No reproduction of any **specific scene or spread** from his books.
- [ ] No **publisher logo, series logo, or trademark** (Golden Books, Busy World, etc.).
- [ ] If the user asked for a copyrighted character/scene, an **original equivalent** was painted and the swap was noted.

## Failure Pattern Scan

Run `references/failure-patterns.md`. Name any hit; do not call the image "mostly fine."

- [ ] Decorative animals
- [ ] Watercolor-textured flowchart
- [ ] Atmosphere instead of cooperation
- [ ] Fake data beauty
- [ ] Reference hallucination / copyright drift
- [ ] Text overload
- [ ] Template lock
- [ ] Wrong owner
- [ ] Medium drift
- [ ] Cutaway-as-orgchart / two-page delta loss / close-up-as-portrait

## Regenerate If

- The animals are decorative (removing them doesn't change the meaning).
- The cooperation collapses into a generic arrow.
- The town looks 3D / flat-vector / clay / voxel.
- Labels are missing, garbled, floating, or invent stations/roles.
- Exact metrics or counts are wrong.
- It reproduces a copyrighted character or scene.
- The cooperation is unclear after a three-second look.
- The image fails the Swap Test.
- The state coding uses UI overlays instead of storybook channels.
- Every shop has every state channel maxed out (over-coded clutter).
- Text ownership is wrong (title stuffed in; or town text-empty when labels were required).
- The image is charming but unclear, or accurate but lifeless.

## Repair vs Regenerate vs Reroute

**Repair** with a targeted edit (see `prompt-template.md` image-edit template):
- a wrong label → edit the sign text.
- a missing smoke plume → add smoke to one chimney.
- a wrong flag color → swap the flag.

**Regenerate** from scratch when:
- the cooperation itself is wrong.
- the medium drifted (3D / flat-vector).
- a copyrighted character appeared.
- exact truth is wrong in multiple places.
- the composition is fundamentally off.

**Reroute** when:
- the job is a strict chart, full social card, structural assembly, single-operator concept, logo, or editable diagram — say the better owner plainly.

## Final Sign-Off

An image ships only when:
- the three-second read passes,
- the cooperation, mode, style, character, label, state, intent, asset-routing, truth, layout, domain, IP, and failure-pattern checks all pass,
- any label text that may be blurred is noted for post-overlay,
- and public/reusable assets have a prompt record (`prompt-records.md`).

Do not call an image "done" until it has passed this checklist. A charming-but-unclear image is a failed image.
