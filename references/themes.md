# 主题

生成一个网页或一套完整 HTML PPT 前，先选一套 theme。Theme 决定页面气质；纹样应服务 theme，不要互相打架。

## 规则

- 一个生成结果只用一套 theme：一个网页页面或一套完整 deck。
- 不要混用不同 theme 的变量。
- 先按 theme 的 `recommended_color_family` 匹配纹样，再看 density 和 motif。
- 重复背景保持安静，默认使用 `--gf-pattern-opacity`。
- 文字压在纹样上时，先加纸色层或半透明面板。
- 生成 CSS 时优先使用 theme variables，不要随手写 random hex。

## CSS Variables

| Variable | 含义 |
| --- | --- |
| `--gf-ink` | 主文字和强线条 |
| `--gf-paper` | 主背景 |
| `--gf-paper-tint` | 次级背景 |
| `--gf-muted` | 弱化文字 |
| `--gf-line` | 细线和边框 |
| `--gf-accent` | 主国风强调色 |
| `--gf-accent-2` | 第二强调色 |
| `--gf-pattern-opacity` | 重复纹样默认透明度 |
| `--gf-pattern-blend` | 纹样叠加默认混合模式 |

## Theme Presets

### `ink-wash` 水墨宣纸

用于安静编辑页、散文、古典文化、茶、诗词和博物馆阅读型页面。

```css
:root {
  --gf-ink: #161412;
  --gf-paper: #f3efe6;
  --gf-paper-tint: #e7dfd0;
  --gf-muted: #6f675d;
  --gf-line: #c9bda9;
  --gf-accent: #8c1d18;
  --gf-accent-2: #2f5d50;
  --gf-pattern-opacity: 0.08;
  --gf-pattern-blend: multiply;
}
```

推荐纹样颜色：`neutral`, `dark`, `green`。

### `porcelain-blue` 青瓷月白

用于精致文化、研究、科技克制感、瓷器、档案和青花编辑页。

```css
:root {
  --gf-ink: #10243a;
  --gf-paper: #f4f7f6;
  --gf-paper-tint: #dce8ea;
  --gf-muted: #587080;
  --gf-line: #aec4cc;
  --gf-accent: #1f5d8c;
  --gf-accent-2: #9a6a2f;
  --gf-pattern-opacity: 0.09;
  --gf-pattern-blend: multiply;
}
```

推荐纹样颜色：`blue`, `cyan`, `neutral`。

### `tang-vermilion-gold` 唐宫朱金

用于节庆、仪式、发布会、标题页、新年、庆典和高能量唐风场景。

```css
:root {
  --gf-ink: #2a1710;
  --gf-paper: #f7ead2;
  --gf-paper-tint: #ecd1a5;
  --gf-muted: #7a5140;
  --gf-line: #cf9b5f;
  --gf-accent: #b3261e;
  --gf-accent-2: #c8942e;
  --gf-pattern-opacity: 0.12;
  --gf-pattern-blend: multiply;
}
```

推荐纹样颜色：`red`, `orange`, `yellow_gold`。

### `jade-green` 青玉竹色

用于自然、园林、茶、养生、文化产品、安静品牌和春夏国风场景。

```css
:root {
  --gf-ink: #14241d;
  --gf-paper: #f1f3e8;
  --gf-paper-tint: #dce5d4;
  --gf-muted: #566b5c;
  --gf-line: #aabca5;
  --gf-accent: #2f6f53;
  --gf-accent-2: #a66f2b;
  --gf-pattern-opacity: 0.10;
  --gf-pattern-blend: multiply;
}
```

推荐纹样颜色：`green`, `cyan`, `neutral`。

### `dunhuang-earth` 敦煌土色

用于历史、旅行、壁画、遗产、展览、丝路、工艺和暖色纪录片感页面。

```css
:root {
  --gf-ink: #2d2016;
  --gf-paper: #f0dfbf;
  --gf-paper-tint: #dfc28e;
  --gf-muted: #75593b;
  --gf-line: #b88952;
  --gf-accent: #b95a2d;
  --gf-accent-2: #2f6a73;
  --gf-pattern-opacity: 0.11;
  --gf-pattern-blend: multiply;
}
```

