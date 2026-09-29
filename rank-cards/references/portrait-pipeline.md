# Portrait Pipeline

This is the core of the skill. A ranking card looks professional or amateur based on one
thing: whether every subject went through the SAME pipeline. Mismatched crops, backgrounds,
lighting, and art styles are the loudest "thrown together" tell. Pass every portrait through
the same five steps, no exceptions.

## Two production paths — pick one before generating

A single text-to-image prompt cannot composite ten real, recognizable people onto a shared
backdrop and duotone them identically — it will hallucinate or smear faces. Decide the path
first:

- **Path A — real people** (球星, 作家, 导演 with real likenesses): do NOT ask the model to
  assemble the card. Export each subject as an individual cutout, apply one duotone in an
  editor, and lay them out on the grid. The model only renders the empty frame, tier bands,
  and chrome. This is the only way to get true unity with real likenesses.
- **Path B — generated subjects** (illustrated characters, icons, original mascots, or a
  deliberately stylized register): render ALL subjects in ONE pass / one prompt so the
  treatment is automatic and identical. Never ask one generation to both invent and unify N
  faces.

## Real-person likeness

When subjects are real public figures, prefer compositing licensed or owned photos (Path A).
If you generate, use an openly stylized/illustrated register rather than photoreal
impersonation, and never fabricate a photoreal real person sitting in a defamatory "worst"
tier. Likeness, IP, and reputation are real exposure — treat them with the same care the
sticker skill gives to not copying IP.

## The five locks

Lock these once, then apply identically to every subject:

1. **Same crop & framing** — all head-and-shoulders, OR all chest-up. Eyelines on a common
   horizontal. Faces at the same relative scale in every cell. Mixed crops read as amateur.
2. **Same background** — one shared backdrop for everyone: a solid, a single gradient, or a
   unified texture. Knock each subject out of their original photo and place them on the
   common backdrop. Never leave the original photo backgrounds in — that is the collage look.
3. **Same color treatment** — apply ONE finish to all: a duotone wash (shadows → color A,
   highlights → color B), a desaturate-then-tint, or a matched key light. Duotone is the
   default unifier because it forces visual unity over photos shot in totally different
   conditions. Pretend each subject came from a neutral backdrop with even diffused light,
   then tint all of them the same way.
4. **Same edge / frame** — either all clean cutouts, or all wrapped in the same ring/badge.
   Never mix a ringed portrait with a bare one. A tier-colored ring is a clean way to
   double-encode tier membership.
5. **One art register** — all photographic-realistic, OR all illustrated. Never mix a
   painted portrait with a photo with a cartoon in one card. For pre-photography subjects
   (writers, classical composers, scientists), convert everything to one register.

## Choosing the photo (the editorial call)

Decide once, apply to all:

- **Era / form** — match the basis. 历史地位 / 巅峰 → peak-era imagery (peak haircut, peak
  kit). 现役 ranking → current. Don't mix peak-era and current in one card.
- **Kit / affiliation** — pick the signature peak-club jersey OR the national team, and hold
  it for everyone. Don't put one subject in club colors and another in country.
- **Expression** — neutral, confident, dignified for status/段位 cards. Action shots only if
  the whole card is action-themed. Keep everyone at the same emotional register.
- **Recognizability** — choose the most iconic, instantly-identifiable likeness. Ambiguous
  angles kill the "I know him" hit that makes the card land.

## Quality floor

- Set a sharpness/resolution minimum. One soft, pixelated, or watermarked face drags the
  whole card down.
- If generating portraits rather than compositing real photos, render ALL subjects in one
  consistent pass — same model, same treatment, same resolution — so the pipeline is
  automatic rather than retrofitted.

## Duotone quick recipe

When unifying disparate source photos, duotone is the fastest path to a designed look:

- pick two colors: a deep shadow tone and a light highlight tone (often tied to the card's
  accent or the tier color)
- map every portrait's shadows to the dark tone and highlights to the light tone
- keep the same two tones for every subject in the card
- result: faces shot decades apart, in different lighting, read as one consistent set

## The one-line test

> Could these portraits plausibly have been shot in the same studio, on the same day, by the
> same photographer?

If no, the pipeline failed. Pull the outliers back through the five locks and regenerate.
