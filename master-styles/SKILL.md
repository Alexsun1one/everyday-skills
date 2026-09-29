---
name: master-styles
description: The shared AESTHETIC ENGINE for this skill collection — a token library, not a destination skill. The content skills (cover-pop, sticker-set, quote-cards, rank-cards, and new ones) AUTO-ROUTE into it: given the user's subject, they pick the fitting visual register and pull transferable master tokens (palette logic, composition, negative space, light, texture, motif, restraint) from it — so a poet ranking renders as ink-wash literati art and a product cover renders premium, automatically, without the user naming a style. Covers masters and movements (Müller-Brockmann, Saul Bass, Malika Favre, Noma Bar, Platon, Hopper, Klimt, Hokusai, Kenya Hara, plus Chinese ink: 宋元山水/文人画/书法/工笔). It powers the others; it is rarely invoked on its own. Use directly only when a user explicitly asks to art-direct one image with a named aesthetic. Never reproduce an artist's actual famous works or shallow "in the style of X" pastiche.
---

# Master Styles

Master Styles is the shared aesthetic engine for this collection. It is not usually a skill you invoke directly — the content skills (cover-pop, sticker-set, quote-cards, rank-cards…) auto-route into it, choosing the visual register that fits the user's subject and pulling the right tokens. Its job is to make an image look world-class by borrowing the RULES a master obeys and applying them to the user's own subject — never by copying the master's actual pictures.

How the routing works: each content skill maps the subject/domain/mood to a register (e.g. 古代诗人 → 水墨山水/文人画, 现代球星 → 现代运动卡, 西方作家 → 古典油画肖像, 高级封面 → 瑞士网格 + 一个强调色), then applies that register's tokens automatically. The user does not name a style; the skill routes. `references/style-routing.md` is the concrete subject→register lookup table — read it FIRST; this file and `references/master-library.md` are the token vocabulary that routing draws from.

The recognizable thing about a master is the rule, not the picture. Müller-Brockmann's signature is "everything snaps to a mathematical grid," not his concert posters. Noma Bar's is "the empty gap forms a second true image," not his gun-face. Platon's is "a face is the only event on a void, lit from just above the lens," not his Putin portrait. This skill extracts those rules as transferable tokens, blends one or two, keeps the subject the hero, and refuses pastiche.

## Workflow

1. Read the user's subject and what is being made (a cover for X, a card about Y, a portrait of Z).
1.5. Read `references/style-routing.md` first and route the subject to ONE register — the subject decides; you do not pick a master by hand.
2. Name the desired feeling: elegance, graphic punch, warmth, gravitas, narrative, opulence, or loud energy.
3. Pick token sources by the TOKEN you need, not by fame — use `references/blending.md` to choose.
4. Take a structure token from one master and a palette/light token from another (one or two sources, never six).
5. Pick the ONE shared restraint principle both will obey (the refusal that keeps it elegant).
6. Run the Token Transfer Test: are these tokens, not a costume? Does it avoid the actual famous work? Does the subject stay the hero?
7. Read the chosen masters' entries in `references/master-library.md` and the axes in `references/token-axes.md`.
8. Build the final image prompt with `references/prompt-template.md`, applying the tokens to the user's subject.
9. Generate one image at a time.
10. Run QA with `references/qa-checklist.md`; regenerate if it reproduces a famous work, reads as costume pastiche, mixes too many styles, or buries the subject.

## Token Transfer Test

Before generating, answer:

```text
style plan:
- user subject: what we are actually making
- desired feeling: elegance / punch / warmth / gravitas / narrative / opulence / loud
- token sources (1-2, chosen by token not fame):
  - structure token: from {master} — {grid / centered void / radial / scale contrast / corner-wedge ...}
  - palette·light token: from {master} — {two clashing flats / raking long shadows / gold ground / glowing field ...}
- shared restraint: the ONE refusal both obey (no gradients / no diagonal / no environment / no decoration ...)
- anti-pastiche check: does NOT reproduce {the actual famous work}; subject stays the hero
- forbidden famous work (per token): {work A — what the structure token must NOT resemble}, {work B — what the palette/light token must NOT resemble}
- forbidden drift: name-drop w/o tokens / costume imitation / copying actual works / 6-style mud / style buries subject / maximalist token forced onto an anti-clutter host
```

