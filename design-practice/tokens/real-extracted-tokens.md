---
type: reference
created: 2026-06-27
source: computed CSS pulled live from 16 shipped world-class products (Playwright, headless chromium 1440px)
---

# Real Engineering Tokens — pulled from 16 shipped world-class products

> These are not invented. Each block is the ACTUAL computed token system of a live, shipped, world-class site, extracted from its CSS custom properties + computed styles. Use them as ground truth when you need real numbers (type scale, weight, radius, easing) instead of guessing. The aesthetic "feel" half lives in references/world-class-teardowns/ (Codex moodboard); this is the "numbers" half.

## linear — precision tool · dark
- **fonts**: Inter Variable · Berkeley Mono
- **font-weights in use**: 300, 400, 510, 590
- **type scale (px)**: 10, 11, 12, 13, 13.3333, 14, 15, 16, 18, 20, 24, 48, 64
- **type samples**: h1 64px/64px w510 ls-1.408px · h2 48px/48px w510 ls-1.056px · h3 20px/26.6px w590 ls-0.24px · p 15px/24px w400 ls-0.165px · a 14px/21px w510 lsnormal · button 13px/19.5px w400 lsnormal · label 16px/24px w400 lsnormal · li 16px/24px w400 lsnormal
- **radii**: 0px 4px 4px 0px, 0px 2px 2px 0px, 1px, 2px, 2px 0px 0px 2px, 4px, 4px 0px 0px 4px, 6px, 7px, 8px, 12px, 12px 12px 0px 0px, 16px, 20px, 22px, 50%, 400px, 9999px
- **easing curves**: cubic-bezier(0.25, 0.46, 0.45, 0.94) | cubic-bezier(0.25, 0.46, 0.45, 0.94), cubic-bezier(0.25, 0.46, 0.45, 0.94) | ease-out
- **durations**: 0.1s, 0.16s, 0.16s, 0.16s, 0.2s, 0.4s
- **palette (text colors)**: rgb(247, 248, 248) · rgb(255, 255, 255) · rgb(138, 143, 152) · rgb(8, 9, 10) · rgb(208, 214, 224) · rgb(226, 228, 230) · rgb(98, 102, 109) · rgb(226, 228, 231) · rgba(0, 0, 0, 0) · rgb(109, 120, 213)
- **backgrounds**: rgb(8, 9, 10) · rgb(94, 106, 210) · rgb(35, 37, 42) · rgb(229, 229, 230) · rgb(9, 10, 11) · rgb(16, 17, 18) · rgb(18, 20, 20) · rgba(255, 255, 255, 0.02)
- **top shadows**: `rgba(0, 0, 0, 0) 0px 8px 2px 0px, rgba(0, 0, 0, 0.01) 0px 5px 2px 0px, rgba(0, 0, 0, 0.04) 0px 3px 2px 0px, rgba(0, 0, 0, 0.07) 0px 1px 1px 0px, rgba(0, 0, 0, 0` · `rgba(0, 0, 0, 0.1) 0px 0px 0px 2px` · `rgba(0, 0, 0, 0.2) 0px 0px 0px 1px` · `rgb(35, 37, 42) 0px 0px 0px 1px inset`

**COLOR tokens** (named CSS vars, real):
```
--color-text-secondary: #d0d6e0
--color-text-tertiary: #8a8f98
--color-line-tertiary: #18191a
--color-white: #fff
--color-accent: #7170ff
--color-border-translucent: #ffffff0d
--color-line-secondary: #202122
--color-bg-level-3: #191a1b
--editor-text-color: #e4e5e9
--color-line-primary: #37393a
--color-fg-primary: #f7f8f8
--color-bg-quinary: #282828
--color-text-quaternary: #62666d
--color-border-secondary: #34343a
--color-accent-tint: #18182f
--color-accent-hover: #828fff
--header-bg: #0b0b0bcc
--color-line-quaternary: #141515
--color-black: #000
--color-border-tertiary: #3e3e44
--scrollbar-color-hover: #fff3
--color-link-hover: #fff
```

**TYPE tokens** (named CSS vars, real):
```
--font-variations: "opsz" auto
--text-large-line-height: 1.6
--title-1-line-height: 1.4
--font-size-title1: 2.25rem
--font-settings: "cv01", "ss03"
--title-3-letter-spacing: -.012em
--title-9-line-height: 1
--font-emoji: "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Segoe UI", "Twemoji Mozilla", "Noto Color Emoji", "Android Emoji"
--text-mini-letter-spacing: -.01em
--text-regular-letter-spacing: -.011em
--font-size-miniPlus: .75rem
--font-size-microPlus: .6875rem
--text-small-line-height: calc(21 / 14)
--editor-line-height: 1.6
```

**SPACE tokens** (named CSS vars, real):
```
--header-height: 72px
--editor-todolist-checkbox-width: 14px
--text-large-line-height: 1.6
--title-1-line-height: 1.4
--font-size-title1: 2.25rem
--text-micro-size: .75rem
--title-3-letter-spacing: -.012em
--editor-block-menu-size: 20px
--editor-last-invisible-paragraph-spacing: 10px
--title-9-line-height: 1
--scrollbar-size-active: 10px
--text-mini-letter-spacing: -.01em
--text-regular-size: .9375rem
--text-regular-letter-spacing: -.011em
```

**RADIUS tokens** (named CSS vars, real):
```
--editor-block-radius: 6px
--radius-rounded: 9999px
--radius-circle: 50%
--radius-8: 8px
--radius-12: 12px
--radius-32: 32px
--rounded-full: 9999px
--radius-24: 24px
--radius-4: 4px
--radius-6: 6px
--radius-16: 16px
```

**SHADOW tokens** (named CSS vars, real):
```
--btn-overlay-shadow-hover: none
--shadow-low: 0px 2px 4px #0000001a
--shadow-high: 0px 7px 32px #00000059
--shadow-tiny: 0px 0px 0px transparent
--btn-overlay-shadow: none
--shadow-none: 0px 0px 0px transparent
--shadow-medium: 0px 4px 24px #0003
--shadow-stack-low: 0px 8px 2px 0px #0000, 0px 5px 2px 0px #00000003, 0px 3px 2px 0px #0000000a, 0px 1px 1px 0px #00000012, 0px 0px 1px 0px #00000014
```

**MOTION tokens** (named CSS vars, real):
```
--ease-out-quad: cubic-bezier(.25, .46, .45, .94)
--speed-highlightFadeOut: .15s
--ease-in-out-quart: cubic-bezier(.77, 0, .175, 1)
--ease-in-out-circ: cubic-bezier(.785, .135, .15, .86)
--ease-out-quart: cubic-bezier(.165, .84, .44, 1)
--speed-quickTransition: .1s
--ease-in-circ: cubic-bezier(.6, .04, .98, .335)
--ease-in-quart: cubic-bezier(.895, .03, .685, .22)
--ease-in-out-cubic: cubic-bezier(.645, .045, .355, 1)
--ease-in-out-quint: cubic-bezier(.86, 0, .07, 1)
--ease-in-out-expo: cubic-bezier(1, 0, 0, 1)
--ease-out-circ: cubic-bezier(.075, .82, .165, 1)
--ease-out-quint: cubic-bezier(.23, 1, .32, 1)
--ease-in-quint: cubic-bezier(.755, .05, .855, .06)
```

---

## stripe — editorial fintech · white
- **fonts**: sohne-var
- **font-weights in use**: 300, 400, 500
- **type scale (px)**: 8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 26, 32, 48, 56
- **type samples**: h1 48px/55.2px w300 ls-0.96px · h2 32px/35.2px w300 ls-0.64px · h3 26px/29.12px w300 ls-0.26px · p 32px/35.2px w300 ls-0.64px · a 16px/normal w400 lsnormal · button 14px/14px w400 lsnormal · li 16px/normal w400 lsnormal
- **radii**: 0px 0px 6px 6px, 1px, 2px, 3px, 4px, 5px, 6px, 6px 6px 0px 0px, 6px 0px 0px 6px, 8px, 16px, 100%
- **easing curves**: cubic-bezier(0.45, 0.05, 0.55, 0.95) | cubic-bezier(0.4, 0, 0.2, 1) | cubic-bezier(0.45, 0.05, 0.55, 0.95), cubic-bezier(0.45, 0.05, 0.55, 0.95), cubic-bezier(0.45, 0.05, 0.55, 0.95) | cubic-bezier(0.6, 0, 0.2, 0.5) | cubic-bezier(0.25, 1, 0.5, 1), cubic-bezier(0.25, 1, 0.5, 1), cubic-bezier(0.25, 1, 0.5, 1) | cubic-bezier(0.25, 1, 0.5, 1) | ease-in | ease-in-out, ease-in-out, ease-in-out | linear | steps(1) | cubic-bezier(0.165, 0.84, 0.44, 1) | cubic-bezier(0.16, 1, 0.3, 1)
- **durations**: 0.1s, 0.12s, 0.15s, 0.15s, 0.15s, 0.2s, 0.2s, 0.2s, 0.24s, 0.24s, 0.24s, 0.24s, 0.25s, 0.25s, 0.25s, 0.1s, 0.3s, 0.3s, 0.3s, 0.3s, 0.3s, 0.3s, 0.4s, 0.4s, 0.4s, 0.5s, 0.5s, 0s, 0.6s, 0.8s, 1s, 1.2s
- **palette (text colors)**: rgb(0, 0, 0) · rgb(83, 58, 253) · rgb(6, 27, 49) · rgb(255, 255, 255) · rgb(100, 116, 141) · rgb(129, 184, 26) · rgba(0, 14, 255, 0.5) · rgb(45, 37, 100) · rgb(26, 44, 68) · rgb(39, 57, 81)
- **backgrounds**: rgba(255, 255, 255, 0.8) · rgb(83, 58, 253) · rgba(255, 255, 255, 0) · rgb(255, 255, 255) · rgb(232, 233, 255) · rgba(255, 255, 255, 0.65) · rgb(229, 237, 245) · rgb(255, 224, 209)
- **top shadows**: `rgba(0, 0, 0, 0.1) 0px 30px 60px -50px, rgba(50, 50, 93, 0.25) 0px 30px 60px -10px` · `rgba(23, 23, 23, 0.08) 0px 15px 35px 0px` · `rgba(23, 23, 23, 0.06) 0px 3px 6px 0px` · `rgba(50, 50, 93, 0.12) 0px 16px 32px 0px`

**COLOR tokens** (named CSS vars, real):
```
--hds-color-core-neutral-975: #0d253d
--hds-color-accent-border-solid: #533afd
--hds-color-accentColorMode-ruby-icon-solid: #ea2261
--hds-color-util-brand-900: #1c1e54
--hds-color-action-bg-subduedHover: #b9b9f9
--hds-color-input-text-label: #273951
--hds-color-accentColorMode-magenta-surface-subduedAlt: #ffe6f5
--hds-color-input-text-selected: #273951
--hds-color-input-text-popover: #273951
--hds-color-shadow-sm-top: #00377014
--hds-color-button-ui-iconHover: #2e2b8c
--hds-color-input-text-placeholder: #7d8ba4
--hds-color-core-brandDark-800A: #4b31d080
--hds-color-core-lemon-500: #9b6829
--hds-color-shadow-lg-top: #0037701a
--hds-color-util-bg-min: #fff
--hds-color-core-neutral-50A: #a8c3de4d
--hds-color-util-neutral-50: #e5edf5
--hds-color-input-selector-text-range: #665efd
--hds-color-accentColorMode-lemon-surface-subdued: #fff2d8
--hds-color-accentColorMode-magenta-icon-gradientMiddle: #f96bee
--hds-color-core-neutralDark-25: #f2f7fe
```

