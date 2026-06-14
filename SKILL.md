---
name: itbxm-chinese-guofeng-skill
description: 生成国风网页、横向翻页 HTML PPT、文旅落地页、餐饮首页、新中式品牌页、文化课程页、博物馆展陈页、入境游英文/双语导览页，以及其他静态国风版式。作者 IT部小明 / itbxm。
---

# IT部小明国风 Skill

使用这个 Skill 生成静态国风网页和横向翻页 HTML PPT。它内置唐风纹样、七套国风主题、简繁中文字体策略、版式、组件、模板和验证脚本。

## 默认交互语言

- 面向中文用户时，默认用中文沟通、追问、解释和交付。
- 生成中文内容时，默认使用简体中文 `zh-Hans`；用户明确要求繁体时使用 `zh-Hant`。
- 用户要求英文、入境游、外国游客导览或 bilingual 时，可生成英文或中英双语结构。
- 保留技术 id、文件名、路径、CSS class、theme id、layout id 和 JSON key 的英文原文，不要翻译这些机器接口。

## 核心规则

- 生成完整网页或 HTML PPT 前，先读 `references/workflow.md`。
- 用户要求 PPT、HTML PPT、HTML deck 或演示稿时，必须读 `references/deck-workflow.md`，先写 deck blueprint，再逐页生成；每页都要标注 layout ID、核心信息、事实风险、素材 slot、素材关键词、provider/状态、纹样任务、`dark/decorated` 和 `data-reveal`。
- 用户只给宽泛需求时，**必须先暂停生成，向用户提出中文 Preflight 问题**。Preflight 不是 agent 内部的自我判断，而是面向用户的交互。参考 `references/workflow.md` 的「通用开工前问题模板」，一次性问清：① 目标受众与使用场景 ② 输出形式与规模 ③ 核心内容板块 ④ 素材与事实状态 ⑤ 参考风格、品牌规范与默认授权。问题要按任务类型替换例子，让用户可以批量回答。**在用户回答之前，不要开始生成任何 HTML 代码。**（平台提示：部分 AI 平台倾向跳过提问直接生成，如 GPT 系列；遇到此类平台时，请在回复开头用加粗文字标注「⏸ 生成前需要您确认以下问题」，强化停顿信号。）
- 仅当用户明确说"不用问了直接做"、"你来决定"、"给个初稿先"或类似指令时，才允许跳过提问，使用默认值并在交付说明中显眼标注所有假设。用户没有回应 ≠ 用户说了"不用问"。
- 完整网站、页面项目或 HTML PPT 默认交付为可搬走的静态站点项目，而不是孤立 HTML 文件；项目内必须包含被引用的本地纹样、图片和 runtime 资产。
- 静态站点内只能用相对路径引用项目资产，例如 `assets/patterns/...`、`assets/images/...`、`assets/runtime/...`；不要引用 `<skill-root>`、用户主目录、系统绝对路径或 agent 缓存目录。
- 完整输出前必须处理 Preflight 五组问题，并至少明确输出规模、国风主题、素材策略。详见 `references/workflow.md` 的「通用开工前问题模板」和「三项必问（STOP-GATE）」。
- 先判断用途：文化教育、商业转化、品牌展示或活动传播，再选择视觉方向。
- 把用户当成决策者，而不是设计软件操作者：先帮助用户确定受众、目标、信息优先级和资料缺口。
- 用户需求含糊时，使用 `references/workflow.md` 里的“方向顾问”：`撞`、`借`、`请`。不要只做安全国风：米色纸张、红印章、边框和空泛诗意文案。
- 事实先于风格：不要编造日期、价格、地址、路线、来源、展品信息、菜单、产品功效、排名或历史细节。
- 素材前置是硬流程：真实品牌、产品、人物、地点、活动、空间、榜单、工具、商业介绍、课程证据和内容科普默认先读 `references/asset-workflow.md`，列素材 slot、选择 provider、采集候选、评分和记录来源，再进入版式设计。
- **核心素材先于版式，资产 > 风格。** 具名品牌、产品、App、工具、榜单或对比页必须先列 `brand-logo` slot；实体产品必须列产品图 slot；数字产品必须列 UI 截图 slot。核心素材没达到 8/10 时，宁可用诚实占位或向用户要素材，不要用 CSS 剪影、泛图、AI 仿真图或纹样装饰假装已经解决。
- 图片素材是素材前置的一部分：地点、展品、菜品、产品、服饰、空间、活动、人物、路线和品牌案例默认先判断真实图片是否内容必需；内容图必需时先取图、评分和记录来源，取不到才列中文素材清单并使用诚实占位。
- **严禁使用 AI 图片生成工具（如 generate_image、DALL-E、Midjourney 等）来替代地点、景点、建筑、菜品、展品、产品或人物的真实照片。** AI 生成的仿真照片与真实场景不符，会严重误导用户。AI 生成图片仅允许用于：纯装饰纹理、抽象背景、或用户明确要求 AI 风格插画的场景。
- 涉及公共地标、景点、博物馆、寺庙、餐厅、品牌、产品、活动或具名工具时，**默认主动采集真实素材**并下载到项目 `assets/images/`，而不是等待用户"明确允许"；用户拒绝后再改用诚实占位。素材搜索使用双通道 + 多渠道矩阵：国内源通道优先本地素材、官网/政府/文旅/博物馆/品牌官网和国内平台线索；国际开放源通道包含海外官网、开放图库、Met Museum Open Access、Art Institute of Chicago API、Unsplash/Pexels 内容相关线索和有限预算的 Wikimedia。Logo 走 SVGL / Simple Icons / Google favicon / 官方 brand 或 press 页；UI 走 App Store / Google Play / 官网截图 / 官方视频截帧线索。国内题材优先使用 `python3 scripts/fetch-guofeng-assets.py --slot "<素材位>" --type <类型> --query "<中文关键词>" "<英文关键词>" --out <site-root>/assets/images --source-profile domestic --count 10 --pick 2`；通用不确定题材使用 `--source-profile balanced --wikimedia-count 2`；国际/开放版权题材才使用 `--source-profile international --wikimedia-count 2`。国内强反爬平台只生成 `asset-leads.md`，用浏览器辅助保存可见素材或截图，不写绕风控脚本。
- 如果 `python3 --version` 和 `node --version` 都不可用，不要把用户卡在安装运行时上。继续生成静态站点或 HTML PPT：用浏览器/WebSearch/用户提供素材/诚实占位替代脚本采集，手写 `assets/sources/asset-manifest.md` 和 `image-sources.md`，交付前按 `references/checklist.md` 手动自检，并在交付说明中标注 `未运行自动素材脚本或 HTML 验证脚本，已按 checklist 手动检查`。
- 场景明确时读 `references/scenarios.md`，覆盖课程、博物馆、非遗/工艺、入境游、地方餐饮、文旅活动和本地品牌。
- 选择纹样前读 `data/patterns.json`，只使用 metadata 里真实存在的路径。
- 纹样按版式任务优先选择，再看主题颜色、密度、母题和标签。
- 每个生成结果只选一套主题：一个网页页面或一套完整 deck 内不要混用多个 theme preset。
- 只使用可商用的开源字体，并保留字体原始 family name。
- 简体内容用 `zh-Hans` / SC 字体，繁体内容用 `zh-Hant` / TC 字体；除非内容确实混排，不要同时加载 SC 和 TC。
- Google Fonts 中存在的字体（例如 Noto 系列）可通过 Google Fonts CSS API 加载；必须使用 `https://fonts.googleapis.com/css2...`，不要手写 `fonts.gstatic.com/s/...` 字体文件 URL。
- `ZhaohuaMinA`、`KingHwaOldSong-MN` 使用 ITBXM R2 托管的 `result.css` 切片字体：`https://cdn.itbxm.com/fonts/ZhaohuaMinA/result.css` 与 `https://cdn.itbxm.com/fonts/KingHwaOldSong-MN/result.css`。
- 不要在输出项目里打包 TTF、手写 `@font-face` 字体文件 URL，或引用旧的 `fonts.itbxm.com` 字体地址。
- 不要创造后台、数据库、登录、上传、支付、实时地图、预约系统或图片生成服务。
- 演示型输出优先交付 HTML PPT；除非用户另行要求其他工具链，不要承诺 PPTX 编辑能力。
- HTML PPT 的素材获取逻辑与网页完全一致：地点、展品、菜品、路线、产品、人物、空间、活动、品牌案例、榜单对象和工具 logo 必须逐页判断真实素材是否必需；内容素材必需时先列 slot、选 provider、取候选、8/10 评分和记录来源，并把最终素材决策写入 `assets/sources/guofeng-asset-spec.md`，再进入 slide 设计。
- 完整生成后必须附简短中文交付说明：输出规模、国风方向、已使用素材与占位素材、待确认事实、下一步建议补充的资料。

