# 通用真实素材协议

当输出涉及真实品牌、产品、人物、地点、活动、空间、榜单、工具、商业介绍、课程证据、内容科普或任何内容型图片时，先读本文件。本文件负责“素材前置”：先决定要找什么素材、用哪个 provider、是否能自动采集、如何记录状态；`references/image-framing.md` 负责图片进入版式后的裁切、图注和视觉处理。

核心原则：**资产 > 风格，核心素材先于版式。** Logo、产品图、UI 截图、地点/展品/菜品真实图、活动/空间证据，比配色、字体和纹样更能决定输出是否可信。找不到核心素材时，宁可 `占位待补` 或向用户索取，不要用 CSS 剪影、泛图、AI 仿真照片或装饰纹样假装解决。

## 1. 素材 Slot 先行

生成网页或 HTML PPT 前，先列素材 slot。每个 slot 至少记录：

| Slot | Type | 必需性 | 中文关键词 | 英文关键词 | Provider | 状态 | 评分 | 最终文件 | 来源页 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Hero 西湖主视觉 | place | 必需 | 西湖 杭州 全景 | West Lake Hangzhou panorama | domestic lane / balanced | 已验证/待用户确认/占位待补 | 8/10 | assets/images/... | 来源 URL |

支持的素材类型：

- `place`：地点、景区、城市、建筑、街区、路线节点。
- `person`：真实人物、讲师、创始人、嘉宾、历史人物画像。
- `product`：实体产品、包装、礼品、器物、设备。
- `brand-logo`：品牌 logo、产品 logo、榜单/对比对象 logo。
- `ui`：App、网站、SaaS、工具界面截图。
- `food`：菜品、菜单实物、餐厅招牌菜。
- `space`：店铺、展厅、茶室、民宿、活动场地、办公空间。
- `event`：活动现场、发布会、展览、课程、演出。
- `artifact`：展品、文物、非遗器物、书画、工艺材料。
- `document`：书籍封面、PDF 截图、报告页、证书、票据。
- `evidence`：截图、数据图、案例页面、榜单证据。
- `generic`：通用场景图；仅在与内容有内在关联时使用。

装饰图不强行配 stock photo。取图前先问：去掉这张图，信息是否受损？受损才作为必需 slot。

核心素材硬规则：

- 具名品牌、产品、App、工具、榜单或对比页：每个具名对象必须列 `brand-logo` slot。
- 实体产品、包装、器物、茶酒香器、伴手礼：必须列 `product` slot，优先官方产品页或 press kit。
- 数字产品、App、SaaS、工具页面：必须列 `ui` slot，优先 App Store、Google Play、官网 screenshot、官方演示视频或用户账号截图。
- 地点、展品、菜品、空间、活动、人物：只要图片会影响理解、信任或转化，就按必需 slot 处理。

## 2. Provider 分级

默认走双通道稳健分级：低反爬自动采集，强平台只做线索和浏览器辅助，不写绕风控脚本。平台支持并行 agent 时，可同时派发“国内素材 agent”和“国际开放源 agent”；不支持并行时，同一个 agent 按国内源通道 -> 国际开放源通道顺序执行。

| 等级 | 用法 | Provider |
| --- | --- | --- |
| A 自动采集 | 可以脚本下载或复制 | 本地素材、用户项目目录、官方网站、品牌官网、文旅/政府/博物馆/高校/主办方官网、海外官网、开放图库、有限预算 Wikimedia、Met Museum Open Access、Art Institute of Chicago API、SVGL、Simple Icons、Google favicon |
| B 线索/浏览器辅助 | 只生成 `asset-leads.md`，由浏览器打开后保存可见素材或截图 | App Store、Google Play、官方视频截帧、Unsplash/Pexels 内容相关摄影线索、微信公众号、小红书、点评/美团、携程/马蜂窝、京东/天猫官方店、抖音/快手、百度/搜狗/360 图片搜索 |
| C 不自动抓取 | 不绕登录、签名、token 或强风控 | 登录墙、强风控、批量历史内容、需要签名参数或绕过 token 的平台 |

