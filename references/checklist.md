# 交付检查清单

交付国风网页或 HTML PPT 前运行本清单。它只检查生成结果：视觉质量、阅读体验、场景有用性、静态 HTML 边界和最终验证。

## P0：必须修

- 不留下 `[必填]` 占位。
- 每个本地纹样路径都存在于 `data/patterns.json`。
- 繁体输出不保留 `lang="zh-CN"`，并使用 TC 字体族。
- 简体输出使用 SC 字体族，除非内容明确混排。
- 发布 HTML/CSS 不使用 `.ttf`、`format("truetype")`、旧 `fonts.itbxm.com` 或手写 `fonts.gstatic.com/s/...` 字体文件 URL。
- Google Fonts 中存在的 Noto 等字体可以使用 `https://fonts.googleapis.com/css2...`；装饰字体使用已注册的 `https://cdn.itbxm.com/fonts/.../result.css`。
- 输出 HTML/CSS 不引用 `<skill-root>`、用户主目录、系统绝对路径或 agent 缓存目录。
- 输出项目内被引用的 `assets/patterns/`、`assets/images/`、`assets/runtime/` 文件真实存在。
- 完整网站、页面项目或 HTML PPT 已按静态站点结构交付，不是只有 HTML 文件却依赖外部本机资源。
- 远程图片没有热链；搜索到的图片已下载到 `assets/images/` 并记录到 `assets/sources/image-sources.md`。
- 涉及真实品牌、产品、人物、地点、活动、空间、榜单、工具、商业介绍、课程证据或内容科普时，已先读 `references/asset-workflow.md`，列出素材 slot，并生成或维护 `assets/sources/asset-manifest.md` 和 `assets/sources/guofeng-asset-spec.md`。
- 素材候选已记录到 `assets/sources/asset-candidates.json`；B 级平台线索已记录到 `assets/sources/asset-leads.md`，没有写绕登录、token、签名或强风控的抓取脚本。
- 完整输出已处理通用 Preflight 与三项 STOP-GATE：目标受众与使用场景、输出形式与规模、核心内容板块、素材与事实状态、参考风格/品牌规范、国风主题和素材策略均已向用户提出并获得回答（或用户明确说了"不用问"/"你来决定"/"先出初稿"）。
- **输出中不包含 AI 生成的仿真照片**（地标、景点、建筑、菜品、展品、产品或人物场景）。如果使用了 generate_image 等工具，必须仅限于纯装饰纹理或用户明确要求的 AI 风格场景。
- **涉及公共场所时，已主动建议联网搜索真实照片**（或用户已拒绝并改用占位；或运行环境不支持联网，已在交付说明中提供图片获取指引）。
- **每张搜索下载的图片已通过来源页验证**（页面标题/图片描述/地理标签确认地点匹配），验证状态已标注在交付说明或 `image-sources.md` 中。未通过验证的图片已替换为诚实占位。
- **涉及具名品牌、产品、App、工具、榜单或对比页时，已逐个列出 logo/产品图/UI 截图 slot**；缺失项已标 `占位待补` 或写入 `asset-leads.md`。
- **核心素材遵循资产 > 风格**：Logo、产品图、UI 截图、地点/展品/菜品真实图不被 CSS 剪影、泛图、AI 仿真图、纹样或远程热链替代。
- 正文不使用书法、篆刻、手写或装饰艺术字体。
- 普通网页不包含 JavaScript、PPT deck runtime 或 `data-reveal`。
- HTML PPT 的正文、路线、图注、价格、地址、时间和英文说明不使用装饰字体变量。
- HTML PPT 的 runtime 控制标记没有放在 `[data-guofeng-deck]` 容器上；进度条、按钮和 overview panel 保持模板结构。
- HTML PPT 已先写 deck blueprint；每页包含 layout ID、核心信息、事实风险、素材 slot、素材关键词、provider/状态、纹样任务、`dark/decorated` 和 `data-reveal`。
- HTML PPT 中地点、展品、菜品、路线、产品、人物、空间、活动和品牌案例等内容图已逐页纳入素材前置；必需图片已按 `references/asset-workflow.md` 和 `references/image-framing.md` 执行候选采集、8/10 评分和来源记录。
- HTML PPT 中榜单对象、具名工具、品牌、产品、UI 截图和课程证据已逐页做素材前置；必需素材已按 `references/asset-workflow.md` 执行 slot、provider、candidate、score 和 final 记录。
- HTML PPT 图片未达到 8/10 时，slide 使用诚实占位，blueprint 与交付说明标注 `占位待补`。
- 宽泛需求已完成全场景 Preflight：**已用中文一次性向用户提出问题并获得回答**，覆盖目标受众与使用场景、输出形式与规模、核心内容板块、素材与事实状态、参考风格/品牌规范和默认授权。
- 用户说"网站"时，已明确是单页落地页、内容型长页还是多页面小站；若用户跳过提问且默认单页长页初稿，已在交付说明中显眼标注。
- 用户说"PPT"时，已明确 HTML deck 页数和类型；若用户跳过提问且默认 5-7 页初稿，已在交付说明中显眼标注。
- 文化教育内容的知识点、注释、图注和来源保持可读。
- 商业、品牌、文旅、餐饮、产品或活动页面包含必要实用信息：地点、时间、路线、菜单、价格、规格、预约、导航、购买、联系方式或咨询入口。
- 未列明场景已映射到文化教育、商业转化、品牌展示或活动传播。
- 陌生材料已识别受众、交付物、核心信息、资料状态、必须保留内容和禁止内容。
- 输出不编造价格、日期、地址、路线、引用、排名、产品 claim、菜单项、展品 metadata 或历史事实。
- 缺来源的事实已显式处理：标 `待确认` / `to confirm`、留空，或改成不作事实承诺的描述。

