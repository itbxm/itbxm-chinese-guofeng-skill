# ITBXM Chinese Guofeng Skill · Websites / HTML PPT / Culture-Tourism Pages

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skill](https://img.shields.io/badge/AI%20Agent-Skill-7c3aed.svg)](SKILL.md)
[![HTML](https://img.shields.io/badge/output-HTML%20%2F%20PPT-c2410c.svg)](assets/templates/)

> 中文说明: [README.md](README.md)

This is a local Agent Skill for Chinese guofeng visual work in Claude Code, Codex, Cursor, and similar tools. It packages Tang-style pattern assets, seven guofeng themes, Chinese typography guidance, website templates, and an HTML PPT runtime so an agent can generate static guofeng websites and horizontal HTML slide decks.

Repository: <https://github.com/itbxm/itbxm-chinese-guofeng-skill>

Good use cases:

- Cultural courses, museum pages, intangible heritage, history, and poetry
- Temple, garden, neighborhood, city-culture, and inbound-tourism guides
- Local dining, tea, wine, incense, homestays, and souvenir pages
- New Chinese-style brand pages, culture-tourism events, and HTML launch decks

It is static by design. It does not provide backend systems, login, upload, payment, live maps, reservations, or image generation services.

## 30-Second Start

### Option 1: Ask Your Agent To Install It

Send this to Claude Code, Codex, Cursor, or another local agent:

```text
Please install itbxm-chinese-guofeng-skill.
Repository: https://github.com/itbxm/itbxm-chinese-guofeng-skill

If you are Claude Code, install it at:
~/.claude/skills/itbxm-chinese-guofeng-skill

If you are Codex, install it at:
~/.agents/skills/itbxm-chinese-guofeng-skill

If you use another skills / tools / plugins directory, put it there.
After installation, read SKILL.md and tell me how I can use this Skill.
```

### Option 2: Put It In A Skills Folder

For Claude Code:

```bash
git clone https://github.com/itbxm/itbxm-chinese-guofeng-skill ~/.claude/skills/itbxm-chinese-guofeng-skill
```

For Codex:

```bash
git clone https://github.com/itbxm/itbxm-chinese-guofeng-skill ~/.agents/skills/itbxm-chinese-guofeng-skill
```

Other local agents can use the same idea: place this repository in their configured skills, tools, or plugins directory, then point the agent at `SKILL.md`.

If you are comfortable with command-line installers, you can also try:

```bash
npx skills add https://github.com/itbxm/itbxm-chinese-guofeng-skill --skill itbxm-chinese-guofeng-skill
```

Then ask:

```text
Use itbxm-chinese-guofeng-skill to create a guofeng HTML landing page for an inbound tourism route in Hangzhou.
```

## Prompting Tips

You can describe your request in natural language. Clearer context usually produces better results:

```text
Scenario: I need a homepage for a Jiangnan restaurant.
Audience: Young travelers and out-of-town visitors in Hangzhou.
Output: Static website / 6-page HTML PPT.
Content: Signature dishes, address, opening hours, reservation CTA, brand story.
Materials: I have the menu and address, but no dish photos; real venue imagery is okay.
Style: New Chinese, clean, slightly premium; no fixed brand colors.
```

Short prompts are fine too:

```text
Use itbxm-chinese-guofeng-skill to create a bilingual guofeng landing page for a 3-day inbound tourism route in Hangzhou. Mark incomplete facts as to be confirmed.
```

```text
Use itbxm-chinese-guofeng-skill to turn this traditional culture course outline into an 8-page HTML PPT for undergraduate general education students.
```

```text
Use itbxm-chinese-guofeng-skill to create a homepage for a new Chinese-style fragrance brand. I do not have brand guidelines yet; ask me what materials you need.
```

## Example Prompts

```text
Create an English temple guide page for first-time foreign visitors to China.
```

```text
Turn this museum object brief into a 6-page guofeng HTML PPT deck.
```

```text
Create a guofeng homepage for a Jiangnan restaurant, highlighting signature dishes, address, opening hours, and reservation CTA.
```

```text
Use this business plan to create a new Chinese-style fragrance launch deck.
```

```text
Create a bilingual culture-tourism landing page for a 3-day Dunhuang route.
```

## What It Does Well

- **24 Tang-style pattern sets**: each includes tile, horizontal strip, vertical strip, and cover accent assets.
- **Seven guofeng themes**: ink wash, porcelain blue, Tang vermilion gold, jade green, Dunhuang earth, night lacquer, and hua-chao rouge.
- **Two output types**: static websites and horizontal HTML PPT decks.
- **Cultural and commercial scenarios**: courses, museums, poetry, routes, menus, brand stories, and signup pages.
- **Simplified, Traditional, English, and bilingual guidance**: typography and readability recommendations for multiple language modes.
- **Portable static output**: generated work can be saved, deployed, or edited as a normal static project.

## Good Fit / Poor Fit

Good fit:

- Cultural education, course decks, salons, museum pages
- Inbound tourism, temple/garden/city guides, local routes
- Local dining, tea/wine/incense, homestays, souvenirs
- New Chinese-style brands, culture-tourism events, HTML launch decks

Poor fit:

- Backend dashboards, login, upload, payment, databases
- Live map APIs, real-time booking, orders, inventory
- Heavy spreadsheets, financial models, collaborative editing
- Online image generation or remote decorative font hosting

## Project Structure

```text
SKILL.md                 # Agent entry guide
data/                    # Pattern, theme, and font metadata
references/              # Workflow, scenarios, themes, typography, layouts, components, checklist
assets/patterns/         # 24 PNG/WebP Tang-style pattern sets
assets/templates/        # web-page.html and ppt-deck.html seed templates
assets/runtime/          # Local HTML PPT runtime
scripts/                 # Asset collection and HTML validation scripts
```

## License And Fonts

This repository is released under the [MIT License](LICENSE). Repository-owned code, documentation, templates, metadata, and original itbxm pattern assets may be used, modified, and redistributed under MIT, including commercial use.

This project mainly uses open-source, commercially usable Noto fonts for stable reading in body text, menus, routes, prices, addresses, English explanations, and dense captions.

Decorative fonts were open-sourced by [特里王](https://www.zhihu.com/people/wang-ting-rui-61) and are commercially usable. If the decorative font CSS is unavailable, pages fall back to Noto or system fonts.

## Acknowledgements

This project's Skill structure, README pacing, and HTML PPT workflow were inspired by 歸藏's [op7418/guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill). Thanks to 歸藏 for exploring and open-sourcing a clear way to package Agent Skills.

It also learns from 花叔's [alchaincyf/huashu-design](https://github.com/alchaincyf/huashu-design), especially HTML-native design, decision-maker-oriented workflows, five-dimensional review, image-first thinking, and resistance to overly safe generic design.
