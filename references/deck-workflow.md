# HTML PPT Deck Workflow

用户要求 PPT、HTML PPT、HTML deck、演示稿、课程 slides、发布会 slides 或路演稿时，必须读取本文件。本 Skill 的 PPT 交付物是横向翻页 HTML deck，不承诺 PPTX 母版编辑、PowerPoint 对象编辑或 PDF/PPTX 导出，除非用户另行指定其他工具链。

## 1. 先确认交付边界

- 输出格式：单文件 HTML deck + 本地 `assets/`。
- runtime：沿用 `assets/runtime/guofeng-deck.js`，不要改 `data-guofeng-deck` 和导航控制标记。
- 素材：与普通网页完全同一套素材前置规则；PPT 只是在 blueprint 中逐页标注素材 slot、provider、状态和 `guofeng-asset-spec.md` 最终决策。
- 用户只给宽泛需求时，先按 `references/workflow.md` 做中文 Preflight；用户明确说“先出初稿”时可默认 5-7 页，但必须写明假设。

## 2. 先写 Deck Blueprint

生成 HTML 前先写 deck blueprint。5-7 页默认初稿可以一次生成，但仍必须有 blueprint；8 页以上必须先规划节奏，再进入逐页 HTML。

推荐表头：

| 页码 | Deck role | Layout ID | 单页核心信息 | 事实风险 | 素材 slot | 素材关键词 | Provider/状态 | Asset spec | 纹样任务 | slide class | reveal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | cover | cover | 一句话记住主题 | 标题/日期待确认 | Hero 地点主视觉/place/必需 | `西湖 杭州 全景` / `West Lake Hangzhou` | domestic lane / 已验证 | guofeng-asset-spec.md | cover-accent | decorated/dark | 1-4 |

每页必须只保留一个主记忆点。辅助点超过 4 个时拆页，不要把课程、路线、产品卖点或展品说明压成一页。

## 3. Deck 类型

选择一种主类型，再按内容增删页面。

| 类型 | 默认节奏 |
| --- | --- |
| 课程型 | cover -> learning goal -> concept -> example/artifact -> exercise/takeaway -> closing |
| 博物馆/遗产型 | cover -> chapter -> artifact -> context/timeline -> detail/quote -> visit/takeaway -> closing |
| 文旅导览型 | cover -> route overview -> place text-image -> itinerary/timeline -> tips/card-grid -> booking/closing |
| 品牌发布型 | cover -> problem/context -> product/artifact -> proof/case -> offer/CTA -> closing |
| 活动/路演型 | cover -> agenda -> venue/guest -> timeline -> participation/CTA -> closing |

## 4. 素材前置接入 PPT

每一页都要判断是否有内容素材必需项：

- 地点、展品、菜品、路线、产品、人物、空间、活动、品牌案例、榜单对象、工具 logo、UI 截图、课程证据。
- 只要内容素材必需，先执行 `references/asset-workflow.md` 的 slot -> provider -> candidates -> score -> final -> asset spec 流程；图片进入版式时再读 `references/image-framing.md`。
- 使用图片时下载到输出项目 `assets/images/`，来源写入 `assets/sources/asset-manifest.md`、`asset-candidates.json`、`guofeng-asset-spec.md` 和 `image-sources.md`。
- 具名品牌、产品、App、工具、榜单或对比页必须逐个列 logo；实体产品必须列产品图；数字产品必须列 UI 截图。资产不达标时 slide 使用诚实占位，不用纹样或 CSS 剪影替代。
- 未找到 8/10 素材时，当前 slide 使用诚实占位，并在 blueprint 与交付说明中标注 `占位待补`。

素材状态只使用四类：

- `已验证`：来源能确认对象/地点匹配，授权或来源状态已记录。
- `待用户确认`：视觉可用，但来源、授权或对象细节需要用户确认。
- `占位待补`：未找到 8/10 素材，使用诚实占位。
- `不需要素材`：该页以文字、数据、纹样或结构表达为主。

推荐取图命令：

```bash
python3 scripts/fetch-guofeng-assets.py --slot "<素材位名称>" --type <place|person|product|brand-logo|ui|food|space|event|artifact|document|evidence|generic> --query "<中文关键词>" "<英文关键词>" --out <site-root>/assets/images --source-profile domestic --count 10 --pick 2
```

## 5. Deck Rhythm

- 8 页以上必须先规划缩略图节奏，避免连续多页使用同一种卡片网格。
- 相邻内容页应交替使用 `cover/chapter`、`text-image`、`artifact`、`timeline`、`quote`、`card-grid`、`closing` 等结构。
- `dark` 只用于封面、章节页、强转场或结尾页；不要让多数内容页都变成深色。
- `decorated` 只用于需要纹样存在感的页面；正文解释页保持更安静。
- `data-reveal` 使用 1-4 级即可；不要为了“动效丰富”拉长延迟。

## 6. 生成 HTML

1. 复制 `assets/templates/ppt-deck.html`。
2. 保留 runtime 结构：`data-guofeng-deck`、`data-deck-progress-text`、`data-deck-progress-fill`、`data-deck-prev`、`data-deck-next`、`data-deck-overview`、`data-deck-overview-panel`。
3. 按 blueprint 逐页替换 slide，不要在普通网页中复用 `data-reveal`。
4. 使用稳定图片槽：`deck-image-frame`、`deck-image-wide`、`deck-image-square`、`deck-caption-band`。
5. 使用 slide utility：`deck-quote-slide`、`deck-timeline-strip`、`deck-artifact-panel`、`deck-chapter-seal`、`deck-safe-footer`。
6. 每页保留标题和 footer/signature 区。

## 7. 检查与交付

- 保存后运行 `python3 scripts/validate-guofeng-html.py <deck.html>`。
- 手动检查 cover、最密内容页、含图片页和 closing 页。
- 交付说明必须包含：页数、deck 类型、素材状态列表、占位待补项、事实待确认项。
