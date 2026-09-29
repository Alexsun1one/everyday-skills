# Component Spec Dictionary — pixel-level prompt library

> This is the precision layer of the skill. Where `references/stage2-*` explains the discipline, this directory gives you **copy-paste-ready, pixel-exact prompt fragments** for every common component. Feed these to an image model or a code agent and the output stops drifting.

## Why this exists

Article line 1201: *"很多产品看着乱,不是因为某一个页面特别差,而是因为每个页面都在临时发明零件:这个按钮圆角 6px,那个按钮圆角 10px..."* The cure is not more discipline talk — it's a frozen spec per component, so no one invents pixels on the fly.

Sun's intent (2026-06-27): user says "make me a task manager", the skill emits **pixel-level prompt fragments** for every component (button 36px tall, hover bg gray-50, checkbox 16px left-aligned, avatar 32px circle, badge 20px tall padding 0 8px...). Generation becomes near-deterministic.

## How to use

1. Identify which components your page needs (from the Stage-1 IA draft).
2. Open each component's file in this directory.
3. Copy the **Prompt Fragment** block into your image-model or code-agent prompt.
4. The fragments compose — a list row contains a checkbox + avatar + badge + text, each pulled from its own file, all snapping to the same 4px grid.

## Component file structure (every file follows this)

```markdown
# Component: <name>

## Spec table (pixel-exact)
| Token | Value | Notes |

## 8-state matrix
| State | Visual | Copy | Behavior |

## Prompt fragment (English, copy-paste)
<block>

## Prompt fragment (Chinese, copy-paste)
<block>

## Tailwind classes
<code>

## Reverse examples (plastic vs human)
<table>

## Composes with
<list of other components this one nests>
```

## Component inventory

### Tier 1 — core (ship first, used in 90% of pages)

| File | Component | Why core |
| --- | --- | --- |
| `button.md` | Button (primary/secondary/ghost/icon) | the loudest human-made signal |
| `input.md` | Input + Textarea + form field | forms are where users suffer |
| `table-row.md` | Table/list row (3 densities) | data density is a product skill |
| `card.md` | Card (container of grouped info) | the basic content box |
| `drawer.md` | Right-side drawer (detail panel) | preserves list context |
| `modal.md` | Modal (destructive confirm only) | hard interrupts |
| `toast.md` | Toast (success/error/info) | system feedback |
| `empty-state.md` | Empty state (3 kinds) | most-abused state |
| `badge.md` | Badge / tag / pill | labels & status |
| `avatar.md` | Avatar (with status dot) | user representation |
| `checkbox.md` | Checkbox + radio + switch | selection controls |
| `nav-sidebar.md` | Sidebar nav + top bar | the app skeleton |

### Tier 2 — extended (add as needed)

| File | Component |
| --- | --- |
| `select.md` | Select / dropdown / combobox |
| `datepicker.md` | Date picker / calendar |
| `tabs.md` | Tabs / segmented control |
| `pagination.md` | Pagination / load-more |
| `search-command.md` | Search bar + ⌘K command palette |
| `filter-drawer.md` | Filter drawer (low-frequency filters) |
| `tooltip.md` | Tooltip / popover |
| `skeleton.md` | Loading skeleton (per content shape) |
| `progress.md` | Progress bar / spinner / step indicator |
| `breadcrumb.md` | Breadcrumb / page header |
| `comment.md` | Comment / thread / activity feed |
| `menu.md` | Context menu / dropdown menu |

## The 4px grid (the one rule that makes everything snap)

Every dimension in this dictionary is a multiple of 4 (half-steps allowed: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96...). This is Tailwind v4's default (`--spacing: 0.25rem`), it's Linear's base unit, it's Material 3's base unit. No 13px margins, no 7px gaps. If you find yourself writing one, stop — you're inventing instead of using the scale.

