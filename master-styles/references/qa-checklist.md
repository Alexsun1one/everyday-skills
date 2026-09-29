# QA Checklist

## Accept

Run these three falsifiable tests FIRST — they measure the thing the old "gallery-grade" bullet
only asserted:

- **Famous-work test (falsifiable):** Before you accept, NAME the one actual famous work this
  output is closest to (e.g. *The Kiss* / *Nighthawks* / *The Great Wave* / 富春山居图 /
  Platon's Obama). Put the output and that work side by side in your mind. If a stranger would
  say "that's a copy/remix of {work}", regenerate. If you cannot name a specific work it risks
  copying, the token was applied as a rule — pass.
- **Squint test (falsifiable):** Shrink the image to a 200px thumbnail. In one second, can you
  name (a) the subject and (b) the single dominant restraint (the void / the grid / the raking
  light / the 留白)? If the subject does not read first, or the look collapses to generic "AI
  render", regenerate.
- **Peer-shelf test (falsifiable):** Name a real piece in the SAME tradition the register points
  to (a real 文人画 hanging scroll for ink; a real Pentagram grid poster for Swiss; a real
  Platon portrait for face-on-void). Placed on the same shelf, does this output look intentional
  or look like an amateur imitation? If amateur, regenerate.

Then the objective bullets:

- The plan names concrete tokens (palette logic, structure, light, restraint), not just an
  artist's name.
- At most two token sources are blended, with one shared restraint; the result is coherent,
  not muddy.
- The restraint principle is visibly kept (the master's refusal — no gradients, no diagonal,
  no environment, no decoration, etc.).
- Any text is clean and correct.

## Regenerate

- **Reproduces a famous work — disqualifying test:** name the single closest actual work
  (*The Kiss* / *Nighthawks* / *The Great Wave* / 富春山居图 / Public Theater marks / the NYC
  subway map / Platon's Putin or Obama). If you CAN name one and the output shares its
  composition, motif, or palette signature, it is a copy — regenerate. "I can't think of one"
  is not a pass; if you skipped naming it, you skipped the test.
- **Costume pastiche — disqualifying test:** list the surface tics present (gold everywhere /
  a wave / a sunburst / a gold-line grid). For each, point to the STRUCTURAL rule it should
  encode (Klimt = flat gilded ground + one realistic anchor; Hokusai = key-line + scale
  contrast + one graded-blue passage). If a tic is present but its structural rule is absent,
  it is a costume — strip the tic and re-apply the rule, or regenerate.
- Any 书法 title, 印章, or tier label has melted, doubled, or invented glyphs, or the tier
  labels were set in Latin S/A/B/C on a Chinese ink subject.
- It "name-dropped" a style but applied no real tokens — a vague blur or generic vibe.
- Four or more styles are mixed into mud.
- The style buries the subject; the content is hard to read under the aesthetic.
- The restraint was skipped, so the image looks busy and generic.
- An artist's lineage was mislabeled, importing the wrong tokens (e.g. treating Malika Favre
  as Art Deco rather than Pop/Op).

## Repair Moves

If it reproduces a famous work:

```text
Regenerate applying only the RULES (palette logic, structure, restraint) to the user's own
subject. Change the composition and motifs so it does not resemble {famous work}.
```

If it is costume pastiche:

```text
Strip the surface tics. Re-specify the actual structural token and restraint, and apply them
to the subject. The borrowed thing is the method, not the ornament.
```

If too many styles are mixed:

```text
Cut to one structure source + one palette/light source + one shared restraint. Remove the rest.
```

If the style buries the subject:

```text
Dial the style back until the subject reads first. Keep one structure token and one
palette/light token; reduce density; restore the focal hierarchy.
```

If it looks generic:

```text
Add the restraint principle explicitly (the master's refusal) and one decisive token. Generic
output is almost always a missing restraint.
```
