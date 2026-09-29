---
type: reference
created: 2026-06-27
source: synthesized from live computed CSS of 16 shipped world-class products (see real-extracted-tokens.md)
priority: P0
---

# Token Synthesis — what "世界级质感" actually measures as

> This is the engineering-token half of the double-track (the aesthetic-feel half is `references/world-class-teardowns/`). Every number below was pulled live from a shipped, world-class site — not invented. When the skill generates a page, pull defaults from HERE instead of guessing; guessing is how AI lands on the median. Raw per-site evidence: `tokens/real-extracted-tokens.md`.

Sites measured: Linear, Stripe, Vercel, Family, Arc, Notion, Apple, Figma, Raycast, Resend, Rauno, Emil Kowalski, Supabase, Framer, Mintlify, v0.

## The one-paragraph finding

World-class 质感 is **restraint executed with precision**, not richness. Across 16 sites the *vocabularies are small* (2–4 font weights, a 6-step radius scale, one accent) but the *values are exact and characterful* (a real typeface, the precise weight, a named easing curve). AI-slop is the inverse: large vocabularies (rainbow palette, random radii, default Inter) executed carelessly. Two routes to quality showed up: **systemic** (Stripe/Notion/v0 expose 600–800 CSS vars — quality enforced by a token system) and **bespoke** (Family ships 49 vars — quality hand-crafted). Pick one consciously; never land between them.

## 1. Typography — characterful, paired, tightly weighted

**No site defaults to Inter-only.** The real faces in production:

| Site | Body | Display / accent | Mono |
|---|---|---|---|
| Linear | Inter **Variable** | — | Berkeley Mono |
| Stripe | **sohne-var** (Söhne) | — | — |
| Vercel / v0 | **Geist** | — | Geist Mono |
| Notion | NotionInter | **Lyon Text** (serif) | — |
| Resend | Inter | **Domaine** (serif display) | — |
| Arc | **Marlin / Marlin Soft** | — | — |
| Apple | SF Pro Text | SF Pro **Display** | — |
| Supabase | **Circular** | — | Source Code Pro |
| Figma | figmaSans (variable) | — | figmaMono |
| Raycast / Mintlify | Inter | — | Geist/Paper Mono |

