# Agent Usage Patterns

Choose the asset by layout job before choosing the motif.

For full websites or HTML PPT decks, choose a theme from `data/themes.json` before selecting an ornament. For small isolated snippets such as a divider or side border, choosing by layout job alone is acceptable.

| Layout job | Preferred asset | CSS repeat | Common size |
| --- | --- | --- | --- |
| Title divider | `assets.strip_horizontal` | `repeat-x` | `32-72px` high |
| Header band | `assets.strip_horizontal` | `repeat-x` | `48-96px` high |
| Side border | `assets.strip_vertical` | `repeat-y` | `24-64px` wide |
| Subtle background | `assets.tile` | `repeat` | original tile ratio, low opacity |
| Cover accent | `assets.cover_accent` | `no-repeat` | large crop, edge or corner placement |
| Layered background | `assets.tile` | `repeat` | low opacity or blend mode |

## Defaults

- If the user asks for a complete HTML deck, landing page, or full-page starting point, read `references/templates.md` and copy the closest seed template.
- If the user asks for a full Chinese-style website or PPT page, read `references/themes.md` and pick one theme first.
- If the user asks for a Chinese-style title decoration, use `strip_horizontal`.
- If the user asks for a side border or page-side ornament, use `strip_vertical`.
- If the user asks for a soft background, use `tile` at low opacity.
- If the user asks for a deck cover slide or chapter opener, use `cover_accent`.
- If body text must remain readable, avoid dense high-contrast repeats behind text.

## Theme-Aware Selection

After choosing a theme:

1. Filter patterns by the requested `usage_modes`.
2. Prefer `color_family` values listed in the selected theme's `recommended_color_family`.
3. Prefer `sparse` or `medium` density for visible dividers, side borders, and readable layouts.
4. Use `dense` patterns for cover accents, hero texture, or low-opacity layered backgrounds.
5. Apply theme variables from `references/themes.md` instead of hard-coded ad hoc colors.

## HTML/CSS Templates

Divider:

```html
<div class="guofeng-divider" style="height:48px;background-image:url('PATH_TO_STRIP_HORIZONTAL');background-repeat:repeat-x;background-size:auto 48px;"></div>
```

Side border:

```html
<aside class="guofeng-side-border" style="width:44px;background-image:url('PATH_TO_STRIP_VERTICAL');background-repeat:repeat-y;background-size:44px auto;"></aside>
```

Subtle background:

```html
<section class="guofeng-soft-bg" style="background-image:url('PATH_TO_TILE');background-repeat:repeat;background-size:auto;opacity:.10;"></section>
```

Layered background:

```html
<section class="guofeng-layered" style="background-color:var(--gf-paper);background-image:url('PATH_TO_TILE');background-repeat:repeat;background-size:auto;background-blend-mode:var(--gf-pattern-blend);"></section>
```

## Restrictions

- Do not invent paths.
- Do not mix multiple theme presets in one page or deck.
- Do not default to full-page dense backgrounds.
- Do not use catalog previews, corner experiments, or nine-slice frame experiments as production defaults.
