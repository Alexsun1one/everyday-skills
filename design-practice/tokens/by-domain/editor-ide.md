---
type: reference
created: 2026-06-27
source: computed CSS pulled live from editor / IDE / dev-tool web products (10/12 OK; zed + deepnote timed out)
priority: P0
domain: editor / IDE / dev-tool
---

# Domain tokens — Editor / IDE / Dev-tool

> **Why this file exists (Sun's lesson):** the visual token library is **domain-specific**. A CRM is not an editor is not an IDE. `tokens/00-token-synthesis.md` was extracted mostly from SaaS/landing sites; this file captures what the **editor/IDE/dev-tool** domain actually does differently. Route here when building anything code-adjacent (editor, IDE, terminal, notebook, agent console, log viewer, EXO-style tool UI). Raw data: `tokens/_extract/raw-tokens-ide.json`. The library grows per domain under `tokens/by-domain/`.

Sites measured: cursor, warp, replit, codesandbox, stackblitz, observable, val.town, github, sourcegraph, windsurf.

## What this domain does DIFFERENTLY from SaaS/CRM

### 1. The mono IS the identity — bespoke sans+mono pairing is mandatory
Every serious editor/IDE ships a **custom or characterful typeface AND a matching mono**, and uses the mono far beyond code — in labels, metrics, tabs, status, keybindings. Real production pairs:

| Tool | Sans | Mono |
|---|---|---|
| Cursor | **CursorGothic** (custom) | (system mono) |
| Warp | **Matter** | **Azeret Mono** |
| Windsurf | NB International Pro | **Geist Mono** |
| GitHub | **Mona Sans VF** | **Mona Sans Mono** |
| Sourcegraph | **PolySans** | **Poly Sans Mono** |
| Replit | IBM Plex Sans / ABC Diatype | (Plex Mono lineage) |
| Observable | Inter | **Spline Sans Mono** |
| Stackblitz | Inter / Manrope | **PT Mono** |
| val.town | IBM Plex Sans | (mono) |

→ **Rule:** never ship a code-tool UI in system-mono-by-accident. Choose a characterful mono (Berkeley Mono, Geist Mono, JetBrains Mono, IBM Plex Mono, Commit Mono) and use it as a *design element*, not just for `<code>`. The mono carries the "engineered/precise" identity this domain lives on.

### 2. Tighter radii (precision > softness)
Editors round LESS than landing pages — controls at **2–6px**, not 8–12px. Cursor 2/3/4, Warp 1–6, Observable 2/4, Windsurf 2–8. Tight radii read as "precise instrument." (Compare SaaS canonical 6/8/12.) Surfaces/panels still 8–12; chrome and inline controls stay 2–4.

### 3. Wider weight range, often variable
GitHub runs variable fine weights (**425 / 440 / 460 / 480** / 500 / 600 / 800); Stackblitz to 800; Sourcegraph 300–700. Editors exploit variable fonts for micro-hierarchy in dense chrome where size can't change. (vs SaaS's tight 400/500/590.)

### 4. Two system sizes, both extreme
Either a **huge token system** (GitHub **1988** CSS vars, Replit **1050** — every surface themed, multi-theme-ready) or **fully bespoke** (Sourcegraph **20**). Code tools almost always need themes (light/dark/high-contrast), which pushes toward the systemic end — if you build one, generate the full semantic token tier and theme it.

### 5. Motion & color
- Easing: the Material standard `cubic-bezier(0.4,0,0.2,1)` dominates; GitHub adds easeOutExpo `cubic-bezier(0.16,1,0.3,1)` for reveals. Same ease-out family as everywhere — but editors keep motion **minimal** (high-frequency keyboard actions get no animation).
- Color: dark-first, deep neutrals with a faint hue (never pure #000); **one accent** + dense **semantic** sets (syntax/diff/log colors are a real token category here: added/removed/modified, error/warn/info, plus a syntax palette). This semantic richness is unique to the domain.

## Canonical editor/IDE defaults (paste into a code-tool generation prompt)
```
/* editor / IDE domain — override per chosen theme */
--font-sans: "Geist", "Inter", system-ui;        /* or a bespoke grotesk */
--font-mono: "Berkeley Mono", "Geist Mono", "JetBrains Mono", ui-monospace;  /* the identity — use it in UI, not just code */
--weight-body: 400; --weight-med: 500; --weight-strong: 600;  /* exploit variable weights for dense chrome */
--radius-control: 4px; --radius-panel: 8px; --radius-pill: 9999px;  /* tighter than SaaS */
--ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
--dur-fast: 120ms; --dur: 180ms;                 /* snappier; remove motion from keyboard-repeat actions */
/* semantic sets are first-class here: syntax palette + diff(added/removed/modified) + log(error/warn/info/debug) */
/* dark-first; deep neutral with a faint hue, not pure #000; ONE accent. Theme everything via semantic tokens. */
```

> When building EXO-style agent consoles / log viewers / terminals: density + mono identity + tight radii + semantic status colors + zero gratuitous motion. The "flat" failure mode in this domain = no luminance stacking, no mono identity, uniform weight, no semantic color system, and dead-static chrome (no hover/focus/active micro-feedback on rows/cells).
