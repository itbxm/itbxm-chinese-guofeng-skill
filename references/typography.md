# 字体

字体的任务是把国风氛围和可读内容分开。只使用可商用的开源字体，并保留原始 font family name。

## 书写系统选择

写 CSS 前先按脚本选择字体包：

- 简体中文、中国大陆或 `lang="zh-CN"` 页面使用 `zh-Hans` / SC 字体。
- 繁体中文、台湾、香港、澳门或 `lang="zh-TW"` / `lang="zh-HK"` 页面使用 `zh-Hant` / TC 字体。
- 不要同时加载 SC 和 TC 字体包，除非内容确实简繁混排。
- 用户没指定时，从正文判断；没有正文或混合时默认 `zh-Hans`，并说明可切换 `zh-Hant`。
- 发布网页用 `data/fonts.json` 的 `script_profiles` 选择 Noto CSS，并加载已注册的 ITBXM R2 装饰字体 CSS。

## Web Font Delivery

发布网页使用 Google Fonts CSS API 加载 Noto 字体，并使用 ITBXM R2 `result.css` 加载装饰字体：

- `KingHwaOldSong-MN`: `https://cdn.itbxm.com/fonts/KingHwaOldSong-MN/result.css`
- `ZhaohuaMinA`: `https://cdn.itbxm.com/fonts/ZhaohuaMinA/result.css`
- 不要在生成网页中打包 TTF 或手写 `@font-face` 字体文件 URL。
- web font 后面必须保留 system fallback。

## Font Roles

| Role | 简体栈 | 繁体栈 | 用途 |
| --- | --- | --- | --- |
| `--font-body` | `"Noto Sans SC", "Source Han Sans SC", "Microsoft YaHei UI", "Microsoft YaHei", "PingFang SC", system-ui, sans-serif` | `"Noto Sans TC", "Source Han Sans TC", "Microsoft JhengHei UI", "Microsoft JhengHei", "PingFang TC", system-ui, sans-serif` | 正文、图注、导航、UI 标签 |
| `--font-title-serif` | `"Noto Serif SC", "Source Han Serif SC", "Songti SC", "SimSun", serif` | `"Noto Serif TC", "Source Han Serif TC", "Songti TC", "PMingLiU", "MingLiU", serif` | 古典标题、编辑标题、文化 deck |
| `--font-title-sans` | 同简体正文 | 同繁体正文 | 现代国风网页、产品页、信息密集页 |
| `--font-poem` | `"KingHwaOldSong-MN", "京華老宋体-MN折中印刷字形", "Noto Serif SC", "Source Han Serif SC", "Kaiti SC", "STKaiti", "KaiTi", serif` | `"KingHwaOldSong-MN", "京華老宋体-MN折中印刷字形", "Noto Serif TC", "Source Han Serif TC", "Kaiti TC", "BiauKai", "PMingLiU", serif` | 诗句、引用、短题记 |
| `--font-meta` | `"Noto Sans Mono", "SFMono-Regular", Consolas, ui-monospace, monospace` | `"Noto Sans Mono", "SFMono-Regular", Consolas, ui-monospace, monospace` | 页码、日期、metadata、技术标签；不是中文正文字体 |
| `--font-display-heavy` | `"ZhaohuaMinA", "朝华标题A", "Noto Serif SC", "Source Han Serif SC", "Songti SC", "SimSun", serif` | `"ZhaohuaMinA", "朝華標題A", "Noto Serif TC", "Source Han Serif TC", "PMingLiU", serif` | 网站 hero、deck cover、章节页、强视觉中文短标题 |
| `--font-display-light` | `"KingHwaOldSong-MN", "京華老宋体-MN折中印刷字形", "Noto Serif SC", "Source Han Serif SC", "Songti SC", "SimSun", serif` | `"KingHwaOldSong-MN", "京華老宋体-MN折中印刷字形", "Noto Serif TC", "Source Han Serif TC", "Songti TC", "PMingLiU", serif` | 题签、展签、署名、短文化标题、PPT 卡片标题 |
| `--font-art` | `var(--font-display-heavy)` | `var(--font-display-heavy)` | 印章、匾额、章节标记、短装饰标签 |

