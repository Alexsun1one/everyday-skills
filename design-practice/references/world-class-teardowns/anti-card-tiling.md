# Anti-Card-Tiling Layout Patterns

> ℹ️ **Canonical version is `references/web-craft/06-anti-card-tiling.md`** (more complete: 6 layout systems + ASCII + CSS + decision tree + anti-plastic checklist). This file is a supplementary second take — read web-craft/06 first; use this only for extra examples.

The plastic default is "centered headline + three equal cards." It is weak because it makes all ideas peer-level, kills narrative direction, and hides the real constraint the page should solve. Cards are fine for repeated entities. They are not a universal composition system.

## 1. Editorial Asymmetric Grid

**Why it is better:** it creates sequence and emphasis before the user reads. A large claim, narrow proof rail, image bleed, and small footnote field immediately tell the eye what matters.

**Engineering constraints:** define named grid areas, not ad hoc absolute positioning. Use 12 columns desktop, 4 columns tablet, 1 column mobile. Let the hero claim and proof rail stack on mobile while preserving order.

**Use when:** the page needs thought leadership, trust, research, or a premium content rhythm.

**Pitfall:** asymmetry without alignment becomes messy. Every irregular edge still needs a grid reason.

## 2. Bento With Size Contrast

**Why it is better:** bento works when module sizes encode importance. A 5x3 proof block plus 1x1 status modules is hierarchy; six equal tiles are just cards with rounded corners.

**Engineering constraints:** use explicit grid spans and aspect ratios. Limit radius to the product style. Reserve content overflow behavior for each module.

**Use when:** the product has multiple capabilities but one or two must dominate.

**Pitfall:** decorative bento with meaningless screenshots becomes trend cosplay.

## 3. Overlap / Bleed Composition

**Why it is better:** overlap expresses relationship: API over transaction map, product screenshot over compliance proof, photo crossing text column. It implies depth and editorial direction.

**Engineering constraints:** define z-index layers and safe overlap zones. Add contrast masks for text over media. Disable or simplify overlap under narrow breakpoints.

**Use when:** the page needs to show system relationships rather than peer feature bullets.

**Pitfall:** random overlap is worse than cards. Overlap must mean dependency, sequence, or evidence.

## 4. Magazine Feature + Sidebar

**Why it is better:** a feature story layout gives the page pacing: headline, standfirst, pull quote, image, index, sidebar proof. It feels authored.

**Engineering constraints:** control text measure at 55-72 characters, keep pull quotes out of the main reading order for screen readers, and art-direct image crops.

**Use when:** editorial, culture, premium services, founder narratives, research reports.

**Pitfall:** using a serif headline alone does not make a magazine layout. The page needs rhythm, not just font flavor.

## 5. Data Cockpit

**Why it is better:** professional users do not want feature cards; they want simultaneous context. Split panes, tables, timelines, maps, and inspectors show that the product can survive real work.

**Engineering constraints:** use deterministic row heights, sticky headers, virtualized tables, keyboard navigation, and cross-highlighting tokens. Keep semantic colors reserved for state.

**Use when:** analytics, trading, ops, security, observability, admin, logistics.

**Pitfall:** if every pane has its own visual style, density becomes chaos.

## 6. Split Pane + Inspector

**Why it is better:** a master-detail layout exposes workflow. The user sees the object list, selected item, and decision controls in one frame.

**Engineering constraints:** fixed nav width, flexible main pane, inspector min/max width, resizable splitters if needed. On mobile, inspector becomes a sheet with preserved selection state.

**Use when:** project management, documents, issue tracking, CRM, asset review, technical editors.

**Pitfall:** do not hide the inspector behind a modal if comparison is the core task.

## 7. Timeline / Path / Rail

**Why it is better:** rails turn a page into a journey. A vertical chapter rail, horizontal deployment path, or diagonal narrative current gives the user a route through complex content.

**Engineering constraints:** build the rail as navigation, not decoration. It needs current state, keyboard focus, scroll sync, and reduced-motion behavior.

**Use when:** launches, case studies, onboarding, process explanation, immersive scroll.

**Pitfall:** a decorative line that does not match content order creates false structure.

## 8. Object-As-Stage

**Why it is better:** instead of cards describing the product, the product/object becomes the composition. Labels, controls, details, and proof attach to the object itself.

**Engineering constraints:** reserve the object canvas with aspect ratio, anchor labels to object coordinates, test crop behavior at mobile and desktop, and provide text fallback.

**Use when:** luxury products, hardware, maps, 3D scenes, scientific/technical visualization.

**Pitfall:** a beautiful object with disconnected marketing copy is just a wallpaper hero.

## 9. One Giant Proof + Micro Evidence

**Why it is better:** one strong proof surface creates belief faster than many small claims. Micro evidence around it adds credibility without flattening hierarchy.

**Engineering constraints:** choose the proof object first: API response, real screenshot, benchmark trace, before/after, map, invoice, terminal, table. Surround it with annotations, not cards.

**Use when:** developer tools, fintech, AI products, infrastructure, enterprise trust.

**Pitfall:** fake proof is worse than no proof. If the screenshot/API/table is decorative, users feel the fraud.

## Rescue Checklist

If a page is drifting into card tiling, ask:

1. What is the single most important proof object?
2. Which items are truly peer-level, and which are supporting evidence?
3. Can one section become a split pane, timeline, map, table, or object stage?
4. Does color encode meaning or just decorate?
5. Can hierarchy be created with span, crop, overlap, or rail before adding another card?
6. What happens on mobile: stack, sheet, carousel, or simplified proof?

