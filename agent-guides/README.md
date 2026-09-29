# Agent Guides

Every skill in this repo has two layers:

1. **Workflow layer** — the decision gate, the structured plan, the style DNA, the QA. This
   is plain Markdown and portable across agent tools.
2. **Rendering layer** — the image model that turns the final prompt into pixels. This
   depends on the model, especially for Chinese text.

The workflow layer is what you install. The skills do not require Codex skill metadata, MCP,
custom commands, or any specific runtime — just an agent that follows Markdown instructions.

## Codex

Copy a skill folder into the Codex skills directory and restart:

```bash
mkdir -p ~/.codex/skills
cp -R cover-pop ~/.codex/skills/cover-pop
```

Call it with `$cover-pop` / `$sticker-set` / `$quote-cards`.

## Claude Code

Two options:

- **Project skill**: drop the skill folder into the project so the `SKILL.md` is discoverable,
  then ask Claude to use it by name.
- **CLAUDE.md snippet**: paste the relevant rules into the project's `CLAUDE.md`. Minimal
  snippet:

```markdown
## Cover Pop

When the user asks for a 封面 / 小红书封面 / 公众号封面 / 视频封面, use the Cover Pop workflow:
identify the target reader and scroll moment, write the core promise, pick a cover archetype,
run the Stop Test, write a thumbnail-readable title, then produce the final image prompt and
QA it. Do not make it look 微商, 土味, like a PPT title slide, or AI-plastic. Full rules:
cover-pop/SKILL.md and cover-pop/references/.
```

Swap in `sticker-set` (Chat-Moment Test, model-sheet-first consistency), `quote-cards` (Save
Test, typographic hierarchy), `rank-cards` (Ranking Integrity Test, one portrait pipeline), or
`master-styles` (Token Transfer Test, extract-and-blend art direction) the same way.

`master-styles` can also layer on top of another skill: plan the content with that skill, then
add one structure token + one palette/light token + one restraint from `master-styles` for the
art direction.

## Cursor

Turn a skill into a project rule (`.cursor/rules/*.mdc`): use the skill's `SKILL.md` body as
the rule content, with Cursor-style frontmatter (`description`, `globs`, `alwaysApply`). Keep
the references nearby so the rule can point at them.

## Hermes Agent / OpenClaw / Other Agents

Treat a skill as a reusable workflow prompt or project-level instruction. Give the agent the
`SKILL.md` plus its `references/`. The agent does not need to understand any package format —
it just needs to follow the chain:

```text
decision gate -> structured plan -> style DNA -> final image prompt -> QA
```

## Rendering Notes

- The workflow plans the image and writes the prompt; a strong image model renders it.
- Chinese text is the most fragile part. If the model mangles characters, use the
  `text-fix` edit prompt in each skill's `references/prompt-template.md`, or generate with a
  blank text area and overlay the exact text in an editor.
- If the agent you use has no strong image generation, let it own the planning and the final
  prompt, then send that prompt to a stronger image model.
