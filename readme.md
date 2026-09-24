# Yu Wang — Academic Portfolio

个人学术主页，基于 `generate.py` 的静态生成，不使用 Hugo/Jekyll。源文件主要在 `config.yaml`、`content/*.md`、`templates/*.html`；生成产物在仓库根目录和 `blogs/` 目录。

## 快速开始

```bash
uv sync
npm install
npm run build
uv run python localServe
```

- Python 环境由 `uv` 根据 `pyproject.toml` 和 `uv.lock` 管理
- `npm run build` 会更新 MathJax 资源和 `assets/site.css`，再生成网站与 PDF CV
- 本地预览默认在 `http://localhost:4000/`
- `assets/site.css` 是 Tailwind 构建产物，不要手改

## 仓库结构

```text
config.yaml
generate.py
content/
  index.md
  blog.md
  blog_posts/*.md
templates/
  base.html
  home.html
  blog_base.html
  blog_home.html
  blog_post.html
assets/
  tailwind.css
  site.css
```

- `content/index.md`：主页内容，`About Me` 正文就在这里的 markdown body
- `content/blog.md`：Blog 首页说明文字
- `content/blog_posts/*.md`：Blog 文章源文件
- `templates/*.html`：Jinja2 模板

## 在 About Me 中引用 Blog 文章

这套机制作用于所有 markdown 正文，最常见的就是 `content/index.md` 的 `About Me` 部分。你只需要在 markdown 里写引用语法，生成器会在构建时自动替换成真正的博客链接。

支持范围：

- `content/index.md` 的正文
- `content/blog.md` 的正文
- `content/blog_posts/*.md` 的正文
- 其他 `content/*.md` 页面的正文

不支持范围：

- YAML front matter
- `excerpt`、`summary`、`title` 这类 front matter 字段

### 用法 1：按 slug 引用，链接文字自动使用文章标题

```markdown
[[blog:notes-from-discussions-about-ai-with-friends]]
```

会被展开成指向 `/blogs/notes-from-discussions-about-ai-with-friends/` 的链接，链接文字默认就是该文章标题。

### 用法 2：按 slug 引用，并自定义链接文字

```markdown
我最近写过 [[blog:notes-from-discussions-about-ai-with-friends|一篇关于 AI 边界的长文]]。
```

### 用法 3：按文章标题引用，链接文字自动使用文章标题

```markdown
[[blog-title:与不同领域的朋友讨论 AI 的记录，AI 能做什么，以及 AI 的局限]]
```

### 用法 4：按文章标题引用，并自定义链接文字

```markdown
我最近写过 [[blog-title:与不同领域的朋友讨论 AI 的记录，AI 能做什么，以及 AI 的局限|一篇关于 AI 的讨论记录]]。
```

### 解析规则

- `blog:` 后面写文章的最终 slug
- `blog-title:` 后面写文章标题
- `|` 后面的部分可选；不写时，默认把文章标题作为链接文字
- 标题匹配会忽略首尾空白和多余空格；英文大小写不敏感
- 文章 slug 来自 front matter 里的 `slug`，如果没写，就由文件名自动生成

### 什么时候该用 slug，什么时候该用标题

- 优先推荐 `[[blog:slug]]`，因为最稳定，不会因改标题而失效
- `[[blog-title:标题]]` 更适合临时写作，但要求标题唯一
- 如果两篇文章标题相同，构建会报错，并提示你改用 `[[blog:slug]]`

### 构建失败的情况

以下情况会直接让 `python3 generate.py` 或 `npm run build` 失败：

- 写了不存在的 slug
- 写了不存在的标题
- 用 `blog-title:` 引用了一个重复标题
- 写成了空引用，例如 `[[blog:]]`

这样做的目的是避免静默生成坏链接。

### 想原样显示这段语法怎么办

用反引号包起来即可：

```markdown
`[[blog:notes-from-discussions-about-ai-with-friends]]`
```

### 一个完整示例

在 `content/index.md` 的正文里这样写：

```markdown
I recently wrote [[blog:notes-from-discussions-about-ai-with-friends|a long note on AI, teaching, and academic life]].
```

