# 版式

这些 layout 是国风网页和 HTML PPT 的生产结构。所有 layout 都应基于模板 CSS 和 `references/components.md` 中的类组合。

## 预检

- 先为一个网页或一套完整 deck 选择一套主题，再选纹样。
- 写 CSS 前先选择 `zh-Hans`、`zh-Hant`、English 或 bilingual 字体策略。
- 只使用 `data/patterns.json` 中存在的路径。
- 阅读区保持低透明纹样。
- 除非生成 HTML 内部自己定义，否则不要发明 `references/components.md` 之外的组件类。

## Layout Index

| ID | 名称 | 适合 | 推荐主题 | 纹样任务 |
| --- | --- | --- | --- | --- |
| L01 | Hero Cover | 网站首屏、deck cover | any theme | cover accent、side border、subtle background |
| L02 | Chapter Divider | PPT 章节页、section break | `ink-wash`, `night-lacquer` | cover accent、divider |
| L03 | Poem Quote | 诗句、金句、题记 | `ink-wash`, `jade-green` | divider、subtle background |
| L04 | Text Image | 文章段落、产品/地点介绍 | `porcelain-blue`, `jade-green` | side border、subtle background |
| L05 | Artifact Showcase | 展品、产品、工艺 | `porcelain-blue`, `dunhuang-earth` | cover accent、divider |
| L06 | Card Grid | 功能列表、文化点、服务 | any theme | subtle background、divider |
| L07 | Timeline | 历史、行程、流程 | `dunhuang-earth`, `porcelain-blue` | side border、divider |
| L08 | Data Poster | 大数字、证据、公开数据 | `porcelain-blue`, `night-lacquer` | subtle background |
| L09 | Scroll Narrative | 长叙事、城市文化 | `ink-wash`, `dunhuang-earth` | side border、divider |
| L10 | Closing Seal | 收束页、署名、takeaway | `ink-wash`, `night-lacquer` | cover accent |
| L11 | Course Explainer | 知识点、讲座页 | `ink-wash`, `porcelain-blue` | subtle background、divider |
| L12 | Museum Label | 展签、器物说明 | `porcelain-blue`, `dunhuang-earth` | divider、side border |
| L13 | Travel Itinerary | 入境游路线 | `dunhuang-earth`, `jade-green` | side border、subtle background |
| L14 | Local Food Menu | 餐厅、菜品、地方美食 | `tang-vermilion-gold`, `jade-green` | divider、cover accent |

## HTML Skeletons

### L01 Hero Cover

```html
<section class="slide">
  <div class="pattern-bg"></div>
  <div class="cover-accent"></div>
  <div class="side-border"></div>
  <div class="content">
    <div class="guofeng-kicker">[主题 / Theme]</div>
    <h1 class="title">[主标题]</h1>
    <p class="subtitle">[一句说明]</p>
    <a class="guofeng-cta" href="[链接]">[行动]</a>
  </div>
</section>
```

### L02 Chapter Divider

```html
<section class="slide dark">
  <div class="pattern-bg"></div>
  <div class="content">
    <span class="guofeng-seal">[章]</span>
    <h2 class="title">[章节名]</h2>
    <div class="guofeng-scroll-divider"></div>
    <p class="subtitle">[章节导语]</p>
  </div>
</section>
```

### L03 Poem Quote

```html
<section class="section">
  <div class="guofeng-quote">
    <p class="guofeng-quote-text">
      <span class="guofeng-poem-line">
        <span class="guofeng-poem-half">[上句逗号前半句，]</span>
        <span class="guofeng-poem-half">[上句逗号后半句。]</span>
      </span>
      <span class="guofeng-poem-line">
        <span class="guofeng-poem-half">[下句逗号前半句，]</span>
        <span class="guofeng-poem-half">[下句逗号后半句。]</span>
      </span>
    </p>
    <p class="guofeng-annotation">[译文 / 背景 / 解读]</p>
  </div>
</section>
```

- 古诗、词句和对联优先用 `guofeng-poem-line` + `guofeng-poem-half` 表达句法，不要只用 `<br>` 控制换行。
- 现代短金句可直接放在 `guofeng-quote-text` 中；超过 12-14 个中文字符时拆成语义完整的行，避免标点、单字或半句孤立。

### L04 Text Image

```html
<section class="section">
  <div class="grid-2">
    <div>
      <div class="guofeng-kicker">[类别]</div>
      <h2 class="section-title">[标题]</h2>
      <p class="lead">[正文]</p>
    </div>
    <figure class="guofeng-figure">
      <img src="[图片路径]" alt="[说明]">
      <figcaption class="guofeng-caption">[图注]</figcaption>
    </figure>
  </div>
</section>
```

### L05 Artifact Showcase

```html
<section class="section">
  <div class="guofeng-museum-label">
    <span class="guofeng-era-tag">[年代]</span>
    <h2>[器物 / 产品名]</h2>
    <p>[材料、产地、用途、文化意义]</p>
  </div>
</section>
```

### L06 Card Grid

```html
<section class="section">
  <div class="guofeng-card-grid">
    <article class="guofeng-paper-card">[卡片 1]</article>
    <article class="guofeng-paper-card">[卡片 2]</article>
    <article class="guofeng-paper-card">[卡片 3]</article>
  </div>
</section>
```