国内平台图片不以版权为主要阻塞点，但必须记录来源页和采集状态，方便用户追溯。Wikimedia 只作为国际开放源或开放版权题材的有限预算候选，不作为每个国内素材 slot 的默认自动出口。

## 2.1 多渠道来源矩阵

按素材类型选择渠道，而不是所有 slot 都机械请求 Wikimedia：

| 素材类型 | 优先渠道 |
| --- | --- |
| `brand-logo` | SVGL API -> Simple Icons -> 官网 brand/press/press-kit -> 官网 inline SVG -> Google favicon -> 官方社媒头像线索 |
| `product` | 官方产品页 hero/gallery -> press kit -> 官方新闻稿 -> 官方发布片/演示视频截帧 -> 用户提供素材；国内产品可补京东/天猫官方店线索 |
| `ui` | App Store -> Google Play -> 官网 screenshots section -> 官方演示视频截帧 -> 用户账号截图 |
| `artifact` / `document` | 官方博物馆/馆藏页 -> Wikimedia Commons -> Met Museum Open Access -> Art Institute of Chicago API -> 国内博物馆/文旅/高校线索 |
| `place` / `food` / `space` / `event` | 本地素材 -> 官网/政府/文旅/博物馆/品牌官网 -> 国内平台浏览器线索；国际或开放题材才补 Wikimedia、Unsplash/Pexels |
| `generic` | 默认不自动上 stock photo；只有图片与内容有内在关联时，才使用 Unsplash/Pexels 线索 |

`5-10-2-8` 质量门槛：核心内容图默认跨多渠道搜索，`--count 10 --pick 2`，从候选里选 1-2 张 8/10 以上素材。Logo 是识别根基，有就必须用；其他素材低于 8/10 时宁可 `占位待补`。

## 3. 默认采集命令

新流程默认使用通用素材脚本，并按题材选择 source profile：

国内题材：

```bash
python3 scripts/fetch-guofeng-assets.py \
  --slot "Hero 西湖主视觉" \
  --type place \
  --query "西湖 杭州 全景" "West Lake Hangzhou panorama" \
  --out site/assets/images \
  --source-profile domestic \
  --count 10 \
  --pick 2
```

通用不确定题材：

```bash
python3 scripts/fetch-guofeng-assets.py \
  --slot "Hero 主视觉" \
  --type generic \
  --query "<中文关键词>" "<英文关键词>" \
  --out site/assets/images \
  --source-profile balanced \
  --wikimedia-count 2 \
  --count 10 \
  --pick 2
```

国际/开放版权题材：

```bash
python3 scripts/fetch-guofeng-assets.py \
  --slot "Artifact 主图" \
  --type artifact \
  --query "Mona Lisa" \
  --out site/assets/images \
  --source-profile international \
  --wikimedia-count 2 \
  --count 10 \
  --pick 2
```

常用参数：

```bash
--source-url "<官方页面 URL>"
--local-dir "<本地素材目录>"
--source-profile domestic|international|balanced
--wikimedia-count <每次命令允许的 Wikimedia 候选数，0 表示禁用>
--manifest <site-root>/assets/sources/asset-manifest.md
--candidates <site-root>/assets/sources/asset-candidates.json
--asset-spec <site-root>/assets/sources/guofeng-asset-spec.md
--domain "<brand-domain>"
```

旧命令 `scripts/fetch-guofeng-images.mjs` 保留一个版本周期作为兼容入口；完整生成默认优先用 `scripts/fetch-guofeng-assets.py`。`scripts/fetch-guofeng-images.py` 仅作为 Wikimedia 快捷入口，不要用于国内题材的批量素材 slot。

## 3.1 无运行时 fallback

如果 `python3 --version` 和 `node --version` 都不可用，不要要求用户先安装运行时才能继续。改用手动/浏览器辅助素材流程：

