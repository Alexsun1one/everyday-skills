# Everyday Skills

> A set of agent skills for ordinary people: make publish-grade covers, sticker sets, and
> idea cards — without a designer.

[中文](README.md)

Everyday Skills is a collection of installable, open-source, cross-agent skill packages.
Each skill is not a filter or a template — it is a **strict workflow**: decide whether the
image is worth making, force a vague idea into a clear plan, then hand a final prompt to an
image model to produce something you can publish as-is.

It inherits the method of [Paper Operators](../skillsdesign) — **a strict skill skeleton
that turns a thing ordinary people do badly into publish-grade output** — but each skill
carries its own visual identity and quality bar.

## Shared Workflow DNA

Every skill shares one skeleton:

1. **Decision gate** — first ask "should this image exist at all, and for whom?" Reject the
   empty, the filler, the decorative.
2. **Structured plan** — break intent into target reader, core promise, archetype,
   hierarchy… ending in one final prompt.
3. **Subject-based aesthetic auto-routing** — each skill reads the subject and AUTOMATICALLY
   picks the fitting visual register (poets → ink-wash, footballers → sports card, 国学 cards →
   calligraphy, knowledge → Swiss grid), applying transferable tokens from
   [`master-styles`](master-styles/), the **shared aesthetic engine**. The user never names a
   style, and master-styles is **not a standalone skill you invoke** — it is the engine the
   content skills route into.
4. **Style DNA + anti-template rules** — spell out what NOT to make (微商 spam, PPT slides,
   tacky posters, AI plastic). This is the quality moat.
5. **QA checklist** — explicit accept / regenerate / repair. If it fails, redo it.

Same method, any tool: Codex, Claude Code, Cursor, Hermes Agent, and OpenClaw can all use
the same rules, as long as they follow plain Markdown instructions.

## Skills

**Everyday line** — high-frequency, ready to use:

| Skill | Job | For |
| --- | --- | --- |
| [`cover-pop`](cover-pop/) | Social covers (Xiaohongshu / WeChat / video / Moments) whose one job is to earn the tap | Anyone who posts content |
| [`sticker-set`](sticker-set/) | A consistent set of chat stickers from one original character, with captions | People who want their own sticker pack |
| [`quote-cards`](quote-cards/) | Turn one idea — a quote, tip, or note — into a collectable typographic card | Knowledge sharers, note-takers |

**Advanced line** — a stronger harness for designer-grade output:

| Skill | Job | For |
| --- | --- | --- |
| [`rank-cards`](rank-cards/) | Ranking / tier cards (football legacy, GOAT pyramids, Top-N) generalized to writers, musicians, directors | Ranking/recap creators |
| [`master-styles`](master-styles/) | Extract world-class artists' transferable visual tokens to elevate any image; usable as an aesthetic engine over other skills | Anyone who wants a premium, art-directed look |

Each skill is self-contained (`SKILL.md` + `references/` + its own `README.md`) and can be
lifted out and open-sourced on its own.

## Quick Start

### Codex

Copy any one skill folder into the Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R cover-pop ~/.codex/skills/cover-pop
```

Then call it:

```text
Use $cover-pop to plan a Xiaohongshu cover for "3 steps to write social posts that don't cringe". Plan first, don't generate yet.
```

### Other Agents (Claude Code / Cursor / Hermes / OpenClaw)

No Codex skill format needed. Paste the skill's `SKILL.md` and `references/` as project
instructions, rules, or a workflow prompt. See [`agent-guides/README.md`](agent-guides/README.md)
for per-tool notes and [`examples/prompts.md`](examples/prompts.md) for more examples.

Note: what travels across agents is the planning + prompting + QA workflow; final image
quality depends on the image model, especially for rendering Chinese text. When text renders
badly, use the text-fix flow in each skill's `prompt-template.md`, or generate with a blank
text block and overlay the exact text in an editor.

## License

MIT. See [`LICENSE`](LICENSE).