## 全场景 Preflight

当用户只给一句宽泛需求、材料类型不完整、行业或场景没有明确列出时，先做 Preflight。目标是**像中文设计顾问一样尽早向用户提问暴露关键缺口**，而不是闷头生成。Preflight 不只服务旅游或文旅；网站、HTML PPT、品牌页、课程页、餐饮页、博物馆展陈页、活动页、产品页、导览页和其他国风视觉产出都适用。

- 先归类到一个或多个稳定用途：文化教育、商业转化、品牌展示、活动传播。
- 先判断五项：目标受众与使用场景、输出形式与规模、核心内容板块、素材与事实状态、参考风格与品牌规范。
- 如果材料形态不清楚，提取受众、交付物、核心信息、资料状态、必须保留内容和禁止内容。
- 宽泛需求首轮必须一次性列出 5 组中文问题，让用户批量回答，避免一问一答拖慢用户。问题要跟当前任务相关，不机械照搬全部例子，但必须覆盖会改变版式、语气、语言、素材处理或交付规模的关键项。
- **必须向用户提出这些问题并等待回答。**用户没有回应时不要把沉默当成授权。
- 仅当用户明确跳过提问时，才允许使用默认值推进，且交付说明中必须显眼标注 `假设`、`占位内容`、`待确认事实`、`下一步建议补充的资料`。
- 用户说"网站"时，不默认等于单页；先区分单页落地页、内容型长页、多页面小站。用户明确跳过时默认"单页长页初稿"，并说明它不是多页面网站。
- 用户说"PPT"时，先区分 HTML deck 页数、演讲型、课程型或发布会型。用户明确跳过时默认 5-7 页 HTML deck 初稿，并说明页数假设。
- 用户说"页面"时，默认单页，但仍需判断是导览页、产品页、菜单页、展品页、活动页还是品牌首页。
- 国风主题未明确时，给出 2-3 个适合场景的 theme/direction 建议，并推荐一个默认方案。
- 素材策略未明确时，必须询问。涉及公共场所、具名品牌、产品、人物、活动、空间、榜单或工具时，默认方案是联网采集真实素材并下载到本地；用户拒绝后才改用诚实占位。
- 品牌、产品或商业展示页默认先问 logo、产品图、品牌色、字体规范、参考页面和禁用元素。
- 按信息任务映射场景：概念、路线、器物、菜单/产品、品牌故事、活动报名、证据或收束观点。
- 缺少事实时，留空、标 `待确认` / `to confirm`，或改写成不作事实承诺的文案。
- 如果用户要求超出静态 Skill 边界的能力，例如后台、上传、支付、实时地图、预约系统或在线图片生成，说明边界并提供静态 HTML/PPT 替代方案。