**TYPE tokens** (named CSS vars, real):
```
--hds-font-input-text-md-lineHeight: 1.3
--hds-font-heading-xs-lineHeight: 1.2
--hds-font-heading-md-letterSpacing: -0.01em
--hds-font-quoteAttribution-md-weight: 300
--hds-font-text-lg-letterSpacing: 0em
--hds-font-heading-md-weight: 300
--hds-font-heading-xl-lineHeight: 1.03
--hds-font-input-groupHeading-weight: 300
--hds-font-text-lg-lineHeight: 1.4
--hds-color-heading-subdued: #64748d
--hds-color-heading-solid: #061b31
--hds-font-input-description-lineHeight: 1.3
--hds-font-family: "sohne-var","SF Pro Display",sans-serif
--hds-font-text-xxl-letterSpacing: -0.02em
```

**SPACE tokens** (named CSS vars, real):
```
--hds-font-input-text-md-lineHeight: 1.3
--hds-space-core-1900: 152px
--hds-space-core-300: 24px
--hds-font-heading-xs-lineHeight: 1.2
--hds-space-core-250: 20px
--hds-space-core-2000: 160px
--hds-font-heading-md-letterSpacing: -0.01em
--hds-font-text-lg-letterSpacing: 0em
--hds-font-heading-xl-lineHeight: 1.03
--hds-space-input-text-paddingX-lg: 16px
--hds-space-input-text-paddingY-sm: 8px
--hds-font-text-lg-lineHeight: 1.4
--hds-font-input-description-lineHeight: 1.3
--hds-space-core-radius-none: 0px
```

**RADIUS tokens** (named CSS vars, real):
```
--hds-space-core-radius-none: 0px
--hds-space-core-radius-round: 99999px
--hds-space-core-radius-lg: 16px
--hds-space-button-radius-sm: 2px
--hds-space-core-radius-xs: 2px
--hds-space-core-radius-xl: 32px
--hds-space-core-radius-md: 6px
--hds-space-core-radius-sm: 4px
--hds-space-button-radius-lg: 4px
--navigation-border-radius: 6px
```

**SHADOW tokens** (named CSS vars, real):
```
--hds-shadow-sm-top-offset-y: 5px
--hds-shadow-sm-bottom-offset-y: 2px
--hds-color-shadow-sm-top: #00377014
--hds-shadow-xs-top-blur: 10px
--hds-shadow-xs-bottom-blur: 4px
--hds-color-shadow-lg-top: #0037701a
--hds-shadow-xs-top-offset-y: 2px
--hds-shadow-sm-bottom-offset-x: 0px
--hds-shadow-xl-bottom-offset-x: 0px
--hds-shadow-xl-bottom-offset-y: 10px
--hds-shadow-lg-bottom-blur: 20px
--hds-shadow-xl-bottom-spread: -16px
--hds-color-shadow-xl-bottom: #003b890f
--hds-shadow-sm-bottom-spread: 0px
```

**MOTION tokens** (named CSS vars, real):
```
--navigation-duration-slow: 300ms
--navigation-duration: 240ms
--navigation-hamburger-duration: 0.25s
```

---

## vercel — geek · pure black · geist
- **fonts**: Geist · Geist Mono
- **font-weights in use**: 400, 450, 500, 600
- **type scale (px)**: 8, 12, 13, 14, 16, 20, 22, 24, 30, 56, 64
- **type samples**: h1 64px/64px w400 ls-3.84px · h2 56px/56px w450 ls-3.36px · h3 12px/16px w400 ls0.6px · p 16px/24px w400 lsnormal · a 16px/24px w400 lsnormal · button 14px/20px w400 lsnormal · label 14px/21px w400 lsnormal · li 16px/24px w400 lsnormal
- **radii**: 2px, 4px, 6px, 8px, 3.35544e+07px, 3.35544e+07px 6px 6px 3.35544e+07px
- **easing curves**: cubic-bezier(0.4, 0, 0.2, 1) | linear | cubic-bezier(0, 0, 0.2, 1) | cubic-bezier(0.32, 0.72, 0, 1) | cubic-bezier(0.23, 1, 0.32, 1) | cubic-bezier(0.3, 0.57, 0.07, 0.95)
- **durations**: 0.1s, 0.15s, 0.2s, 0.25s, 0.3s, 0.4s, 0.5s, 0.7s, 1s, 1.2s
- **palette (text colors)**: rgb(23, 23, 23) · rgb(0, 114, 245) · rgb(0, 0, 0) · rgb(77, 77, 77) · rgb(255, 255, 255) · rgb(143, 143, 143) · rgba(0, 0, 0, 0) · rgb(125, 125, 125) · rgb(168, 168, 168) · rgb(102, 102, 102)
- **backgrounds**: rgb(255, 255, 255) · rgb(250, 250, 250) · rgb(23, 23, 23) · rgb(235, 235, 235) · oklab(0.984799 0.0000446141 0.0000197291 / 0.5) · rgb(102, 102, 102)
- **top shadows**: `rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgb(255, 255, 255) 0px 0` · `rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.04) 0px ` · `rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.1) 0px 1` · `rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgb(235, 235, 235) 0px 0`

**COLOR tokens** (named CSS vars, real):
```
--ds-shadow-border-large: 0 0 0 1px #00000014, 0px 2px 2px #0000000a, 0px 8px 16px -4px #0000000a, 0 0 0 1px hsla(0, 0%, 98%, 1)
--ship-text: #ff5b4f
--ds-focus-ring-outline: 2px solid hsla(212, 100%, 48%, 1)
--geist-console-text-color-default: #000
--color-gray-300: hsla(0, 0%, 90%, 1)
--geist-secondary-lighter: #eaeaea
--geist-violet-background-tertiary: #eae5f4
--geist-secondary-dark: #333
--ds-focus-ring: 0 0 0 2px hsla(0, 0%, 100%, 1), 0 0 0 4px hsla(212, 100%, 48%, 1)
--ds-background-200: hsla(0, 0%, 98%, 1)
--accents-3: #999
--dropdown-triangle-stroke: #fff
--accents-8: #111
--geist-selection-text-color: hsla(0, 0%, 95%, 1)
--accents-2: #eaeaea
--ds-shadow-border-small: 0 0 0 1px #00000014, 0px 2px 2px #0000000a, 0 0 0 1px hsla(0, 0%, 98%, 1)
--ds-contrast-fg: #fff
--ds-shadow-background-border: 0 0 0 1px hsla(0, 0%, 98%, 1)
--geist-console-text-color-blue: #0070f3
--geist-warning-lighter: #ffefcf
--accents-4: #888
--geist-secondary-light: #999
```

**TYPE tokens** (named CSS vars, real):
```
--text-base--line-height: calc(1.5 / 1)
--font-mono: "Geist Mono", ui-monospace, SFMono-Regular, Roboto Mono, Menlo, Monaco, Liberation Mono, DejaVu Sans Mono, Courier New, monospace, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol
--tracking-wider: .05em
--geist-form-small-font: .875rem
--font-weight-thin: 100
--geist-form-large-font: 1rem
--text-8xl--line-height: 1
--geist-form-small-line-height: .875rem
--default-font-family: "Geist", Arial, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol
--tracking-tighter: -.05em
--font-weight-extrabold: 800
--text-sm--line-height: calc(1.25 / .875)
--text-3xl--line-height: calc(2.25 / 1.875)
--font-weight-medium: 500
```

**SPACE tokens** (named CSS vars, real):
```
--geist-space-64x: 256px
--tw-inset-ring-shadow: 0 0 #0000
--text-base--line-height: calc(1.5 / 1)
--geist-space-small-negative: -32px
--tw-inset-shadow: 0 0 #0000
--banner-min-height: 64px
--tw-space-x-reverse: 0
--spacing-fluid-24-40: clamp(1.5rem, -.2143rem + 2.8571vi, 2.5rem)
--geist-space-16x: 64px
--geist-space-large-negative: -48px
--geist-space-gap-half-negative: -12px
--geist-gap-half: 12px
--geist-space-24x: 96px
--spacing-fluid-16-24: clamp(1rem, .1429rem + 1.4286vi, 1.5rem)
```

**RADIUS tokens** (named CSS vars, real):
```
--geist-radius: 6px
--geist-marketing-radius: 8px
--radius-3xl: 1.5rem
```

**SHADOW tokens** (named CSS vars, real):
```
--ds-shadow-border-large: 0 0 0 1px #00000014, 0px 2px 2px #0000000a, 0px 8px 16px -4px #0000000a, 0 0 0 1px hsla(0, 0%, 98%, 1)
--tw-inset-ring-shadow: 0 0 #0000
--tw-inset-shadow: 0 0 #0000
--dropdown-box-shadow: 0 4px 4px 0 #00000005
--tw-shadow-alpha: 100%
--ds-shadow-large: 0px 2px 2px #0000000a, 0px 8px 16px -4px #0000000a
--ds-shadow-border-small: 0 0 0 1px #00000014, 0px 2px 2px #0000000a, 0 0 0 1px hsla(0, 0%, 98%, 1)
--tw-ring-shadow: 0 0 #0000
--shadow-sticky: 0 12px 10px -10px #0000001f
--tw-drop-shadow-alpha: 100%
--ds-shadow-background-border: 0 0 0 1px hsla(0, 0%, 98%, 1)
--shadow-large: 0 30px 60px #0000001f
--tw-ring-offset-shadow: 0 0 #0000
--ds-shadow-small: 0px 2px 2px #0000000a
```

**MOTION tokens** (named CSS vars, real):
```
--ease-in: cubic-bezier(.4, 0, 1, 1)
--animate-cmdkScaleIn: cmdkScaleIn .3s cubic-bezier(.175, .885, .32, 1.1)
--animate-sandbox-left-reverse: sandbox-left-reverse .5s ease-in-out forwards
--animate-flip-front: flip-front .5s cubic-bezier(.4, .04, .04, 1) forwards
--animate-cmdkFadeIn: cmdkFadeIn .3s cubic-bezier(.175, .885, .32, 1.1)
--animate-sandbox-left: sandbox-left .5s ease-in-out forwards
--animate-cmdkScaleOut: cmdkScaleOut .3s cubic-bezier(.175, .885, .32, 1.1)
--tw-animation-direction: normal
--animate-feedbackFadeIn: feedbackFadeIn .1s cubic-bezier(.16, 1, .3, 1)
--animate-slide-in: slide-in 1.25s cubic-bezier(.4, .04, .04, 1) forwards
--animate-feedbackAppear: feedbackAppear .5s .1s ease forwards
--animate-loading-skeleton: loading-skeleton 1.5s ease-in-out infinite reverse
--animate-flip-back: flip-back .5s cubic-bezier(.4, .04, .04, 1) forwards
--animate-thinking-loader-fast: thinking-loader .85s linear infinite
```

---

