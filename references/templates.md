# 模板使用

当用户要求完整国风网页、PPT 风格 HTML deck 或可复用起稿时，使用这些种子模板。

HTML PPT 是本 Skill 的主要演示格式：它是本地浏览器可播放的横向 HTML deck，不是 PPTX 编辑器工作流。不要仅凭本 Skill 承诺母版编辑、PowerPoint 对象编辑或 PPTX 导出。

## 可用模板

| 模板 | 路径 | 用途 |
| --- | --- | --- |
| PPT deck | `assets/templates/ppt-deck.html` | 横向 HTML slides、封面、章节页、键盘演示 |
| Web page | `assets/templates/web-page.html` | 国风落地页、文化产品页、编辑型首页 |

## 使用流程

1. 读 `references/workflow.md`，**用中文向用户一次性提问确认**目标受众与使用场景、输出形式与规模、核心内容板块、素材与事实状态、参考风格/品牌规范、方向顾问路线、国风主题和素材策略（详见通用开工前问题模板与 STOP-GATE）。**等待用户回答后再进入步骤 2。** 网页和 HTML PPT 都必须经过此步骤，不要跳过。
2. 用户要求 PPT、HTML PPT、HTML deck 或演示稿时，读 `references/deck-workflow.md`，先写 deck blueprint；每页标注素材 slot、素材关键词和 provider/状态，再复制 `ppt-deck.html`。
3. 读 `references/scenarios.md`，确认文化教育或商业场景规则。
4. 读 `data/themes.json` 和 `references/themes.md`。
5. 为一个网页或一套完整 deck 选择一套主题，并替换模板中的 `--gf-*` 变量。
6. 读 `references/typography.md` 和 `data/fonts.json`；推断 `zh-Hans` 或 `zh-Hant`，并使用对应 Noto Google Fonts CSS API URL 与已注册装饰字体 `result.css`。
7. 读 `references/layouts.md` 和 `references/components.md`；使用注册 layout id 和 `.guofeng-*` 组件类。
8. 读 `references/motion.md`：普通网页只用 CSS micro motion，HTML PPT 保留本地 deck runtime。
9. 涉及真实品牌、产品、人物、地点、活动、空间、榜单、工具、商业介绍、课程证据或内容科普时，读 `references/asset-workflow.md`，先列素材 slot、provider、候选和状态；使用图片或截图时再读 `references/image-framing.md`。
10. 读 `data/patterns.json`。
11. 替换模板纹样路径：
    - `tile.webp`：低透明重复背景，保留原始比例。
    - `strip-horizontal.webp`：分割线、标题带、caption band。
    - `strip-vertical.webp`：侧边纹样。
    - `cover-accent.webp`：hero 或封面重点装饰。
12. 把用到的纹样复制到输出项目的 `assets/patterns/`，把图片复制到 `assets/images/`，素材来源记录写入 `assets/sources/`，HTML PPT runtime 复制到 `assets/runtime/`。
13. 用最终内容替换模板标签、标题和正文。
14. 正文区域保持低透明纹样；只有 hero、deck cover 或深色章节页可提高存在感。
15. 交付前读 `references/checklist.md`；保存 HTML 后运行 `python3 scripts/validate-guofeng-html.py`。

## 模板规则

- 先判断输出规模，再复制模板；用户说"网站"时不要自动等同于一个 `web-page.html` 单页。
- **网页和 HTML PPT 都必须经过通用 Preflight 与 STOP-GATE 提问流程**，不要因为输出类型不同就跳过用户确认。
- 多页面小站先规划页面清单，再分别复用模板和组件。
- 默认生成单页长页或 5-7 页 HTML deck 初稿时，交付说明必须写明规模假设。
- HTML PPT 默认初稿仍必须先有 deck blueprint；8 页以上必须先规划 rhythm，避免连续多页同类卡片网格。
- 完整输出默认是静态站点项目：HTML 文件和被引用的 `assets/` 必须一起交付。
- 不要引用 `<skill-root>`、用户主目录、系统绝对路径或 agent 缓存目录中的纹样、图片、runtime。
- HTML/CSS 只使用项目内相对路径，例如 `assets/patterns/...`、`assets/images/...`、`assets/runtime/...`。
- 不要留下 `[必填]` 占位。
- 一个网页或一套完整 deck 不要混用多套主题。
- 有 theme variables 时不要随机硬编码颜色。
- 段落不要使用装饰字体或艺术字体。
- Noto 字体使用 Google Fonts CSS API；装饰字体使用已注册的 ITBXM R2 `result.css`。
- 不要打包 TTF 或手写 `@font-face` 字体文件 URL。
- 普通网页不要加 JavaScript；只使用 CSS micro motion。
- 生成繁体输出时，不要保留 `lang="zh-CN"`，要切换到对应 `script_profiles` 和 TC 字体。
- 不要把 dense 纹样直接放在正文背后。
- 不要编造资产路径；每个路径必须存在于 `data/patterns.json`。
- 文化教育页面保持知识层级、注释和图注可读。
- 商业页面保持实用信息和 CTA 比装饰文案更清楚。

