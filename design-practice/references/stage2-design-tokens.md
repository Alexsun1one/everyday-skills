# Stage 2 — Design Tokens (three layers, mandatory)

> No tokens, no Stage 2. Tokens are layer ④ of the Five-Layer Blade. This file is the full spec — copy-paste ready.

## Why

Article line 973: **"按钮不认识 #2563EB,按钮只认识 button.primary.bg."** Hardcoded colors are the unmaintainable tell. Tokens make design, code, and AI generation all obey the same rules.

Article line 940: **"没有令牌,团队越大越乱;有了令牌,复杂产品才有秩序."**

## The three layers

### Layer 1 — Primitive (palette)
The raw materials. No meaning, just "what colors exist".

```text
color:
  gray-50  #F9FAFB
  gray-100 #F3F4F6
  gray-200 #E5E7EB
  gray-300 #D1D5DB
  gray-400 #9CA3AF
  gray-500 #6B7280
  gray-600 #4B5563
  gray-700 #374151
  gray-800 #1F2937
  gray-900 #111827

  blue-50  #EFF6FF
  blue-100 #DBEAFE
  blue-500 #3B82F6
  blue-600 #2563EB
  blue-700 #1D4ED8

  red-500  #EF4444
  red-600  #DC2626
  green-500 #10B981
  green-600 #059669
  amber-500 #F59E0B
  amber-600 #D97706

font:
  family-sans  "Inter", system-ui, sans-serif
  family-mono  "JetBrains Mono", monospace

space:
  1   4px
  2   8px
  3   12px
  4   16px
  5   20px
  6   24px
  8   32px
  10  40px
  12  48px
  16  64px

radius:
  sm   4px    (small badge, tag)
  md   8px    (button, input)
  lg   12px   (card)
  full 9999px (avatar, pill button)

shadow:
  sm   0 1px 2px rgba(0,0,0,0.05)
  md   0 4px 6px rgba(0,0,0,0.07)
  lg   0 10px 15px rgba(0,0,0,0.10)

duration:
  fast    100ms
  normal  200ms
  slow    300ms

easing:
  ease-out  cubic-bezier(0.16, 1, 0.3, 1)   (entrance)
  ease-in   cubic-bezier(0.7, 0, 0.84, 0)   (exit)
  standard  cubic-bezier(0.4, 0, 0.2, 1)    (general)
```

### Layer 2 — Semantic (job of the color)
Assigns a job. This is the layer themes (light/dark) swap.

```text
color.text:
  primary     gray-900      (body, headings)
  secondary   gray-500      (captions, hints)
  disabled    gray-400      (disabled text)
  inverse     white         (text on primary bg)
  link        blue-600
  danger      red-600
  success     green-600

color.bg:
  canvas      white         (page background)
  surface     white         (card background)
  muted       gray-50       (subtle sections)
  overlay     gray-900/40   (modal backdrop)

color.border:
  default     gray-200
  strong      gray-300
  focus       blue-500      (focus ring)
  danger      red-500

color.state:
  primary     blue-600      (primary actions)
  hover       blue-700
  active      blue-800
  danger-bg   red-50
  success-bg  green-50
  warning-bg  amber-50

font.size:
  xs    12px / 1.4
  sm    14px / 1.5    (body)
  md    16px / 1.5    (large body)
  lg    18px / 1.4    (subsection)
  xl    20px / 1.3    (section heading)
  2xl   24px / 1.2    (page heading)
  3xl   32px / 1.1    (hero)

font.weight:
  regular   400
  medium    500
  semibold  600

space.layout:
  section    space-12 (48px)
  block      space-6  (24px)
  element    space-3  (12px)
  inline     space-2  (8px)
```

### Layer 3 — Component (the part)
Maps semantic tokens to a specific component slot.

```text
button.primary:
  bg          color.state.primary
  bg.hover    color.state.hover
  bg.active   color.state.active
  bg.disabled gray-300
  text        color.text.inverse
  border      transparent
  radius      radius.md
  padding     space-2 space-4
  font        font.weight.medium, font.size.sm

button.secondary:
  bg          color.bg.surface
  bg.hover    gray-50
  border      color.border.default
  text        color.text.primary

input:
  bg          color.bg.canvas
  border      color.border.default
  border.focus color.border.focus
  text        color.text.primary
  placeholder color.text.secondary
  radius      radius.md
  padding     space-2 space-3

card:
  bg          color.bg.surface
  border      color.border.default
  radius      radius.lg
  padding     space-6
  shadow      shadow.sm

badge:
  bg          color.bg.muted
  text        color.text.secondary
  radius      radius.sm
  padding     space-1 space-2
```

## The rule

**Components never reference primitives directly.** A button uses `button.primary.bg` (component), which resolves to `color.state.primary` (semantic), which resolves to `blue-600` (primitive). Change the semantic mapping for dark mode, and every button follows.

## Dark mode

Article line 1189: **"深色模式也不是把白底黑字反一下."**

- dark bg uses deep gray (`gray-900`, `gray-800`), not pure black
- text uses off-white (`gray-100`), not pure white — pure white on pure black is harsh
- primary blue desaturates ~15% in dark mode (vivid colors glare on dark)
- shadow becomes "surface rises = slightly lighter" instead of drop-shadow

```text
DARK MODE semantic overrides:
  color.text.primary   gray-100
  color.text.secondary gray-400
  color.bg.canvas      gray-900
  color.bg.surface     gray-800
  color.bg.muted       gray-700/50
  color.border.default gray-700
  color.state.primary  blue-500 (desaturated)
```

## WCAG contrast (article line 764)

- body text: ≥ 4.5:1 against bg
- large text (≥ 18px or 14px bold): ≥ 3:1
- never use `gray-400` on `white` for body text (fails 4.5:1)
- focus ring: ≥ 3:1 against adjacent colors

## 8pt grid (article line 1082)

All spacing snaps to multiples of 4 (half-steps allowed: 4, 8, 12, 16, 20, 24, 32...). No "13px margin" or "7px gap". This is what makes a UI feel "orderly" instead of "almost".

## Failure modes

| Failure | Symptom | Fix |
| --- | --- | --- |
| Hardcoded color in component | `style="background: #2563EB"` | use `button.primary.bg` token |
| Missing semantic layer | component → primitive directly | add the semantic mapping |
| Dark mode = inverted colors | pure black + pure white | use deep gray + off-white |
| Non-grid spacing | 13px, 7px, 22px | snap to 4/8 grid |
| Low contrast body text | gray-400 on white | bump to gray-500 or darker |
