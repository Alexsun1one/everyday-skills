# World-Class Web Teardowns

> ⚠️ **READ `00-moodboard-tokens.md` FIRST — it carries the authoritative aesthetic tokens AND the hard image-gen rule.** Critical caveat: these moodboard images are valid as **mood/direction only** (palette, composition, type personality). They are **NOT UI specs**. The dense SaaS / tool / data directions (precision-tool interiors, data-dense terminal) fall apart on zoom — fake data, off-grid alignment, no real component system: *skin without skeleton.* The "Extract First" column below means *aesthetic intent*, never literal UI tokens. For SaaS / tool / dashboard specs, the only valid source is real shipped products → `tokens/00-token-synthesis.md`.

This corpus is for `design-practice`: visual intuition first, engineering tokens second. The moodboard images are synthetic references generated with Image Gen, using fictional products so the style can be studied without copying real brands.

Image generation status: 12/12 generated. No missing image-gen items.

## Moodboard Index

| File | Direction | Extract First | Do Not Copy |
|---|---|---|---|
| `moodboard/01-precision-tool-dark-axis.png` | Precision tool, dark | command palette, dense panes, single cyan accent | fake Linear clone, decorative glow |
| `moodboard/02-precision-tool-dark-caliper.png` | Precision tool, dark | keyboard-first rows, right inspector, mono metadata | random dark dashboard cards |
| `moodboard/03-editorial-fintech-ledger-field.png` | Editorial fintech, white | gradient type, proof stack, API evidence | purple hero gradient |
| `moodboard/04-editorial-fintech-northstar-treasury.png` | Editorial fintech, white | footnotes, map/ledger overlap, trust rhythm | bank-logo cosplay |
| `moodboard/05-brutalist-geek-nullstack.png` | Brutalist geek, black | hard bento, dot matrix, terminal proof | soft SaaS glass cards |
| `moodboard/06-brutalist-geek-forge-day.png` | Brutalist geek, black | huge mono number, release-note layout | generic launch countdown |
| `moodboard/07-warm-editorial-field-notes.png` | Warm editorial | serif headline, bleed photo, pull quote | blog template |
| `moodboard/08-luxury-maison-vale.png` | Luxury | omission, image crop, micro typography | empty page with no hierarchy |
| `moodboard/09-data-dense-vector-desk.png` | Data-dense pro tool | trading cockpit, split panes, order ladder | KPI card grid |
| `moodboard/10-data-dense-plantroom.png` | Data-dense pro tool | schematic canvas, incident drawer, grouped rows | 3-column dashboard |
| `moodboard/11-immersive-scroll-pelagic-index.png` | Immersive scroll | full-bleed scene, chapter rail, anchored labels | static hero wallpaper |
| `moodboard/12-japanese-minimal-plain-works.png` | Japanese minimal | quiet grid, small photography, material notes | bland whitespace |

## What Makes A Page World-Class

1. **Hierarchy uses at least three levers**: size, weight, color, spacing, opacity, and position work together. A page that only changes font size feels amateur.
2. **Density is earned**: dense interfaces need alignment, grouping, row rhythm, and semantic color. Density without grammar is clutter.
3. **There is one signature move**: command palette, dot matrix, bleed image, chapter rail, product crop, order ladder. If nothing is recognizable, the page is generic.
4. **The first viewport has a clear motion path**: the eye knows where to enter, what to inspect next, and where the page wants the user to go.
5. **Whitespace has a job**: it groups, isolates, slows, or increases premium feel. It is not unused space.
6. **Cards are not the default unit**: use cards only when each item is truly peer-level. Otherwise use panes, rails, overlap, tables, canvases, timelines, or editorial grids.
7. **Typography carries personality**: font choice, weight range, numeral style, measure, and label treatment must match the product's trust contract.
8. **Color is constrained**: one primary accent is often stronger than five brand colors. Semantic colors are reserved for real meaning.
9. **Motion is cause-and-effect**: UI transitions should use transform/opacity, `ease-out` or spring-like curves, usually 150-300ms for controls and 300-700ms for narrative scroll.
10. **Edges are deliberate**: radius, borders, shadows, and dividers form a system. Random 16px cards with heavy shadows are a smell.
11. **Real content pressure is visible**: tables, filters, proof, APIs, footnotes, product details, and empty states show the design survives use.
12. **The page solves a hard constraint**: trust, speed, editability, scanability, spectacle, luxury, operational density, or calm. Beauty without a constraint becomes decoration.
13. **Responsive behavior is implied by the layout**: grids have obvious collapse rules, fixed-format elements have aspect ratios, and text has safe measures.
14. **Aesthetic tokens and engineering tokens agree**: if the design says "precision", the CSS must use precise scales, tabular numerals, visible focus states, and restrained motion.

