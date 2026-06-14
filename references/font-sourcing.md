# Font Sourcing And Delivery

This project uses commercially usable fonts with explicit source evidence. Web output prioritizes fast, stable rendering and loads decorative Chinese fonts through ITBXM R2 `result.css` files.

## Policy

- Published web pages use Google Fonts CSS API for Noto fonts.
- Decorative fonts use ITBXM R2 `result.css` links:
  - `https://cdn.itbxm.com/fonts/KingHwaOldSong-MN/result.css`
  - `https://cdn.itbxm.com/fonts/ZhaohuaMinA/result.css`
- Do not bundle TTF files or hand-write `@font-face` font-file URLs in generated HTML/CSS.
- CSS stays in the generated project or template.
- Choose SC fonts for `zh-Hans` and TC fonts for `zh-Hant`; do not load both unless the page intentionally mixes scripts.
- Every registered font must have clear license/source evidence and `commercial_use_allowed: true`.

## Metadata Requirements

Each font entry in `data/fonts.json` must include:

- `id`
- `name`
- `font_family`
- `script`
- `role`
- `license`
- `license_url`
- `license_evidence_url` when `license_url` does not point to a standard license text
- `open_source`
- `commercial_use_allowed`
- `css_variable`
- `fallback_stack`
- `weights`

Decorative web fonts must also include:

- `author`
- `author_url`
- `usage`
- `restrictions`
- `web_css_url`
- `web_source`

Source rules:

- `google_css_url` values must start with `https://fonts.googleapis.com/` when present.
- Decorative `web_css_url` values must start with `https://cdn.itbxm.com/fonts/` and end with `/result.css`.
- Web templates must not contain `.ttf`, `format("truetype")`, old `fonts.itbxm.com` URLs, or handwritten `fonts.gstatic.com/s/...` URLs.
- Use the real font family names, not display-friendly aliases.

## Web CSS Pattern

For published web pages, load Noto through Google Fonts CSS API and decorative Chinese fonts through ITBXM R2 `result.css`.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.itbxm.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Mono:wght@400;600&family=Noto+Sans+SC:wght@400;600&family=Noto+Serif+SC:wght@400;600&display=swap">
<link rel="stylesheet" href="https://cdn.itbxm.com/fonts/KingHwaOldSong-MN/result.css">
<link rel="stylesheet" href="https://cdn.itbxm.com/fonts/ZhaohuaMinA/result.css">
```

```css
:root {
  --font-body: "Noto Sans SC", "Source Han Sans SC", "Microsoft YaHei UI", "Microsoft YaHei", "PingFang SC", system-ui, sans-serif;
  --font-title-serif: "Noto Serif SC", "Source Han Serif SC", "Songti SC", "SimSun", serif;
  --font-display-heavy: "ZhaohuaMinA", "朝华标题A", "Noto Serif SC", "Source Han Serif SC", "Songti SC", "SimSun", serif;
  --font-display-light: "KingHwaOldSong-MN", "京華老宋体-MN折中印刷字形", "Noto Serif SC", "Source Han Serif SC", "Songti SC", "SimSun", serif;
}
```

If a decorative CSS file is unavailable, the page falls back to Noto/system fonts through the CSS stack.

## Decorative Web Fonts

Current decorative font families:

- `朝华标题明朝体A` / `ZhaohuaMinA`: heavier display font for website hero titles, deck cover slide titles, chapter openers, and brand hero text.
- `京华老宋体MN` / `KingHwaOldSong-MN`: lighter decorative serif for poems, title slips, exhibit labels, signatures, and short cultural headings.

Both are credited to 特里王: `https://www.zhihu.com/people/wang-ting-rui-61`.

Font source evidence is kept in `data/fonts.json` and README.

Do not use decorative fonts for long body text, menus, route descriptions, course paragraphs, prices, addresses, or dense captions.

## Adding A Font

1. Confirm the font has clear license/source evidence and is commercially usable.
2. Add its real `font_family` to `data/fonts.json`.
3. Add its script or locale, such as `zh-Hans`, `zh-Hant`, or `Latn`.
4. Add author and author homepage when the font is not from Google/Noto.
5. Add a `google_css_url` only if the font is available from Google Fonts CSS API.
6. Add a `web_css_url` only when the ITBXM R2 `result.css` has been prepared.
7. Add author/source evidence for every third-party font.
8. Do not bundle TTF files in this repository.