**Rules the data proves:**
- Use a face **with character** (Söhne, Geist, Marlin, Circular) or at minimum Inter **Variable** — never "system-ui by accident."
- **Pair a sans with a mono** — near-universal; mono signals "engineered." Use mono for metrics, code, labels, eyebrows.
- A **serif display** (Lyon, Domaine) is the fastest route to editorial 质感 (Notion, Resend) — pair serif headline + sans body.
- **Weight sets are tight: 2–4 weights.** Canonical: `400 / 500 / 600` body-to-emphasis. Linear's precision: **`510` and `590`** (variable-font fine weights — NOT 500/600; this is why Linear text "feels" different). Figma fine-tunes at `320 / 330`. Body text is `400`, never lighter for paragraphs; `300` only for large display.
- Display weight rarely exceeds `600–700`. Heavy 800/900 is mostly absent from premium tools (Arc 800 is the exception, it's playful).

→ Per-site type scales (the actual px ramps) are in `real-extracted-tokens.md`.

## 2. Radius — a 6-step scale, restraint over round

Real distinct radii cluster hard. **Canonical world-class radius scale:**

```
2px   — hairline (inputs inside dense tables, chips)
4px   — small controls, badges
6px   — buttons, inputs (the workhorse — Vercel/Stripe/Linear)
8px   — cards, menus, popovers
12px  — large cards, modals, sheets
16px  — hero surfaces, sheet tops
24px  — large feature panels
9999px / 50% — pills & avatars only
```

Controls live at **6–8px**, surfaces at **12–16px**. The AI tell is "everything `rounded-2xl`/24px+." Note: directional radii (`12px 12px 0 0`) are common for sheets/tabs docking to an edge — a craft signal. (The `33554400px` artifact in raw data = a `calc()` full-round; treat as pill.)

## 3. Motion — the ease-out family, with real named curves

UI motion is overwhelmingly **ease-out** (fast start, gentle settle = "instantly responsive"). Use these **real, in-production curves** as the motion token set instead of CSS `ease`:

| Token | Curve | Feel / use | Seen in |
|---|---|---|---|
| `--ease-standard` | `cubic-bezier(0.4, 0, 0.2, 1)` | Material workhorse; default UI transition | Vercel, Supabase, v0, Emil, Resend, Mintlify |
| `--ease-out-soft` | `cubic-bezier(0.25, 0.46, 0.45, 0.94)` | gentle, "Linear" calm | Linear |
| `--ease-out-expo` | `cubic-bezier(0.16, 1, 0.3, 1)` | dramatic premium reveal, big elements | (easeOutExpo) Family `(0.19,1,0.22,1)` |
| `--ease-out-quint` | `cubic-bezier(0.22, 1, 0.36, 1)` | luxurious long settle | luxury/brand |
| `--ease-drawer` | `cubic-bezier(0.32, 0.72, 0, 1)` | sheets/drawers (Vaul signature) | Emil/Vaul |
| `--ease-spring` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | playful overshoot; toggles, success | v0, expressive |
| `--ease-in-out` | `cubic-bezier(0.45, 0.05, 0.55, 0.95)` | symmetric, for looping/continuous | Stripe |

**Discipline (from research + data):** durations mostly **120–300ms** for UI, longer only for hero reveals; animate **transform/opacity** only; `ease-in` is essentially absent for enter (it feels sluggish); reserve overshoot/spring for one or two moments, not everywhere.

## 4. Color — one accent, restrained field

- Palettes are **narrow**: a dominant neutral field + **one** accent, plus semantic status colors. Evenly-weighted multi-color palettes are absent.
- **Not indigo-by-default.** Real accents are bespoke (Linear violet `#5E6AD2`, Stripe blurple/Iris, Supabase green, Vercel pure mono + saturated accent). The point isn't "avoid purple," it's **own your accent**, don't inherit `indigo-500`.
- Dark-first tools (Linear, Raycast, Supabase) build neutrals from a near-black with subtle hue, not pure `#000`/`#111`. Per-site exact hexes are in `real-extracted-tokens.md`.

## 5. The systemic-vs-bespoke fork (var counts)

| Route | Var count | Examples | How quality is enforced |
|---|---|---|---|
| **Systemic** | 400–800 vars | Stripe 689, Notion 795, v0 802, Supabase 610, Vercel 546, Linear 397 | a real token system: primitive→semantic→component; consistency is structural |
| **Bespoke** | <160 vars | Family 49, Emil 82, Apple 97, Figma 104, Arc 120, Rauno 159 | hand-crafted per-surface; consistency is taste + few moving parts |

**Implication for the skill:** for a product/SaaS (multi-surface, must scale) → go systemic, generate the token tiers. For a landing/brand/portfolio (one surface, must wow) → go bespoke, hand-tune. Landing pages built "systemically" feel generic; products built "bespoke" rot. Match the route to the archetype (see `references/web-craft/01-page-archetypes.md`).

## Canonical defaults block (paste into a generation prompt)

```
/* world-class real-data defaults — override per chosen direction, never ship raw */
--font-sans: "Geist", "Inter var", system-ui;   /* a face with character; pair a mono */
--font-mono: "Geist Mono", "Berkeley Mono", monospace;
--weight-body: 400; --weight-medium: 500; --weight-strong: 590;  /* tight, precise */
--radius-control: 6px; --radius-card: 12px; --radius-surface: 16px; --radius-pill: 9999px;
--ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
--ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
--dur-fast: 150ms; --dur: 220ms; --dur-slow: 320ms;
/* ONE accent, owned — not indigo-500. dark neutrals carry a subtle hue, not pure #000 */
```