## P1：应该修

- 一个网页或一套完整 deck 只使用一套主题。
- SC 和 TC 字体包不同时加载，除非内容确实混排。
- PPT 页脚、页码和底部文字留在安全区。
- HTML PPT 包含键盘导航、进度、ESC 索引和 reduced-motion fallback。
- HTML PPT overview 使用 `[hidden]` 显隐规则，不依赖 runtime 不会添加的 `.open` class。
- 8 页以上 HTML PPT 已规划 deck rhythm；相邻内容页没有连续复用同一种 card-grid/quote/timeline/text-image 结构。
- HTML PPT 每页只有一个主记忆点；超过 4 个辅助点已拆页。
- HTML PPT 的素材状态在交付说明中逐项标注为 `已验证`、`待用户确认`、`占位待补` 或 `不需要素材`。
- 英文或双语说明使用可读 sans/serif 字体栈。
- 使用默认值或资料不完整时，说明关键假设。
- 输出只使用已注册主题、layout、component、font 和 pattern assets。
- 真实图片决定成败但缺失时，使用诚实占位或素材清单，不编造图片来源。
- 地点、展品、菜品、产品、服饰、空间、活动、人物、路线和品牌案例缺真实图片时，交付说明列出中文素材清单。
- 素材采集默认使用 `scripts/fetch-guofeng-assets.py`；`scripts/fetch-guofeng-images.py` 只作为 Wikimedia 快捷入口。旧 `.mjs` 脚本仅作为一个版本周期的兼容入口。
- 国内题材默认使用 `--source-profile domestic`，不得把 Wikimedia 当作每个 slot 的默认自动出口；通用题材使用 `--source-profile balanced --wikimedia-count 2`，国际/开放版权题材才使用 `--source-profile international --wikimedia-count 2`。
- Huashu 多渠道来源已按类型使用：Logo 优先 SVGL / Simple Icons / Google favicon / 官方 brand 页；UI 优先 App Store / Google Play / 官网截图 / 官方视频截帧；美术/博物馆/历史内容可用 Met Museum Open Access 和 Art Institute of Chicago API；Unsplash/Pexels 只作为内容相关摄影线索。
- 如果 Python 和 Node 都不可用，允许跳过自动脚本，但必须按无运行时 fallback 手写 `asset-manifest.md` / `image-sources.md`，并在交付说明中标注 `未运行自动素材脚本或 HTML 验证脚本，已按 checklist 手动检查`。
- 国内强平台（公众号、小红书、点评/美团、携程/马蜂窝、京东/天猫、抖音/快手、图片搜索）只作为线索或浏览器辅助来源，不作为默认自动抓取 provider。
- 完整生成后附中文交付说明：输出规模、国风方向、已用素材/占位素材、待确认事实、下一步建议补充资料。

## P2：国风质感与体验

### 0. 国风五维评审

**现象**：页面好看但难判断是否有效。

**根因**：只看美感，没有看用户实际体验。

**做法**：从五个维度检查：场景准确、信息可读、纹样克制、字体合适、行动清楚。

**自检**：用户能回答“这是对的场景吗、我看得懂吗、纹样是否受控、字体是否合适、下一步做什么吗”。

