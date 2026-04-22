# Yu Wang — Academic Portfolio

个人学术主页，基于 Markdown + YAML 驱动，Tailwind CSS 本地构建。

---

## 快速开始

```bash
pip install -r requirements.txt   # 首次安装依赖
npm install                       # 首次安装 Tailwind 构建依赖
npm run build:css                 # 生成 assets/site.css
python3 generate.py               # 构建所有页面
python3 localServe                # 启动本地预览 http://localhost:4000/
```

`python3 localServe` 现在会在启动时自动执行 `npm run build:css` 和 `generate.py`，并在你修改内容、模板或 Tailwind 配置后自动重新构建预览。

---

## 1.  **不要删除的文件**：
- `config.yaml` — 全站共享配置
- `content/*.md` — 你的内容源文件
- `templates/` — Jinja2 模板
- `generate.py` — 构建脚本
- `localServe` — 本地开发服务器
- `img/` — 头像和 favicon
- `CNAME` — GitHub Pages 自定义域名
- `.nojekyll` — 阻止 GitHub 的 Jekyll 构建
- `googlee3e5239673270969.html` — Google 搜索验证
- `requirements.txt` — Python 依赖

---

## 2. 如何添加新页面

### 步骤 1：创建 Markdown 文件

在 `content/` 目录下新建 `.md` 文件，例如 `content/my-page.md`：

```markdown
---
title: "页面标题"
template: home          # 使用 "home" 或 "course" 模板
---

这里写你的 Markdown 正文内容。
```

### 步骤 2：构建

```bash
python3 generate.py                   # 构建所有页面
python3 generate.py content/my-page.md  # 或只构建这一个
```

这会在根目录生成 `my-page.html`。

### 步骤 3：添加导航（可选）

如果需要在顶部导航栏中显示，编辑 `config.yaml` 的 `nav` 部分：

```yaml
nav:
  - label: NewPage
    url: "/my-page.html"
```

### 可用模板

| 模板名 | 用途 | front matter 中必填字段 |
|---|---|---|
| `home` | 主页、通用学术页面 | `experience`, `education`, `articles`, `preprints`, `talks`, `grants`, `journals`, `reviewing`, `courses` |
| `course` | 课程详情页 | `semester`, `instructor`, `topics`, `assessment`, `materials` |
| `blog_home` | Blog 首页 | 无必填字段，文章列表会自动注入 |

> **提示**：front matter 中的字段都是可选的，模板会自动跳过缺失的部分。

---

## 3. 大模型开发指南

> **本节面向 AI 编程助手**。当你被要求修改本网站时，阅读这一节即可快速了解架构。

### 架构总览

```
config.yaml              ← 全站共享数据（个人信息、侧边栏链接、导航）
tailwind.config.js       ← Tailwind 主题配置
assets/
  tailwind.css           ← Tailwind 输入文件
  site.css               ← 构建输出 CSS
content/
  index.md               ← 主页内容（Markdown + YAML front matter）
  blog.md                ← Blog 首页内容（Markdown + YAML front matter）
  blog_posts/*.md        ← Blog 文章源文件
  neural-networks.md     ← 课程页内容
templates/
  base.html              ← Jinja2 基础模板（导航栏、侧边栏、页脚）
  blog_base.html         ← Blog 独立基础模板
  blog_home.html         ← Blog 首页模板
  blog_post.html         ← Blog 文章模板
  home.html              ← 主页模板（继承 base.html）
  course.html            ← 课程页模板（继承 base.html）
generate.py              ← 构建脚本：解析 .md → 渲染 Jinja2 → 输出 .html
```

### 数据流

```
config.yaml ─┐
content/*.md ├──→ generate.py ──→ Jinja2 渲染 ──→ index.html / neural-networks.html / blog/index.html
templates/*.html ┘

templates/*.html + content/*.md ──→ tailwindcss CLI ──→ assets/site.css
```

- `config.yaml` 中的数据通过 `{{ config.xxx }}` 在模板中访问
- `.md` 文件的 YAML front matter 通过 `{{ page.xxx }}` 在模板中访问
- `.md` 文件的 Markdown 正文渲染为 HTML 后通过 `{{ body }}` 在模板中访问

### 设计系统：Academic Slate

完整设计规范见 `stitch/academic_slate/DESIGN.md`。以下是核心要点：

#### 色彩体系