Generate only when:

- the plan names concrete **tokens**, not just an artist's name ("two clashing flats + negative space carving the subject", not "make it Malika Favre")
- it will **not reproduce** the master's actual famous work
- the **subject stays the hero** — a viewer should notice the content before the style
- the **restraint principle** is kept — every master's elegance comes from what they refuse
- the plan passes the **Famous-work test**: you have NAMED the specific famous work each token risks reproducing (e.g. "structure token from Klimt → must NOT resemble *The Kiss*"), and the plan states the one change that breaks that resemblance. A plan that cannot name the work it must avoid has not converted the name into a token — it is still a costume. Do not generate.

HARD GATE: if any token source in the plan is named without (a) the concrete token verb and (b) the specific famous work it must NOT resemble, STOP and rewrite the plan. Do not generate from an unnamed-work plan.

## Core Principle: Extract, Blend, Apply

Three operating rules (see `references/blending.md`):

- **Extract, don't copy.** Borrow the method and restraint; never reproduce the artist's actual motifs, compositions, or wordmarks. If the output reads as *The Kiss* rather than "gold-ground luxe applied to a coffee brand," it failed.
- **Blend 1–2 token sets, not six.** Take a structure token from one master and a palette/light token from another. Mixing 4–6 styles produces mud. One structure + one color/light + one shared restraint.
- **The subject stays the hero.** Style serves content. If the style buries the subject, dial it back.

## As an Aesthetic Engine

Master Styles can run on top of another skill. A cover, a card, or a ranking card gets its plan from its own skill, then Master Styles supplies the art direction — e.g. a ranking card with "Platon-style face-on-void portraits + a Swiss grid," or a cover with "Hopper raking light + Hara emptiness." Plan the content first, then layer one or two tokens.

**The host skill's restraint wins.** Only blend tokens whose restraint is compatible with the host. Covers and cards forbid clutter — never apply a maximalist token (Tadanori Yokoo collage, Klimt dense ornament, Paula Scher edge-to-edge type) to a quote-card or a clean cover; it directly violates their anti-clutter / negative-space DNA. If a token fights the host's anti-pattern list, pick a different master. The aesthetic engine elevates the host; it never overrides the host's refusals.

**Restraint-compatibility gate (HARD when run under a host).** Before applying any token, check the host's anti-pattern / forbidden-drift list. If the candidate token's register is maximalist (Yokoo collage, Klimt dense ornament, Paula Scher edge-to-edge type, Sagmeister built-object) AND the host forbids clutter (covers, quote-cards, rank-cards), it is INCOMPATIBLE — pick a different master from the same feeling row. Maximalist registers are allowed ONLY when the host's own archetype is genuinely loud (活动/潮流/promo) and the host's readability rule still passes. State the host's restraint in the plan and confirm the chosen token obeys it; if it fights the host's anti-pattern list, do not generate.

## Output Contract

For planning, return:

```text
user subject:
desired feeling:
structure token (from / what):
palette·light token (from / what):
shared restraint:
anti-pastiche check:
forbidden famous work (per token): {work A}, {work B}
how the tokens map onto the subject:
final image prompt:
QA risks:
```

For generation, produce one image at a time and report:

- image path
- the tokens applied (structure / palette·light / restraint)
- one line on how they serve the subject
- whether it passes QA or needs regeneration

## References

- `references/style-routing.md`: the subject→register lookup table — read FIRST to route the subject to one master register before pulling tokens.
- `references/token-axes.md`: the reusable visual dimensions (palette logic, composition, negative space, light, texture, motif, type, restraint).
- `references/master-library.md`: 25 world-class masters and their extractable tokens, use-when, restraint, and anti-pastiche transfer note.
- `references/blending.md`: how to choose by token and combine one structure + one palette/light + one restraint.
- `references/prompt-template.md`: planning, final generation, and edit templates.
- `references/qa-checklist.md`: acceptance, regeneration, and anti-pastiche repair rules.
