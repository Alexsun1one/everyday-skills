---
type: reference
created: 2026-06-27
priority: P0
stage: 3
---

# Stage 3 — Render → Critique → Refine Loop

> **Executable heart of design-practice.** Stage 2 produces HTML; Stage 3 closes the loop with a real browser. Text-only "self-review" is role-play — this is evidence.

## When to run

After Stage 2 high-fidelity HTML exists (local `.html` or deployed URL). **Never ship first output.**

```text
generate HTML → render-critique.mjs → read report.json + LOOK at 3 screenshots
→ score 10 dims → fix ONLY weakest dim → re-run → repeat
```

Harness path: `tooling/render-critique.mjs`  
Playbook install: `cd tooling && npm i && npx playwright install chromium`

## The loop (agent runbook)

### Step 1 — Render & collect

```bash
node tooling/render-critique.mjs path/to/page.html --out tooling/reports
```

Harness delivers:

- 3 full-page screenshots (1440×900, 768×1024, 390×844)
- `report.json` — signals, axe, rubric partial scores, gate status
- `report.md` — human-readable summary

### Step 2 — Read evidence (two channels)

| Channel | What to read | Trust level |
|---------|--------------|-------------|
| **Objective** | `report.json` → console, axe, LCP/CLS, token-drift, overflow, state flags | High — measured in Chromium |
| **Visual** | Open `desktop-*.png`, `tablet-*.png`, `mobile-*.png` | Required — hierarchy, typography, restraint cannot be faked from DOM |

**Combine, don't substitute.** Harness `score: null` + `needs_visual_judgment` means **you** assign 0–5 with one-line evidence from the screenshot, not from code memory.

### Step 3 — Score all 10 dimensions

Use the rubric in `report.json` → `rubric`. For each dimension:

```text
dimension: <id>
score: 0-5
reason: one line, cites screenshot region OR report signal
```

Harness auto-scores dims 2, 4–9. Agent completes dims 1, 3, 10 from screenshots.

### Step 4 — Fix ONE dimension only

Pick the **single lowest score** across all 10. Edit HTML/CSS for that dimension only.

| If weakest is… | Fix direction (examples) |
|----------------|--------------------------|
| hierarchy | One primary action, 5-3-2 weight, demote secondary CTAs |
| spacing | Snap to 4/8 grid, increase whitespace between groups |
| typography | Real type scale, tighten display, fix line-length |
| contrast_a11y | Fix axe violations, add `:focus-visible`, ARIA labels |
| color_tokens | Move hex to semantic `var(--*)`, kill indigo-default |
| state_coverage | Add hover/focus/disabled/loading/empty/error variants |
| motion | Shorten to <300ms ease-out, transform/opacity only, `prefers-reduced-motion` |
| performance | Reduce CLS, skeleton, defer non-critical |
| responsive | Fix 390 overflow, stack/reflow at tablet |
| restraint | Remove a card row, add signature detail, kill centered-everything |

**Do not rewrite the whole page.** One dimension per iteration keeps the loop honest.

### Step 5 — Re-run harness

Same command, new timestamped report folder. Compare scores and gate status.

### Stop criteria

| Condition | Action |
|-----------|--------|
| All 10 dimensions ≥ 4 | Ship (then run qa-* delivery gates) |
| 4 iterations reached | Deliver **best-so-far** + flag remaining gaps in report |
| Gate still failing (console / serious axe / 390 overflow) | Keep looping even if visual scores look fine |

**Hard cap: 4 iterations.** Never accept first output.

## Evidence + judgment matrix

```text
┌─────────────────────┬──────────────────────────┬─────────────────────────┐
│ Dimension           │ Harness evidence         │ Agent must look?        │
├─────────────────────┼──────────────────────────┼─────────────────────────┤
│ Hierarchy           │ screenshot paths only    │ YES — 1s primary action │
│ Spacing             │ off-grid count, samples  │ confirm visually        │
│ Typography          │ font-family count        │ YES — scale & rhythm    │
│ Contrast & a11y     │ axe violations, focus    │ spot-check focus ring   │
│ Color & tokens      │ hex/var, indigo hits     │ confirm palette restraint│
│ State coverage      │ static CSS flags         │ verify real UI states   │
│ Motion              │ CSS duration/properties  │ optional spot-check     │
│ Performance         │ LCP, CLS, DOM count      │ confirm no jank visually│
│ Responsive          │ overflow flags           │ YES — mobile screenshot │
│ Restraint           │ center ratio, shadows    │ YES — anti-AI-median    │
└─────────────────────┴──────────────────────────┴─────────────────────────┘
```

## Relationship to other references

| File | Role |
|------|------|
| `ai-self-review-loop.md` | Text-only generation loop (Stage 2 inline) — **not a substitute** |
| `qa-*.md` | Delivery gates **after** Stage 3 loop converges |
| `anti-plastic-fix-guide.md` | Fix recipes when weakest dim is color/hierarchy/restraint |

Stage 3 runs **during** refinement; qa-* runs **before** human handoff.

## Anti-pattern table

| 反模式 | 为什么坏 | 修正 |
|--------|----------|------|
| Scored from code without opening screenshots | Hierarchy/typography/restraint are visual; DOM lies | Open all 3 PNGs every iteration |
| Rewrote entire page instead of weakest dim | Loses working parts; can't attribute improvement | One rubric dimension per pass |
| Declared done without re-running harness | "Fixed" nothing measurable | Re-run `render-critique.mjs` after every edit |
| Faked visual scores to pass loop | Same as AI plastic — self-congratulation | `score: null` stays null until agent sees PNG |
| Ignored exit code 1 | Console errors and axe serious still ship | Fix gate failures before celebrating scores |
| 4 iterations of spacing tweaks only | Weakest dim stuck because visual dims never scored | Score dims 1/3/10 explicitly each round |
| Skipped mobile screenshot | 390 overflow is a hard gate | Always read `mobile-390x844.png` |
| Used `file://` manually | Chromium blocks; harness serves localhost | Let harness auto-serve local HTML |

## Example iteration log (template)

```text
iteration: 1
harness: tooling/reports/2026-06-27T12-00-00-000Z/
gate: FAIL (2 console errors)
weakest: color_tokens (2/5) — 47 hex, indigo hit
fix: moved surfaces to var(--surface-*), replaced #5E6AD2 with --brand
---
iteration: 2
gate: PASS
weakest: hierarchy (agent 2/5) — three equal-weight CTAs in header
fix: demoted "Export" to ghost, enlarged primary "New deal"
---
iteration: 3
all >= 4 → stop
```

## One sentence

**Harness gathers evidence; agent sees; fix one thing; run again — never trust the first render.**
