# Template Style Library

## Purpose

The best result is not "pick a template and fill it". The best result is "find high-quality style anchors that match the user's intent, then rebuild a deck-specific system."

Use this file when:

- The user asks for a style.
- The user says a deck should look premium, cinematic, consulting-like, investor-ready, playful, technical, etc.
- The source has no brand system.
- The user wants several visual directions.

## Local-First Workflow

Use the local anchor library first:

```bash
python3 scripts/select_style_anchors.py --query "AI investor pitch dark technical" --limit 3
```

Then refresh current web references only when:

- the user asks for a very specific style,
- the deck has high stakes,
- the local anchors do not fit,
- or the subject depends on current visual conventions.

## Template Scouting Workflow

1. Translate intent into search terms:
   - deck type: pitch deck, board update, sales proposal, product launch, research report, lesson, portfolio.
   - industry: AI, biotech, finance, healthcare, education, luxury, consumer, climate.
   - tone: dark technical, premium minimal, editorial, playful, Swiss, cinematic, data desk.
2. Run `scripts/select_style_anchors.py` and pick 2-4 local anchors.
3. Search 2-4 current template/inspiration sources only if needed.
4. Save a style card for each anchor:

```text
style anchor:
- source/link:
- best for:
- visual thesis:
- palette:
- type feel:
- layout grammar:
- slide archetypes:
- what to borrow:
- what not to copy:
```

5. Show 3 directions using real user content. Do not ask the user to choose from abstract names only.

## Useful Template/Reference Sources

Use current web search when stakes are high. Local anchor recipes are the default; web sources are refresh points, not dependencies.

- Pitch template gallery: broad professional presentation templates.
- Beautiful.ai templates: pitch decks, seed/Series B, investor presentations, reports, sales decks, smart-slide style systems.
- Canva presentation templates: broad visual variety and quick category scans.
- Figma Slides/community: modern product, startup, and design-led deck styles.
- Adobe Express, Slidesgo, Envato, Dribbble, Behance: useful for visual scan, but verify quality manually.
- Public pitch deck examples: useful for narrative categories, not always good visual models.

Starting links:

- https://pitch.com/templates
- https://www.beautiful.ai/presentations
- https://www.canva.com/presentations/templates/
- https://www.figma.com/templates/presentations/

## Style Registers With Search Terms

| User intent | Search terms | Good anchors |
| --- | --- | --- |
| Investor-ready AI startup | `AI pitch deck dark data product premium`, `seed deck technical dashboard` | Technical Blueprint, Data Desk, Studio Keynote |
| Consulting / board | `strategy presentation executive dark data`, `board deck KPI report` | Swiss Grid, Data Desk, Premium Minimal |
| Product launch | `product keynote cinematic presentation`, `SaaS launch deck template` | Studio Keynote, Premium Minimal |
| Healthcare trust | `healthcare investor deck calm clinical`, `medical report presentation` | Calm Trust, Research Report |
| Education/course | `training deck template clean lesson`, `workshop slides playful` | Paper System, Playful Learning |
| Consumer brand | `brand presentation editorial premium`, `campaign deck bold` | Editorial Magazine, Bold Poster |

For richer local recipes, read `references/style-anchor-library.md` and `assets/style-anchor-library.json`.

## Template Quality Gate

Reject anchors that:

- Are just generic gradient/card walls.
- Cannot support dense content slides.
- Have a beautiful cover but weak data/table pages.
- Depend on stock photos unrelated to the user's subject.
- Use illegible type, tiny labels, random icon styles, or decorative clutter.
- Would make the user's product/claim less credible.

## How To Borrow

Borrow:

- Palette semantics.
- Type hierarchy.
- Margin and grid rhythm.
- Section separator logic.
- Chart treatment.
- Reusable components.
- Motion/reveal tone.

Do not copy:

- Proprietary images, logos, icons, mascots, or exact slide layouts.
- A competitor's distinctive brand world.
- A template's sample copy, fake metrics, or chart data.

## Style Direction Output

Before full deck build, produce:

```text
direction 1:
- name:
- best when:
- style anchors:
- cover concept:
- content-slide system:
- risk:

direction 2:
...

direction 3:
...
```

Then build real previews or screenshots using actual user content.
