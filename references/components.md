# 组件

组合版式时使用这些类。组件 CSS 放在生成 HTML 或模板里，不要托管到 R2。

## 通用组件

### `guofeng-kicker`

标题上方的小类别标签。用于主题、章节、section 或场景名。

```html
<div class="guofeng-kicker">ink-wash · 水墨宣纸</div>
```

### `guofeng-seal`

印章感短标签。文字控制在 1-4 个中文字符或短 code。

```html
<span class="guofeng-seal">风</span>
```

### `guofeng-quote`

诗句、引用或关键句块。配合 `guofeng-quote-text` 和 `guofeng-annotation`。

古诗、词句和对联要用结构化诗行，不要用 `<br>` 硬插换行。每个 `guofeng-poem-line` 表示视觉上的一整句或一联；七言、五言等句子可用两个 `guofeng-poem-half` 包住逗号前后半句，避免浏览器在“雨亦 / 奇。”这类位置随意折断。

```html
<blockquote class="guofeng-quote">
  <p class="guofeng-quote-text">
    <span class="guofeng-poem-line">
      <span class="guofeng-poem-half">水光潋滟晴方好，</span>
      <span class="guofeng-poem-half">山色空蒙雨亦奇。</span>
    </span>
    <span class="guofeng-poem-line">
      <span class="guofeng-poem-half">欲把西湖比西子，</span>
      <span class="guofeng-poem-half">淡妆浓抹总相宜。</span>
    </span>
  </p>
  <p class="guofeng-annotation">这里放译文、出处或解释。</p>
</blockquote>
```

短金句或现代引用不是诗词时，可以直接写一行；超过 12-14 个中文字符时优先降字号或拆成语义完整的 `guofeng-poem-line`，不要让标点、单字或半句孤立成行。

### `guofeng-scroll-divider`

使用注册横向纹样的分割线。

```html
<div class="guofeng-scroll-divider"></div>
```

### `guofeng-side-ornament`

侧边竖向纹样，用于边框或叙事 section。

```html
<section class="section guofeng-section--side-ornament">
  <div class="guofeng-side-ornament" aria-hidden="true"></div>
  <div class="section-content">[正文内容]</div>
</section>
```

- 正文 section 中，侧边纹样必须参与布局：推荐使用独立列、`gap` 或明确安全内距。
- 不要把 `.guofeng-side-ornament` 绝对定位到正文容器上方；它会在窄屏、长文或双语段落中压住文字。
- 移动端把竖纹改为横向分隔，放在正文之前或章节之间。

### `guofeng-paper-card`

用于文化点、服务特点或备注的可读卡片。

```html
<article class="guofeng-paper-card">
  <h3>一处知识点</h3>
  <p>保持正文清晰，不把纹样放在文字正下方。</p>
</article>
```

### `guofeng-caption`

图片、展品、来源或图表说明。

```html
<figcaption class="guofeng-caption">清代瓷器纹样参考，展陈说明。</figcaption>
```

### `guofeng-foot`

页脚或 deck 页码区域。

```html
<footer class="guofeng-foot"><span>ITBXM</span><span>03</span></footer>
```

### `guofeng-vertical-inscription`

短竖排题签。只用于 2-12 个中文字符。

```html
<p class="guofeng-vertical-inscription">山河入卷</p>
```

### `guofeng-stat`

一个重要数字的数据标识。

```html
<div class="guofeng-stat"><strong>72h</strong><span>三日城市行程</span></div>
```

## 文化教育组件

### `guofeng-knowledge-card`

用于一个概念、一个教学点或一个讲座 takeaway。

```html
<article class="guofeng-knowledge-card">
  <span class="guofeng-kicker">知识点</span>
  <h3>留白</h3>
  <p>留白不是空，而是让信息有呼吸。</p>
  <p class="guofeng-annotation">适合课程页、讲座页、知识解释页。</p>
</article>
```

### `guofeng-era-tag`

朝代、年代、日期或阶段标签。

```html
<span class="guofeng-era-tag">唐 · 8 世纪</span>
```

### `guofeng-museum-label`

博物馆式展品或档案标签。

```html
<article class="guofeng-museum-label">
  <span class="guofeng-era-tag">宋</span>
  <h3>青瓷碗</h3>
  <p>器型、釉色、用途与观看重点。</p>
</article>
```

### `guofeng-annotation`

短注释、译文、来源或背景说明。

```html
<p class="guofeng-annotation">注：此处用于解释术语，不承担主正文。</p>
```

## 商业组件

### `guofeng-itinerary-card`

入境游或城市路线步骤。

```html
<article class="guofeng-itinerary-card">
  <span class="guofeng-info-pill">Day 1 · 09:00</span>
  <h3>故宫北门集合</h3>
  <p>Meet your guide, enter through the north gate, and start with court architecture.</p>
</article>
```

### `guofeng-place-card`

景点、餐厅、民宿或场地卡片。

```html
<article class="guofeng-place-card">
  <h3>西湖茶舍</h3>
  <p>Tea tasting, garden view, English-friendly service.</p>
  <span class="guofeng-info-pill">Hangzhou · 2h</span>
</article>
```

### `guofeng-dish-card`

菜品或菜单项。

```html
<article class="guofeng-dish-card">
  <span class="guofeng-info-pill">Signature</span>
  <h3>东坡肉</h3>
  <p>Slow-braised pork belly, sweet soy glaze, Hangzhou style.</p>
  <strong>¥68</strong>
</article>
```

### `guofeng-info-pill`

价格、地址、时长、辣度、开放状态或可用性的实用小标签。

```html
<span class="guofeng-info-pill">Open 10:00-21:00</span>
```

### `guofeng-cta`

明确行动链接。用于预约、导航、看菜单、购买、咨询或报名。

```html
<a class="guofeng-cta" href="[链接]">预约体验</a>
```

## 限制

- 需要阅读或翻译的文字不要做进图片里。
- `guofeng-seal` 或 `guofeng-info-pill` 不要伪装成按钮。
- 竖排题签不要用于长段正文。
- 含正文的卡片内部不要直接放 dense pattern 背景。
- 侧边纹样、边框和封面装饰不得覆盖可读正文、图注、价格、路线或英文说明。
