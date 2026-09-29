# QA Checklist

## Accept

- **Thumbnail/squint test (falsifiable):** shrink the card to 200px wide. In one second, name the
  ONE hero line / number / term you read first. If you cannot name it, or two elements compete for
  first, the hierarchy failed — regenerate.
- **Save-or-scroll test (falsifiable):** if this exact card appeared in your feed, would you
  screenshot it, OR keep scrolling? Answer one word. If the honest answer is "scroll," or the only
  reason to save is the words (not the card — i.e. copy-pasted plain text would serve identically),
  regenerate. State the reason a real person saves THIS rendering, not the idea.
- **Real-account test (falsifiable):** name a real 小红书 / 公众号 account that posts cards in this
  register. Placed next to one of their cards, does this look more amateur (flatter hierarchy,
  tighter margins, louder color)? If yes, regenerate.
- There is exactly one savable idea on the card.
- One alignment is held throughout the card.
- **Decoration count:** count every non-text graphic element. The card allows AT MOST ONE (a thin
  rule OR a quotation mark OR one accent block OR a numeral-rail — not several). If you count two or
  more decorative elements, regenerate.
- **Margin check:** confirm a clear empty band of at least 8% of the width on all four edges, and
  that no glyph or rule enters it. If text or decoration touches the band, regenerate.
- The palette is restrained: paper / ink + at most one accent, max two fonts.
- The Chinese characters are correct — no melted, doubled, or gibberish glyphs.
- The aspect ratio matches the card (1:1 by default, 3:4 for longer cards).

## Regenerate

- Everything is the same weight and size; there is no focal line.
- It reads as a PPT slide: equal-weight bullets, a colored title bar, a slide footer.
- It reads as a poster: imagery dominating and drowning the words.
- It is cluttered or over-full, or carries more than one idea.
- The palette is a rainbow, or there is gradient glow / 微商 gold-red on the text.
- The characters are wrong, doubled, or partly gibberish.
- The alignment is mixed (centered lines over left-aligned ones).
- There are stickers, emoji, clip art, mascots, or sparkle bursts.
- The hero is less than 2× the support's height (flat hierarchy) — even if technically the largest.
- It is neat but says nothing worth saving.

## Repair Moves

If the hierarchy is flat (most common):

```text
Strengthen hierarchy: enlarge the hero so it is clearly the largest element, shrink the
support and meta. The eye must land on the hero first. Keep the composition and palette.
```

If it carries too many ideas:

```text
Cut to one idea. Keep only the single line / number / takeaway worth the whole card. Remove
the rest and give the hero a calm field of negative space.
```

If it is cluttered or over-full:

```text
Add negative space: increase the outer margins on all four sides, widen the line spacing,
and let the hero breathe. Remove any decoration that is not a thin rule, a quotation mark,
a small accent block, or a numeral.
```

If the text is wrong:

```text
Re-render the text as EXACTLY {hero / support / meta}, with clean correct Chinese characters,
no melted/doubled/gibberish glyphs. Keep the composition. Remove any extra hallucinated text
or watermark. If clean text is impossible, leave an empty hero zone for overlay.
```

If the palette is loud:

```text
Restrain the palette: paper / off-white base, one deep ink, and at most one accent color on
the number or key word. Remove gradients, glow, and extra colors. Use max two fonts.
```