构建后，首页 `About Me` 区块会自动生成一个指向对应博客文章的可点击链接。

## Blog 写作规则

- Blog 首页内容来自 `content/blog.md`
- Blog 文章源文件放在 `content/blog_posts/`
- 每篇文章会自动生成到 `/blogs/<slug>/index.html`
- Blog 首页会自动按日期倒序列出文章

目前生成器会读取这些常用 front matter 字段：

```yaml
title:
date:
excerpt:
summary:
slug:
```

- `slug` 可选；不写就按文件名自动生成
- 文章正文按普通 Markdown 渲染
- 正文中的本地图片会被复制到对应的 `blogs/<slug>/` 目录

### 博客题图

普通博客与论文解读都支持可选的 `cover`。题图位于标题及作者/日期信息之后、正文之前，按原图比例完整显示并适应屏幕宽度。未配置时不显示题图区块。

把图片放在 `img/blog/`，并在文章的 front matter 中添加：

```yaml
cover:
  image: "/img/blog/null-controllability-analytic-noise.png"
  alt: "A noisy blue wave settles to zero while local control acts on region G."
  width: 1672
  height: 941
  # caption: "可选的图注"
```

`width` 和 `height` 可填原始像素尺寸；`alt` 为图片的文字描述。图片不会被裁切或拉伸。

构建时，`generate_images.py` 会自动把本地 PNG、JPEG、静态 WebP 题图生成 480、960、1600 像素宽的 WebP 版本（质量 82，不放大小图），并自动填写实际尺寸及 `srcset`。浏览器根据屏幕宽度和像素密度选择合适的文件，手机无需下载完整大图。原图保留在源文件位置，输出在 `assets/generated/covers/`，不要手工修改。相同原图重复构建不会改写输出；更新原图会复用文件名并更新缓存标识，不会不断创建带新名字的副本。远程题图、SVG 和动图保持原样。

## 论文解读（Paper Notes）

论文解读复用 `content/blog_posts/` 和 `/blogs/<slug>/` 的生成流程，用 `paper_post` 模板沿用学术主页的版式。

1. 在 `content/blog_posts/` 新建 Markdown 文件，例如：

   ```yaml
   ---
   title: "解读标题"
   slug: "my-paper-notes"
   template: "paper_post"
   date: 2026-09-24
   math: true
   listed: true
   ---
   ```

2. 在 `content/index.md` 对应的 `books`、`articles` 或 `preprints` 条目中添加 `blog: "my-paper-notes"`（与 `title`、`links` 同级）。书籍解读可在文章 front matter 中设置 `kicker: "Book Notes"`，默认标签为 `Paper Notes`。
3. 在 front matter 后写正文，运行 `npm run build`。

主页会在该论文已有链接后追加同样样式的 `[Blog]`，论文标题也会链接到同一篇解读，在当前标签页打开。没有 `blog` 字段的论文保持原样；引用不存在的博客会让构建报错。阅读页的作者和 Article/ArXiv 链接直接复用论文条目的信息，返回链接定位到原论文。

首篇解读在 `content/blog_posts/null-controllability-analytic-noise.md`，正文可直接用 Markdown 编辑。`listed: true` 会同时列入 Blog 首页；改为 `listed: false` 后仅从论文条目的 Blog 链接访问，仍能预览正文。空正文会显示准备中的提示。只有首页显示个人资料侧栏；课程介绍、论文解读及其他二级页面不生成侧栏，也没有展开或收起按钮。日常博客保留原有版式。

### 数学公式

论文解读默认开启 MathJax；日常博客也可以通过 `math: true` 开启。公式先由 Arithmatex 保护，再交给 MathJax 排版，避免 Markdown 改写下标、星号、反斜杠和矩阵换行。

```markdown
行内公式：$u_0 \in L^2(G)$，或 \(u(T)=0\)。

$$
\mathbb{E}\int_0^T \|u(t)\|_{L^2(G)}^2\,dt < \infty.
$$

\begin{equation}
  a^2+b^2=c^2 \label{eq:example}
\end{equation}

见公式 $\eqref{eq:example}$。
```

