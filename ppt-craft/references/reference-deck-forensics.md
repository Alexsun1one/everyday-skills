# Reference Deck Forensics

## Goal

When the user supplies a PPTX/PDF/template that "looks good", study why before redesigning. Borrow the system, not the private content or exact layouts.

Use this file for:

- Supplied PPTX/PDF examples.
- Existing deck beautify.
- "Make it like this" requests.
- Building a house style from a strong reference.

## Quick Script

Run when possible:

```bash
python3 scripts/analyze_reference_deck.py --pptx reference.pptx --pdf reference.pdf
```

The script reports slide/page count, canvas size, text density, top fonts, colors, media, and representative titles. Treat the report as clues, then inspect screenshots manually.

## Manual Forensics Checklist

1. **Narrative machine**
   - What mental model does the deck install in the first 3-5 slides?
   - What is the enemy/current state?
   - What is the category claim?
   - Where does proof begin?
   - How does the deck close the action?

2. **Slide archetypes**
   - Cover / manifesto.
   - Binary contrast: old vs new, mask vs truth, outside vs inside.
   - Layer map: L1/L2/L3, stack, pyramid, operating system.
   - Evidence dashboard: chart + large number + micro case.
   - System architecture: numbered pipeline or graph.
   - Future split: bad path vs optimized path.
   - Vision moment: cinematic image with sparse copy.
   - Ask / roadmap / contact close.

3. **Visual system**
   - Canvas ratio and safe margins.
   - Background field: light, dark, paper, image, gradient, texture.
   - Typography roles: display, body, mono/data, captions, labels.
   - Color semantics: primary accent, secondary accent, warning, success, muted text.
   - Repeated chrome: logo, page marker, section label, footer, corner brackets, rules.
   - Component grammar: cards, terminal windows, panels, chips, charts, callouts.

4. **Density and rhythm**
   - Average text density by section.
   - Alternation between dense proof pages and low-density emotional pages.
   - Whether each slide has one dominant claim.
   - Whether charts have a single visible takeaway.

5. **Asset policy**
   - Are images symbolic, product screenshots, generated hero art, or diagrams?
   - Are charts native/editable or rasterized?
   - Are icons consistent?
   - Are backgrounds reused or varied?

6. **Editability reality**
   - Empty master/layout means the deck is handcrafted page-by-page.
   - Many raster assets mean visual fidelity may beat editability.
   - If the user wants editable PPTX, preserve the design language but simplify effects.

## Private Reference Example: InnerScan Investor Deck

Observed from a user-supplied private deck. Do not copy text, claims, logos, or assets. Borrow only the reusable design logic.

- **Format**: 16:9, 960x540 PDF pages; PPTX also 16:9.
- **Build pattern**: nearly empty master/layout, many handcrafted objects per slide, heavy use of PNG/SVG assets.
- **Typography**: mono/data face + Chinese sans + Chinese serif display; small labels are systematic, not random.
- **Palette**: dark navy base, gold as thesis/attention, cyan as system/positive signal, red as danger, gray as scaffolding.
- **Opening**: cinematic biological/brain metaphor cover, then a high-concept conflict page.
- **Story engine**: strong metaphors turn abstract AI/psychology into memorable binaries: definition vs understanding, anesthesia vs scalpel, beauty camera vs CT scan, surface data vs hidden data.
- **Proof pages**: chart + large number + micro case sidebar. Each page has a data takeaway and a human-sized case.
- **Rhythm**: dashboard proof pages are interrupted by cinematic vision pages and route/future-split pages.
- **Close**: action page, not a generic "thank you"; combines urgency, investment reason, terminal-like status, and contact card.

Reusable rule: build a deck-specific visual world. Do not merely apply a template skin.

## Borrowing Without Copying

Turn reference observations into a style lock:

```text
reference-derived style lock:
- narrative engine:
- slide archetypes to reuse:
- palette semantics:
- typography roles:
- component grammar:
- proof pattern:
- emotional breathers:
- forbidden copying:
```

For a new deck, rewrite each borrowed archetype around the new source's thesis. If the slide still reads like the reference deck after replacing the text, it is too derivative.
