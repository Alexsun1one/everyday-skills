# Design Tokens

This token system has three tiers.

1. **`tokens/dtcg/` is the canonical source.** It uses DTCG-style JSON with `$value`, `$type`, and `{group.token}` references, so the same values can feed CSS today and other platforms later. `base.json` holds primitives and cross-direction scales; `semantic.json` holds component-facing meanings; `theme-*.json` files override palette, owned accent, type personality, density, radius, and motion choices per direction.

2. **`tokens/css/` is directly importable.** These files are generated from DTCG and can be used by generated pages with `@import "./tokens/css/precision-dark.css";`. Every emitted value is a CSS custom property, so pages do not translate token names by hand.

3. **The existing Markdown files explain the judgment.** Files like `00-token-synthesis.md`, `by-domain/editor-ide.md`, and `references/world-class-teardowns/00-moodboard-tokens.md` remain the WHY layer: what to choose, when to choose it, and what failure modes to avoid. Do not edit those prose sources when rebuilding tokens.

## Rebuild

```bash
node tokens/build-tokens.mjs
```

The script has no runtime dependencies. It reads `tokens/dtcg/base.json`, `semantic.json`, and all `theme-*.json` files, resolves DTCG references, validates that every token has `$type`, and emits `tokens/css/base.css` plus one CSS file per direction.

## Add a Direction

1. Add `tokens/dtcg/theme-<direction>.json`.
2. Set `$extensions.designPractice.direction`, `ownedAccent`, `typePersonality`, and `signatureMove`.
3. Override only the tokens that truly differ: usually `color.accent.owned`, `color.palette.*`, semantic `color.*`, `font.family.*`, and selective `radius.*` or `motion.*`.
4. Run `node tokens/build-tokens.mjs`.
5. Import `tokens/css/<direction>.css` in the generated page.

Current directions: `precision-dark`, `editorial-fintech`, `warm-editorial`, `luxury`, `brutalist`, `data-dense`, and `editor-ide`.
