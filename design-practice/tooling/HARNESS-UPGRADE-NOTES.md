# Harness Upgrade Notes — Round 2 (2026-06-28)

Driven by a real-product stress-test that exposed two blind spots: the harness **false-passed** a non-responsive page and **false-flagged** good controls. Both are now fixed and calibrated against real pages.

## render-critique.mjs — a REAL mobile responsive audit (was: horizontal-page-scroll only)
The old `responsive` check only asked "does the page scroll horizontally at 390?" — which a **fixed desktop grid hidden by `overflow:hidden`** silently passes (it clips content instead of scrolling). New audit, run at **390 and 360** (worst viewport wins):
- **Clipping** — elements whose box extends past the viewport (`right > vw` / `left < 0`) even under `overflow:hidden`; off-canvas drawers/panels exempted. This is the core catch.
- **Fixed / min widths** — `width`/`min-width` px > viewport, grid track sums, flex-nowrap children sums (strict vs soft).
- **Horizontal scroll** — separated into **root (page) scroll = failure** vs **inner `overflow-x:auto` contained-scroll = the recommended pattern, NOT penalized** (per `responsive-adaptive-mastery.md`).
- **Touch targets** — interactive els < 44×44 (hard-flag < 24×24); **inline links (`<a display:inline*`) exempted** per WCAG 2.2 SC 2.5.8.
- **Body text < 12px** — primary copy only (meta/caption/badge utility classes skipped).
Scored 1–5 via `scoreResponsive()` with severe/moderate/minor clip tiers; emits a `responsiveDetail` with per-metric counts + samples so the agent gets ACTIONABLE output, not just a number.

### Calibration done after first run (don't tune to a number — look at what's flagged)
First run false-failed the responsive Cadence showcase on (a) inline-link touch targets and (b) a single inner contained-scroll. Fixed: exempt inline links; only penalize **root** page-scroll, never inner contained-scroll. After calibration the harness still correctly **caught a real bug** in Cadence (a tab `#tab-deep` overflows 112px at 360px) — proof it's honest, not lax.

## behavior-audit.mjs — a11yDepth + dead-button false-positive fix
- **Dead-button test now EXCLUDES** controls where no-op is correct: `disabled`/`aria-disabled`, already-active toggles (`aria-pressed/selected/checked=true`), and file-dialog triggers (open a native picker → no DOM mutation). Before this, a well-built product scored 70% live / 1 dead inflated to look like 9 dead.
- **New `a11yDepth` block**: keyboard focus-visible reachability (does Tab reach controls + show a visible focus ring?), dialog focus-trap + Esc-to-close, and ARIA semantics sanity (dialog has a name, tablist roving tabindex, toggles have aria-pressed/checked). Folded into an `a11yDepthScore`.

## Verification deltas
| Page | Before | After | Verdict |
|---|---|---|---|
| digital-twin (fixed 3-col grid + overflow:hidden) | responsive **5/5** (false pass) | responsive **2/5** (29 clipped, 1 fixed-width) | true-fail — blind spot closed |
| Cadence landing (real responsive) | responsive 5/5 | responsive **2/5** | real catch — a tab overflows 112px at 360px (flagged for fix) |
| digital-twin (well-built controls) | behavior 4/5, 9 "dead" | behavior **5/5**, 1 dead, 95% live | false-positives removed |

## Output fields added
`render-critique`: `responsiveDetail{ clippedCount, clippedMaxOverflow, fixedWidthCount/strictFixedWidthCount, horizontalScrollCount/horizontalRootScrollCount, touchBelow24/44, smallTextCount, samples{...} }` + CWV (CLS/LCP/INP).
`behavior-audit`: `skipped`, `fileDialog`, `a11yDepth{ focusVisibleRatio, dialogs[], ariaViolations[] }`, `a11yDepthScore`.