## family — luxury · immersive craft
- **fonts**: Inter · Family · LFE Sans
- **font-weights in use**: 400, 500, 600
- **type scale (px)**: 12, 13, 13.3333, 14, 15, 16, 17, 19, 20, 23, 44, 68
- **type samples**: h1 68px/74.8px w500 ls-1.36px · p 14px/20px w400 ls-0.09px · a 16px/normal w500 lsnormal · button 15px/normal w500 ls-0.09px · li 16px/normal w400 lsnormal
- **radii**: 2px, 4px, 6px, 7.5%, 8px, 9.6px, 10px, 12px, 17px, 24px 0px 0px 24px, 32px, 40px, 50%, 72px
- **easing curves**: ease-out | cubic-bezier(0.19, 1, 0.22, 1) | ease-in-out
- **durations**: 0.1s, 0.18s, 0.2s, 0.22s, 0.4s, 1s
- **palette (text colors)**: rgb(71, 70, 69) · rgb(38, 38, 38) · rgb(40, 38, 36) · color(display-p3 0.203922 0.203922 0.2) · rgb(18, 18, 18) · rgb(132, 130, 129) · rgb(255, 255, 255) · rgb(0, 0, 0) · rgb(128, 128, 128) · rgba(71, 70, 69, 0.7)
- **backgrounds**: rgb(43, 47, 67) · rgb(255, 255, 255) · rgb(246, 244, 239) · rgb(23, 23, 23) · rgba(0, 0, 0, 0.05) · color(display-p3 0.984314 0.980392 0.976471) · rgb(0, 0, 0) · rgb(255, 0, 0)
- **top shadows**: `rgba(0, 0, 0, 0.1) 0px 3px 16px 0px` · `rgba(0, 0, 0, 0.04) 0px 0px 0px 1px` · `rgba(0, 0, 0, 0.15) 0px 0px 24px 0px` · `color(display-p3 0.94902 0.941176 0.929412) 0px 0px 0px 0px inset`

**COLOR tokens** (named CSS vars, real):
```
--background-invalid: #fff0f0
--color-text: #343433
--color-invalid: #FF4E4E
--color-border: #E8E8E8
--color-primary: #343433
--color-warning: #F6C30F
--color-valid: #00C454
--background-warning: #fefae6
--color-anchor: #6187FE
--background-valid: rgba(0,196,84,0.1)
--body-muted: color(display-p3 0.5176470588235295 0.5098039215686274 0.5058823529411764)
```

**TYPE tokens** (named CSS vars, real):
```
--heading: color(display-p3 0.20392156862745098 0.20392156862745098 0.2)
```

---

## arc — playful premium
- **fonts**: Marlin · Marlin Soft SQ · Exposure VAR · ABC Oracle · Times · -apple-system · ABC Favorit Mono · InterVariable
- **font-weights in use**: 400, 500, 600, 700, 800
- **type scale (px)**: 12, 13, 13.3333, 14, 16, 17, 20, 24, 28, 32, 36, 40, 45.51
- **type samples**: h1 32px/31.2px w700 ls-1.6px · p 20px/24px w400 lsnormal · a 16px/normal w400 lsnormal · button 13.3333px/normal w400 lsnormal · li 16px/normal w400 lsnormal
- **radii**: 4px, 8px, 10px, 22px
- **easing curves**: ease, ease | ease-in-out | ease, ease-out | ease-out
- **durations**: 0.1s, 0.15s, 0.15s, 0.2s
- **palette (text colors)**: rgb(0, 0, 0) · rgb(255, 255, 255) · rgba(0, 0, 0, 0.65) · rgb(255, 250, 221) · rgb(255, 252, 236) · rgb(39, 2, 194) · rgba(0, 0, 0, 0) · rgb(49, 57, 251) · rgb(105, 105, 105)
- **backgrounds**: rgb(49, 57, 251) · rgb(255, 255, 255) · rgb(255, 252, 236) · rgba(0, 0, 0, 0.85) · rgb(39, 2, 194)
- **top shadows**: `rgba(0, 0, 0, 0.25) 0px 2px 8px 0px` · `rgba(0, 0, 0, 0.1) 0px 5px 5px 0px`

**COLOR tokens** (named CSS vars, real):
```
--colors-focusOutline: #96C4FF
--colors-primary7: rgb(207, 56, 40)
--colors-highContrast: #000
--colors-students-light_grey-hover: rgb(215, 214, 196)
--colors-primary6: rgb(250, 69, 49)
--colors-brandOffwhite: #FFFCEC
--colors-secondary4: rgb(0, 130, 121)
--colors-secondary2: rgb(0, 201, 195)
--colors-brandDeepBlue: #2404AA
--colors-lowContrast: #FFF
--colors-students-light_green: rgb(211, 224, 129)
--colors-primary4: rgb(252, 130, 121)
--colors-primary12: rgb(9, 2, 1)
--colors-secondary7: rgb(0, 56, 40)
--colors-secondary11: rgb(0, 4, 2)
--colors-secondary5: rgb(0, 105, 88)
--colors-students-off_white: rgb(245, 244, 226)
--colors-primary11: rgb(26, 4, 2)
--colors-students-arc_pinkish: rgb(242, 94, 107)
--colors-students-dark_blue: rgb(39, 2, 194)
--colors-students-light_blue: rgb(205, 204, 223)
--colors-primary8: rgb(162, 43, 31)
```

**TYPE tokens** (named CSS vars, real):
```
--fontSizes-20: 20px
--lineHeights-20: 20px
--fonts-body: "InterVariable", "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen", "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif
--lineHeights-48: 48px
--fontSizes-24: 24px
--fontSizes-48: 48px
--fontWeights-700: 700
--fonts-boostSans: -apple-system, BlinkMacSystemFont, sans-serif
--fonts-sans: Marlin, -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen", "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif
--lineHeights-32: 32px
--fonts-exposure: "Exposure VAR", "Helvetica", sans-serif
--lineHeights-56: 56px
--lineHeights-24: 24px
--lineHeights-12: 12px
```

**SPACE tokens** (named CSS vars, real):
```
--space-16: 16px
--lineHeights-20: 20px
--space-72: 72px
--space-4: 4px
--space-40: 40px
--space-8: 8px
--space-32: 32px
--lineHeights-48: 48px
--padding: 32px
--space-64: 64px
--announcement-banner-height: 0px
--navbar-height: 64px
--lineHeights-32: 32px
--max-width: 1280px
```

**SHADOW tokens** (named CSS vars, real):
```
--shadows-large: 0 30px 60px rgba(0, 0, 0, 0.12)
--shadows-medium: 0 8px 30px rgba(0, 0, 0, 0.12)
--shadows-small: 0 5px 10px rgba(0, 0, 0, 0.12)
```

---

## notion — warm editorial
- **fonts**: NotionInter · Lyon Text
- **font-weights in use**: 400, 500, 600, 700
- **type scale (px)**: 0, 12, 14, 16, 18, 20, 22, 24, 32, 40, 42, 48, 54, 72, 96
- **type samples**: h1 96px/100px w600 ls-4.6px · h2 54px/56px w700 ls-1.875px · h3 22px/28px w700 ls-0.25px · p 14px/20px w400 lsnormal · a 16px/24px w400 lsnormal · button 16px/24px w400 lsnormal · li 12px/16px w500 ls0.125px
- **radii**: 4px, 5px, 8px, 8px 8px 0px 0px, 12px, 12px 0px 0px, 12px 12px 0px 0px, 16px, 50%, 100%, 9999px
- **easing curves**: cubic-bezier(0.42, 0, 1, 1) | ease-in-out | cubic-bezier(0.86, 0, 0.07, 1) | cubic-bezier(0.45, 0, 0.55, 1), cubic-bezier(0.45, 0, 0.55, 1) | cubic-bezier(0.45, 0, 0.55, 1) | cubic-bezier(0.645, 0.045, 0.355, 1) | cubic-bezier(0, 0, 0.58, 1) | cubic-bezier(0.42, 0, 1, 1), cubic-bezier(0.42, 0, 1, 1)
- **durations**: 0.1s, 0.15s, 0.15s, 0.15s, 0.2s, 0.2s, 0.2s, 0.3s
- **palette (text colors)**: rgba(0, 0, 0, 0.95) · rgba(0, 0, 0, 0.898) · rgba(0, 0, 0, 0.54) · rgb(0, 117, 222) · rgba(0, 0, 0, 0) · rgb(0, 0, 0) · rgb(255, 255, 255) · rgb(49, 48, 46) · rgb(9, 127, 232) · rgb(0, 91, 171)
- **backgrounds**: rgb(255, 255, 255) · rgb(242, 249, 255) · rgb(254, 243, 241) · rgb(255, 245, 224) · rgb(249, 249, 248) · rgb(0, 117, 222) · rgb(255, 201, 94) · rgb(247, 116, 99)
- **top shadows**: `rgba(0, 0, 0, 0) 0px 1px 0px 0px` · `rgba(0, 0, 0, 0.01) 0px 0.175px 1.041px 0px, rgba(0, 0, 0, 0.02) 0px 0.8px 2.925px 0px, rgba(0, 0, 0, 0.027) 0px 2.025px 7.847px 0px, rgba(0, 0, 0, 0.04) 0px 4p` · `rgba(0, 0, 0, 0.008) 0px 0.667px 3.502px 0px, rgba(0, 0, 0, 0.016) 0px 2.933px 7.252px 0px, rgba(0, 0, 0, 0.02) 0px 7.2px 14.462px 0px, rgba(0, 0, 0, 0.024) 0px`

**COLOR tokens** (named CSS vars, real):
```
--color-brown-900: #523410
--color-card-accent: #097fe8
--color-pink-500: #ff64c8
--color-orange-600: #dd5b00
--color-button-primary-background-active: #005bab
--color-orange-800: #793400
--color-teal-400: #2a9d99
--color-button-tertiary-text: #000000f2
--color-blue-700: #005bab
--color-alpha-black-100: #0000000d
--color-button-primary-border: #ffffff00
--color-purple-800: #391c57
--color-alpha-white-400: #ffffff4d
--color-action-button-primary-background-focus: #f6f5f4
--color-background-surface-neutral-focus: #dfdcd9
--color-background-surface-accent-muted: #f2f9ff
--color-code-comment: #0000008a
--color-terminal-text: #000000f2
--color-gray-300: #dfdcd9
--color-icon-button-active: #615d59
--color-gray-500: #78736f
--color-campaigns-dev-platform-dos-white: #ffffff
```

**TYPE tokens** (named CSS vars, real):
```
--font-letter-spacing-sans-1100-semibold: -0.2875rem
--typography-article-body-letter-spacing: 0
--typography-article-title-subtle-font: 700 2rem /2.5rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"
--typography-article-navigation-font: 400 0.875rem /1.25rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"
--typography-interaction-menu-list-heading-font: 500 0.75rem /1rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"
--typography-global-body-font: 400 1rem /1.5rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"
--typography-sans-1100-semibold-letter-spacing: -0.2875rem
--typography-serif-350-regular-font: 400 1.25rem /1.75rem "Lyon Text",Georgia,YuMincho,"Yu Mincho","Hiragino Mincho ProN","Hiragino Mincho Pro","Songti TC","Songti SC",SimSun,"Nanum Myeongjo",NanumMyeongjo,Batang,serif
--typography-serif-800-regular-letter-spacing: -0.125rem
--typography-sans-1000-regular-letter-spacing: -0.25rem
--typography-sans-600-bold-letter-spacing: -0.046875rem
--font-line-height-700: 3rem
--font-line-height-600: 2.5rem
--typography-sans-100-medium-letter-spacing: 0
```

**SPACE tokens** (named CSS vars, real):
```
--font-letter-spacing-sans-1100-semibold: -0.2875rem
--typography-article-body-letter-spacing: 0
--typography-sans-1100-semibold-letter-spacing: -0.2875rem
--dimension-spacing-0: 0
--typography-serif-800-regular-letter-spacing: -0.125rem
--typography-sans-1000-regular-letter-spacing: -0.25rem
--typography-sans-600-bold-letter-spacing: -0.046875rem
--font-line-height-700: 3rem
--font-line-height-600: 2.5rem
--spacing-card-padding-inline-block: 2rem
--typography-sans-100-medium-letter-spacing: 0
--spacing-gutter-md: 1.5rem
--font-line-height-900: 4rem
--dimension-spacing-12: 0.75rem
```

