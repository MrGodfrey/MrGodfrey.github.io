# AGENTS

简要仓库说明，供后续代理快速上手。

## 项目结构
- 这是一个基于 `generate.py` 的静态学术主页，不是 Hugo/Jekyll。
- 源文件主要在 `config.yaml`、`content/*.md`、`templates/*.html`。
- 生成产物在仓库根目录：`index.html`、`neural-networks.html`。
- `assets/site.css` 由 Tailwind 构建生成，不要手改。
- Python 环境由 `uv` 通过 `pyproject.toml` 和 `uv.lock` 管理。

## 常用操作
- 改内容：优先修改 `content/index.md`。
- 构建：`npm run build`。
- 构建会通过 `generate_cv.py` 自动更新 `files/cv-yu-wang.pdf`；单独更新用 `npm run build:cv`。CV 复用主页源数据，基金列金额，不收录报告；不要直接编辑 PDF。
- CV 的 `.meta.json` 生成记录随 PDF 一起提交，保证内容不变时跨天构建也不变更日期。博客题图由 `generate_images.py` 自动生成响应式 WebP，原图保留；不要手改 `assets/generated/covers/`。
- 本地预览：`uv run python localServe`。
- 发布：`npm run deploy`（可用 `npm run deploy -- "提交说明"`），自动构建、commit 并 push `master`。GitHub Pages 直接从仓库静态文件发布。此命令会提交全部未被忽略的网站修改，仅在用户授权发布时执行。

## 修改约定
- 不直接编辑生成文件，除非是在核对构建结果。
- 涉及 Tailwind 类名、模板或 `assets/tailwind.css` 的改动后，要重新生成 CSS。
- 这个仓库可能有无关的 `.DS_Store` 改动，除非用户要求，不要顺手带进提交。
- 当用户要求把学生优秀项目添加到课程主页时，在 `content/neural-networks.md` 的 `projects` 列表新增项目条目，按现有格式填写 `title`、`description`、`team` 以及 GitHub/Bilibili 链接，然后运行 `npm run build` 更新生成页面。