## Direction Token Tables

### 1. Precision Tool · Dark

| Token | Recommendation |
|---|---|
| Palette | `--bg:#050607`, `--surface:#0D0F12`, `--panel:#13161B`, `--border:#252A33`, `--text:#F2F4F8`, `--muted:#7D8591`, `--accent:#00C2FF` or `#B6F09C`, `--success:#4ADE80`, `--danger:#FF5C7A` |
| Typography | Geist / Inter / SF Pro for UI, 400/500/600. JetBrains Mono / Berkeley Mono for timestamps, IDs, shortcuts, 11-13px. Use tabular numerals. |
| Layout | App shell, not landing page. 224px nav rail, central dense table or timeline, 320-420px inspector drawer, 1px hairline grid, 4-8px radius. |
| Motion | Micro: 120-180ms `cubic-bezier(.16,1,.3,1)`. Command palette open: 160-220ms scale 0.98 to 1 + opacity. Row focus: instant color plus 120ms border/fill. |
| Density | High. 32-40px rows, 12-14px body, 8px horizontal cell rhythm. Every color chip must encode state. |
| Signature | Keyboard-first command palette plus mono metadata on a dense dark operating surface. |
| Engineering Constraint | Must support keyboard focus, hover/focus parity, virtualized long lists, and stable row heights. |

### 2. Editorial Fintech · White

| Token | Recommendation |
|---|---|
| Palette | `--bg:#FFFFFF`, `--surface:#F6F9FC`, `--ink:#0A2540`, `--muted:#425466`, `--border:#D9E2EC`, `--blue:#2563EB`, `--teal:#14B8A6`, `--green:#059669`, `--amber:#D97706` |
| Typography | Neue Haas Grotesk / Söhne / Inter for body. One display grotesk headline 64-96px, 600-700. IBM Plex Mono for API/proof. Optional restrained serif numerals for quotes/statements. |
| Layout | 12-column grid, 96-144px desktop gutters, asymmetric hero. Product evidence overlaps diagram/API/map layers. Footnotes and proof strips replace feature cards. |
| Motion | Diagram draw: 500-800ms stagger. Hover proof layer: 180ms translateY(-2px). Page transition mostly fade/slide, never bouncy. |
| Density | Medium. Above fold should feel airy, but proof areas need real API snippets, transaction rows, or compliance details. |
| Signature | Editorial trust: gradient type, thin proof diagrams, API block, and financial evidence stacked into one composition. |
| Engineering Constraint | Avoid fake screenshots. Use actual product states, real-ish constraints, and accessible gradient text fallback. |

### 3. Brutalist Geek · Pure Black

| Token | Recommendation |
|---|---|
| Palette | `--bg:#000000`, `--surface:#050505`, `--raised:#0B0B0B`, `--border:#2A2A2A`, `--text:#FFFFFF`, `--muted:#A1A1AA`, `--accent:#FF4D00` or `#BFFF00`, `--success:#00E676` |
| Typography | Mono-first: Berkeley Mono / JetBrains Mono / Geist Mono. Display sans only for one oversized word. Uppercase labels 10-12px with 0.04em tracking. |
| Layout | Hard bento, but with size contrast: 5x3 hero block, 1x1 metrics, terminal column, dot-grid field. Radius 0-4px. |
| Motion | Snappy, almost mechanical. 100-160ms hover, 240ms panel reveal. Terminal cursor blink can be 900-1100ms. |
| Density | Medium-high. Dense modules on a black canvas, but negative space must be dramatic. |
| Signature | Pure black, harsh modules, dot matrix, terminal proof, one high-saturation accent. |
| Engineering Constraint | Contrast must be checked. Black-on-black surfaces need border and elevation tokens, not shadows alone. |

### 4. Warm Editorial / Magazine

| Token | Recommendation |
|---|---|
| Palette | `--bg:#F6EFE4`, `--paper:#FFF9EF`, `--ink:#211A16`, `--muted:#776B61`, `--rule:#D8CBB9`, `--rust:#B55332`, `--olive:#657247`, `--sky:#A8C7D7` |
| Typography | Canela / Tiempos / Editorial New style serif for display, 72-112px at 300-500. Lyon / Source Serif / Charter for body. Inter/Avenir for tiny labels. |
| Layout | Asymmetric magazine grid. Bleed image, pull quote, side rail, article index, varied text column widths. Content may overlap if contrast is controlled. |
| Motion | Slow editorial reveal: 400-700ms fade/clip, scroll-linked image parallax under 8% movement. Prefer `cubic-bezier(.22,1,.36,1)`. |
| Density | Medium-low in hero, medium in index/annotation areas. Text measure 55-72ch. |
| Signature | Print magazine rhythm translated to web: serif headline + bleed photo + pull quote + warm rules. |
| Engineering Constraint | Need responsive art direction for image crops and text wrap. Do not let overlaps survive blindly on mobile. |

