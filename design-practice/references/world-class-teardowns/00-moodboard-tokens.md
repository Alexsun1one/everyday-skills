---
type: reference
created: 2026-06-27
source: aesthetic tokens extracted by the orchestrator (Opus) from Codex-generated moodboard images (moodboard/*.png), verified by eye
priority: P0
---

# Moodboard Aesthetic Tokens — the "feel" half of the double-track

> Codex generated 9 art-directed reference images (moodboard/). They are useful ONLY as aesthetic **mood/direction** — palette, composition archetype, type personality, the "signature move." They are **NOT UI specs**, and they are **NOT all equally valid** (see the caveat). The **numbers** half is `tokens/00-token-synthesis.md` (real CSS from shipped sites). Route a design: pick a direction here for *feel* → pull exact scales there for *spec*.

## ⚠️ CRITICAL CAVEAT — image-gen UI is skin without skeleton
AI image models paint the *look* of a UI; they cannot produce a real one. On zoom, the **dense SaaS / tool / data directions (D1 precision-tool interior, D6 data-dense terminal) fall apart**: fake/noise data, wobbling off-grid alignment, no component system — *exactly the "skin without skeleton" disease this skill exists to cure.* They are convincing only at thumbnail scale.

**Rule (bake into the skill): never use a generated image as a product-UI reference.**
- ✅ Image-gen mood is valid for **brand / editorial / luxury / marketing-hero** genres — D4 Field Notes, D5 Maison Vale, and the *landing-page composition* of D2 — where the value is composition + photography + big type and there is no dense data/grid to hallucinate.
- ❌ For **SaaS / tool / dashboard / data UI**, the only legitimate references are **real shipped products**: use `tokens/00-token-synthesis.md` + real screenshots (Linear/Vercel/Raycast/Stripe). Never these images.

Hex values below are eyeball estimates — treat as direction, refine against the real-token file.

## How to use
1. In the Intent Brief, match GOAL×AUDIENCE×TONE to ONE direction below.
2. Lock it as the persistent "direction object" cascaded into every generation + render pass (the competitive-teardown adopt-list).
3. Pull the matching scales from `tokens/00-token-synthesis.md`. Never mix two directions (Claude `frontend-design`: "do not mix directions casually").

---

## D1 · Precision Tool — dark (`moodboard/01-…axis`, `02-…caliper`)
*Linear × terminal × monitoring. The "every element earns its place" tool.*
> ⚠️ **Mood-only.** On zoom the interior is plausible but the grid wobbles and it's a flat painting — do NOT treat as a SaaS UI spec. For real precision-tool specs use Linear/Vercel/Raycast in `tokens/00-token-synthesis.md`. Keep only: palette + layout archetype (multi-pane + command palette + shortcut footer) + the green-on-near-black mood.
- **Palette**: canvas near-black with a green-ish hue `#0B0E0C`–`#0D1117`; text `#C9D1C9`/dim `#6B7268`; **single accent acid-green `#4AE168`/`#3FB950`**; status dots red/amber/green.
- **Type**: compact sans (Inter var 510/590) + **mono for IDs/metrics/labels** (Berkeley/Geist Mono). Tiny sizes, tight leading.
- **Layout**: multi-pane — left nav, central **dense data table** (mono rows), right detail pane, **keyboard-shortcut footer**, ⌘K command-palette overlay. No cards.
- **Density**: extreme. Signature move: **a visible keyboard-shortcut bar + command palette** = "this is a tool for pros."
- **Route when**: dev tools, ops/observability, internal pro tooling, "keyboard-first."

## D2 · Editorial Fintech — light (`03-…ledger-field`, `04-…northstar-treasury`)
*Stripe/Mercury caliber. Trust through editorial restraint.*
- **Palette**: white/warm-white `#FFFFFF`/`#FAFAF8`; ink `#0A0A0A`; **one blue accent `#2F5FE0`/`#1D4ED8`**; light dashboard cards `#F4F6FA`; semantic green/red for figures.
- **Type**: clean grotesk sans body + **a serif-italic accent line in the hero** ("Move with clarity") — the fastest editorial signal.
- **Layout**: **left-aligned asymmetric hero** + floating product dashboard bleeding right; big real stat blocks ($35.4B+, 99.98%); **comparison table** (us vs Traditional vs Legacy).
- **Density**: medium, generous whitespace. Signature move: **serif-italic accent word + real numbers, not adjectives.**
- **Route when**: fintech, B2B SaaS marketing, trust-led conversion pages.

## D3 · Brutalist Geek — pure black (`05-…nullstack`, `06-…forge-day`)
*Vercel-Ship / hackathon energy. Monospace, terminal, high voltage.*
- **Palette**: pure black `#000`/`#0A0A0A`; high-contrast white; **one acid accent lime `#C6F24E`/`#A3E635`** (or hot signal color); terminal-green code.
- **Type**: **mono-led** (display + body both mono or geometric sans + mono); ALL-CAPS labels; ASCII/box-drawing structure.
- **Layout**: hard grid with visible rules/borders; **giant live countdown**, terminal/diff panel, schedule grid, a sticker/graffiti wildcard element; status `// SYSTEM OPERATIONAL` chrome.
- **Density**: high, intentionally raw. Signature move: **a terminal/diff or live counter as hero, not a screenshot.**
- **Route when**: dev events, launches, infra/platform, crypto-geek, "ship" energy.

## D4 · Warm Editorial Magazine (`07-…field-notes`)
*National Geographic on the web. Photography + serif + drop cap.*
- **Palette**: warm paper `#F5F1E8`; ink `#1C1B19`; **earth accent terracotta/rust `#B5523A`**; muted natural secondary; full-bleed photography.
- **Type**: **large serif display** (high contrast) + serif or humanist body; **drop cap**; small mono/sans eyebrows + section numbers.
- **Layout**: **asymmetric editorial grid** — oversized cover headline, drop-cap intro column, portrait photo bleeding right, **pull-quote block**, data figures (+18% / 37 / 2.3M), stacked feature essays.
- **Density**: medium; composed like a printed spread. Signature move: **drop cap + pull-quote + photo bleed.**
- **Route when**: journals, long-form, brand storytelling, mission/culture, climate/non-profit.

## D5 · Luxury Maison (`08-…maison-vale`)
*Aesop / fragrance-house. Negative space is the product.*
- **Palette**: warm cream `#F3EFE9`; near-black `#1A1A1A`; **muted gold `#B8924F`**; one dark moody product photo.
- **Type**: **thin high-contrast serif display** (Didone-ish) for the name; tiny ALL-CAPS sans for nav/labels with wide tracking.
- **Layout**: extreme **negative space**; product photo **bleeding off one edge**; small scent/spec table; **numbered chapter footer** (01 The Story · 02 Notes…); restrained "RESERVE" CTA.
- **Density**: very low — luxury = space. Signature move: **huge serif name + one bled product shot + acres of whitespace.**
- **Route when**: luxury, beauty/fragrance, fashion, premium hardware, high-end hospitality.

## D6 · Data-Dense Terminal (`09-…vector-desk`)
*Bloomberg / trading desk. Maximum information per pixel.*
> ⚠️ **Worst offender — image is unusable as a UI reference.** On zoom the dense numeric panels are noise-data dressed as a terminal (repeated garbage decimals, meaningless correlation cells): zero real skeleton. Keep ONLY the palette idea (dark blue-black + semantic red/green). For real dense-UI specs, study real terminals/dashboards — never this image.
- **Palette**: very dark blue-black `#0A0E14`; **semantic green `#26A69A` / red `#EF5350`** (gains/losses); cyan/blue UI chrome; tiny dim-gray labels.
- **Type**: **tabular mono everywhere**, micro sizes, tight rows; numbers right-aligned, fixed-width.
- **Layout**: dozens of synchronized panels — candlestick chart, **order-book depth (red/green)**, watchlists, tickers, market-depth viz; no whitespace wasted.
- **Density**: maximal. Signature move: **live red/green tabular data as the entire surface — no hero, no marketing.**
- **Route when**: trading/analytics, dashboards for experts, monitoring, anything where density IS the value.

---

## Cross-direction laws (true of all 9 images)
1. **One owned accent** per direction — never a rainbow, never default indigo.
2. **Real content** — real headlines, real numbers, real product shots; no lorem, no gradient blobs.
3. **A signature move** per direction (command palette / serif-italic accent / terminal hero / drop cap / bled product / live tabular) — the thing that makes it recognizable.
4. **Composition over card-grid** — every image uses asymmetry, bleed, density, or editorial grid. Not one is a 3-card tile.
5. **Type carries the identity** — mono for tools, serif for editorial/luxury, grotesk for fintech. The face is chosen, never default.
