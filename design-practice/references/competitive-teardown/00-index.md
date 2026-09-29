---
type: reference
created: 2026-06-27
priority: P0
---

# Competitive Doctrine — why the good ones have 质感, and where our moat is

> Synthesis of three teardowns: `01-lovart-makedesign.md` (engineered design agents), `02-open-source-builders.md` (v0/Lovable/Bolt/Onlook/Make Real — inspectable system prompts), and Claude's own `frontend-design` skill (read first-hand). One conclusion, one moat.

## The one conclusion
**质感 is not "trying harder" — it is the elimination of choices that produce the median.** Every high-quality AI design product wins the same way: it *constrains generation* so slop can't occur, *plans before generating*, *commits to one direction*, *injects real assets*, and *loops on real rendered output*. Generic generators do none of these and regress to the mean (purple gradient, centered hero, 3 cards, Inter, lorem).

## The 6 mechanism families (what to bake in)

| # | Mechanism | Who proves it | Our home |
|---|---|---|---|
| 1 | **Plan before pixels** — decompose into a shown plan (job/audience/sections/hierarchy/assets) before generating | Lovart MCoT | Stage 0 judgment + Stage 1 drafts |
| 2 | **Direction gate + commit** — generate 2–3 style directions, pick one, lock it as a downstream constraint; never mix | Lovart moodboard · Claude "pick a direction and commit" | Intent Brief + new moodboard step |
| 3 | **Token contract + numeric bounds** — all color/space/type/radius/motion from a defined set; 3–5 colors, ≤2 families, body ≥14px | v0, Lovable, tweakcn | `tokens/00-token-synthesis.md` |
| 4 | **Named negative constraints** — forbid the tells by name (gradient blobs, emoji-icons, centered-max-width app frame, lorem, default purple) | v0, Make Real, Claude anti-patterns | rubric dim 10 + a NEVER list |
| 5 | **Real assets, real content** — real logos (SVGL), real icons (Lucide), generated images, real copy + hex palettes + font pairings; text stays editable text | everyone; Lovart vector layer | web-craft + generation prompt |
| 6 | **Render → critique → refine loop** — run it, look at it, score it, fix the weakest, repeat | Bolt WebContainer, Make Real, Onlook | **Stage 3 harness** |

## Our moat — what NONE of them have
The teardown's most important finding: **not one competitor documents an explicit, rubric-scored critique loop.** They curate, they constrain, they iterate conversationally — but the "critic" is a human eyeballing, or nothing. They also have **no transferable design *judgment* layer** (task-field, complexity conservation, true-vs-empty simple, object-state-permission) — that's tacit in their teams, absent from their tools.

So this skill's defensible edge is the **stack none of them assemble in one place**:

1. **A judgment layer** (from 《设计的实践》27 chapters) — the *why* before the *what*. Competitors have skin discipline; we add skeleton judgment.
2. **Real-extracted engineering tokens** from 16 shipped products — ground-truth numbers, not a model's guess.
3. **An explicit 10-dimension rubric** that scores the *rendered* page and names the single weakest element — a measurable quality bar, not vibes.
4. **A closed render→critique→refine loop** that runs that rubric against real screenshots until the bar is met — the thing every competitor approximates and none formalizes.

Plan + commit + constrain + real assets are **table stakes we adopt**. Judgment + measured tokens + rubric-scored visual loop are **the moat we own**. That combination is what makes the output "几乎可以直接交付" — and what makes the engine itself sellable.

## Adopt-list delta (added to the build because of this teardown)
- A **moodboard / direction-gate** step (2–3 directions → commit) — new, before Stage 1.
- A **NEVER list** of named AI-smell prohibitions — injected into every generation prompt.
- A **persistent brand/direction object** cascaded into every render pass.
- **Asset discipline**: SVGL logos + Lucide icons + real copy; no placeholder boxes.
- Keep Stage 3 as the formal, rubric-scored version of the loop they only approximate.
