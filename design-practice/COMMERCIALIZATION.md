# Commercialization — what's sellable here, and why it's defensible

> The valuable asset is **not the markdown**. It's the **engine**: a closed render→critique→refine loop, scored by a real rubric, grounded in real-extracted tokens, finished by a compound-craft layer — plus a transferable design-judgment layer none of the competitors expose. This doc defines what can be packaged, sold, and delivered "几乎可以直接交付."

## The moat (what nobody else assembles in one place)
From the competitive teardown (`references/competitive-teardown/`): every high-质感 tool (v0, Lovable, Bolt, Lovart, Claude Design) constrains generation, plans before pixels, commits to a direction, injects real assets, and loops on rendered output. **None of them documents an explicit rubric-scored visual critique loop, and none has a transferable design-judgment layer.** This skill is the union:

1. **Judgment layer** — 27-chapter design judgment (task-field, complexity conservation, true-vs-empty simple, object-state-permission). The *why* before the *what*.
2. **Real-extracted tokens** — ground truth from 16 shipped products, not a model's guess.
3. **The 10-dim rubric** — a measurable quality bar that names the single weakest element.
4. **The closed loop** — render in a real browser, score, fix weakest, repeat (`tooling/render-critique.mjs`).
5. **The compound-craft layer** — the invisible 0.1-details that make 4/5 → SSS.

Plan + commit + constrain + real assets are **table stakes we adopt**. Layers 1–5 are **the moat we own**.

## Three sellable products (same engine, different packaging)

### A. The Design Quality Engine (API / CLI) — *highest value*
`render-critique` as a hosted service: input any URL or HTML → output the 10-dim scored report + screenshots + the prioritized "single weakest element + concrete fix." A **"design linter / quality gate as a service."**
- **Buyers:** AI-app builders (v0/Lovable/Bolt-style), agencies, design-system teams, CI pipelines.
- **Model:** usage-based (per audit) + seat-based for teams; CI plan (gate every PR's UI).
- **Why it sells:** every AI-builder ships median UI and has no objective quality bar. This *is* the bar.

### B. The Skill / Agent (licensed) — *productize the whole pipeline*
The full `design-practice` skill as a licensed agent capability: idea → world-class, deliverable UI with skeleton + real tokens + the loop. Sold as a Claude/Cursor/Codex skill, or embedded in a product.
- **Buyers:** dev shops, solo founders, internal platform teams.
- **Model:** per-seat subscription; white-label for agencies; enterprise (private token library tuned to their brand).

### C. The Token + Craft Library (data product) — *the asset, standalone*
`tokens/` (real engineering tokens) + `world-class-teardowns/` (aesthetic directions) + `craft-details-invisible.md` (the compound-craft audit) as a curated, continuously-refreshed design intelligence dataset.
- **Buyers:** design tooling companies, theme marketplaces.
- **Model:** dataset subscription; refresh cadence (re-extract shipped sites quarterly).

## The delivery boundary ("几乎可以直接交付")
What the engine guarantees vs. what still needs a human:
- ✅ **Guaranteed:** gate-clean (no console errors, AA a11y, responsive 320–1440), token-disciplined, all states present, the 10-dim bar ≥4, compound-craft audited.
- ⚠️ **Human last-mile:** licensed brand typeface (self-hosted), bespoke illustration/photography, final copy voice, the single bold "wow" moment for brand pages, legal/brand sign-off. (Mirror of Lovart's "export editable formats for last-mile" lesson.)
- ❌ **Out of scope:** backend/data wiring, real auth, production infra.

## Pricing posture (directional)
- Engine (A): land on per-audit credits ($ per render-critique) + a CI seat tier; the value metric is "audits run."
- Skill (B): per-seat/month; enterprise tier = private brand-tuned token library + on-prem harness.
- Library (C): annual dataset license with quarterly refresh.

## What to build next to make it sellable
1. Harden `render-critique.mjs` → a service (queue, headless pool, auth, hosted screenshots).
2. Make the report name **every** failing element (axe nodes, off-grid selectors) — already partly done; finish it so fixes are one-click.
3. A thin web UI: paste URL → see the scored report + before/after. The demo *is* the sales pitch.
4. A self-refreshing token pipeline (re-run the 16-site extractor on a schedule).