### 5. Luxury / High-End Product

| Token | Recommendation |
|---|---|
| Palette | `--bg:#FAF8F3`, `--surface:#FFFFFF`, `--ink:#161412`, `--muted:#7B746B`, `--hairline:#E4DED3`, `--champagne:#B89B5E`, `--deep-green:#19352B` |
| Typography | Didot / Canela / Reckless style serif for product names, 300-400. Neue Haas / Inter for nav and details, 11-15px. Thin uppercase labels with careful spacing. |
| Layout | Extreme negative space, one monumental crop, micro details on baseline grid, no boxed cards, CTA as quiet typographic object. |
| Motion | Slower and smoother: 350-700ms image reveal, 180-240ms hover, no spring bounce. Use opacity + clip-path + subtle transform. |
| Density | Low. Each item must earn its place. Product details can be dense but tiny. |
| Signature | Luxury through omission: huge image crop, hairline rules, microcopy, restrained action. |
| Engineering Constraint | Images need art-directed crops and reserved aspect ratios. Compression artifacts or layout shift destroy the illusion. |

### 6. Data-Dense Pro Tool

| Token | Recommendation |
|---|---|
| Palette | Dark: `#0B0E11/#11161C/#2A3340/#DDE4EE`. Light: `#F5F7FA/#FFFFFF/#D5DDE7/#17202A`. Semantic: buy `#22C55E`, sell/error `#EF4444`, cobalt `#246BFD`, amber `#F59E0B`. |
| Typography | IBM Plex Sans / Inter for UI. IBM Plex Mono / JetBrains Mono for values. 11-14px rows, tabular numerals, no display drama inside work surface. |
| Layout | Cockpit: nav tree, primary canvas, split panes, order ladder/table, timeline, inspector, bottom log. Use resizable panes and persistent filters. |
| Motion | Utility-first: hover/cross-highlight 80-140ms, drawer 180-240ms, live chart updates throttled. Reduced motion must keep all data readable. |
| Density | Very high. Density is acceptable only with alignment, grouping, sticky headers, row states, and semantic color. |
| Signature | A professional cockpit where tables, timelines, maps, and inspectors cross-highlight each other. |
| Engineering Constraint | Needs virtualization, sticky columns/headers, keyboard nav, accessible chart summaries, and deterministic row height. |

### 7. Immersive Scroll / Awwwards-Level

| Token | Recommendation |
|---|---|
| Palette | Scene-led. Example: `--deep:#061923`, `--mid:#0E3A4A`, `--cyan:#35D0E2`, `--phosphor:#B6F572`, `--text:#F4F8F8`, `--muted:#89A9AE`, `--coral:#FF6B5F` |
| Typography | Modern grotesk display 48-72px, body 15-17px, mono labels 10-12px. Type sits like instrumentation, not marketing copy. |
| Layout | Full-bleed scene, chapter rail, scroll progress, anchored annotations, diagonal or radial movement path. UI must be attached to scene features. |
| Motion | Scroll-linked camera or layer progress. 600-1200ms chapter transitions, but UI controls still 150-250ms. Always provide reduced-motion fallback. |
| Density | Low-medium in copy, high in anchored labels. Avoid filling the whole scene with text. |
| Signature | A visual world whose scroll path is the information architecture. |
| Engineering Constraint | Must validate nonblank canvas/media, image loading, mobile crops, and text contrast over moving backgrounds. |

### 8. Japanese Minimal / Quiet Grid

| Token | Recommendation |
|---|---|
| Palette | `--bg:#F7F5EF`, `--paper:#FFFFFF`, `--ink:#25231F`, `--muted:#7C776E`, `--line:#DCD6CA`, `--indigo:#2F4A60`, `--stock:#4F7C5A` |
| Typography | Noto Sans JP / Hiragino Sans / Yu Gothic style sans, 400/500. 13-16px body, 11px labels. Avoid dramatic display unless it is a product/category title. |
| Layout | Quiet modular grid, modest product photos, material swatches, measurement notes, tiny nav, one blank interval. More object catalogue than landing page. |
| Motion | Minimal: 120-180ms opacity/underline/state change. Page transitions can be 220-320ms fade. No parallax unless nearly invisible. |
| Density | Low-medium. The page can hold tables/details, but each cluster is separated by silence. |
| Signature | Visible grid discipline plus tactile object information at a modest scale. |
| Engineering Constraint | Needs precise image sizing, baseline alignment, and whitespace rules. If spacing is random, it becomes bland instead of quiet. |

