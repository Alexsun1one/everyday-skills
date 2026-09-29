---
type: reference
created: 2026-06-27
source: teardown of v0, Lovable, Bolt.new, Onlook, Subframe, Magic Patterns, tldraw Make Real, 21st.dev, tweakcn, Stitch — incl. leaked/published system prompts
priority: P0
---

# Why the good AI builders ship better 质感 — the 5 portable levers

> Reverse-engineered from the tools whose output is visibly less AI-slop, focusing on the ones whose code/system-prompts are inspectable. The finding: they don't have better taste than the median — **they constrain generation so the median can't happen.** Every lever below is portable into this skill.

## "OpenDesign" disambiguation
Name collision, not one product. The prominent referent is **Open Design** ([open-design.ai](https://open-design.ai/), [github nexu-io/open-design](https://github.com/nexu-io/open-design)) — an open-source, local-first, BYOK **Claude-Design alternative** that orchestrates 17+ coding CLIs and ships a "Skills" + "Design Systems" library with sandboxed preview. As a category exemplar it stands for the **open, inspectable, design-system-grounded** wing — the wing worth mining.

## Lever A — Ground in a real component/design system; never free-style CSS
The single most consistent quality move. Lovable's prompt: *"The design system is everything… never write custom styles in components… USE SEMANTIC TOKENS… DO NOT use direct colors like text-white, text-black, bg-white"* — themed via `index.css` + `tailwind.config.ts`, shadcn customized **through variants, not class hacks** ([Lovable Agent Prompt](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools/blob/main/Lovable/Agent%20Prompt.txt)). The stack converges on **shadcn/ui + Tailwind + Radix** (accessible behavior + token theming for free). Subframe emits **deterministic** code from a real 47-component system — "what is designed is exactly what you get." AI-smell comes from ad-hoc CSS; the fix is constraining generation to curated primitives.

## Lever B — Bound the palette & type numerically, with hard rules
v0 encodes restraint as numerics: *"ALWAYS use exactly 3-5 colors total… NEVER exceed 5… ALWAYS limit to maximum 2 font families… NEVER use fonts smaller than 14px… NEVER use purple/violet prominently unless asked"* ([v0 system prompt](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools)). The most copyable artifact in the space: short bounded scales beat open-ended "make it beautiful." **tweakcn** externalizes the same idea — generates the full shadcn token set (OKLCH colors, radius, shadow, type) with curated presets, so a coherent palette is a *starting point* not a per-element decision ([tweakcn](https://tweakcn.com/)).

## Lever C — Restraint as explicit negative constraints ("don't do X")
Quality correlates with what the prompts FORBID. v0: *"NEVER generate abstract shapes like gradient circles, blurry squares, or decorative blobs as filler… NEVER use emojis as icons."* Make Real bans the AI frame: *"DO NOT wrap the entire app in a centered container with max-width and margins… the `<body>` tag IS the app, not a container holding the app"* ([make-real prompt.ts](https://github.com/tldraw/make-real/blob/main/app/prompt.ts)). Lovable forbids placeholder images & dark-mode toggles. **Pattern: enumerate the median AI-smell behaviors and prohibit them by name.**

## Lever D — Real content & assets, never lorem
v0 references images by local path + demands alt text; Lovable *"Do not let placeholder images in your design, you generate them."* 21st.dev's Magic ships **SVGL** brand logos + Lucide icons; Magic Patterns lets you reference your own components (`@Library/Button`) so output pulls real product UI. Real copy + real logos + real icons defeat the "skeleton demo" look.

## Lever E — Render → preview → self-heal loop (the loop we're building)
The higher-quality tools close a loop instead of one-shotting:
- **Make Real**: feeds the model the *previous result's HTML alongside the new annotated screenshot* — prior code is source of truth, the drawing is "the NEW changes" ([tldraw.dev](https://tldraw.dev/blog/make-real-the-story-so-far)).
- **Onlook**: instruments source so every DOM element maps to its code location; edits flow iframe↔code ([onlook-dev/onlook](https://github.com/onlook-dev/onlook)).
- **Bolt.new**: runs the app in a **WebContainer** so the model gets real runtime/errors to react to.

Execute → observe → diff → fix is what separates "plausible screenshot" from "actually works and refines." **This is exactly our Stage 3.**

## Tool → #1 quality lever
| Tool | #1 lever |
|---|---|
| v0 | hard numeric constraints (3–5 colors, ≤2 fonts, no purple) |
| Lovable | "design system is everything" — semantic tokens, zero ad-hoc styles |
| Bolt.new | WebContainer live-execution → real error feedback loop |
| Onlook | DOM↔source mapping for element-level direct manipulation |
| Subframe | deterministic codegen from a real component system |
| Magic Patterns | import *your* design system so output matches real product |
| Make Real | previous-HTML-as-source-of-truth + annotation self-heal |
| 21st.dev Magic | curated pre-tested components + SVGL real logos via MCP |
| tweakcn | one-click coherent shadcn token set (OKLCH/radius/shadow/type) |

## Portable into THIS skill (the build list)
1. **Ship a token contract, not freestyle CSS** — all color/space/radius/shadow/type from a defined set; forbid inline literals. → pairs with `tokens/00-token-synthesis.md`.
2. **Bound palette & type numerically** — 3–5 colors, 1 primary + neutrals, ≤2 families, body ≥14px, line-height 1.4–1.6, no prominent purple unless asked.
3. **Carry an always-injected rules/`DESIGN.md`** so aesthetics are persistent context, not per-prompt.
4. **Maintain a named negative-constraint list** — gradient blobs, emoji-as-icons, centered-max-width app frame, hand-rolled illustration SVGs, lorem. (→ feeds the rubric's dim 10.)
5. **Default to a curated component library** (shadcn/Radix), customize via variants — a11y + good defaults free.
6. **Inject real assets** — SVGL logos, Lucide icons, real/generated images by path with alt; never placeholder boxes.
7. **Run render→screenshot→inspect→fix** — our Stage 3 harness.
8. **Prior code = source of truth on iteration** — feed previous code + targeted diff, don't regenerate wholesale.
9. **Offer curated theme presets** (tweakcn-style) that bias away from the median.
10. **Enforce contrast/pairing invariants** — override a bg → override the fg; always set a base background.
11. **Element-level diff-based refinement** backed by source mapping.
12. **Prefer deterministic emission where possible** — resolve decisions in a constrained system, then emit code, to cut LLM variance.