- 仍然先列素材 slot、类型、关键词、provider 和状态。
- A 级来源改为浏览器/WebSearch/用户提供素材：官网、品牌 press 页、博物馆/景区/学校/主办方页面；国际开放源可补 Wikimedia 页面。
- B/C 级来源仍只做线索，不写绕风控脚本。
- 下载不到或无法确认来源时，使用诚实占位，并标 `占位待补` 或 `待用户确认`。
- 手写 `assets/sources/asset-manifest.md`、`guofeng-asset-spec.md` 和 `image-sources.md`；没有候选 JSON 时，在交付说明中写明 `未生成 asset-candidates.json`。
- 交付说明必须写明：`未运行自动素材脚本，已按 asset-workflow 手动记录来源/占位状态`。

## 4. Provider 使用建议

- 本地素材优先：用户给过的图、项目目录、`~/Downloads`、`_archive/`、用户指定素材库。
- 官方站优先：具体品牌、产品、活动、机构、学校、展会、景区、博物馆、课程主办方，优先找官网、press、产品页、新闻稿、展览页。
- 国内题材优先 `--source-profile domestic`；它不会请求 Wikimedia，而是生成国内平台 leads，交给浏览器辅助。
- 通用不确定题材使用 `--source-profile balanced --wikimedia-count 2`；Wikimedia 只作为少量补充候选。
- 国际地点、海外品牌、开放文物、Commons 覆盖明确的对象使用 `--source-profile international --wikimedia-count 2`。
- Logo 单独处理：出现真实品牌/产品名时，`brand-logo` slot 必须走 `svgl,simple-icons,official-web,google-favicon` 链路；榜单、对比、推荐类 deck 中每个具名对象都要列 logo slot。
- UI 截图优先官方：App Store、Google Play、官网 screenshot、产品演示页、官方视频截帧、用户提供截图。
- 美术/博物馆/历史内容可用国际开放馆藏：Wikimedia Commons、Met Museum Open Access、Art Institute of Chicago API；国内展品仍优先官方馆藏页和博物馆/文旅/高校来源。
- Unsplash/Pexels 只作为内容相关摄影线索，不给文章列表、设置页、抽象 banner 或纯装饰位滥用 stock photo。
- B 级平台只做线索：不要尝试批量抓小红书、点评、淘宝、抖音、公众号历史文章；需要时打开浏览器，保存可见图或截图，并标 `待用户确认`。

## 5. 候选与评分

脚本生成：

- `assets/sources/asset-manifest.md`：slot 计划、状态和最终选择。
- `assets/sources/asset-candidates.json`：候选素材、provider、来源页、评分、是否入选。
- `assets/sources/asset-leads.md`：B/C 级平台线索和浏览器辅助动作。
- `assets/sources/image-sources.md`：最终入 HTML 的图片来源记录。
- `assets/sources/guofeng-asset-spec.md`：最终素材决策文件，记录 slot、type、必需性、候选数量、入选分数、最终文件、用途建议和占位原因。

最终只使用 8/10 以上素材；低于 8 分宁可 `占位待补`。评分维度：

- 匹配度：来源页能确认对象、地点、品牌、产品或事件。
- 来源稳定度：本地/用户提供、官方站、开放图库优先。
- 分辨率：hero 建议 ≥1600px，产品/展品/卡片建议 ≥1000px。
- 构图：主体清楚，不过暗、不糊、不被严重裁切。
- 可追溯性：来源页、provider、采集日期能记录。

## 6. 失败路径

- A 级自动采集失败：换关键词、加 `--source-url`、加 `--local-dir` 或换 A 级 provider。
- B 级平台有线索：写 `asset-leads.md`，用浏览器辅助保存或截图。
- C 级来源：不自动抓取，改用用户提供素材、官方来源或诚实占位。
- 最终仍无 8/10 素材：HTML 使用诚实占位，manifest 与交付说明标 `占位待补`。
- 核心素材已选定：HTML/PPT 只能引用 `guofeng-asset-spec.md` 中的本地最终文件路径；不得用远程热链、CSS 剪影、泛图或 AI 仿真图替代。