## HTML PPT 注意事项

`ppt-deck.html` 使用横向 scroll-snap slides，可直接从本地文件系统打开。种子模板包含封面、内容页和结尾页。

> HTML PPT 与网页遵循同一个通用 Preflight 与 STOP-GATE 流程：生成前必须用中文向用户批量确认受众、页数和类型、核心内容、素材/事实状态、参考风格、国风主题和素材策略。不要因为是 PPT 就跳过提问直接生成。

> HTML PPT 生成前必须读取 `references/deck-workflow.md` 并写 deck blueprint。Blueprint 至少包含 deck 类型、页码、layout ID、单页核心信息、事实风险、素材 slot、素材关键词、provider/状态、纹样任务、`dark/decorated` 和 `data-reveal`。

扩展时：

- 保留 `data-guofeng-deck`、`.deck-progress`、`.deck-controls`、`.deck-overview` 和 `../runtime/guofeng-deck.js`，除非用户明确要求静态 deck。
- `data-guofeng-deck` 只能放在 slide 容器上；不要把 `data-deck-progress-text`、`data-deck-progress-fill`、`data-deck-prev`、`data-deck-next` 或 `data-deck-overview` 放到同一个元素上。
- deck runtime 控制标记必须保持模板结构：进度文字在独立 progress text div，进度条在 `.deck-progress-fill`，上一页/索引/下一页在 `.deck-button` 按钮，overview panel 使用 `.deck-overview[data-deck-overview-panel][hidden]`。
- `data-reveal` 只用于 HTML PPT 的轻微入场动效，不要加到普通网页。
- 地点、展品、菜品、路线、产品、人物、空间、活动、品牌案例、榜单对象、工具 logo 和 UI 截图等内容素材必需时，先执行 `references/asset-workflow.md` 的 slot、provider、candidate、score 和 final 流程；PPT 图片也写入 `assets/images/`，来源写入 `assets/sources/`。
- 未找到 8/10 素材时，对应 slide 使用诚实占位，并在 blueprint 和交付说明中标注 `占位待补`。
- 每页保留可读标题和页脚/页码/署名区域。
- 桌面演示保持每页 `100vw` by `100vh`。
- 底部内容不要压到 footer 区。
- `dark` 只用于高对比封面、章节页或结尾页。
- 强 `cover-accent` 只用于封面、章节和结尾页。
- 普通内容页更干净：纸色背景、一层浅 tile、分割线或侧边纹样。
- 相邻内容页优先交替使用 cover/chapter、text-image、artifact、timeline、quote、card-grid 和 closing；每页只保留一个主记忆点，超过 4 个辅助点拆页。
- 重复 `tile.webp` 背景要保留原始比例，不要强行变成正方形。
- HTML PPT 可以比网页更积极使用装饰字体：封面和章节标题可用 Zhaohua，短标题、卡片标题、诗句和展签可用 KingHwa。
- 解释、路线、菜单描述、价格、地址、时间、图注和英文内容必须使用可读 Noto/system 字体栈。

## 网页注意事项

`web-page.html` 是首屏网站模板，包含 hero 和 section grid。

扩展时：

- 首屏必须聚焦品牌、地点、产品或页面主题。
- 纹样是氛围，不是主要阅读表面。
- 卡片保持简洁的矩形结构。
- 移动端 section 使用单列。
- CSS-only micro motion 可用于 hero 入场、hover、focus 和轻微卡片抬升。
- 普通网页不要使用 `data-reveal`、deck runtime、滚动触发 JavaScript 或循环装饰动画。