## CSS Starter: Simplified Chinese

```css
:root {
  --font-body: "Noto Sans SC", "Source Han Sans SC", "Microsoft YaHei UI", "Microsoft YaHei", "PingFang SC", system-ui, sans-serif;
  --font-title-serif: "Noto Serif SC", "Source Han Serif SC", "Songti SC", "SimSun", serif;
  --font-title-sans: "Noto Sans SC", "Source Han Sans SC", "Microsoft YaHei UI", "Microsoft YaHei", "PingFang SC", system-ui, sans-serif;
  --font-poem: "KingHwaOldSong-MN", "京華老宋体-MN折中印刷字形", "Noto Serif SC", "Source Han Serif SC", "Kaiti SC", "STKaiti", "KaiTi", serif;
  --font-meta: "Noto Sans Mono", "SFMono-Regular", Consolas, ui-monospace, monospace;
  --font-display-heavy: "ZhaohuaMinA", "朝华标题A", "Noto Serif SC", "Source Han Serif SC", "Songti SC", "SimSun", serif;
  --font-display-light: "KingHwaOldSong-MN", "京華老宋体-MN折中印刷字形", "Noto Serif SC", "Source Han Serif SC", "Songti SC", "SimSun", serif;
  --font-art: var(--font-display-heavy);
}
```

## CSS Starter: Traditional Chinese

```css
:root {
  --font-body: "Noto Sans TC", "Source Han Sans TC", "Microsoft JhengHei UI", "Microsoft JhengHei", "PingFang TC", system-ui, sans-serif;
  --font-title-serif: "Noto Serif TC", "Source Han Serif TC", "Songti TC", "PMingLiU", "MingLiU", serif;
  --font-title-sans: "Noto Sans TC", "Source Han Sans TC", "Microsoft JhengHei UI", "Microsoft JhengHei", "PingFang TC", system-ui, sans-serif;
  --font-poem: "KingHwaOldSong-MN", "京華老宋体-MN折中印刷字形", "Noto Serif TC", "Source Han Serif TC", "Kaiti TC", "BiauKai", "PMingLiU", serif;
  --font-meta: "Noto Sans Mono", "SFMono-Regular", Consolas, ui-monospace, monospace;
  --font-display-heavy: "ZhaohuaMinA", "朝華標題A", "Noto Serif TC", "Source Han Serif TC", "Songti TC", "PMingLiU", serif;
  --font-display-light: "KingHwaOldSong-MN", "京華老宋体-MN折中印刷字形", "Noto Serif TC", "Source Han Serif TC", "Songti TC", "PMingLiU", serif;
  --font-art: var(--font-display-heavy);
}
```

选择变量后，可用这些通用 selector：

```css
body { font-family: var(--font-body); }
.guofeng-title { font-family: var(--font-title-serif); }
.guofeng-display-title { font-family: var(--font-display-heavy); }
.guofeng-light-title { font-family: var(--font-display-light); }
.guofeng-modern-title { font-family: var(--font-title-sans); }
.guofeng-poem,
.guofeng-inscription { font-family: var(--font-poem); }
.guofeng-seal,
.guofeng-plaque { font-family: var(--font-art); }
.guofeng-meta { font-family: var(--font-meta); }
```

## 场景建议