### L07 Timeline

```html
<section class="section">
  <div class="guofeng-timeline">
    <article><span class="guofeng-era-tag">[时间]</span><p>[事件]</p></article>
    <article><span class="guofeng-era-tag">[时间]</span><p>[事件]</p></article>
  </div>
</section>
```

### L08 Data Poster

```html
<section class="slide">
  <div class="content">
    <div class="guofeng-stat"><strong>[数字]</strong><span>[含义]</span></div>
    <p class="lead">[数据解释]</p>
  </div>
</section>
```

### L09 Scroll Narrative

```html
<section class="section guofeng-section--side-ornament">
  <div class="guofeng-side-ornament" aria-hidden="true"></div>
  <div class="guofeng-scroll-text section-content">
    <h2>[叙事标题]</h2>
    <p>[分段叙事正文]</p>
  </div>
</section>
```

侧边纹样必须占用自己的布局列或安全内距；不要绝对定位覆盖正文。

### L10 Closing Seal

```html
<section class="slide dark">
  <div class="cover-accent"></div>
  <div class="content">
    <span class="guofeng-seal">[印]</span>
    <h2 class="title">[收束句]</h2>
    <p class="subtitle">[落款 / 下一步]</p>
  </div>
</section>
```

Closing 默认只使用一层主纹样或一层封面装饰。若同时使用 tile 与 cover accent，第二层必须极低透明度并柔和渐隐，不得形成硬边遮罩或竖向断层。

### L11 Course Explainer

```html
<section class="section">
  <article class="guofeng-knowledge-card">
    <span class="guofeng-kicker">[知识点]</span>
    <h2>[概念]</h2>
    <p>[解释]</p>
    <p class="guofeng-annotation">[例子 / 注释]</p>
  </article>
</section>
```

### L12 Museum Label

```html
<section class="section">
  <article class="guofeng-museum-label">
    <span class="guofeng-era-tag">[朝代 / 年份]</span>
    <h2>[展品名]</h2>
    <p>[材质 / 尺寸 / 来源]</p>
    <p class="guofeng-annotation">[看点说明]</p>
  </article>
</section>
```

### L13 Travel Itinerary

```html
<section class="section">
  <div class="guofeng-itinerary-card">
    <span class="guofeng-info-pill">[Day 1 / 09:00]</span>
    <h3>[地点]</h3>
    <p>[路线、交通、体验说明]</p>
  </div>
</section>
```

### L14 Local Food Menu

```html
<section class="section">
  <article class="guofeng-dish-card">
    <span class="guofeng-info-pill">[招牌 / Spicy / Seasonal]</span>
    <h3>[菜名]</h3>
    <p>[食材、味型、故事]</p>
    <strong>[价格]</strong>
  </article>
</section>
```

## 选择规则

- 教育型输出优先 `L03`、`L07`、`L11`、`L12`。
- 商业型输出优先 `L05`、`L06`、`L13`、`L14`。
- `L01`、`L02`、`L10` 用于网页和 deck 的节奏。
- `L08` 需要真实数字和解释，不要用于模糊 claim。

## Deck Rhythm

HTML PPT 应像有引导的序列，不是一组断开的页面。

| Deck type | 推荐页序 |
| --- | --- |
| 文化课程 | L01 cover, L11 concept, L04 example, L06 key points, L03 quote, L10 closing |
| 博物馆/遗产 | L01 cover, L02 chapter, L12 label, L05 artifact, L07 timeline, L10 closing |
| 入境游 | L01 cover, L13 itinerary, L04 place intro, L06 services/tips, L08 proof if data exists, L10 CTA closing |
| 本地餐饮 | L01 cover, L14 menu, L05 signature dish, L06 dining features, L04 story/location, L10 reservation closing |

Deck 规则：

- 每页需要可读标题，以及 footer、页码、署名或来源区。
- 商业 slides 上的地址、时间、价格、路线、预约、菜单或咨询信息必须可见。
- 教育 slides 要足够安静，方便阅读和记笔记。
- 强 `cover-accent` 只用于 cover、chapter divider 或 closing。
- 普通内容页保持干净：纸色背景、浅 tile、divider 或 side ornament；不要反复放大角花。
- 内容页通常最多一层 pattern。
- 含正文的 side ornament 要参与布局，closing/hero 的双纹样层必须避免硬边断层。
- 重复 `tile.webp` 背景保留原始比例；不要把非正方形 tile 强行设成正方形。
- HTML PPT 可适度使用装饰字体：cover 和 chapter titles 可用 `--font-display-heavy`；短 section title、card title、展签和诗句可用 `--font-display-light` 或 `--font-poem`。
- 装饰字体标题只要可能换行，`line-height` 不得低于 `1.12`，推荐 `1.16-1.24`。
- 正文、解释、实用信息、英文、价格、地址和图注使用 `--font-body` 或可读 Noto/system 字体栈。
- `data-reveal` 少量使用：title -> body/card group -> footer。
- 不要让密集正文、价格、地址、图注或来源因动画延迟阅读。
