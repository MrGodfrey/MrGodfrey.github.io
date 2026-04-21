# AGENTS

简要仓库说明，供后续代理快速上手。

## 项目结构
- 这是一个基于 `generate.py` 的静态学术主页，不是 Hugo/Jekyll。
- 源文件主要在 `config.yaml`、`content/*.md`、`templates/*.html`。
- 生成产物在仓库根目录：`index.html`、`neural-networks.html`。
- `assets/site.css` 由 Tailwind 构建生成，不要手改。

## 常用操作
- 改内容：优先修改 `content/index.md`。
- 构建：`npm run build`。
- 本地预览：`python3 localServe`。
- 发布：构建后提交并推送 `master`，GitHub Pages 直接从仓库静态文件发布。

## 修改约定
- 不直接编辑生成文件，除非是在核对构建结果。
- 涉及 Tailwind 类名、模板或 `assets/tailwind.css` 的改动后，要重新生成 CSS。
- 这个仓库可能有无关的 `.DS_Store` 改动，除非用户要求，不要顺手带进提交。
