# Variation Engine / 变化引擎

Keep the **semantic invariants** fixed and let the **surface axes** vary. Every generation should rotate surface elements so two runs of the same request look visibly different yet read as the same cooperation. This is what answers "每次出来的图都一样 / give me a different one."

## Semantic Invariants (DO NOT change)

These carry the meaning. If they change, the image is wrong, not just different.

- the **relationship** (handoff, sequence, dependency, contrast, ...)
- the **roles** and their cooperation structure (who hands off to whom, how many stations, where the branch is)
- the **focal cooperation zone** (the one place the eye lands first)
- the **label meanings** (what each shop / station / flag / parcel *means*)
- the **state coding semantics** (smoke = running, red flag = alert, etc.)
- the **lead role's trade** (the Baker is always a Baker)
- the **mode** (panorama / cutaway / two-page / close-up) — unless the user explicitly asks for a different mode

## Surface Axes (DO vary)

These carry no meaning; rotating them produces visible variety without corrupting the cooperation.

| Axis | Range |
| --- | --- |
| **Camera** | top-down, shallow high-angle, eye-level, slight tilt; rotate 90° between panorama layouts |
| **Town layout** | the same shops arranged on a different street pattern (grid vs radial vs riverside); mirror left-right |
| **Focus accent** | which shop wears the single gold bell / gold flag this run (keep it on the focal station, but pick a different accent object) |
| **Lead animal species** | the Baker can be a Cat this run, a Bear next run, a Pig the next — as long as the trade (Baker) is invariant |
| **Anonymous townsfolk cast** | swap which background animals appear (a Hedgehog here, a Goose there) |
| **Weather & time of day** | dawn / morning / noon / dusk; clear / cloudy / light snow; smoke reads differently in each |
| **Season** | spring green / summer full / autumn ochre / winter bare — shifts the palette without changing meaning |
| **Awning & flag patterns** | stripes / checks / solids — purely decorative variety |
| **Vehicle mix** | a cart this run, a bicycle next, a van after — the handoff is the same, the vehicle differs |
| **Signage style** | chalkboard / carved wood / painted cloth — same label text, different container |
| **Crop & aspect** | 16:9 wide vs 4:5 tall vs 1:1 (if the user asks for a card) |

## The Swap Test

The test that ties variation to precision. **If the image could move onto a different article on the same topic without anyone noticing, it has failed.**

A precise image is locked to its document by the **content-specific particulars** (see `intent-reading.md`): the real role names, the real step count, the real bottleneck, the real example. Vary the surface all you like, but never dilute the particulars.

Run the Swap Test on every image:

```text
swap test:
- could this image illustrate a different article on the same topic? yes/no
- if yes, what content-specific particular is missing that would lock it to THIS document?
- action: add the missing particular (a real label, a real count, a real flag state) and regenerate
```

## How to Vary (the workflow)

When the user asks for **one** image: pick surface axes that fit the source's tone (a morning panorama for a "launch" article; a dusk panorama for a "postmortem"). Don't randomize for the sake of it.

When the user asks for **variations / 换一版 / 再来一张不一样的 / give me another**:

1. Keep every semantic invariant fixed.
2. Rotate **at least three** surface axes visibly:
   - camera (e.g. top-down → shallow high-angle)
   - town layout (e.g. riverside → grid)
   - lead animal species (e.g. Cat Baker → Bear Baker)
3. Optionally rotate weather/season for a strong visual difference.
4. Confirm the cooperation still reads identically — same handoffs, same branch, same gate, same focal zone.
5. Report which axes you rotated.

When the user asks for a **series**: see `series-and-chaining.md` — variation across a series follows a *throughline*, not random rotation.

## Anti-Patterns

- **Rotating a semantic invariant** (e.g. swapping the relationship from sequence to parallel) — that's a different image, not a variation.
- **Random rotation that breaks the cooperation** (e.g. the focal zone gets lost in a new layout) — re-tune the layout so the focal zone stays focal.
- **Identical surface** (same camera, same layout, same species) labeled as "a different version" — that's a duplicate.
- **Over-rotating** (every axis changed) so the image no longer reads as the same town — keep at least 2–3 surface axes stable so the family resemblance holds.

## Variation Budget

A good variation rotates **3–4 surface axes** and holds the rest. Rotating all axes produces a different town; rotating none produces a duplicate. Find the middle.

Example rotation set for "give me another version":
- camera: top-down → high-angle from the south
- layout: riverside main street → grid around a central square
- lead species: Cat Baker → Bear Baker
- weather: clear morning → soft overcast noon
- (held: relationship, roles, cooperation, focal zone, labels, mode)

The result looks visibly different but reads as the same cooperation.