**RADIUS tokens** (named CSS vars, real):
```
--border-radius-800: 0.875rem
--border-radius-400: 0.375rem
--border-radius-300: 0.3125rem
--border-radius-900: 1rem
--border-radius-round: 624.9375rem
--border-menu-button-radius: 624.9375rem
--border-icon-button-radius: 0.25rem
--border-radius-600: 0.625rem
--border-radius-200: 0.25rem
--border-button-radius-lg: 0.625rem
--border-radius-0: 0
--border-popover-radius: 0.75rem
--border-menu-list-item-radius: 0.5rem
--border-block-media-radius: 0.75rem
```

**SHADOW tokens** (named CSS vars, real):
```
--shadow-200: 0px 0.175px 1.041px 0px rgb(0% 0% 0%/0.013),0px 0.8px 2.925px 0px rgb(0% 0% 0%/0.02),0px 2.025px 7.847px 0px rgb(0% 0% 0%/0.027),0px 4px 18px 0px rgb(0% 0% 0%/0.04)
--shadow-100: 0px 0.7px 1.462px 0px rgb(0% 0% 0%/0.015),0px 3px 9px 0px rgb(0% 0% 0%/0.03)
--shadow-300: 0px 0.667px 3.502px 0px rgb(0% 0% 0%/0.0096),0px 2.933px 7.252px 0px rgb(0% 0% 0%/0.0157),0px 7.2px 14.462px 0px rgb(0% 0% 0%/0.02),0px 13.867px 28.348px 0px rgb(0% 0% 0%/0.0243),0px 23.333px 52.123px
```

**MOTION tokens** (named CSS vars, real):
```
--motion-duration-300: 300ms
--motion-duration-250: 250ms
--motion-timing-function-ease-in: cubic-bezier(0.42,0,1,1)
--motion-duration-100: 100ms
--motion-global-fade-out-duration: 200ms
--motion-duration-200: 200ms
--motion-timing-function-ease-in-out-quint: cubic-bezier(0.86,0,0.07,1)
--motion-timing-function-linear: cubic-bezier(0,0,1,1)
--motion-timing-function-ease-in-out-cubic: cubic-bezier(0.645,0.045,0.355,1)
--motion-timing-function-ease-in-out-quad: cubic-bezier(0.45,0,0.55,1)
--motion-duration-150: 150ms
--motion-global-transform-timing-function: cubic-bezier(0.86,0,0.07,1)
--motion-timing-function-ease-out: cubic-bezier(0,0,0.58,1)
--motion-global-fade-out-timing-function: cubic-bezier(0.42,0,1,1)
```

---

## apple — product page craft
- **fonts**: SF Pro Text · SF Pro Display · Arial
- **font-weights in use**: 400, 600, 700
- **type scale (px)**: 10, 12, 13.3333, 14, 17, 21, 24, 28, 34, 40, 44, 56
- **type samples**: h1 34px/50px w600 ls-0.374px · h2 12px/16.0005px w400 ls-0.12px · h3 40px/44px w600 lsnormal · p 28px/32px w400 ls0.196px · a 17px/21.0012px w600 ls-0.374px · button 17px/25px w400 lsnormal · li 17px/25px w400 ls-0.374px
- **radii**: 5px, 8px, 50%, 980px, 999px
- **easing curves**: cubic-bezier(0.4, 0, 0.6, 1) | steps(1) | cubic-bezier(0.4, 0, 0.6, 1), cubic-bezier(0.4, 0, 0.6, 1), steps(1) | cubic-bezier(0.4, 0, 0.6, 1), cubic-bezier(0.4, 0, 0.6, 1), cubic-bezier(0.4, 0, 0.6, 1) | cubic-bezier(0.4, 0, 0.6, 1), steps(1, start) | cubic-bezier(0.25, 0.1, 0.3, 1) | cubic-bezier(0.4, 0, 0.6, 1), cubic-bezier(0.4, 0, 0.6, 1) | cubic-bezier(0.4, 0, 0.6, 1), steps(1) | linear | ease-in-out, ease-in-out, ease-in-out, ease-in-out, ease-in-out
- **durations**: 0.02s, 0.02s, 0.02s, 0.06s, 0.08s, 0.1s, 0.12s, 0.14s, 0.16s, 0.18s, 0.2s, 0.22s, 0.24s, 0.24s, 0.24s, 0.25s, 0.3s, 0.32s, 0.32s, 0.32s, 0.32s, 0.32s, 0.32s, 0.4s, 1s, 1s, 1s, 1s, 1s
- **palette (text colors)**: rgb(29, 29, 31) · rgba(0, 0, 0, 0.8) · rgb(110, 110, 115) · rgb(51, 51, 54) · rgb(0, 0, 0) · rgb(255, 255, 255) · rgb(0, 102, 204) · rgb(41, 151, 255) · rgb(245, 245, 247) · rgba(0, 0, 0, 0.48)
- **backgrounds**: rgb(250, 250, 252) · rgba(255, 255, 255, 0.8) · rgb(0, 0, 0) · rgba(232, 232, 237, 0.4) · rgb(245, 245, 247) · rgb(0, 113, 227) · rgba(210, 210, 215, 0.64) · rgb(244, 248, 251)
- **top shadows**: `rgba(0, 0, 0, 0.22) 3px 5px 30px 0px`

**COLOR tokens** (named CSS vars, real):
```
--r-globalnav-background-opened: #fafafc
--sk-body-text-color: rgb(29, 29, 31)
--sk-fill-secondary: rgb(250, 250, 252)
--sk-fill-tertiary: rgb(245, 245, 247)
--sk-fill-orange-secondary: rgb(255, 249, 244)
--sk-fill-gray-secondary: rgb(134, 134, 139)
--sk-fill-red: rgb(227, 0, 0)
--sk-fill-green-secondary: rgb(245, 255, 246)
--sk-fill: rgb(255, 255, 255)
--sk-fill-orange: rgb(245, 99, 0)
--sk-glyph-gray-secondary-alt-alpha: rgba(0, 0, 0, 0.72)
--sk-glyph-gray-secondary-alt: rgb(66, 66, 69)
--sk-focus-color: #0071e3
--sk-fill-green: rgb(3, 161, 14)
--sk-body-link-color: rgb(0, 102, 204)
--sk-fill-gray-tertiary: rgb(210, 210, 215)
--sk-fill-gray-tertiary-alpha: rgba(0, 0, 0, 0.16)
--sk-focus-color-alt: rgb(0, 0, 0)
--sk-fill-gray-secondary-alpha: rgba(0, 0, 0, 0.48)
--sk-fill-gray-alpha: rgba(0, 0, 0, 0.88)
--sk-fill-gray-quaternary-alpha: rgba(0, 0, 0, 0.08)
--sk-headline-text-color: rgb(29, 29, 31)
```

**TYPE tokens** (named CSS vars, real):
```
--sk-body-font-stack: text
--sk-footnote-font-size: 0.6em
--sk-footnote-reduced-font-size: .45em
```

**SPACE tokens** (named CSS vars, real):
```
--r-localnav-viewport-small-min-width: 320px
--hero-content-height: 692px
--r-localnav-viewport-medium-min-width: 834px
--globalnav-height: 44px
--media-gallery-dotnav-gap: 12px
--sk-footnote-font-size: 0.6em
--media-gallery-bottom-content-padding-right: 48px
--sk-paragraph-plus-element-margin: 0.8em
--r-sk-safe-area-inset-start: 0px
--sk-headline-plus-first-element-margin: 0.8em
--r-localnav-gn-height: 44px
--r-globalmessage-segment-height: 0px
--r-localnav-viewport-medium-max-width: 1023px
--media-gallery-section-padding-bottom: 12px
```

**MOTION tokens** (named CSS vars, real):
```
--media-gallery-slide-duration: 800ms
--media-gallery-bottom-copy-duration: 600ms
```

---

## figma — expressive product
- **fonts**: figmaSans · figmaMono
- **font-weights in use**: 320, 330, 400
- **type scale (px)**: 0, 12, 14, 16, 18, 24, 30, 44, 56, 88
- **type samples**: h1 56px/56px w400 ls-1.25px · h2 14px/18.2px w400 ls0.5px · h3 16px/22.4px w400 lsnormal · p 18px/25.2px w330 lsnormal · a 16px/23.2px w400 lsnormal · button 18px/25.2px w330 lsnormal · li 18px/25.2px w330 ls-0.14px
- **radii**: 2px, 4px, 8px, 16px, 24px, 50%, 9999px
- **easing curves**: ease-out, ease-out | ease-out | cubic-bezier(0.8, 0, 0.2, 1) | ease-out, ease-out, ease-out | ease, ease
- **durations**: 0.18s, 0.18s, 0.18s, 0.18s, 0.18s, 0.18s, 0.2s, 0.25s, 0.4s, 0.5s, 0.5s
- **palette (text colors)**: rgb(0, 0, 0) · rgb(255, 255, 255) · oklch(0 0 none / 0.54) · rgba(255, 255, 255, 0.6) · rgb(128, 128, 128)
- **backgrounds**: rgb(255, 255, 255) · rgb(0, 0, 0) · oklch(0 0 none / 0.08) · oklch(0 0 none / 0) · oklch(0 0 none / 0.04) · rgba(255, 255, 255, 0.24) · rgba(255, 255, 255, 0.16) · rgba(0, 0, 0, 0.5)
- **top shadows**: `oklch(0 0 none / 0.16) 0px 1px 0px 0px` · `oklch(0 0 none / 0.16) 0px 0px 0px 1px inset` · `rgba(0, 0, 0, 0.1) 0px 10px 15px -3px, rgba(0, 0, 0, 0.05) 0px 4px 6px -2px`

**COLOR tokens** (named CSS vars, real):
```
--fig-theme-btn-primary-bg: #000000
--fig-theme-fg: #000000
--fig-theme-form-input-bg: color-mix(in oklch, #000000, transparent 92%)
--fig-theme-card-bg: color-mix(in oklch, #000000, transparent 96%)
--fig-theme-border-hover: color-mix(in oklch, #000000, transparent 60%)
--fig-theme-btn-transparent-bg-hover: color-mix(in oklch, #000000, transparent 92%)
--fig-theme-border: color-mix(in oklch, #000000, transparent 84%)
--fig-theme-btn-ghost-bg-hover: color-mix(in oklch, #000000, transparent 96%)
--fig-theme-form-error-fg: #FFFFFF
--fig-theme-form-error-bg: #972121
--fig-theme-badge-bg: color-mix(in oklch, #000000, transparent 92%)
--fig-theme-btn-primary-bg-hover: color-mix(in oklch, #000000, transparent 15%)
--fig-theme-bg: #FFFFFF
--fig-theme-btn-transparent-bg: color-mix(in oklch, #000000, transparent 96%)
--fig-theme-btn-secondary-bg: color-mix(in oklch, #000000, transparent 100%)
--fig-theme-btn-transparent-fg: #000000
--fig-theme-badge-fg: #000000
--fig-theme-btn-ghost-bg: color-mix(in oklch, #000000, transparent 100%)
--fig-theme-btn-primary-fg: #FFFFFF
--fig-theme-fg-muted: color-mix(in oklch, #000000, transparent 46%)
--fig-theme-btn-secondary-fg: #000000
```

**TYPE tokens** (named CSS vars, real):
```
--global-font-mono: "figmaMono","figmaMono Fallback",SF Mono,menlo,monospace
--font-figma-sans: "figmaSans","figmaSans Fallback",SF Pro Display,system-ui,helvetica,sans-serif
--fig-typography-size-display1: 5.5rem
--font-figma-mono: "figmaMono","figmaMono Fallback",SF Mono,menlo,monospace
--global-font-sans: "figmaSans","figmaSans Fallback",SF Pro Display,system-ui,helvetica,sans-serif
--fig-typography-weight: normal
--fig-typography-size-display2: 4rem
```

