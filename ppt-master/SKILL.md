---
name: ppt-master
description: "AI-driven multi-format SVG content generation system. Converts source documents (PDF/DOCX/URL/Markdown) into high-quality SVG pages and exports to PPTX through multi-role collaboration. Use when user asks to \"create PPT\", \"make presentation\", \"生成PPT\", \"做PPT\", \"制作演示文稿\", or mentions \"ppt-master\"."
---

# ppt-master（Progressive Disclosure 瘦身入口）

> **Fleet Progressive Disclosure**: 默认只读本页脊柱。完整旧正文在 `references/full-rulebook.md`（默认不读）。需要细节时按节打开 full-rulebook，禁止通读当仪式。

## 何时用

见下方保留脊柱 / frontmatter description。若任务只需短约束，优先 vault `04-Prompts/UI铁律-速查卡.md`（仅 UI 类）。

## 阅读预算（硬）

1. 读完本页即可开工  
2. 卡住再查 `references/full-rulebook.md` 相关小节  
3. 有 scripts/data 则按需跑脚本，勿灌全表  

## 保留脊柱（摘自原文前部）

# PPT Master Skill

> AI-driven multi-format SVG content generation system. Converts source documents into high-quality SVG pages through multi-role collaboration and exports to PPTX.

**Core Pipeline**: `Source Document → Create Project → [Template] → Strategist → [Image_Generator] → Executor Live Preview → Quality Check → Post-processing → Export`

> [!CAUTION]
> ## 🚨 Global Execution Discipline (MANDATORY)
>
> **This workflow is a strict serial pipeline. The following rules have the highest priority — violating any one of them constitutes execution failure:**
>
> 1. **SERIAL EXECUTION** — Steps MUST be executed in order; the output of each step is the input for the next. Non-BLOCKING adjacent steps may proceed continuously once prerequisites are met, without waiting for the user to say "continue"
> 2. **BLOCKING = HARD STOP** — Steps marked ⛔ BLOCKING require a full stop; the AI MUST wait for an explicit user response before proceeding and MUST NOT make any decisions on behalf of the user
> 3. **NO CROSS-PHASE BUNDLING** — Cross-phase bundling is FORBIDDEN. (Note: the Eight Confirmations in Step 4 are ⛔ BLOCKING — the AI MUST present recommendations and wait for explicit user confirmation before proceeding. Once the user confirms, all subsequent non-BLOCKING steps — design spec output, SVG generation, speaker notes, and post-processing — may proceed automatically without further user confirmation)
> 4. **GATE BEFORE ENTRY** — Each Step has prerequisites (🚧 GATE) listed at the top; these MUST be verified before starting that Step
> 5. **NO SPECULATIVE EXECUTION** — "Pre-preparing" content for subsequent Steps is FORBIDDEN (e.g., writing SVG code during the Strategist phase)
> 6. **NO SUB-AGENT SVG GENERATION** — Executor Step 6 SVG generation is context-dependent and MUST be completed by the current main agent end-to-end. Delegating page SVG generation to sub-agents is FORBIDDEN
> 7. **SEQUENTIAL PAGE GENERATION ONLY** — In Executor Step 6, after the global design context is confirmed, SVG pages MUST be generated sequentially page by page in one continuous pass. Grouped page batches (for example, 5 pages at a time) are FORBIDDEN
> 8. **SPEC_LOCK RE-READ PER PAGE** — Before generating each SVG page, Executor MUST `read_file <project_path>/spec_lock.md`. All colors / fonts / icons / images MUST come from this file — no values from memory or invented on the fly. Executor MUST also look up the current page's `page_rhythm` (`anchor` / `dense` / `breathing`), `page_layouts` (which template SVG to inherit, if any), and `page_charts` (which chart template to adapt, if any). Empty / absent entries are intentional Strategist signals — see executor-base.md §2.1. This rule exists to resist context-compression drift on long decks and to break the uniform "every page is a card grid" default
> 9. **SVG MUST BE HAND-WRITTEN, NOT SCRIPT-GENERATED** — Every SVG page is written by the main agent directly, one page at a time (see rules 6 and 7). Writing or running a Python / Node / shell script that produces the SVG files in batch — looping over pages, templating from data, or emitting them via a generator — is FORBIDDEN, including under "save tokens", "quick draft", or "user is in a hurry" pretexts. The script-generation path was tried on a feature branch and abandoned: cross-page visual consistency depends on per-page authoring with full upstream context, which a generator script cannot reproduce
> 10. **FOLLOW DETERMINISTIC ROUTING RULES** — Do not add blocking routing questions when this skill defines a route. If the user request violates a route precondition, state the required prerequisite and stop that route instead of asking the user to choose around the rule. Ordinary finite options, stylistic preferences, and recoverable details are surfaced with a recommended value plus alternatives at the next existing confirmation gate.

> [!IMPORTANT]
> ## 🌐 Language & Communication Rule
>
> - **Response language**: match the user's input and source materials. Explicit user override (e.g., "请用英文回答") takes precedence.
> - **User-facing option labels**: when presenting confirmations, brief proposals, choices, or finite option sets, use the user's language for labels and explanations. English enum IDs / file fields may appear in parentheses for precision, but never rely on English-only labels such as `deck`, `layout`, `mirror`, or `fidelity` without a localized explanation.
> - **Template format**: `design_spec.md` MUST follow its original 

…(spine truncated; see full-rulebook)


## 完整规则书

→ `references/full-rulebook.md`