### 1. 纹样过重压住阅读

**现象**：正文、菜单、路线、展签或图注压在 dense 纹样上，阅读疲劳。

**根因**：把纹样当主视觉表面，而不是氛围和框景。

**做法**：dense 纹样放到 hero、分隔、侧边或低透明背景；正文下方加纸色层、卡片或安静底色。重复纹样透明度通常控制在 `0.04` 到 `0.14`。

**自检**：正常缩放下，正文、价格、地址、路线、图注和注释应先被读到，纹样后被注意到。

### 1b. 侧边纹样压住正文

**现象**：正文、双语段落或图注与左侧/右侧竖纹、边框重叠。

**根因**：把 `.guofeng-side-ornament` 绝对定位成装饰层，却没有给正文留安全区。

**做法**：侧纹必须参与布局，使用独立列、`gap` 或明确 padding；移动端改为横向分隔。

**自检**：正文换行、放大和窄屏时，文字都不能碰到纹样边界。

### 2. 国风变成普通模板加边框

**现象**：像普通落地页贴了一个中式边框。

**根因**：先选装饰，后想用途、层级、主题和版式。

**做法**：回到用途判断，再选 layout、theme、typography，最后选 pattern。纹样只负责封面重点、分隔、侧边或低透明背景。

**自检**：脑中移除纹样后，页面仍有清楚主题、信息顺序和行动。

### 3. 装饰字体用于实用阅读

**现象**：菜单、路线、价格、地址、英文、密集图注或课程正文使用 `ZhaohuaMinA`、`KingHwaOldSong-MN`、书法或篆刻风格。

**根因**：把装饰字体当通用中文字体。

**做法**：正文和实用信息用 Noto/system 字体栈；装饰字体只用于短 hero 标题、章节名、题签、展签、诗句、印章和署名。

**自检**：用户必须快速理解或行动的信息，都应使用 `--font-body`、`--font-title-serif` 或可读 Noto/system 字体。

### 3b. 诗词断句被浏览器乱折

**现象**：七言、五言或词句被断成“雨亦 / 奇。”、“总相 / 宜。”这类孤立单字、标点或半句。

**根因**：把整首诗写成一个大字号 `.guofeng-quote-text`，只用 `<br>` 粗略换行，浏览器在容器不足时按字宽自动折。

**做法**：古诗、词句和对联使用 `guofeng-poem-line` + `guofeng-poem-half`；每个诗行表达完整句法，必要时降低 quote 字号或让半句整体换行。

**自检**：桌面和移动端都不能出现标点、单字或半句孤立成行；验证脚本如果提示 `poem quote uses <br> without structured poem lines`，必须改结构。

### 3c. 装饰字体多行相撞

**现象**：`ZhaohuaMinA` 或 `KingHwaOldSong-MN` 标题换成两行后，上下笔画重叠。

**根因**：装饰字体字面框更满，却使用了 `line-height: 0.95-1.08` 这类紧贴行高。

**做法**：可能换行的装饰标题 `line-height` 至少 `1.12`，推荐 `1.16-1.24`；长标题改用 `--font-title-serif` 或拆成主副标题。

**自检**：桌面、平板和手机宽度下，标题两行之间有明确呼吸空间。

### 4. 商业页面有氛围但不能行动

**现象**：餐厅、旅游、品牌或活动页漂亮，但缺 CTA、地址、时间、菜单、价格、路线、预约政策或咨询入口。

**根因**：把商业传播当文化氛围页。

**做法**：实用信息先于故事；使用 CTA、info pills、menu cards、itinerary cards 或 place cards。

**自检**：用户不用翻遍页面，就能知道 where、when、what、how much 和 next action。

### 5. 教育或博物馆页好看但不教学

**现象**：课程、博物馆、历史、诗词或工艺页面精致，但概念、注释、来源、展品细节或 takeaway 不清楚。

**根因**：视觉氛围替代了知识层级。

**做法**：明确学习单元：概念 -> 解释 -> 例子 -> 注释/来源 -> takeaway。展品展示已知的名称、年代、材质、意义和图注。

**自检**：每个教学 section 或 slide 只讲一个清楚知识点；图注和注释无需放大即可读。

### 6. 入境游或英文导览仍是中文氛围文案

**现象**：面向外国游客的页面使用中文导航、中文标签或无实用英文解释的诗意文案。

**根因**：只按国风文化处理，没有按入境游/双语信息任务处理。

**做法**：保留中文地名以建立身份，同时补自然英文说明：place、route、duration、language support、meeting point、travel tips。