**SPACE tokens** (named CSS vars, real):
```
--fig-typography-size-formLabel: 0.75rem
--fig-grid-max-content-width: 95rem
--f-lego-block-padding: 7.5rem
--fig-section-block-padding: 5rem
--fig-space-8: 0.5rem
--fig-typography-size-title1: 3.5rem
--fig-typography-size-button: 1rem
--fig-space-12: 0.75rem
--fig-typography-size-caption: 0.875rem
--fig-typography-size-display1: 5.5rem
--f-col-width: calc(min(100vw, 1440px) / 48)
--fig-space-120: 7.5rem
--fig-grid-gutter: 1rem
--fig-typography-size-bodyXL: 1.5rem
```

**RADIUS tokens** (named CSS vars, real):
```
--fig-radius-full: 9999px
--fig-radius-24: 1.5rem
--fig-radius-28: 1.75rem
--fig-radius-8: 0.5rem
--fig-radius-2: 0.125rem
--fig-radius-12: 0.75rem
--fig-radius-4: 0.25rem
--fig-radius-16: 1rem
```

**SHADOW tokens** (named CSS vars, real):
```
--fig-elevation-1-shadow: 0 0.25rem 2rem color-mix(in oklch, #000000, transparent 90%)
--fig-elevation-2: 0 1.5rem 4.375rem 0 color-mix(in oklch, #000000, transparent 90%)
--fig-elevation-2-shadow: 0 1.5rem 4.375rem color-mix(in oklch, #000000, transparent 90%)
--fig-elevation-1: 0 0.25rem 2rem 0 color-mix(in oklch, #000000, transparent 90%)
```

---

## raycast — dark dev tool
- **fonts**: Inter · GeistMono · SF Pro · SF Pro Text
- **font-weights in use**: 300, 400, 500, 600, 700
- **type scale (px)**: 10, 11, 12, 13, 14, 16, 18, 20, 22, 23.75, 24, 32, 56, 64
- **type samples**: h1 64px/70.4px w600 lsnormal · h2 20px/normal w500 ls0.2px · h3 24px/normal w500 ls0.2px · p 18px/normal w400 ls0.2px · a 16px/18.4px w400 lsnormal · button 12px/13.8px w400 lsnormal
- **radii**: 0px 0px 12px 12px, 2px, 2.5px, 3px, 4px, 5px, 6px, 8px, 9px, 11px, 12px, 16px, 19px, 20px, 22px, 31px, 36px, 43px, 86px, 100%, 1000px, 99999px
- **easing curves**: ease, ease | ease-in-out | ease, ease, ease-in-out, ease-in-out | cubic-bezier(0.23, 1, 0.32, 1), cubic-bezier(0.23, 1, 0.32, 1), cubic-bezier(0.23, 1, 0.32, 1), cubic-bezier(0.23, 1, 0.32, 1), cubic-bezier(0.23, 1, 0.32, 1), cubic-bezier(0.23, 1, 0.32, 1) | ease-in-out, ease-in-out | cubic-bezier(0.165, 0.84, 0.44, 1) | cubic-bezier(0.075, 0.82, 0.165, 1), cubic-bezier(0.075, 0.82, 0.165, 1) | cubic-bezier(0.075, 0.82, 0.165, 1) | cubic-bezier(0.23, 1, 0.32, 1)
- **durations**: 0.15s, 0.2s, 0.2s, 0.2s, 0.2s, 0.1s, 0.3s, 0.3s, 0.3s, 0.3s, 0.5s, 0.4s, 0.2s, 0.2s, 0.2s, 0.4s, 0.4s, 0.4s, 0.5s, 0.3s, 0.5s, 0.25s, 0.5s, 0.5s, 1s, 1.2s, 1.5s, 2s
- **palette (text colors)**: rgb(255, 255, 255) · rgb(156, 156, 157) · rgb(47, 48, 49) · rgb(106, 107, 108) · rgba(0, 0, 0, 0) · rgba(255, 255, 255, 0.4) · rgba(255, 255, 255, 0.6) · rgb(230, 230, 230) · rgb(255, 99, 99) · rgb(67, 67, 69)
- **backgrounds**: rgba(255, 255, 255, 0.9) · rgb(230, 230, 230) · rgb(69, 35, 36) · rgb(19, 13, 14) · rgb(7, 8, 10) · rgb(255, 255, 255) · rgba(0, 0, 0, 0.44) · rgba(255, 255, 255, 0.1)
- **top shadows**: `rgba(255, 255, 255, 0.15) 0px 1px 1px 0px inset` · `rgba(0, 0, 0, 0.5) 0px 0px 0px 2px, rgba(255, 255, 255, 0.19) 0px 0px 14px 0px, rgba(0, 0, 0, 0.2) 0px -1px 0.4px 0px inset, rgb(255, 255, 255) 0px 1px 0.4px 0p` · `rgba(245, 48, 107, 0.1) 0px 0px 20px 0px` · `rgba(255, 255, 255, 0.03) 0px 0px 40px 20px, rgba(255, 255, 255, 0.3) 0px 0.5px 0px 0px inset`

**COLOR tokens** (named CSS vars, real):
```
--color-blue-transparent: hsla(202,100%,67%,0.15)
--key-bg-end-color: rgb(13, 13, 13)
--key-bg-start-color: rgb(18, 18, 18)
--color-bg-100: rgb(16,17,17)
--color-bg: #07080a
--color-button-fg: rgb(24,25,26)
--background: #07080a
--reverse-background: #ffffff
--color-yellow: hsl(43,100%,60%)
--color-fg-300: #78787c
--color-button-bg-hover: hsl(0,0%,100%)
--color-button-bg: hsla(0,0%,100%,0.815)
--color-border: hsl(195,5%,15%)
--color-red: hsl(0,100%,69%)
--color-bg-400: rgb(73,75,77)
--color-green: hsl(151,59%,59%)
--color-blue: hsl(202,100%,67%)
--color-fg: hsl(240,11%,96%)
--color-red-transparent: hsla(0,100%,69%,0.15)
--color-green-transparent: hsla(151,59%,59%,0.15)
--color-yellow-transparent: hsla(43,100%,60%,0.15)
--color-fg-400: rgb(94,99,102)
```

**TYPE tokens** (named CSS vars, real):
```
--main-font: "Inter","Inter Fallback",sans-serif
--font-color-rgb: 255,255,255
--reverse-font-color-rgb: 0,0,0
--monospace-font: "JetBrains Mono","JetBrains Mono Fallback",Menlo,Monaco,Courier,monospace
--font-jetbrains-mono: "JetBrains Mono","JetBrains Mono Fallback"
--font-geist-mono: "GeistMono",ui-monospace,SFMono-Regular,Roboto Mono,Menlo,Monaco,Liberation Mono,DejaVu Sans Mono,Courier New,monospace
--font-inter: "Inter","Inter Fallback"
```

**SPACE tokens** (named CSS vars, real):
```
--container-xs-width: 746px
--spacing-4: 32px
--spacing-1: 8px
--spacing-9: 80px
--spacing-13: 224px
--spacing-6: 48px
--spacing-1-5: 12px
--spacing-12: 168px
--removed-body-scroll-bar-size: 0px
--spacing-8: 64px
--grid-gap: 32px
--navbar-height: 76px
--spacing-none: 0px
--spacing-2: 16px
```

**RADIUS tokens** (named CSS vars, real):
```
--radius-md: 6px
```

**MOTION tokens** (named CSS vars, real):
```
--spring-1: linear(0.000000 0%,0.005927 1%,0.022466 2%,0.047872 3%,0.080554 4%,0.119068 5%,0.162116 6%,0.208536 7.000000000000001%,0.2573 8%,0.3075 9%,0.358346 10%,0.409157 11%,0.45935 12%,0.508438 13%,0.556014 1
```

---

## resend — clean dev · minimal
- **fonts**: inter · domaine · aBCFavorit · commitMono · -apple-system · Helvetica
- **font-weights in use**: 400, 500, 600, 700
- **type scale (px)**: 12, 14, 16, 18, 20, 24, 56, 96
- **type samples**: h1 96px/96px w400 ls-0.96px · h2 56px/67.2px w400 ls-2.8px · p 18px/27px w400 lsnormal · a 16px/24px w400 lsnormal · button 16px/24px w400 lsnormal · li 16px/24px w400 lsnormal
- **radii**: 0px 8px 8px 0px, 4px, 6px, 8px, 8px 0px 0px 8px, 10px, 12px, 16px, 16px 16px 0px 0px, 24px, 3.35544e+07px
- **easing curves**: cubic-bezier(0.4, 0, 0.2, 1) | cubic-bezier(0.4, 0, 1, 1) | ease-out | ease-in-out, ease-in-out, ease | cubic-bezier(0.36, 0.66, 0.6, 1) | cubic-bezier(0, 0, 0.2, 1)
- **durations**: 0.15s, 0.2s, 0.3s, 0.5s, 1s, 0.6s, 0.3s
- **palette (text colors)**: rgb(240, 240, 240) · rgba(241, 247, 254, 0.71) · rgb(161, 164, 165) · rgb(255, 255, 255) · rgba(0, 0, 0, 0) · rgb(161, 252, 234) · rgba(252, 253, 255, 0.937) · rgb(235, 236, 237) · rgb(70, 74, 77) · rgb(108, 108, 108)
- **backgrounds**: rgb(0, 0, 0) · rgb(11, 14, 20) · rgb(240, 240, 240) · rgba(34, 255, 153, 0.118) · rgba(214, 235, 253, 0.19) · rgba(131, 84, 254, 0.21) · rgba(0, 119, 255, 0.227) · rgba(250, 130, 0, 0.133)
- **top shadows**: `rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.1) 0px 1` · `rgb(0, 0, 0) 0px 0px 0px 8px` · `rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(176, 199, 217, 0.145) 0px 0px 0px 1px, rgba(0, 0, 0, `

**COLOR tokens** (named CSS vars, real):
```
--color-orange-4: #ff590039
--color-orange-10: #ff801f
--color-green-4: #11ff992d
--text-placeholder: #52595b
--color-green-3: #22ff991e
--color-yellow-9: #ffc53d
--color-gray-a3: #b0c7d925
--color-blue-5: #0081fd6b
--color-gray-12: #f0f0f0
--color-light-slate-3: #0000330f
--color-gray-2: #191b1e
--color-blue-4: #0075ff57
--color-blue-10: #3b9eff
--color-orange-11: #ffa057
--color-white: #fff
--color-black-12: #000000f2
--color-light-gray-a3: #d9d9d9
--color-red-5: #ff204756
--color-black-6: #0006
--text-on-accent: #000
--color-gray-11: #a1a4a5
--color-orange-7: #ff832c75
```

**TYPE tokens** (named CSS vars, real):
```
--font-abc-favorit: "aBCFavorit"
--text-base--line-height: calc(1.5 / 1)
--tracking-wider: .05em
--font-mono: "commitMono", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace
--font-domaine-src: "domaine"
--text-9xl--line-height: 1
--font-weight-bold: 700
--text-xs--line-height: calc(1 / .75)
--font-domaine: "domaine", ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"
--leading-relaxed: 1.625
--leading-snug: 1.375
--text-2xl--line-height: calc(2 / 1.5)
--text-xl--line-height: calc(1.75 / 1.25)
--leading-tight: 1.25
```