推荐纹样颜色：`orange`, `yellow_gold`, `neutral`, `cyan`。

### `night-lacquer` 玄漆金夜

用于高端品牌、黑金 deck cover、夜间活动、戏剧化章节页和高对比标题场景。

```css
:root {
  --gf-ink: #f4ead8;
  --gf-paper: #17110f;
  --gf-paper-tint: #241916;
  --gf-muted: #bca98a;
  --gf-line: #6c5640;
  --gf-accent: #c99a3e;
  --gf-accent-2: #8f1f1b;
  --gf-pattern-opacity: 0.16;
  --gf-pattern-blend: screen;
}
```

推荐纹样颜色：`dark`, `purple`, `red`, `yellow_gold`。

### `hua-chao-rouge` 花朝胭脂

用于花朝、香氛、婚宴、诗会、春日市集、女性文化活动和礼品品牌。保持胭脂、纸色、墨色和少量金色，不要把整页做成单调粉色。

```css
:root {
  --gf-ink: #2a1720;
  --gf-paper: #fbf0ed;
  --gf-paper-tint: #efd2cc;
  --gf-muted: #7a5860;
  --gf-line: #d6aba8;
  --gf-accent: #b0445f;
  --gf-accent-2: #b78a38;
  --gf-pattern-opacity: 0.09;
  --gf-pattern-blend: multiply;
}
```

推荐纹样颜色：`rose`, `red`, `neutral`, `yellow_gold`。

## 选择指南

| 用户需求 | 使用 theme |
| --- | --- |
| 中文编辑页、诗词、茶、安静文化 | `ink-wash` |
| 青花瓷、科技、研究、档案 | `porcelain-blue` |
| 节庆、新年、仪式、发布会标题页 | `tang-vermilion-gold` |
| 园林、养生、茶品牌、自然国风 | `jade-green` |
| 敦煌、壁画、历史、遗产、旅行 | `dunhuang-earth` |
| 高端、黑金、夜间活动、戏剧化 deck cover | `night-lacquer` |
| 花朝、香氛、婚礼、诗会、春日市集、女性文化、礼品品牌 | `hua-chao-rouge` |

## 纹样匹配

选 theme 后：

1. 按 `usage_modes` 筛 `data/patterns.json`。
2. 优先选择 `color_family` 出现在 theme 推荐颜色里的纹样。
3. divider、side border 和可见文字区域用 `sparse` 或 `medium`。
4. `dense` 只用于 cover accent、hero 或极低透明度背景层。
5. 纹样视觉很强时，先降 opacity，再考虑改 theme color。

## Pattern Ownership

| Theme | Primary patterns | 备注 |
| --- | --- | --- |
| `ink-wash` | `006`, `013`, `016`, `019`, `024` | 安静 neutral/dark/green，适合诗词、课程和博物馆阅读。 |
| `porcelain-blue` | `007`, `008`, `014`, `020`, `024` | blue/cyan/neutral，适合瓷器、档案、研究和精致展陈。 |
| `tang-vermilion-gold` | `004`, `009`, `015`, `021`, `023` | red/gold，适合节庆、仪式、发布和新年。 |
| `jade-green` | `001`, `011`, `014`, `019`, `020` | green/cyan，适合茶、园林、养生和安静餐饮。 |
| `dunhuang-earth` | `005`, `010`, `015`, `022`, `023` | orange/gold，适合历史、旅行、遗产、壁画和工艺。 |
| `night-lacquer` | `003`, `012`, `016`, `017`, `023` | dark/purple/red/gold，适合高端戏剧化页面。 |
| `hua-chao-rouge` | `002`, `018`, `009`, `024`, `015` | rose 主纹样加 red/neutral/gold 辅助，适合花事和礼品场景。 |

`002` 和 `018` 主要属于 `hua-chao-rouge`。`009`、`024`、`015` 保持原主题归属，但可作为 `hua-chao-rouge` 的兼容辅助选择。