| 场景 | 推荐组合 |
| --- | --- |
| 文化 PPT 或博物馆式页面 | `Noto Serif SC/TC` 标题 + `Noto Sans SC/TC` 正文 |
| 现代品牌国风网页 | `Noto Sans SC/TC` 标题/正文 + 纹样点缀 |
| 诗词、茶、香、古典文学 | 短诗句可用 `KingHwaOldSong-MN`，解释用 Noto/system |
| 数据或产品展示 | `Noto Sans SC/TC` 正文 + mono metadata 用于拉丁数字、id 和 code |
| 网站 hero 或 deck cover | 主标题可用 `ZhaohuaMinA`，正文用 sans |
| 入境游 | 装饰字体只用于中文地名或视觉标题；英文说明用可读 sans/serif |
| 地方餐饮 | 店名、菜系名、招牌菜名可用装饰字体；价格、地址、菜单描述和预约信息不用 |

## 可读性规则

- 正文默认使用 Noto 或系统字体。
- 装饰字体只用于短文本：网页 2-12 个中文字符最稳；HTML PPT 的封面、章节和短文化标题可到约 16 个中文字符。
- 装饰字体标题只要可能换成两行，`line-height` 不得低于 `1.12`，推荐 `1.16-1.24`；不要使用 `0.95`、`0.98` 或 `1` 这类紧贴行高。
- 超过约 12 个中文字符的网页 hero 标题、混排英文标题或双语标题，优先改用 `--font-title-serif`，或拆成短主标题 + 可读副标题。
- `--font-meta` 只用于拉丁数字、id、code-like 标签和紧凑 metadata；中文描述仍用 `--font-body`。
- 段落不要用书法、篆刻、装饰明宋或高装饰字体。
- dense 纹样背后有文字时，先加实色或半透明纸色层。
- 古典温度用 serif 标题；现代产品或信息密集场景用 sans 标题。
- 诗词 quote 不要把整首诗写成一个大字号段落再用 `<br>` 换行；用 `guofeng-poem-line` 表示一整句或一联，用 `guofeng-poem-half` 包住逗号前后半句，并通过 CSS 降字号或半句换行保护断句。
- PPT 中文正文通常至少 18px，图注至少 14-16px。
- 竖排题签要短且留足字距；不要旋转长段正文。
- 课程正文、路线说明、菜单说明、价格、地址和密集图注不要使用 `--font-display-heavy` 或 `--font-display-light`。

## HTML PPT Typography

HTML PPT 可以比普通网页更积极使用装饰字体。

- 正文、路线、菜单、课程解释、图注、价格、地址和时间使用 `--font-body`。
- `--font-display-heavy` / Zhaohua 用于 cover title、chapter title、强视觉页面和重要短中文标题。
- `--font-display-light` / KingHwa 用于诗句、展签标题、题签、卡片标题、文化注释和短 section heading。
- `--font-title-serif` 是普通内容标题、较长标题和装饰字体影响阅读时的 fallback。
- cover、chapter 和 closing 的装饰标题如果超过一行，使用 `line-height: 1.16-1.24`；长标题拆行或改用 `--font-title-serif`。
- 现代商业 deck 标题可用 `--font-title-sans`。
- `--font-art` 用于 cover title、章节标记、印章、匾额、署名和短装饰标签。
- `--font-poem` 用于诗句、短文化引用、展签式标题和课程 pause page。
- HTML PPT quote 页同样使用结构化诗行；不要让浏览器把七言、五言或词牌句拆在单字、标点或半句中间。
- 入境游或双语 deck 的英文说明必须使用可读 sans/serif，不使用中文装饰字体栈。

## Font CSS For Web Pages

发布网页使用 Google Fonts CSS API 加载 Noto web fonts，并用 ITBXM R2 `result.css` 加载装饰字体。不要打包 TTF 或手写字体文件 URL。

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Mono:wght@400;600&family=Noto+Sans+SC:wght@400;600&display=swap">
<link rel="stylesheet" href="https://cdn.itbxm.com/fonts/KingHwaOldSong-MN/result.css">
<link rel="stylesheet" href="https://cdn.itbxm.com/fonts/ZhaohuaMinA/result.css">
```

字体 CSS 不可用时，字体栈会直接回退到 Noto 或本机系统字体。
