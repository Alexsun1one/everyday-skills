# Lettering & Text / 字体与文字呈现

This is the file paper can skip and bricks cannot. On paper you *write* — text embeds freely anywhere, on any scrap. **A brick cannot be written on.** In the LEGO world text has a manufacturing reality: it is a *placed or built element* — a printed tile, brick-built letters, studs on a road, a signboard, a minifig's placard, or the booklet's own page type. Picking the right carrier and matching its real letterform is what makes the image read as authentic bricks instead of "text pasted on top." Read with `style-dna.md` (label discipline), `native-elements.md` (signage elements), and `modes.md` (the instruction/box type layers).

**Core principle:** text is never a floating caption. It is an object with a location, an owner, and a font that fits how that object is made. The constraint is a feature — it forces every label to be a real thing, which looks more designed than free-floating text. Text is also a **variation axis** (the same label can be a printed tile, a brick-built hero word, or a road-stud line) and a **precision axis** (the tiles carry THIS content's real names and counts, not lorem-ipsum) — see the Swap Test in `qa-checklist.md`.

## The Text-Carrier Taxonomy / 文字载体谱系

Pick by how much text, how big, and how it's read. Ranked from most-used to special.

1. **Printed tile / 印字砖** — the workhorse label. A smooth tile (1×1, 1×2, 1×4, 2×2, 2×4) with text/icon printed flat on its face. Holds one short word or 2–6 Chinese characters. Read from above or face-on. Use for module names, station labels, status words. Snap it onto the thing it names.
2. **Brick-built letters / 拼砌字** — letterforms BUILT from bricks/plates, standing on the baseplate or laid flat. Chunky, **locked to the stud grid** (minimum stroke = 1 plate/brick) → blocky modular letterforms, like a pixel display face. Use for ONE hero word, a big title, or a giant number (a step "3", a "v2"). Latin/numerals read well; Chinese is hard here (see below).
3. **Studs-as-pixels / 凸点点阵字** — text spelled by contrasting-color studs on a baseplate grid, like a low-res LED matrix. Read from directly above. Use for a road/floor label, a scoreboard, a retro screen. Short words only; very grid-constrained.
4. **Signboard / street sign / 招牌·路牌** — a printed sign panel on stud-posts: shop sign, billboard, directional road sign, octagon stop sign. Read perpendicular (face the camera). Doubles as a directional element (see `native-elements.md`). Use for district names, route signs, rules-at-a-point.
5. **Minifig-held sign / 小人仔举牌** — a minifig holds a placard, clipboard, or newspaper tile with text. The text gets a *voice / owner*. Use for attribution, a guide's "you are here", a quote, a speaker.
6. **Instruction page type / 说明书排版层** — text that lives ON THE PAGE, not in the build: step-number badges in circles, the parts call-out counts (`2×4 砖 ×3`), clean caption lines, the small finished-preview label. Flat, page-level. Instruction-Sheet mode only.
7. **Box-art display banner / 盒面标题条** — the product-name banner: big, bold, in a colored bar. Box-Art mode only. **Original product name — never the LEGO wordmark.**
8. **Printed decorative tiles / 印花装饰砖** — computer screens, control panels, newspapers, license plates, maps. Incidental text that makes the world specific and real.

## Font Logic / 字体长什么样

The direct answer to "字体应该是什么样子". Match the carrier:

| Carrier | Letterform | Feel |
| --- | --- | --- |
| Printed tile / signboard | **friendly rounded geometric sans** — even stroke, slightly condensed, generous counters | the authentic LEGO printed-element face: clean, legible small |
| Brick-built hero letters | **modular stud-grid letterforms** — blocky, min 1-plate stroke, right-angle/45° joints | chunky, toy-like; the grid constraint IS the charm |
| Studs-as-pixels | **low-res matrix glyphs** | retro screen / scoreboard |
| Instruction page | **neutral grotesque (Helvetica-like) sans** | the universal build-booklet standard |
| Box-art banner | **bold condensed display sans**, high contrast, often a white keyline | punchy product display |

One hero text element max per image (a brick-built title OR a box banner). Everything else is small printed tiles. Don't mix three display faces.

## Chinese in Bricks / 中文怎么办

Chinese is the hard case and must be handled on purpose:

- **Default: printed tiles & signboards in a clean rounded sans.** This matches the LEGO print face and stays legible at small size. Put 2–6-character labels on tiles, district names on signboards.
- **Brick-built Chinese: only 1–2 simple hero characters** (e.g. 「家」「云」「门」) as a bold statement, because most characters have too many strokes for the stud grid and turn to mush. For anything longer, do not brick-build — use a printed tile.
- **Exact / multi-line / list Chinese → the overlay path** (see `prompt-template.md`): render the build with **blank printed tiles / empty signboards** in the right spots, then set the precise text in an editor. Let the image model render text only for a single very short hero word where one wrong glyph survives.
- Never send dense multi-line Chinese to the image model and hope; garbled glyphs read as broken, not as bricks.

**Empirical calibration (current image models, validated on real renders):** 3–6 *very short* printed-tile labels (2–4 chars each) render legibly and look authentic. The failure is not the requested labels — it is **extra Chinese the model invents on its own** (a caption strip, sub-text on a signboard), which garbles. So in the final prompt, name the exact glyph strings to render and explicitly forbid any other Chinese; push every caption/sentence to the overlay path. Cap on-image model-rendered Chinese at the few hero labels; everything else is blank-for-overlay.

## Placement Rules / 摆放规则

The LEGO answer to paper's free embedding:

- **Never float.** Text sits on a real carrier at a readable angle: top-read tiles/roads from a high angle; face-read signs perpendicular to camera; brick-built titles standing on the baseplate facing the lens.
- **Match carrier to surface:** a name on the module it labels (printed tile snapped on), a route name on the road (studs or a road sign), a district on a signboard at its entrance, a step number on the page (instruction mode).
- **Owner & location:** every label belongs to the thing it names. A floating word with no carrier is a regenerate.
- **Density honesty:** 3–6 short labels for a simple build; instruction call-outs may be denser because counting parts is the manual's job; box art is near-wordless except the banner.
- **One focal word.** The hero title (brick-built or banner) is the only large text; quiet everything else to small tiles so the focal module still wins.

## Text as Variety & Precision / 文字既是变化也是精准

- **Variety:** rotate the carrier across images so text doesn't always appear as "a printed tile top-left" — a hero word may be brick-built in one image, a road-stud line in another, a minifig placard in a third. This kills one source of the "每张都差不多" feeling.
- **Precision:** the tiles, signs, and call-outs carry **this content's real words and numbers** — the document's actual section names, the system's real module names, the prompt's actual parts, the real count in `×N`. Generic placeholder labels are the tell of a template build. If the labels would fit any other topic unchanged, the build isn't precise (see Swap Test in `qa-checklist.md`).

## Accept / Regenerate

Accept:

- Every piece of text sits on a real carrier (tile / brick-built / road-studs / signboard / placard / page layer), never floating.
- The letterform matches the carrier (rounded sans on tiles, blocky modular for brick-built heroes, neutral sans for instruction pages, bold display for box banners).
- Chinese is on tiles/signs in a clean sans, or brick-built only for 1–2 simple hero characters, or routed to overlay when exact/multi-line.
- One hero text element; the rest are quiet small tiles; the focal module still wins.
- Labels carry THIS content's real names/counts, not generic placeholders.
- Original letterforms only — no LEGO wordmark, no reproduced brand font.

Regenerate:

- Text floats with no carrier, or is a flat caption pasted over the photo.
- Brick-built Chinese turns to unreadable stroke-mush, or multi-line Chinese is garbled.
- The font is a generic system font ignoring the carrier (e.g. a thin serif printed on a stud tile).
- Two or three display faces fight; or tiny fake text fills the scene.
- Labels are generic and swappable onto any topic (a template, not this content).
- It renders the LEGO logo/wordmark or copies the brand letterform.