## 工作流

1. 读 `references/workflow.md`，**用中文向用户一次性提问确认**受众与使用场景、输出规模、输出类型、用途、核心内容、素材/事实状态、国风方向、素材策略、参考风格和品牌规范（详见通用开工前问题模板与 STOP-GATE）。**等待用户回答后再进入步骤 2。**
2. 场景涉及文化教育、博物馆、非遗/工艺、课程、入境游、餐饮、文旅、本地品牌或未列明场景时，读 `references/scenarios.md`。
3. 读 `data/themes.json` 和 `references/themes.md`，选择一套主题。
4. 读 `data/fonts.json` 和 `references/typography.md`，选择 `zh-Hans`、`zh-Hant`、English 或 bilingual 字体策略。
5. 读 `references/layouts.md`，选择匹配内容类型的 layout id。
6. 读 `references/components.md`，使用已注册的 `.guofeng-*` 组件类。
7. 读 `data/patterns.json`，按 `usage_modes`、`color_family`、`density`、`motif_type`、`tags`、`name_zh` 和 `usage_prompt` 选择资产。
8. 用户要求 PPT、HTML PPT、HTML deck 或演示稿时，读 `references/deck-workflow.md`，先输出 deck blueprint；5-7 页初稿可一次生成，8 页以上必须先规划 rhythm。
9. 用户要求完整起稿或完整 HTML 时，读 `references/templates.md`，复制 `assets/templates/` 中最接近的模板，并把用到的纹样、图片和 runtime 复制到输出项目的 `assets/` 下。
10. 输出涉及真实品牌、产品、人物、地点、活动、空间、榜单、工具、商业介绍、课程证据或内容科普时，读 `references/asset-workflow.md`，先列素材 slot、执行 provider 分级采集、写入 manifest/candidates/leads/source 记录；如果 Python 和 Node 都不可用，按无运行时 fallback 手写来源记录并使用浏览器辅助或诚实占位。
11. 读 `references/motion.md`；普通网页只用 CSS micro motion，HTML PPT 使用本地 deck runtime。
12. 输出包含照片、截图、展品、菜品、路线图、用户提供 AI 图或图片占位时，读 `references/image-framing.md`，先判断图片是否决定成败；内容图必需时先执行素材前置、8/10 评分和来源记录，再进入 HTML 设计。
13. 用户要求添加、打包、托管或使用自定义字体时，读 `references/font-sourcing.md` 和 `data/fonts.json`。
14. 交付前读 `references/checklist.md`；保存 HTML 时尽量运行 `python3 scripts/validate-guofeng-html.py`；如果 Python 和 Node 都不可用，必须按 checklist 手动检查并在交付说明中写明未运行自动验证。

