# Slide Design System

World-class PPT production needs a design system before image generation. `layout-blueprint.json` is not enough if it only reserves rectangles. The deck must also define typography, plates behind text, line grammar, icon/marker families, and asset constraints.

Use this reference before skeleton rendering, image prompting, HTML styling, or PPTX export.

## Core Rule

Every serious deck must have three locked layers:

1. **Layout geometry**: stage, safe area, claim/support/visual/evidence/loop boxes.
2. **Design system**: font stack, type scale, color tokens, foreground object kit, line/icon grammar.
3. **Asset prompt contract**: what image generation must leave empty, where the subject may live, and which text is external editable overlay.

If any of these layers is missing, do not generate final images.

## Typography Contract

Use `assets/slide-design-system.json` as the default machine-readable system.

Default Chinese type roles:

| Role | Use | Default |
| --- | --- | --- |
| `kicker` | section hint / source / speaker context | 18px, weight 800 |
| `hero_line` | split hero title line | 48px, weight 850 |
| `title_line` | regular slide title line | 40px, weight 850 |
| `subtitle` | strong one-sentence support | 24px, weight 650 |
| `body` | 1-3 line explanation | 21px, weight 540 |
| `caption` | decision rule, footnote strip | 17px, weight 700 |
| `label` | chip, node, station, callout label | 15px, weight 800 |
| `table` | dense evidence table | 15px, line height 1.24 |

Rules:

- Large Chinese headlines are separate positioned lines, not one auto-wrapping block.
- No important text sits directly on image texture.
- Every text region declares a type role in the skeleton.
- Paragraph line length must be designed, not left to browser flow.

## Foreground Object Kit

A polished deck needs object richness, not only text + image.

Use 2-4 object families per slide:

- text backplates: `paper-card`, `dark-strip`, `caption-band`, `ticket-label`, `sticky-note`, `receipt`, `floating-plaque`
- structure objects: `number-badge`, `route-chip`, `callout-ticket`, `evidence-drawer`, `magnifier-window`, `stamp`, `tab`, `divider-rail`
- lines: `single-arrow`, `dashed-handoff`, `loop-connector`, `bracket`, `leader-line`
- icons: `check`, `dot`, `flag`, `lens`, `drawer`, `receipt`, `ladder`, `stamp`

Do not use icons as decoration. Icons, badges, and lines must clarify reading order, state, or relation.

## Text Backplate Rules

When text overlaps or sits near a generated image:

- title: quiet field or strong paper-card/dark-strip
- body: paper-card/caption-band with at least 16px inner padding
- chip/node label: small plaque or ticket attached to the relevant object
- table/chart: dedicated evidence plate, not floating on an image
- caption on image: caption-band or receipt strip, never raw text

This is mandatory for hybrid/editable routes.

## Layout Rhythm

Reject a deck when most slides are only:

- left text + right image
- top text + bottom image
- same card grid repeated

Acceptable variation:

- title plate crossing over visual edge
- image stage with foreground floating plaques
- diagonal or loop path with attached labels
- evidence table anchored to a proof object
- magnifier window / zoom callout
- receipt strip / stamp / number-badge sequence
- section card plus partial full-bleed asset

The goal is not decoration. The goal is a richer visual reading path.

## Skeleton Requirements

The skeleton renderer must show:

- geometry boxes;
- type roles and expected font sizes;
- backplate/plate requirements;
- visual region and image subject zone;
- text-safe zones and no-go zones for image generation;
- foreground overlay object families;
- repeated-layout warnings where possible.

If the skeleton contact sheet looks like abstract boxes, it is not sufficient. A skeleton should already reveal the deck's type hierarchy, object grammar, and asset constraints.

## QA

Fail and revise if:

- a slide has text on a busy image without a plate;
- the image prompt does not reserve title/support/evidence/loop zones;
- the prompt asks for labels that later need to be editable;
- three consecutive slides use the same split;
- a table/chart/card appears without a designed plate;
- font sizes are invented per slide instead of using the type system.