**SPACE tokens** (named CSS vars, real):
```
--tw-inset-shadow-alpha: 100%
--tw-inset-ring-shadow: 0 0 #0000
--text-base--line-height: calc(1.5 / 1)
--text-9xl--line-height: 1
--tw-inset-shadow: 0 0 #0000
--text-xs--line-height: calc(1 / .75)
--tw-space-x-reverse: 0
--text-2xl--line-height: calc(2 / 1.5)
--spacing: .25rem
--text-xl--line-height: calc(1.75 / 1.25)
--tw-border-spacing-y: 0px
--tw-space-y-reverse: 0
--text-4xl--line-height: calc(2.5 / 2.25)
--text-5xl--line-height: 1
```

**RADIUS tokens** (named CSS vars, real):
```
--radius-4xl: 2rem
--radius-sm: .25rem
--radius-2xl: 1rem
--radius-md: .375rem
--radius-lg: .5rem
--radius-3xl: 1.5rem
--radius-xs: .125rem
--radius-xl: .75rem
```

**SHADOW tokens** (named CSS vars, real):
```
--tw-inset-shadow-alpha: 100%
--tw-inset-ring-shadow: 0 0 #0000
--tw-inset-shadow: 0 0 #0000
--tw-shadow-alpha: 100%
--scroll-shadow-line-color: #212629
--shadow-4xl: 2px 13px 68px 7px #0000001a
--shadow-button: 0px 0px 4px #ffffff0f, 0px 1px 14px #ffffff1f, 0px 3px 32px #ffffff2e
--tw-ring-shadow: 0 0 #0000
--tw-drop-shadow-alpha: 100%
--shadow-3xl: 0 0 60px 30px #f2f2f2
--tw-ring-offset-shadow: 0 0 #0000
--tw-shadow: 0 0 #0000
```

**MOTION tokens** (named CSS vars, real):
```
--ai-shimmer-speed: 2s
--ease-in: cubic-bezier(.4, 0, 1, 1)
--animate-fade-out: fade-out .2s ease
--animate-header-slide-down-fade: header-slide-down-fade 1s ease-in-out
--default-transition-duration: .15s
--animate-pulse: pulse 2s cubic-bezier(.4, 0, .6, 1) infinite
--animate-ai-shimmer-text: ai-shimmer-text 2.5s linear infinite
--animate-disco-border: disco 6s linear infinite
--animate-open-scale-in-fade: open-scale-in-fade .2s ease-in-out
--default-transition-timing-function: cubic-bezier(.4, 0, .2, 1)
--ai-border-speed: 3s
--ease-out: cubic-bezier(0, 0, .2, 1)
--animate-close-scale-out-fade: close-scale-out-fade .2s ease-in-out
--animate-close-slide-up-fade: close-slide-up-fade .2s
```

---

## rauno — craft / interaction detail
- **fonts**: X
- **font-weights in use**: 400, 500
- **type scale (px)**: 13.3333, 14, 16, 32, 75, 85, 720
- **type samples**: h1 32px/normal w500 lsnormal · h3 720px/normal w400 lsnormal · p 85px/normal w400 lsnormal · a 16px/normal w400 lsnormal · button 13.3333px/normal w400 lsnormal
- **radii**: 12px, 9999px
- **easing curves**: ease-in-out | ease-in-out, ease-in-out, ease-in-out
- **durations**: 0.15s, 0.2s, 0.2s, 0.2s
- **palette (text colors)**: rgb(0, 0, 0) · rgb(23, 23, 23) · rgb(111, 111, 111)
- **backgrounds**: rgb(255, 255, 255) · rgb(255, 255, 2) · color(display-p3 0.99 0.4 0.02) · rgb(143, 143, 143)
- **top shadows**: —

**COLOR tokens** (named CSS vars, real):
```
--colors-focus: hsl(0 0% 56.1%)
--colors-blue10: hsl(208 100% 47.3%)
--colors-grayA9: hsl(0 0% 0% / 0.439)
--colors-green7: hsl(146 38.5% 69.0%)
--colors-gray7: hsl(0 0% 85.8%)
--colors-green9: hsl(151 55.0% 41.5%)
--colors-teal2: hsl(169 64.7% 96.7%)
--colors-blue2: hsl(210 100% 98.0%)
--colors-blueA9: hsl(206 100% 50.0% / 0.980)
--colors-grayA10: hsl(0 0% 0% / 0.478)
--colors-blueA8: hsl(206 99.8% 45.1% / 0.632)
--colors-blue3: hsl(209 100% 96.5%)
--colors-green3: hsl(139 55.2% 94.5%)
--colors-grayA11: hsl(0 0% 0% / 0.565)
--colors-gray6: hsl(0 0% 88.7%)
--colors-grayA2: hsl(0 0% 0% / 0.027)
--colors-teal4: hsl(169 53.1% 90.2%)
--colors-amber10: hsl(35 100% 55.5%)
--colors-teal8: hsl(172 42.1% 52.5%)
--colors-grayA7: hsl(0 0% 0% / 0.141)
--colors-red9: hsl(358 75.0% 59.0%)
--colors-blue6: hsl(209 81.2% 84.5%)
```

**TYPE tokens** (named CSS vars, real):
```
--fontSizes-20: 20px
--lineHeights-20: 20px
--lineHeights-48: 48px
--fonts-serif: Georgia, serif
--fontSizes-48: 48px
--lineHeights-32: 32px
--lineHeights-56: 56px
--lineHeights-24: 24px
--fontWeights-800: 800
--fontSizes-10: 10px
--fontWeights-400: 400
--fontSizes-12: 12px
--lineHeights-40: 40px
--fontSizes-32: 32px
```

**SPACE tokens** (named CSS vars, real):
```
--lineHeights-20: 20px
--space-9: 72px
--space-4: 32px
--space-7: 56px
--space-8: 64px
--lineHeights-48: 48px
--space-5: 40px
--lineHeights-32: 32px
--lineHeights-56: 56px
--lineHeights-24: 24px
--space-3: 24px
--space-1: 8px
--space-10: 80px
--lineHeights-40: 40px
```

**SHADOW tokens** (named CSS vars, real):
```
--shadows-large: 0 30px 60px rgba(0, 0, 0, 0.12)
--shadows-medium: 0 8px 30px rgba(0, 0, 0, 0.12)
--shadows-tooltip: 0px 4px 8px 0px rgba(0, 0, 0, 0.04), 0px 1px 1px 0px rgba(0, 0, 0, 0.02)
--shadows-small: 0 5px 10px rgba(0, 0, 0, 0.12)
```

**MOTION tokens** (named CSS vars, real):
```
--transitions-snappy: cubic-bezier(.2, .8, .2, 1)
```

---

## emil — animation craft
- **fonts**: Sans
- **font-weights in use**: 400, 500
- **type scale (px)**: 14, 16
- **type samples**: p 14px/23.1px w400 lsnormal · a 14px/23.1px w500 lsnormal · button 14px/20px w400 lsnormal · label 16px/24px w400 lsnormal
- **radii**: 6px, 8px, 9999px
- **easing curves**: cubic-bezier(0.4, 0, 0.2, 1)
- **durations**: 0.15s
- **palette (text colors)**: rgb(0, 0, 0) · rgb(33, 32, 28) · rgb(99, 99, 94) · rgb(253, 253, 252)
- **backgrounds**: rgb(249, 249, 248) · rgb(255, 255, 255) · rgb(33, 32, 28)
- **top shadows**: `rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.08) 0px 0px 0px 1px, rgba(0, 0, 0, 0.04) 0px 2px 2px 0px`

**COLOR tokens** (named CSS vars, real):
```
--color-gray-alpha-100: #00000003
--ds-shadow-border-large: 0 0 0 1px rgba(0,0,0,.08),0px 2px 2px rgba(0,0,0,.04),0px 8px 16px -4px rgba(0,0,0,.04)
--color-gray-800: #bcbbb5
--shiki-foreground: #21201c
--color-gray-alpha-600: #00000026
--color-gray-alpha-800: #00000044
--brand: #fad657
--color-gray-alpha-700: #00000031
--color-gray-alpha-300: #0000000f
--color-gray-alpha-400: #00000017
--color-gray-300: #f1f0ef
--ds-inset-border: inset 0 0 0 1px rgba(0,0,0,.08)
--tw-ring-color: rgba(59,130,246,.5)
--scrollbar-color-active: rgba(0,0,0,.3)
--color-gray-500: #e2e1de
--color-gray-1000: #82827c
--color-gray-alpha-900: #00000072
--color-gray-900: #8d8d86
--tw-ring-offset-color: #fff
--ds-shadow-border: 0 0 0 1px rgba(0,0,0,.08)
--color-gray-700: #cfceca
--ds-shadow-border-small: 0 0 0 1px rgba(0,0,0,.08),0px 2px 2px rgba(0,0,0,.04)
```

**TYPE tokens** (named CSS vars, real):
```
--font-variations: "opsz" auto
--font-serif-inline: "serifInline","serifInline Fallback"
--font-settings: "cv01","ss03"
--font-mono: "Mono","Mono Fallback"
--font-sans: "Sans","Sans Fallback"
--font-serif: "Serif","Serif Fallback"
```

**SPACE tokens** (named CSS vars, real):
```
--tw-border-spacing-x: 0
--ds-inset-border: inset 0 0 0 1px rgba(0,0,0,.08)
--tw-ring-offset-width: 0px
--tw-border-spacing-y: 0
--ds-inset-border-light: inset 0 0 0 1px rgba(0,0,0,.08)
```

**SHADOW tokens** (named CSS vars, real):
```
--tw-ring-offset-shadow: 0 0 #0000
--tw-ring-shadow: 0 0 #0000
--ds-shadow-border-large: 0 0 0 1px rgba(0,0,0,.08),0px 2px 2px rgba(0,0,0,.04),0px 8px 16px -4px rgba(0,0,0,.04)
--ds-shadow-fullscreen: 0 0 0 1px rgba(0,0,0,.08),0px 1px 1px rgba(0,0,0,.02),0px 8px 16px -4px rgba(0,0,0,.04),0px 24px 32px -8px rgba(0,0,0,.06)
--ds-shadow-small: 0px 2px 2px rgba(0,0,0,.04)
--ds-shadow-menu: 0 0 0 1px rgba(0,0,0,.08),0px 1px 1px rgba(0,0,0,.02),0px 4px 8px -4px rgba(0,0,0,.04),0px 16px 24px -8px rgba(0,0,0,.06)
--ds-shadow-tooltip: 0 0 0 1px rgba(0,0,0,.08),0px 1px 1px rgba(0,0,0,.02),0px 4px 8px rgba(0,0,0,.04)
--ds-shadow-large: 0px 2px 2px rgba(0,0,0,.04),0px 8px 16px -4px rgba(0,0,0,.04)
--ds-shadow-border: 0 0 0 1px rgba(0,0,0,.08)
--ds-shadow-border-small: 0 0 0 1px rgba(0,0,0,.08),0px 2px 2px rgba(0,0,0,.04)
--ds-shadow-modal: 0 0 0 1px rgba(0,0,0,.08),0px 1px 1px rgba(0,0,0,.02),0px 8px 16px -4px rgba(0,0,0,.04),0px 24px 32px -8px rgba(0,0,0,.06)
--ds-shadow-medium: 0px 2px 2px rgba(0,0,0,.04),0px 8px 8px -8px rgba(0,0,0,.04)
--tw-shadow: 0 0 #0000
--tw-shadow-colored: 0 0 #0000
```

---

