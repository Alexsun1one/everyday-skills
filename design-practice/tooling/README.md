# design-practice Render Critique Harness

Stage 3 executable heart: **render → collect signals → emit report** for the design-practice skill.

Real browser critique replaces role-playing a critic over text-only output.

## Install

```bash
cd tooling
npm install
```

The harness falls back to the **system Google Chrome** automatically if the Playwright-bundled Chromium is absent. No `playwright install` step is required — this avoids the Azure CDN download hanging on networks where `playwright.azureedge.net` is unreachable.

## Usage

```bash
node render-critique.mjs <path-to-html-or-url> [--out <dir>]
```

Examples:

```bash
# Local HTML (auto-served over ephemeral localhost — file:// is blocked)
node render-critique.mjs ../demo-crm-v3.html --out reports

# Remote URL
node render-critique.mjs https://example.com --out reports
```

Each run creates a timestamped folder under `--out` (default `tooling/reports/`):

| Artifact | Purpose |
|----------|---------|
| `desktop-1440x900.png` | Full-page screenshot |
| `tablet-768x1024.png` | Full-page screenshot |
| `mobile-390x844.png` | Full-page screenshot |
| `desktop-states.png` | Contact sheet: default / hover / focus for button, nav link, table row, input |
| `state-*-{default,hover,focus}.png` | Individual interaction-state crops |
| `report.json` | Machine-readable signals + rubric |
| `report.md` | Human-readable critique |

## What the report contains

### Objective signals (harness-measured)

- **Console:** errors, warnings, uncaught page exceptions
- **Network:** failed requests (4xx/5xx or connection failure)
- **Performance (Core Web Vitals):** LCP ms + LCP element, CLS + shift count, approximate INP ms + event name, DOM node count
- **Design system snapshot:** type scale (px), palette (hex), radius scale, easing curves — compare against `00-token-synthesis.md`
- **Spacing rhythm (authored CSS):** detected base unit (4/8px mode/GCD), off-scale authored padding/margin/gap values with example selectors — not computed sub-pixel layout noise
- **Accessibility (actionable axe):** per violation — rule id, impact, help, up to 15 nodes each with target selector(s); color-contrast includes fg/bg hex, measured ratio, required threshold
- **Interaction states:** programmatic hover/focus on representative elements + contact sheet PNG
- **Token-drift heuristics:** font-family count, distinct colors, hex vs `var()`, indigo-default palette hits, `text-align:center` ratio, `:focus-visible` presence, drop-shadow usage
- **State coverage (static):** CSS/HTML signals for hover/focus/active/disabled/loading/empty/error/permission
- **Motion (static):** transition duration >500ms, non-transform/opacity properties, `prefers-reduced-motion`
- **Responsive:** horizontal/vertical overflow per viewport

### 10-dimension rubric (0–5)

| # | Dimension | Harness |
|---|-----------|---------|
| 1 | Hierarchy (视觉层级) | **Visual** — agent scores from screenshots |
| 2 | Spacing & rhythm (间距节奏) | Auto from authored off-scale spacing count |
| 3 | Typography (字体) | **Visual** — agent scores; harness extracts type scale |
| 4 | Contrast & a11y (对比可访问性) | Auto from axe + focus-visible |
| 5 | Color & token discipline (色彩token纪律) | Auto from hex/var ratio + indigo hits + palette |
| 6 | State coverage (状态完整) | Auto from static state flags + interaction captures |
| 7 | Motion (动效) | Auto from CSS transition/animation scan |
| 8 | Performance (性能) | Auto from LCP/CLS/INP/DOM signals |
| 9 | Responsive integrity (响应式) | Auto from overflow at 390×844 |
| 10 | Restraint & originality (克制与原创) | **Visual** — agent scores from screenshots |

Dimensions marked `needs_visual_judgment` include screenshot paths and measured hints. **Do not fake scores** — the agent looks at PNGs and completes those dimensions.

`nextWorkItem` in the report names the **single weakest auto-scored dimension** as the default fix target. After visual scoring, the agent picks the overall weakest across all 10.

## Exit codes

| Code | Meaning |
|------|---------|
| `0` | Gate pass: no console errors, no critical/serious axe violations, no overflow at 390×844 |
| `1` | Gate fail (see `gate.reasons` in report) |
| `2` | Usage error or harness crash |