**自检**：不懂中文的外国游客仍能理解路线、地点、时间和下一步。

### 7. 图片、菜品或展品输给装饰

**现象**：纹样、背景或标题比用户需要查看的对象、菜品、地点、截图或展品更抢眼。

**根因**：没有围绕真实视觉证据调整装饰比例和对比。

**做法**：让主体图更大更干净；展品和产品使用中性背景；纹样放边缘、低透明层或小分隔。

**自检**：问“页面在展示什么”，答案应是对象、菜品、地点、路线或证据，而不是纹样。

### 7b. Closing 或 hero 背景出现遮罩断层

**现象**：底部 closing、hero 或封面区域出现一条明显竖向/横向断裂，像多盖了一层遮罩。

**根因**：整屏 tile、cover accent、渐变遮罩等多层纹样覆盖范围不同，透明度又接近。

**做法**：closing 默认只用一层主纹样；双层时让第二层极低透明度并柔和渐隐，避免硬边。

**自检**：缩小页面看整体背景，不能看到明显拼接线或局部变暗块。

### 8. HTML PPT 节奏单一

**现象**：多页 deck 重复同样密度、卡片网格和纹样位置。

**根因**：复制一页成功样式，而没有规划 deck rhythm。

**做法**：密集信息页和安静阅读页交替；按内容需要混合 cover、chapter、text-image、card grid、timeline、object showcase 和 closing。

**自检**：缩略图视图中，相邻 slides 不应全是同一密度和结构。

### 9. 主题混用或手补颜色

**现象**：颜色互不相关，一段水墨、一段朱红、一段临时 accent。

**根因**：局部改 theme variables 或混用多个 presets。

**做法**：一个网页或一套 deck 使用一套主题；从已选 theme 替换 `--gf-*` 变量，额外颜色必须从主题派生。

**自检**：搜索随机 hex。任何额外颜色必须有明确角色，且不能形成第二套主题。

### 10. 图片比例跟着原图乱跑

**现象**：截图变超宽条、菜品裁切奇怪、展品留白异常、图片网格不齐。

**根因**：复制原图尺寸，没有给 layout slot 稳定比例。

**做法**：给图片绑定标准比例：`16:9`、`16:10`、`4:3`、`3:2`、`1:1` 或固定高度框；使用 `object-fit` 和合适 `object-position`。

**自检**：同一图片组内，视觉尺度、裁切逻辑和 caption rhythm 一致。

### 11. 安全国风替代真实方向

**现象**：米色纸、红印章、边框和诗句都有，但页面可套到任何品牌、景点、课程或餐厅。

**根因**：Agent 回避更具体方向。

**做法**：回到方向顾问：选择 `撞`、`借` 或 `请`，并用策展人、旅行编辑、品牌设计师、课程制作人、餐厅策划或活动制作人视角判断。

**自检**：用一句话说出方向。如果只能说“中国风”，方向还不够具体。

### 12. 国风文案遮住事实缺口

**现象**：漂亮文案暗示历史、权威、高端、路线、价格或活动安排，但源材料没提供这些事实。

**根因**：风格文案填补了事实空白。

**做法**：事实和氛围分开；缺失事实标 `待确认` / `to confirm`、留空，或改成不作事实承诺的描述。

**自检**：每个日期、时间、地址、价格、路线、引用、展品细节、菜单项、产品 claim 和历史陈述必须来自用户材料或已验证来源。

## 最终命令

```bash
jq empty data/fonts.json
jq empty data/themes.json
jq empty data/patterns.json
python3 scripts/validate-guofeng-html.py assets/templates/web-page.html
python3 scripts/validate-guofeng-html.py assets/templates/ppt-deck.html
python3 scripts/validate-guofeng-html.py assets/showcases/pattern-showcase-001-005.html
```

如果 `python3` 和 `node` 都不可用，改为手动最终检查：

- 确认 JSON 文件未被手改破坏；无法运行 `jq` 时，至少检查括号、逗号和字符串引号。
- 确认 HTML 不含 `[必填]`、本机绝对路径、skill 安装路径、远程图片热链、远程 JS、过期字体 URL。
- 确认所有 `assets/patterns/`、`assets/images/`、`assets/runtime/` 引用都已复制到输出项目。
- HTML PPT 确认保留 deck runtime 控件、每页标题、footer/signature、图片 alt 和 caption。
- 交付说明写明：`未运行自动验证脚本，已按 checklist 手动检查`。