## supabase — dev platform · dark green
- **fonts**: Circular · Source Code Pro
- **font-weights in use**: 400, 500
- **type scale (px)**: 12, 14, 16, 18, 24, 36, 72
- **type samples**: h1 72px/72px w400 lsnormal · h2 16px/24px w400 lsnormal · h3 36px/43.2px w400 lsnormal · p 14px/19.25px w500 lsnormal · a 16px/24px w400 lsnormal · button 14px/16px w500 lsnormal · small 12px/16px w400 lsnormal · li 14px/20px w500 lsnormal
- **radii**: 6px, 8px, 11px, 12px, 16px, 3.35544e+07px
- **easing curves**: cubic-bezier(0.4, 0, 0.2, 1) | cubic-bezier(0, 0, 0.2, 1) | ease-out
- **durations**: 0.075s, 0.15s, 0.2s, 0.3s, 0.75s, 1s
- **palette (text colors)**: rgb(23, 23, 23) · rgb(82, 82, 82) · rgb(112, 112, 112) · rgb(63, 207, 142) · rgba(0, 0, 0, 0) · rgb(178, 178, 178) · rgb(0, 187, 104)
- **backgrounds**: oklab(0.990884 0.0000451207 0.0000197887 / 0.9) · rgb(253, 253, 253) · rgb(114, 227, 173) · rgb(255, 255, 255) · rgb(252, 252, 252) · rgb(112, 112, 112) · rgb(169, 241, 202) · rgb(63, 207, 142)
- **top shadows**: `rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px` · `rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.1) 0px 1`

**COLOR tokens** (named CSS vars, real):
```
--color-purple-300: #f9f1fe
--colors-slate-light-alpha-200: #05294d08
--color-pink-500: #f9d8ec
--color-orange-600: #ffcca7
--color-orange-800: #fa934e
--color-neutral-600: oklch(43.9% 0 0)
--color-violet-1100: #5746af
--colors-slate-light-alpha-1000: #00101b82
--color-blue-700: #96c7f2
--color-neutral-300: oklch(87% 0 0)
--color-purple-800: #be93e4
--color-brand-600: hsl(156.5deg 86.5% 26.1%)
--colors-gray-dark-alpha-200: #ffffff08
--color-gray-300: #f3f3f3
--color-amber-300: #fff4d5
--color-gray-500: #e8e8e8
--colors-gray-light-alpha-200: #00000008
--color-brand-300: hsl(147.5deg 72% 80.4%)
--color-green-500: #ccebd7
--color-white: #fff
--color-gray-400: #ededed
--color-blue-400: #e1f0ff
```

**TYPE tokens** (named CSS vars, real):
```
--font-family-body: Inter
--text-base--line-height: calc(1.5 / 1)
--tracking-wider: .05em
--text-8xl--line-height: 1
--default-font-family: Circular,custom-font,Helvetica Neue,Helvetica,Arial,sans-serif
--tracking-tighter: -.05em
--font-weight-extrabold: 800
--text-sm--line-height: calc(1.25 / .875)
--text-3xl--line-height: calc(2.25 / 1.875)
--tracking-widest: .1em
--font-weight-medium: 500
--font-weight-normal: 400
--default-mono-font-family: Source Code Pro,Office Code Pro,Menlo,monospace
--font-weight-bold: 700
```

**SPACE tokens** (named CSS vars, real):
```
--tw-inset-ring-shadow: 0 0 #0000
--text-base--line-height: calc(1.5 / 1)
--spacing-scale: 2px
--tw-inset-shadow: 0 0 #0000
--borderwidth-md: 4px
--tw-space-x-reverse: 0
--spacing-lg: 32px
--card-padding-x-md: 1.5rem
--tw-space-y-reverse: 0
--text-8xl--line-height: 1
--spacing-xl: 64px
--content-width-screen-xl: 1128px
--tw-ring-offset-width: 0px
--auth-ui-card-height: 50vh
```

**RADIUS tokens** (named CSS vars, real):
```
--borderradius-lg: 8px
--radius-sm: .25rem
--borderradius-sm: 4px
--radius-md: .375rem
--radius-lg: .5rem
--borderradius-xs: 2px
--borderradius-xl: 16px
--radius-2xl: 1rem
--borderradius-tableheader: 4px
--radius-3xl: 1.5rem
--radius-xs: .125rem
--radius-xl: .75rem
```

**SHADOW tokens** (named CSS vars, real):
```
--tw-inset-ring-shadow: 0 0 #0000
--tw-inset-shadow: 0 0 #0000
--tw-shadow-alpha: 100%
--tw-ring-shadow: 0 0 #0000
--tw-drop-shadow-alpha: 100%
--tw-ring-offset-shadow: 0 0 #0000
--drop-shadow-xs: 0 1px 1px #0000000d
--tw-shadow: 0 0 #0000
--tw-inset-shadow-alpha: 100%
--drop-shadow-lg: 0 4px 4px #00000026
--drop-shadow-md: 0 3px 3px #0000001f
```

**MOTION tokens** (named CSS vars, real):
```
--animate-dropdown-content-show: overlayContentShow .1s cubic-bezier(.16,1,.3,1)
--ease-in: cubic-bezier(.4,0,1,1)
--animate-slide-down: slideDown .3s cubic-bezier(.87,0,.13,1)
--animate-dropdown-content-hide: overlayContentHide .1s cubic-bezier(.16,1,.3,1)
--animate-panel-slide-right-out: panelSlideRightOut .2s cubic-bezier(.87,0,.13,1)
--animate-line-loading-slower: lineLoading 2.3s infinite
--animate-marquee-vertical: marquee-vertical 180s linear infinite both
--animate-collapsible-down: collapsible-down .1s ease-out
--animate-slide-up: slideUp .3s cubic-bezier(.87,0,.13,1)
--tw-animation-direction: normal
--animate-panel-slide-left-in: panelSlideLeftIn .25s cubic-bezier(.87,0,.13,1)
--animate-slide-up-normal: slideUpNormal .3s cubic-bezier(.87,0,.13,1)
--animate-slide-in: slideIn .25s ease-in both
--tw-animation-fill-mode: none
```

---

## framer — design tool · expressive
- **fonts**: sans-serif · Inter Variable · GT Walsheim Medium · Inter · Input Mono Bold · Input Mono Regular · Inter Medium · JetBrains Mono
- **font-weights in use**: 400, 500, 600, 700
- **type scale (px)**: 0, 9, 10, 12, 13, 14, 15, 16, 17, 18, 20, 44, 54
- **type samples**: h1 54px/54px w500 ls-2.16px · h2 44px/48.4px w500 ls-1.76px · h3 18px/23.4px w400 ls-0.01px · p 14px/14px w400 ls-0.01px · a 12px/normal w400 lsnormal · button 16px/normal w500 ls-0.2px · li 12px/normal w400 lsnormal
- **radii**: 1px, 3px, 4px, 5px, 6px, 7px, 8px, 9px, 10px, 12px, 14px, 15px, 18px, 18px 0px 0px, 19px, 20px, 21px, 25px, 25px 0px 0px, 26px, 30px, 50px, 50%, 100px
- **easing curves**: cubic-bezier(0, 0, 1, 1)
- **durations**: —
- **palette (text colors)**: rgb(0, 0, 0) · rgb(0, 0, 238) · rgb(255, 255, 255) · rgba(255, 255, 255, 0.6) · rgb(153, 153, 153) · rgb(102, 102, 102) · rgb(68, 68, 68) · rgb(204, 204, 204) · rgb(0, 153, 255) · rgba(255, 255, 255, 0.5)
- **backgrounds**: rgb(0, 0, 0) · rgba(255, 255, 255, 0.1) · rgb(255, 255, 255) · rgba(15, 15, 15, 0.95) · rgba(255, 255, 255, 0) · rgb(17, 17, 17) · rgb(36, 36, 36) · rgba(31, 31, 31, 0)
- **top shadows**: `rgba(0, 0, 0, 0.15) 0px 10px 20px 0px, rgba(255, 255, 255, 0.05) 0px 1px 0px 0px inset` · `rgb(17, 17, 17) 0px 0px 0px 2px` · `rgb(17, 17, 17) 0px 0px 0px 1.5px` · `rgba(0, 153, 255, 0.15) 0px 1px 2px 0px, rgba(0, 153, 255, 0.2) 0px 2px 4px 0px`

**RADIUS tokens** (named CSS vars, real):
```
--one-if-corner-shape-supported: 1
```

---

## mintlify — docs · clean
- **fonts**: inter · paperMono · arizonaFlare
- **font-weights in use**: 400, 500
- **type scale (px)**: 12, 14, 16, 18, 24, 35, 36, 44, 50
- **type samples**: h1 50px/52px w400 ls-2px · h2 24px/28px w500 ls-0.24px · h3 16px/24px w500 lsnormal · p 18px/24px w400 lsnormal · a 16px/24px w400 lsnormal · button 14px/16px w500 lsnormal · li 16px/24px w400 lsnormal
- **radii**: 2px, 4px, 6px, 12px 12px 0px 0px, 12px, 24px 24px 0px 0px, 3.35544e+07px
- **easing curves**: cubic-bezier(0, 0, 0.2, 1) | cubic-bezier(0.4, 0, 0.2, 1) | cubic-bezier(0.23, 1, 0.32, 1) | cubic-bezier(0.22, 1, 0.36, 1) | cubic-bezier(0, 0, 0, 1) | cubic-bezier(0.4, 0, 0.2, 1), cubic-bezier(0.34, 1.56, 0.64, 1)
- **durations**: 0.1s, 0.15s, 0.2s, 0.28s, 0.28s, 0.3s, 0.5s, 0.7s
- **palette (text colors)**: rgb(0, 0, 0) · lab(2.42579 -0.165291 -0.470081) · lab(2.42579 -0.165291 -0.470081 / 0.6) · lab(100 0 0) · lab(2.42579 -0.165291 -0.470081 / 0.8) · lab(51.3415 -41.5657 15.3527) · rgb(12, 140, 94) · rgba(0, 0, 0, 0) · rgb(18, 23, 21) · rgb(113, 125, 121)
- **backgrounds**: lab(100 0 0) · lab(2.42579 -0.165291 -0.470081 / 0.03) · lab(2.42579 -0.165291 -0.470081) · rgb(254, 253, 251) · rgba(31, 167, 122, 0.08) · rgb(250, 248, 245) · oklab(0 0 0 / 0.02) · rgba(0, 0, 0, 0.04)
- **top shadows**: `rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.06) 0px 0px 0px 1px, rgba(0, 0, 0, 0) 0px `

**COLOR tokens** (named CSS vars, real):
```
--twoslash-tag-bg: rgba(55,114,207,.125)
--consent-widget-link-text-color: #121715
--collapsible-content-color: #485450
--accordion-icon-color: #485450
--consent-widget-accordion-content-color: #5c5c5c
--color-neutral-300: #cfcdca
--button-shadow-primary: 0 1px 2px hsla(0, 0%, 0%, 0.05),inset 0 0 0 1px #0c8c5e
--consent-widget-branding-link-color: #0c8c5e
--consent-banner-background-color: #fefdfb
--color-speedy-mint: #18e299
--consent-widget-border-color-dark: rgba(0,0,0,.06)
--tabs-list-background: #fefdfb
--consent-dialog-foreground-color: #121715
--consent-dialog-overlay-background-color-dark: color-mix(in oklab, #0a0b0f 50%, transparent)
--color-white: #fff
--consent-widget-background-color-dark: #fefdfb
--consent-widget-accordion-background-color: #fefdfb
--legal-links-color: #476cff
--twoslash-popup-bg: #f3f7f6
--color-pink-2: #ffa3d3
--consent-widget-accordion-content-color-dark: #999
--color-background-tertiary: #ebe9e6
```