Use exit code `1` to block CI until the page is fixed and re-run.

## Agent loop

See `references/stage3-render-refine-loop.md` for the full generate → critique → fix weakest dim → re-run protocol.

---

# Trigger Eval — does SKILL.md trigger on the right requests?

`trigger-eval.mjs` evaluates whether the `description:` frontmatter in `SKILL.md` correctly routes requests:

- **should_trigger** (real product-UI requests) — must fire
- **should_not_trigger** (cover image / sticker / quote card / illustration / system diagram) — must NOT fire
- **near_neighbor** (intentionally ambiguous: "做一个网页", "Linear 风格的截图", "漂亮的后台 UI 不用真功能") — Intent Brief filters these post-trigger, so they're a **soft signal**, not a hard CI block

## Usage

```bash
node trigger-eval.mjs --skill ../SKILL.md --out reports/trigger-eval
```

Optional flags:

- `--cases <path>` — custom case file (default `tooling/trigger-cases.json`)
- `--config <path>` — custom semantic concept config (default `tooling/trigger-semantic-config.json`)
- `--threshold <float>` — override recommended_threshold (default 0.48)
- `--baseline <path/to/other/SKILL.md>` — compare another description (e.g. before/after edit)

## What the report tells you

| Signal | Meaning |
|---|---|
| `false_negatives > 0` | A real UI request was missed — add the trigger phrase to a positive_concept in the config, OR surface that intent in the description. |
| `false_positives > 0` (hard) | A neighbor-skill request fired — add the phrase to a negative_concept OR add a `Do NOT use for:` line in the description. |
| `soft_false_positives > 0` | near_neighbor misfire — expected. Intent Brief gate handles these. Read these to see which ambiguous phrasings users actually use; tighten description only if a clear pattern emerges. |

## How it scores (no LLM call)

Ported concept-based semantic scoring from `yaojingang/yao-meta-skill` (MIT).