## 选择提示

- 正文阅读区使用 sparse 或 medium 纹样；dense 纹样只放低透明背景、hero、封面或章节页。
- 背景透明度通常控制在 `0.04` 到 `0.14`。
- 古典标题优先 `Noto Serif SC/TC`，正文和实用信息优先 `Noto Sans SC/TC`。
- 长正文不要使用书法、篆刻、装饰宋明体或艺术字体。
- 文化教育输出优先知识层级、注释、图注和阅读节奏。
- 商业输出优先可行动信息：预约、导航、菜单、购买、报名、咨询、地址、时间、价格。
- 入境游页面应包含英文或双语结构，不要让外国游客依赖纯中文导航。

## 参考文件

- `references/workflow.md`: 生成流程、默认值和方向顾问。
- `references/scenarios.md`: 文化教育与商业场景映射。
- `references/layouts.md`: 可复用网页与 deck 结构。
- `references/components.md`: 已注册组件类。
- `references/motion.md`: 网页微动效与 HTML PPT 动效规则。
- `references/deck-workflow.md`: HTML PPT 专用 deck blueprint、逐页素材前置和 rhythm 规则。
- `references/asset-workflow.md`: 通用真实素材 slot、provider 分级、候选评分和来源记录。
- `references/image-framing.md`: 图片、展品、菜品、路线、截图和占位处理。
- `references/checklist.md`: 交付前检查。
- `references/agent-usage-patterns.md`: 资产选择规则和简单 HTML 片段。
- `references/themes.md`: 国风主题配色和纹样匹配。
- `references/typography.md`: 简繁中文、英文和双语字体策略。
- `references/templates.md`: 完整网页或 HTML PPT 起稿模板。
- `references/font-sourcing.md`: 第三方或用户自带字体处理。
- `references/source-and-license.md`: 来源、授权和再分发说明。