- 独立公式前后留空行；支持 `$$…$$`、`\[…\]`、`equation` 和 `align` 环境。
- 支持 AMS 自动编号、`\label` / `\eqref`；代码块中的公式保持原样。
- 长公式可以在公式区域内横向滚动，不会撑宽手机页面。
- MathJax 4.1.3 及字体由 `npm run build:math` 从锁定的 npm 依赖复制到 `assets/vendor/`，随静态站点发布；阅读时不依赖外部 CDN。不要手改这些生成文件。
- 配置在 `assets/math-config.js`，需要额外的 LaTeX 宏时可在这里统一添加。

实现参考：[MathJax 本地托管](https://docs.mathjax.org/en/latest/web/hosting.html)、[Arithmatex 公式保护](https://facelessuser.github.io/pymdown-extensions/extensions/arithmatex/)。

## 常用操作

### 改主页内容

- `About Me` 正文：编辑 `content/index.md` 的 markdown body
- 论文、基金、课程等结构化信息：编辑 `content/index.md` 的 YAML front matter
- 主页基金只显示英文项目名、期限和来源；`title_cn` 与 `amount` 仍保留在源文件中
- 每个报告话题只显示按日期倒序排列的最近三次活动，`events` 中的完整记录仍保留

### 自动生成 PDF CV

`npm run build` 和 `uv run python generate.py` 都会自动更新 `files/cv-yu-wang.pdf`。发布时提交这个生成文件，主页的 Download CV 就会提供当前版本，无须再单独维护 PDF。

只更新 CV：

```bash
npm run build:cv
```

- `generate_cv.py` 从 `config.yaml` 与 `content/index.md` 读取姓名、联系方式、研究简介、任职、教育、论文、基金、教学和学术服务信息
- CV 使用英文，基金保留 `amount` 金额；不收录 Invited Talks
- 仅在 CV 中使用的联系方式放在 `config.yaml` 的 `cv` 下；主页地址来自 `site_url`
- PDF 页脚显示 CV 内容最后更新日期；跨天重建、修改报告等不进入 CV 的内容，都不会改变日期或 PDF 文件
- `files/cv-yu-wang.meta.json` 保存 CV 内容指纹、最后更新日期和 PDF 校验值，随 PDF 一起提交；换电脑或重新克隆后仍保留原日期。不要删除或手工修改它；首次生成记录时使用当日日期
- PDF 字体使用随仓库保存的 DejaVu Sans，支持论文标题中的希腊字母；字体和许可证在 `assets/fonts/cv/`
- 不直接修改 PDF。修改上述源文件后重新构建，本地预览也会自动更新

检查生成逻辑：`uv run python -m unittest discover -s tests`。

### 构建

```bash
npm run build
```

或者分开执行：

```bash
npm run build:css
uv run python generate.py
```

### 本地预览

```bash
uv run python localServe
```

### 发布

在仓库目录执行一条命令即可：

```bash
npm run deploy
```

它会检查远端 `master`，运行完整构建（网页、CSS、MathJax 和 PDF CV），提交仓库中所有未被忽略的修改、新文件和删除，然后推送到 `origin/master`。不需要先手动 build、git add、commit 或 push。GitHub Pages 收到推送后自动更新线上页面。

也可以写这次的提交说明：

```bash
npm run deploy -- "Update publications and CV"
```

- 默认提交说明为 `Update academic homepage`；没有文件变化时跳过 commit，仍会推送已有的本地提交
- `.DS_Store` 不会加入提交；发布前请确认仓库内其他未被忽略的文件都是准备发布的内容
- 构建或 Git 操作失败时立即停止；修复后重新执行即可，推送失败时已有的本地提交会保留
- 仅从 `master` 发布；若远端有本地未包含的提交，会停止并提示先合并，不会自动覆盖或强制推送
- 实现在 `scripts/publish.cjs`；原来的 `npm run build` 仍只构建，不提交、不推送
- 发布脚本的临时仓库集成检查：`npm run test:publish`

## 修改约定

- 不直接编辑生成文件，除非只是核对构建结果
- 改了 Tailwind 类名、模板或 `assets/tailwind.css` 之后，要重新生成 CSS
- 仓库里可能会有无关的 `.DS_Store` 变动，除非明确需要，不要带进提交