| Token | 色值 | 用途 |
|---|---|---|
| `primary` | `#000666` | 标题、链接、品牌色 |
| `primary-container` | `#1a237e` | 渐变终点、深色强调 |
| `surface` | `#fbf9f8` | 页面背景 |
| `surface-container-low` | `#f6f3f2` | 侧边栏、次要区块背景 |
| `surface-container-lowest` | `#ffffff` | 卡片浮层 |
| `on-surface` | `#1b1c1c` | 正文文字（**不要用纯黑**） |
| `on-surface-variant` | `#454652` | 辅助文字 |
| `secondary-container` | `#cfe6f2` | 标签/徽章背景 |
| `on-tertiary-container` | `#ae945c` | 分类标注文字 |
| `outline-variant` | `#c6c5d4` | 边框（仅 15% 不透明度） |

#### 排版

- **标题**：`Noto Serif`（font-headline），权威感
- **正文**：`Inter`（font-body），可读性
- **标签**：`Inter`（font-label），大写 + 宽字距

#### 核心规则

1. **No-Line Rule**：禁止使用 1px 实线边框分隔区块，用背景色层级区分
2. **Tonal Depth**：通过 `surface` → `surface-container-low` → `surface-container-lowest` 的色调叠层创建层次
3. **Glassmorphism**：导航栏使用 `bg-surface/80 backdrop-blur-xl`
4. **Ghost Border**：如必须有边框，使用 `outline-variant` 的 15% 不透明度（`border-outline-variant/15`）
5. **Ambient Shadow**：阴影用 `shadow-[0_10px_40px_rgba(0,7,103,0.06)]`（带品牌色调的漫射投影）
6. **CTA 渐变**：主按钮使用 `bg-gradient-to-r from-primary to-primary-container`

#### Tailwind CSS 关键类速查

```
页面背景:     bg-surface
侧边栏背景:   bg-surface-container-low
卡片:         bg-surface-container-lowest rounded-xl shadow-[0_2px_10px_rgba(0,7,103,0.02)]
卡片悬停:     hover:shadow-[0_10px_40px_rgba(0,7,103,0.06)] hover:border-primary
节标题:       font-headline text-3xl font-black text-primary
小节标题:     font-headline text-xl font-bold text-primary
正文:         text-on-surface-variant leading-relaxed font-body
标签:         font-label text-xs uppercase tracking-widest
圆角标签:     px-3 py-1 rounded-full bg-secondary-container text-on-secondary-container text-[10px] font-bold
导航链接:     font-headline font-bold text-on-surface/70 hover:text-primary
导航栏:       fixed top-0 w-full z-50 bg-surface/80 backdrop-blur-xl
```

### 修改指南

| 想改什么 | 改哪个文件 |
|---|---|
| 个人信息（姓名、职称、链接） | `config.yaml` |
| 论文、基金、教学经历、学术服务 | `content/index.md` 的 YAML front matter |
| 主页 About 介绍文本 | `content/index.md` 的 Markdown 正文 |
| Blog 首页介绍文字 | `content/blog.md` |
| Blog 文章 | `content/blog_posts/*.md` |
| 课程内容（大纲、考核、资料链接） | `content/neural-networks.md` |
| 页面布局、HTML 结构 | `templates/*.html` |
| 导航栏、侧边栏、页脚 | `templates/base.html` |
| 颜色、字体、Tailwind 主题 | `tailwind.config.js` |
| 新增页面模板 | 在 `templates/` 中新建 `.html`，继承 `base.html` |

### 构建与验证

```bash
npm run build:css                # 先构建 CSS
python3 generate.py                # 构建
python3 localServe                 # 本地预览 http://localhost:4000/
```

修改 `tailwind.config.js`、`assets/tailwind.css`、`templates/*.html` 中涉及类名的内容后，需要重新运行 `npm run build:css`。
修改任何 `config.yaml`、`content/*.md`、`templates/*.html` 后，都需要重新运行 `generate.py`。
`localServe` 会自动监测 `content/` 的变化并重新构建。

### Blog 用法

- Blog 首页内容来自 `content/blog.md`
- Blog 文章源文件放在 `content/blog_posts/`
- 每篇文章会自动生成到 `/blog/<slug>/index.html`
- Blog 首页会自动按日期倒序列出文章

支持直接复制类似 Hexo 的文章 markdown，生成器目前只会读取这些字段：

```yaml
title:
date:
excerpt:
summary:
slug:        # 可选；不写就按文件名自动生成
```

其余 front matter 会被忽略，不影响生成。文章正文会按普通 Markdown 渲染，图片和链接都可以直接使用。