1. Each concept (positive / negative) is a weighted bag of phrases (en + zh).
2. For each test case, count concepts matched in BOTH description and prompt → semantic coverage (strongest matched concept / strongest desired concept, so a rich description isn't penalized for hitting only its top concept).
3. Add coverage boost for multi-concept hits, support score for extra concepts, lexical support for word overlap.
4. Subtract negative concept penalty. Exclusive negative concepts (cover / sticker / quote / illustration / diagram) drop the score hard.
5. Compare against threshold; report per-family pass rate + misfire table so you know exactly which phrase caused each failure.

## When to run it

- After editing `SKILL.md`'s `description:` field.
- After adding new showcase types or domain extensions.
- When a user reports "the skill didn't trigger" or "the skill fired when it shouldn't".
- Before commit, alongside `render-critique.mjs` — both are the verification gates for this repo.

## Exit codes

| Code | Meaning |
|------|---------|
| `0` | Hard gate pass (no FN, no hard FP). Soft FP from near_neighbor is OK. |
| `2` | Hard gate fail — fix description or cases before commit. |
| `1` | Usage error. |

---

# Context Budget — is the skill still readable by an agent?

`context-budget.mjs` measures whether an agent can actually hold design-practice in its working memory. It separates:

- **Initial load** — `SKILL.md` + `AGENTS.md` + the files SKILL.md explicitly tells agents to read first (agent-playbook, intent-reading, fast-path).
- **Per-stage bundles** — what the agent eats when it enters Stage 0 / 0.5 / 1 / 2 / 3 / Workflow / QA. Each stage is supposed to fit in working memory.
- **Per-need resources** — Components (`components/*.md`) and Visual Language (`visual-language/*.md`) are measured by their LARGEST SINGLE FILE, not the sum, because the agent reads per-need (one component file per component the page contains, one style file per Intent Brief route). This reflects the SKILL.md E6 + E7 workflow.
- **Decorative files** — `.md` files that exist but aren't referenced by any entry path and aren't mentioned by name anywhere else. These are dead weight.
- **Top-heavy files** — individual files >4000 tokens. Split candidates.
- **Showcase debt** — `showcase*/` directories without `index.html`. The skill's claim of "live samples" is unverified for these.

## Usage

```bash
node context-budget.mjs [--root <path>] [--out <dir>] [--json]
```

Default root is cwd. Output goes to `tooling/reports/context-budget/` when `--out` is set.

## Thresholds (calibrated for design-practice, NOT YAO's small-skill defaults)

| Metric | Warn | Fail |
|---|---|---|
| Initial-load tokens | 15000 | 30000 |
| Stage bundle (sum mode) | 12000 | 25000 |
| Per-need resources | — (largest single file shown) | — |

YAO's defaults (700-1300 token initial budget, 80% skill-body ratio) are tuned for small conversational skills. design-practice is a deep domain skill — its `SKILL.md` legitimately runs 8-15k tokens because the whole point is per-stage on-demand depth, not initial load.

## Ignored paths

The tool intentionally ignores:

- `node_modules/`, `.git/`, `tooling/reports/`
- `tokens/_extract/` — raw scraped token data, an asset not agent context
- `references/source-full.md` — the full《设计的实践》article source, reference asset
- `demo-crm*.html`, `COMMERCIALIZATION.md` — superseded / business notes

These are real assets but not part of the agent's reading load.

## When to run it

- After adding new references / components / showcases.
- Before commit, alongside `render-critique.mjs` and `trigger-eval.mjs`.
- When an agent reports "I lost the thread" / "the skill is too big to follow".
- Quarterly health check — the references/ library tends to grow without pruning.

## Exit codes

| Code | Meaning |
|------|---------|
| `0` | Pass (warnings about heavy bundles are OK) |
| `2` | Fail — a bundle exceeds the hard threshold |
| `1` | Usage error |

---

# Failure Mode Regression — does the showcase actually obey the skill?

`failure-regression.mjs` statically detects the subset of SKILL.md's 40 Failure Modes that can be machine-checked on generated HTML. The other ~25 failures are agent-process failures (skipped Intent Brief, no Type-A drafts, etc.) — those live in `references/qa-*.md` as agent self-checks; trying to machine-check them would just produce false positives.

## What it catches

| SKILL.md # | Rule | Severity | What it looks for |
|---|---|---|---|
| #3 | `two_primary_buttons` | fail | Two primary CTAs within one screen with no `<section>`/`<main>`/`<hr>` boundary |
| #4 | `empty_state_no_classification` | fail | "暂无数据" / "No data" / "Empty" without initial/filter/permission signal nearby |
| #5 | `hardcoded_color` | warn | Hex colors used outside `:root` (should be tokens) |
| #6 | `missing_focus_visible` | fail | No `:focus-visible` rule, or `:focus { outline: none }` without replacement |
| #12 | `hover_only_color` | warn | >70% of `:hover` rules only change color (no transform/box-shadow) |
| #13 | `off_grid_spacing` | warn | Off-4px-grid values (13/15/17/22/27/33…) in padding/margin/gap |
| #17 | `mixed_icon_libraries` | fail | Lucide + Heroicons + emoji + Phosphor + Material in one file |
| NEVER | `indigo_violet_gradient_hero` | fail | Indigo/violet/purple gradient in hero region |
| NEVER | `emoji_as_icon` | fail | Emoji inside `<button>`/`<nav>` without SVG fallback |
| NEVER | `overflow_hidden_mobile_mask` | fail | `overflow:hidden` on body + fixed-width layout + no `@media` mobile |
| NEVER | `modal_no_focus_trap_signal` | warn | `role="dialog"` without JS focus-trap signal (static can't prove JS — drive with behavior-audit) |

## Usage

```bash
node failure-regression.mjs <showcase-html> [--out <dir>] [--strict]
```

`--strict` makes warnings also block the exit code.

## When to run it

- After any change to a showcase HTML file.
- Before commit, alongside `render-critique.mjs`, `behavior-audit.mjs`, `trigger-eval.mjs`, `context-budget.mjs`.
- The 4-gate set (render + behavior + trigger + failure) is the project's full verification surface.

## Exit codes

| Code | Meaning |
|------|---------|
| `0` | No failures (warnings allowed unless `--strict`) |
| `2` | Failures detected — fix before claiming showcase "done" |
| `1` | Usage error |

## Known limitations

- Static HTML only — can't catch dynamic state transitions, JS focus-trap, or ARIA live regions. Pair with `behavior-audit.mjs` for behavioral gates.
- Regex-based HTML parsing (no dependency added). False positives possible on unusual markup; verify evidence before fixing.
- Doesn't check the 25+ agent-process Failure Modes (#1, #2, #7-11, #14-16, #18-40). Those require checking the agent's transcript, not the output.
