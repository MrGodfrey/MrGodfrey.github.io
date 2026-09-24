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
- `npm run build` 会先生成 `assets/site.css`，再运行 `uv run python generate.py`
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

2. 在 `content/index.md` 对应的 `articles` 或 `preprints` 条目中添加 `blog: "my-paper-notes"`（与 `title`、`links` 同级）。
3. 在 front matter 后写正文，运行 `npm run build`。

主页会在该论文已有链接后追加同样样式的 `[Blog]`，在当前标签页打开。没有 `blog` 字段的论文保持原样；引用不存在的博客会让构建报错。阅读页的作者和 Article/ArXiv 链接直接复用论文条目的信息，返回链接定位到原论文。

首篇已预留在 `content/blog_posts/null-controllability-analytic-noise.md`。目前正文为空，页面显示准备中；`listed: false` 只控制它暂不出现在日常 Blog 首页，仍可从论文条目的 Blog 链接访问，也可以预览已写入的正文。完成后改为 `listed: true` 即可同时列入 Blog 首页。只有首页显示个人资料侧栏；课程介绍、论文解读及其他二级页面不生成侧栏，也没有展开或收起按钮。日常博客保留原有版式。

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

- 构建完成后提交并推送 `master`
- GitHub Pages 直接从仓库静态文件发布

## 修改约定

- 不直接编辑生成文件，除非只是核对构建结果
- 改了 Tailwind 类名、模板或 `assets/tailwind.css` 之后，要重新生成 CSS
- 仓库里可能会有无关的 `.DS_Store` 变动，除非明确需要，不要带进提交