```text
spacing scale (use these, only these):
  1 = 4px    2 = 8px    3 = 12px   4 = 16px   5 = 20px
  6 = 24px   8 = 32px   10 = 40px  12 = 48px  16 = 64px
  20 = 80px  24 = 96px  32 = 128px
```

## The radius scale (mirrors Linear / Tailwind)

```text
  radius.xs   = 4px    (keyboard keys, tiny chips)
  radius.sm   = 6px    (small controls, inline tags)
  radius.md   = 8px    (buttons, inputs — the workhorse)
  radius.lg   = 12px   (cards)
  radius.xl   = 16px   (screenshot panels, large frames)
  radius.pill = 9999px (badges, status dots only — never primary buttons)
```

## The motion scale (mirrors Linear / article line 1433)

```text
  duration.fast   = 100ms  (hover, press, color shift)
  duration.normal = 180ms  (default — Linear's signature timing)
  duration.slow   = 240ms  (drawer, modal, expand)
  easing.standard = cubic-bezier(0.22, 1, 0.36, 1)  (Linear's curve)
  pressed scale   = 0.97   (Linear's tactile feedback)
```

## The type scale (mirrors article line 1033-1063 + Tailwind)

```text
  text.xs    = 12px / 1.4   (badges, metadata, timestamps)
  text.sm    = 14px / 1.5   (body — the default reading size)
  text.base  = 16px / 1.5   (large body, mobile minimum)
  text.lg    = 18px / 1.4   (subsection)
  text.xl    = 20px / 1.3   (section heading)
  text.2xl   = 24px / 1.2   (page heading)
  text.3xl   = 32px / 1.1   (hero)

  weight.regular  = 400
  weight.medium   = 500  (Linear uses 510 — custom axis)
  weight.semibold = 600  (Linear uses 590)
```

## Authority sources

These specs are triangulated from:
- **Material 3** — button heights (32/40/56), padding (16/24/32), radius (8)
- **shadcn/ui** — Tailwind variant classes (h-9 px-4 py-2 etc.)
- **Linear** — 32-40px rows, 4px grid, #5E6AD2 accent, 180ms motion, 0.97 pressed scale, Inter var 510/590, Berkeley Mono
- **Stripe Elements** — input padding 8x4, focus ring 2px box-shadow, mobile ≥16px font
- **Tailwind v4** — the 4px-base generative spacing scale
- **Article** — button 8 states (line 1281), focus ring (line 1285), empty 3-kinds (line 11681), token 3-layers (line 957)

When a value here conflicts with a reference, **this dictionary wins** (it's the frozen spec).

## Relationship to `references/armory/`

The skill has two precision layers — they complement, not overlap:

| | `references/armory/` | `components/` (this directory) |
| --- | --- | --- |
| **Organized by** | style (Linear / Stripe / Notion / Material3 / Tailwind) | component (button / input / card / …) |
| **What it freezes** | the full token set of a style (colors, spacing, radius, type, motion) | one component's full spec (8-state matrix + prompt fragment + Tailwind + reverse examples) |
| **When to read** | when you've picked a style and need the token values to fill in | when you're writing the prompt for a specific component on the page |
| **Granularity** | token-level (hex / px / ms / cubic-bezier) | component-level (how those tokens assemble into a button, with states and behaviors) |

**Workflow:**
1. User picks intent + style (e.g., "task manager, Linear feel").
2. Read `references/armory/00-index.md` → route to `01-tokens-linear.md` → grab the token set.
3. For each component the page needs, read `components/<name>.md` → grab the 8-state matrix + prompt fragment.
4. The prompt fragment's placeholders (e.g., `color.state.primary`) get filled from the armory's token set.
5. Assemble into a composite prompt (see `examples/example-composite-prompt-task-manager.md`).

**If a component is missing from `components/`**, check `armory/10-basic-*.md` through `armory/23-complex-*.md` (planned) — they may already spec it. If not, add it here following the file structure above.
