---
type: reference
created: 2026-06-27
source: teardown of Lovart (lovart.ai) + make.design — public sites, method posts, hands-on reviews
priority: P1
---

# Lovart & make.design — why their output reads "designed, not slop"

Two asymmetric products, two different mechanisms for the same result.

## Lovart — engineered AI design *agent*
"World's first AI design agent" (by LiblibAI team). Turns one prompt into cohesive, **editable** assets on an infinite canvas (ChatCanvas). Its quality comes from architecture, not luck:

- **MCoT (Mind Chain of Thought)**: a reasoning layer that translates natural language into *systemic design logic* — **decomposes the brief into a structured plan, picks a tool per sub-task, enforces consistency** before generating. It "thinks out loud," asks clarifying questions, generates **mood boards for selection**, *then* executes. This is the **plan → moodboard → generate → refine** loop of a creative director — exactly what one-shot generators skip. ([Inside MCoT](https://www.lovart.ai/blog/inside-mcot-engine-ai-design-reasoning))
- **Multi-model routing**: routes per sub-task across Nano Banana Pro, Seedream, Flux, **Recraft V3 / Ideogram (chosen specifically for legible text + vector/brand)**, GPT-Image, plus Veo/Sora/Kling for video. Right model for logos vs photoreal vs vector vs UI — not one model for everything. ([model list](https://www.lovart.ai/features/all-in-one-ai-models))
- **Text stays real text**: typography on a distinct vector layer governed by kerning/leading; images convertible to true SVG. No baked-pixel gibberish.
- **Brand Consistency Engine**: an initial brand analysis is "permanently anchored" and cascaded across every deliverable; dropped brand assets are internalized.
- **Region-level refine**: Talk · Tab · Tune — click anywhere on canvas for localized feedback; layers, masks, **inpaint/outpaint** → you re-roll a *patch*, not the whole composition. Exports PNG/JPG/SVG/PSD/MP4 for human last-mile polish.
- **Localized taste libraries** (a Chinese-aesthetic "Xingliu" agent) — taste is plural, not one global median.

## make.design — opinionated thin layer over frontier models
Indie/solo product (no disclosed team or model stack). It avoids slop without an agent loop by **pre-structuring the output**: "hands you a complete, *structured* layout — hero, sections, CTA — from one sentence," with "smart visual hierarchy… layouts that guide people to the next click," "made to convert, not just look nice." The discipline lives in **a strong art-directed scaffold + conversion heuristics + house style baked into the system prompt**, plus brand import (colors/assets/tone) so output "feels like it belongs to you."

## The contrast is the lesson
Lovart = quality via **agentic plan + moodboard gate + model routing + region refine + brand object**. make.design = quality via **opinionated scaffold + house style + conversion heuristics**. Neither documents an automated *critique-scoring* loop — that's the gap our Stage 3 rubric fills, and the edge we can hold.

## Portable into THIS skill
1. **Plan before pixels** — decompose into a shown plan (objective/audience/sections/hierarchy/asset list); confirm before generating. (MCoT)
2. **Moodboard gate** — generate 2–3 *style directions* (palette+type+texture) to pick from; lock the choice as a downstream constraint.
3. **Structured scaffold, never blank/median** — force hero→sections→CTA with deliberate hierarchy + conversion intent. (make.design)
4. **Bake an opinionated house style + conversion heuristics** so the default is "considered," not the purple-gradient mean.
5. **Real assets** — actual headlines, palettes-with-hex, font *pairings*; never lorem.
6. **Text stays editable text** on its own layer; route text-in-image to a text-strong model to avoid gibberish.
7. **Persistent brand object** (logo/colors/tone/fonts) injected into every generation call → cascade consistency.
8. **Region-level re-roll** — refine a patch, not the whole page (pairs with our element-level loop).
9. **Export editable formats** so a human does the last-mile (kerning, strict brand, print).
