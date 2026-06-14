# 动效

只在动效能帮助用户理解顺序时使用。发布网页只用 CSS micro motion；HTML PPT 可以使用本地 deck runtime。

## 原则

- 动效慢、轻、少。
- 文字必须立即可读，不要逐字动画正文。
- reveal 顺序跟随阅读顺序：kicker、title、body、figure、footer。
- 尊重 `prefers-reduced-motion`；用户关闭动效时，网页 CSS 和 deck runtime 都应直接显示内容。
- 纹样是氛围，不要让装饰纹样脉冲、旋转或干扰正文。

## 推荐网页微动效

CSS-only motion token：

```css
:root {
  --gf-motion-fast: 160ms;
  --gf-motion-base: 240ms;
  --gf-ease-out: cubic-bezier(0.22, 1, 0.36, 1);
  --gf-shadow-soft: 0 16px 38px rgba(16, 36, 58, 0.08);
  --gf-shadow-lift: 0 22px 56px rgba(16, 36, 58, 0.13);
}
```

| Motion | 用途 | 备注 |
| --- | --- | --- |
| 一次性 fade + slight rise | Hero copy、hero visual、section head | CSS-only；不用 scroll-triggered JavaScript |
| Button hover | CTA 和导航链接 | 小幅颜色变化或 1px vertical change |
| Card hover | 产品、课程、地点、菜品或博物馆卡片 | 边框/颜色变化，最多 `translateY(-2px)` |
| Visual panel hover | 装饰 hero image 或 ornament panel | 非常轻的 saturation 或 background-size 变化 |
| Image zoom | 地点、展品、菜品、产品图容器 | 只缩放图片本身，容器尺寸固定，最多 `scale(1.025)` |

模板可复用工具类：

- `.gf-hover-lift`：通用轻抬升，用于小按钮、图文组或非密集列表项。
- `.gf-card-hover`：卡片边框、阴影和背景微变化，用于产品、课程、地点、菜品、展品卡。
- `.gf-image-zoom`：图片容器 hover 时轻微放大内部 `img`，避免布局跳动。
- `.gf-soft-shadow-hover`：只加阴影不位移，用于不宜移动的面板。
- `.gf-focus-ring`：键盘焦点可见，不依赖 hover。

网页规则：

- 普通网页不要包含 JavaScript。
- 普通网页不要使用 `data-reveal` 或 deck runtime。
- 不要让文字等待动画结束才可读。
- 不要循环动画纹样、印章、标题或背景。
- 所有工具类必须在 `prefers-reduced-motion: reduce` 下关闭 transform、animation 和长 transition。

## 推荐 Deck 动效

| Motion | 用途 | 备注 |
| --- | --- | --- |
| Fade + slight rise | 标题、lead text、card groups | 默认 reveal，使用 `data-reveal` |
| Delayed reveal | 内容层级 | 使用 `data-reveal="2"` 到 `data-reveal="4"` |
| Chapter pause | 章节分隔页 | 一个强标题 + 一个短 subtitle |
| Pattern fade | Cover accents | 低透明度，不循环 |
| Scroll-like sequence | 长叙事 deck | reveal paragraph groups，不逐行 |

## 避免

- 默认使用 WebGL 背景。
- 阅读页上持续运动。
- 正文段落背后的装饰动效。
- 隐藏 CTA、价格、路线、课程注释、来源或图注的动效。
- 生成结果依赖远程动效库。
- 普通网页加入 JavaScript。

## 实现规则

HTML PPT 使用本地 runtime：`assets/runtime/guofeng-deck.js`。在 deck 容器上添加 `data-guofeng-deck`，在需要轻微入场的元素上使用 `data-reveal`。

deck runtime 控制标记必须保持分离：`data-deck-progress-text`、`data-deck-progress-fill`、`data-deck-prev`、`data-deck-next` 和 `data-deck-overview` 不得放在 `[data-guofeng-deck]` 容器上。进度条、按钮和 overview panel 必须沿用模板结构，否则 runtime 会把 slide 容器当控制器改写，导致内容被清空。

网页使用 CSS-only micro motion。除非用户明确要求 presentation-like web experience，不要加载 deck runtime。
