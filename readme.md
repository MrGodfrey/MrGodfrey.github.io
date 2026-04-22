# Yu Wang — Academic Portfolio

个人学术主页，基于 `generate.py` 的静态生成，不使用 Hugo/Jekyll。源文件主要在 `config.yaml`、`content/*.md`、`templates/*.html`；生成产物在仓库根目录和 `blogs/` 目录。

## 快速开始

```bash
pip install -r requirements.txt
npm install
npm run build
python3 localServe
```

- `npm run build` 会先生成 `assets/site.css`，再运行 `python3 generate.py`
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
python3 generate.py
```

### 本地预览

```bash
python3 localServe
```

### 发布

- 构建完成后提交并推送 `master`
- GitHub Pages 直接从仓库静态文件发布

## 修改约定

- 不直接编辑生成文件，除非只是核对构建结果
- 改了 Tailwind 类名、模板或 `assets/tailwind.css` 之后，要重新生成 CSS
- 仓库里可能会有无关的 `.DS_Store` 变动，除非明确需要，不要带进提交
