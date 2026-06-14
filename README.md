# ITBXM Chinese Guofeng Skill · 国风网站 / HTML PPT / 文旅品牌页

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skill](https://img.shields.io/badge/AI%20Agent-Skill-7c3aed.svg)](SKILL.md)
[![HTML](https://img.shields.io/badge/output-HTML%20%2F%20PPT-c2410c.svg)](assets/templates/)

> English version: [README.en.md](README.en.md)

这是一个面向中文用户的本地 Agent Skill，适用于 Claude Code、Codex、Cursor 等工具。它把唐风纹样、国风主题、中文字体策略、网页模板和 HTML PPT runtime 打包在一起，帮助 Agent 生成静态国风网页和横向翻页 HTML PPT。

![功能演示](https://cdn.itbxm.com/img/guofeng-skill-intro.gif)

适合场景：

- 文化课程、博物馆展页、非遗/历史/诗词内容
- 寺庙、园林、街区、城市文化与入境游导览
- 地方餐饮、茶酒香器、民宿、伴手礼展示页
- 新中式品牌页、文旅活动页、发布会 HTML PPT

它专注静态交付，不提供后台系统、登录、上传、支付、实时地图、在线预订或图片生成服务。

![24-patterns](https://cdn.itbxm.com/img/24-patterns.jpg)

## 30 秒开始

### 方式一：让 AI 帮你安装

把下面这段话发给 Claude Code、Codex、Cursor 或其他本地 Agent：

```text
请帮我安装 itbxm-chinese-guofeng-skill。
仓库地址：https://github.com/itbxm/itbxm-chinese-guofeng-skill

如果你是 Claude Code，请安装到：
~/.claude/skills/itbxm-chinese-guofeng-skill

如果你是 Codex，请安装到：
~/.agents/skills/itbxm-chinese-guofeng-skill

如果你有自己的 skills / tools / plugins 目录，请放到对应目录。
安装后请读取 SKILL.md，并告诉我可以怎样使用这个 Skill。
```

### 方式二：手动放进 skills 文件夹

Claude Code 用户：

```bash
git clone https://github.com/itbxm/itbxm-chinese-guofeng-skill ~/.claude/skills/itbxm-chinese-guofeng-skill
```

Codex 用户：

```bash
git clone https://github.com/itbxm/itbxm-chinese-guofeng-skill ~/.agents/skills/itbxm-chinese-guofeng-skill
```

其他本地 Agent 也可以使用同样方式：把仓库放到它配置的 skills、tools 或 plugins 目录，然后让 Agent 读取项目里的 `SKILL.md`。

熟悉命令行的话，也可以尝试：

```bash
npx skills add https://github.com/itbxm/itbxm-chinese-guofeng-skill --skill itbxm-chinese-guofeng-skill
```

装好后，直接对 Agent 说：

```text
使用 itbxm-chinese-guofeng-skill，为杭州入境游路线创建一个国风 HTML 落地页。
```

## 推荐提问方式

你可以直接用自然语言提需求。信息越清楚，生成结果越贴近预期：

```text
场景：我想做一个江南菜餐厅首页
受众：面向来杭州旅游的年轻人和外地游客
输出形式：静态网页 / 6 页 HTML PPT
核心内容：招牌菜、地址、营业时间、预约入口、品牌故事
资料状态：已有菜单和地址，没有菜品照片；可以联网找真实环境图
参考风格：新中式、干净、有一点高级餐厅感；没有固定品牌色
```

也可以更短：

```text
使用 itbxm-chinese-guofeng-skill，帮我做一个杭州入境游三日路线的中英双语国风落地页。资料不完整的地方请标待确认。
```

```text
使用 itbxm-chinese-guofeng-skill，把这份传统文化课程大纲做成 8 页 HTML PPT，面向大学通识课学生。
```

```text
使用 itbxm-chinese-guofeng-skill，为一个新中式香氛品牌做首页。没有品牌规范，你先问我需要哪些资料。
```

## 可以这样用

```text
帮我做一个寺庙英文导览页，面向第一次来中国的外国游客。
```

```text
把这份博物馆展品资料做成 6 页国风 HTML PPT。
```

```text
为一家本地江南菜餐厅做一个国风首页，突出招牌菜、地址、营业时间和预约入口。
```

```text
基于这份商业计划书，做一个新中式香氛品牌的发布会 HTML PPT。
```

```text
为敦煌主题三日游生成一个中英双语文旅落地页。
```

```text
把这篇传统文化课程大纲做成适合课堂讲解的网页 PPT。
```

## 它擅长什么

- **24 组唐风纹样资产**：每组包含平铺纹样、横向纹样、纵向纹样和封面装饰。
- **七套国风主题**：水墨、青瓷、唐宫朱金、青玉、敦煌、玄漆、花朝胭脂。
- **两种输出**：静态网页和横向翻页 HTML PPT。
- **文化与商业都能做**：既能讲知识、展品和诗词，也能做路线、菜单、品牌故事和活动报名页。
- **简繁与双语策略**：简体、繁体、英文和中英双语都有对应的字体与可读性建议。
- **静态可搬走**：生成结果可以作为普通静态项目保存、部署或继续修改。

## 适合 / 不适合

合适：

- 文化教育、课程课件、学术沙龙
- 博物馆、非遗、历史、诗词、城市文化
- 入境游、寺庙/园林/街区导览、文旅路线
- 地方餐饮、茶酒香器、民宿、伴手礼
- 新中式品牌、节庆活动、报名页、发布会 HTML PPT

不适合：

- 后台管理系统、登录注册、上传、支付、数据库
- 实时地图 API、实时预订、库存、订单系统
- 大段复杂表格、财务模型、多人协作编辑
- 需要在线图片生成或远程字体托管的工作流

## 文件结构

```text
SKILL.md                 # Agent 入口说明
data/                    # 纹样、主题、字体 metadata
references/              # 工作流、场景、主题、字体、版式、组件、检查清单
assets/patterns/         # 24 组 PNG/WebP 唐风纹样
assets/templates/        # web-page.html 与 ppt-deck.html 种子模板
assets/runtime/          # HTML PPT 本地翻页 runtime
scripts/                 # 素材采集与 HTML 验证脚本
```

## 开源与字体

本仓库采用 [MIT License](LICENSE)。仓库自有代码、文档、模板、metadata 与 itbxm 原创纹样可按 MIT 使用、修改和分发，包括商业用途。

本项目主要使用开源、可商用的 Noto 字体，保证正文、菜单、路线、价格、地址、英文说明和密集图注的阅读稳定。

装饰字体京华老宋体和朝华标题明朝体由 [特里王](https://www.zhihu.com/people/wang-ting-rui-61) 开源发布，可商用。字体 CSS 不可用时，页面会自动回退到 Noto 或系统字体。

## 致谢

本项目的 Skill 组织方式、README 信息节奏和 HTML PPT 工作流设计，参考了歸藏的 [op7418/guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill)。在此感谢歸藏对 Agent Skill 写作方式的探索和开源分享。

本项目也参考了花叔的 [alchaincyf/huashu-design](https://github.com/alchaincyf/huashu-design)：尤其是 HTML-native 设计 Skill、让用户做决策而不是操作图层、五维评审、图片前置和反“安全设计”的思路。在此感谢花叔的开源分享。