**TYPE tokens** (named CSS vars, real):
```
--consent-widget-title-line-height: 1.25
--text-base--line-height: calc(1.5/1)
--consent-dialog-title-font-size: 0.875rem
--consent-widget-title-weight: 600
--consent-dialog-title-font-weight: 600
--c15t-font-weight-normal: 400
--button-font-size: 0.875rem
--preference-item-leading-gap: .5rem
--consent-widget-line-height: 1.15
--consent-dialog-description-font-size: 1rem
--twoslash-code-font-size: 1em
--c15t-line-height-tight: 1.25
--frame-line-height: 1.5
--consent-dialog-branding-letter-spacing: -.01em
```

**SPACE tokens** (named CSS vars, real):
```
--preference-item-gap: .75rem
--consent-dialog-branding-icon-width: auto
--consent-widget-title-line-height: 1.25
--tw-inset-ring-shadow: 0 0 transparent
--text-base--line-height: calc(1.5/1)
--consent-dialog-title-font-size: 0.875rem
--tw-inset-shadow: 0 0 transparent
--button-font-size: 0.875rem
--preference-item-leading-gap: .5rem
--legal-links-gap: .75rem
--consent-widget-line-height: 1.15
--accordion-padding: 1rem
--consent-dialog-description-font-size: 1rem
--consent-widget-accordion-stack-gap: .75rem
```

**RADIUS tokens** (named CSS vars, real):
```
--accordion-radius: 8px
--radius-4xl: 2rem
--c15t-radius-sm: 4px
--frame-placeholder-border-radius: 1.25rem
--radius-sm: .25rem
--radius-md: .375rem
--radius-lg: .5rem
--c15t-radius-lg: 12px
--c15t-radius-md: 8px
--consent-dialog-card-radius: 12px
--consent-widget-radius: 0
--c15t-radius-full: 9999px
--radius-2xl: 1rem
--consent-banner-border-radius: 12px
```

**SHADOW tokens** (named CSS vars, real):
```
--button-shadow-neutral-hover: none
--accordion-focus-shadow: 0 0 0 2px #0c8c5e
--button-shadow-primary: 0 1px 2px hsla(0, 0%, 0%, 0.05),inset 0 0 0 1px #0c8c5e
--tw-inset-ring-shadow: 0 0 transparent
--tw-inset-shadow: 0 0 transparent
--button-shadow-neutral-hover-dark: none
--tw-shadow-alpha: 100%
--button-shadow-neutral: 0 1px 2px hsla(0, 0%, 0%, 0.05),inset 0 0 0 1px lab(2.42579% -.165291 -.470081/.03)
--button-shadow-neutral-focus-dark: 0 0 0 2px #0c8c5e
--tw-ring-shadow: 0 0 transparent
--tw-drop-shadow-alpha: 100%
--button-shadow-primary-hover-dark: none
--button-shadow-dark: 0 1px 2px hsla(0, 0%, 0%, 0.05)
--consent-banner-shadow-dark: 0 8px 24px hsla(0, 0%, 0%, 0.12)
```

**MOTION tokens** (named CSS vars, real):
```
--color-speedy-mint: #18e299
--legal-links-transition: text-decoration .2s ease
--frame-placeholder-animation: c15t-ui-fadeIn-moBzd .15s cubic-bezier(.165,.84,.44,1)forwards
--accordion-ease: cubic-bezier(0.4, 0, 0.2, 1)
--button-hover-transition-full: background-color 280ms/**/cubic-bezier(0.4, 0, 0.2, 1),box-shadow 280ms/**/cubic-bezier(0.4, 0, 0.2, 1),color 280ms/**/cubic-bezier(0.4, 0, 0.2, 1)
--c15t-duration-slow: 200ms
--c15t-easing-spring: cubic-bezier(0.34, 1.56, 0.64, 1)
--consent-widget-exit-animation: c15t-ui-exit-Yh5ig 280ms/**/cubic-bezier(0.4, 0, 0.2, 1)
--button-hover-transition-color: background-color 280ms/**/cubic-bezier(0.4, 0, 0.2, 1)
--c15t-duration-fast: 280ms
--consent-dialog-animation-timing: ease-out
--consent-banner-exit-animation: c15t-ui-exit-Z4gI_ 280ms/**/cubic-bezier(0.4, 0, 0.2, 1)
--consent-dialog-animation-duration: 150ms
--consent-widget-accordion-ease: cubic-bezier(0.4, 0, 0.2, 1)
```

---

## v00 — ai builder
- **fonts**: GeistSans · GeistMono · Times
- **font-weights in use**: 400, 500, 600
- **type scale (px)**: 10, 13, 14, 16, 18, 20, 24, 32, 48
- **type samples**: h1 32px/40px w600 ls-1.28px · h2 24px/32px w600 ls-0.96px · h3 48px/56px w600 ls-2.88px · p 14px/20px w400 lsnormal · a 14px/20px w500 lsnormal · button 14px/20px w500 lsnormal · li 16px/24px w400 lsnormal
- **radii**: 0px 0px 12px 12px, 4px, 6px, 8px, 12px 12px 0px 0px, 12px, 16px, 35px, 3.35544e+07px
- **easing curves**: cubic-bezier(0.4, 0, 0.2, 1) | cubic-bezier(0.31, 0.1, 0.08, 0.96) | cubic-bezier(0.3, 0.1, 0.1, 0.95) | cubic-bezier(0.34, 1.56, 0.64, 1) | cubic-bezier(0, 0, 0.2, 1)
- **durations**: 0.15s, 0.2s, 0.3s, 0.35s, 0.5s, 0.6s, 1s
- **palette (text colors)**: oklch(0.205 0 0) · oklch(0.51 0 0) · oklch(1 0 0) · rgba(0, 0, 0, 0) · oklch(0.732 0 0) · oklch(0.59 0 0) · rgb(0, 0, 0)
- **backgrounds**: oklch(0.985 0 0) · oklch(1 0 0) · oklch(0.205 0 0) · oklch(0.961 0 0) · oklch(0.94 0 0) · oklch(0 0 0 / 0.078)
- **top shadows**: `rgba(0, 0, 0, 0.02) 0px 1px 1px 0px, rgba(0, 0, 0, 0.04) 0px 4px 8px -4px, rgba(0, 0, 0, 0.06) 0px 16px 24px -8px` · `rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px` · `rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.08) 0px ` · `rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.25) 0px `

**COLOR tokens** (named CSS vars, real):
```
--color-v0-red-800: oklch(58.2% .2049 24.8)
--sh-string: #00e7c1
--fides-overlay-background-color: #f7fafc
--ship-text: #ff5b4f
--color-v0-gray-900: oklch(51% 0 0)
--color-v0-amber-1000: oklch(30.7% .0771 44.5)
--color-v0-amber-200: oklch(96.8% .042 91.4)
--geist-console-text-color-default: #000
--color-v0-green-1000: oklch(28.8% .0449 147.7)
--color-v0-gray-100: oklch(96.1% 0 0)
--fides-overlay-primary-button-text-color: #fff
--geist-secondary-lighter: #eaeaea
--fides-overlay-form-input-background-color: #f7fafc
--color-primary-foreground: oklch(100% 0 0)
--v0-caveat-button-primary-focus: oklch(35% 0 0)
--color-v0-amber-700: oklch(81.7% .164 75.9)
--color-v0-blue-300: oklch(94.8% .026 247.4)
--fides-overlay-gpc-applied-background-color: #38a169
--color-v0-alpha-700: oklch(0% 0 0/.439)
--geist-violet-background-tertiary: #eae5f4
--fides-overlay-secondary-button-text-color: #2d3748
--fides-overlay-background-dark-color: #e2e8f0
```

**TYPE tokens** (named CSS vars, real):
```
--text-base--line-height: calc(1.5 / 1)
--tracking-wider: .05em
--text-9xl--line-height: 1
--fides-overlay-font-size-buttons: calc(16px*0.875)
--fides-overlay-title-font-color: #4a5568
--fides-overlay-font-color: #4a5568
--geist-form-small-font: .875rem
--font-weight-thin: 100
--geist-form-large-font: 1rem
--text-8xl--line-height: 1
--geist-form-small-line-height: .875rem
--tracking-tighter: -.05em
--font-weight-extrabold: 800
--text-sm--line-height: calc(1.25 / .875)
```

**SPACE tokens** (named CSS vars, real):
```
--fides-overlay-padding: 24px
--geist-space-64x: 256px
--tw-inset-ring-shadow: 0 0 #0000
--text-base--line-height: calc(1.5 / 1)
--fides-overlay-width: 680px
--geist-space-small-negative: -32px
--text-9xl--line-height: 1
--tw-inset-shadow: 0 0 #0000
--fides-overlay-modal-secondary-button-group-height: calc(calc(16px*0.875) + 4px*2)
--fides-overlay-font-size-buttons: calc(16px*0.875)
--tw-space-x-reverse: 0
--geist-space-16x: 64px
--geist-space-large-negative: -48px
--geist-space-gap-half-negative: -12px
```

**RADIUS tokens** (named CSS vars, real):
```
--radius-4xl: 2rem
--radius-sm: calc(.5rem - 4px)
--radius-md: calc(.5rem - 2px)
--radius-lg: .5rem
--fides-overlay-badge-border-radius: 4px
--radius: .5rem
--fides-overlay-form-input-border-radius: 4px
--fides-overlay-container-border-radius: 12px
--fides-overlay-component-border-radius: 4px
--geist-radius: 5px
--geist-marketing-radius: 8px
--radius-3xl: 1.5rem
--fides-overlay-language-button-border-radius: 4px
--fides-overlay-button-border-radius: 6px
```

**SHADOW tokens** (named CSS vars, real):
```
--ds-shadow-border-large: 0 0 0 1px #00000014, 0px 2px 2px #0000000a, 0px 8px 16px -4px #0000000a
--tw-inset-ring-shadow: 0 0 #0000
--tw-inset-shadow: 0 0 #0000
--dropdown-box-shadow: 0 4px 4px 0 #00000005
--tw-shadow-alpha: 100%
--ds-shadow-large: 0px 2px 2px #0000000a, 0px 8px 16px -4px #0000000a
--shadow-xl: 0 20px 25px -5px #0000001a, 0 8px 10px -6px #0000001a
--ds-shadow-border-small: 0 0 0 1px #00000014, 0px 1px 2px #0000000a
--tw-ring-shadow: 0 0 #0000
--shadow-sticky: 0 12px 10px -10px #0000001f
--tw-drop-shadow-alpha: 100%
--shadow-sm: 0 0 0 1px hsl(0, 0%, 0%, .08), 0px 2px 1px 0px #0000000a
--shadow-large: 0 30px 60px #0000001f
--tw-ring-offset-shadow: 0 0 #0000
```

**MOTION tokens** (named CSS vars, real):
```
--ease-in: cubic-bezier(.4, 0, 1, 1)
--tw-animation-direction: normal
--ds-motion-popover-timing: cubic-bezier(.175, .885, .32, 1.1)
--tw-animation-fill-mode: forwards
--ds-motion-popover-duration: .2s
--tw-animation-delay: 0s
--default-transition-duration: .15s
--animate-pulse: pulse 2s cubic-bezier(.4, 0, .6, 1) infinite
--default-transition-timing-function: cubic-bezier(.4, 0, .2, 1)
--tw-animation-iteration-count: 1
--ds-motion-overlay-timing: cubic-bezier(.175, .885, .32, 1.1)
--ease-out: cubic-bezier(0, 0, .2, 1)
--animate-bounce: bounce 1s infinite
--ds-motion-timing-swift: cubic-bezier(.175, .885, .32, 1.1)
```

---

