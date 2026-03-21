"""
Site generator — reads Markdown+YAML front matter from content/ and renders
Jinja2 templates into static HTML.

Usage:
    python generate.py              # build all .md files in content/
    python generate.py content/index.md   # build a single file
"""

import os
import re
import sys

import yaml
import markdown
from jinja2 import Environment, FileSystemLoader

# ------------------------------------------------------------------ helpers

CONFIG_FILE = "config.yaml"
CONTENT_DIR = "content"
TEMPLATE_DIR = "templates"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_front_matter(text):
    """Return (front_matter_dict, body_markdown)."""
    m = re.match(r"\A---\s*\n(.*?\n)---\s*\n(.*)", text, re.DOTALL)
    if m:
        fm = yaml.safe_load(m.group(1)) or {}
        body = m.group(2)
    else:
        fm = {}
        body = text
    return fm, body


def render_authors(text):
    """Turn **name** in author strings into <strong>name</strong>."""
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


# ------------------------------------------------------------------ build

def build_page(md_path, config, env):
    with open(md_path, "r", encoding="utf-8") as f:
        raw = f.read()

    page, body_md = parse_front_matter(raw)
    body_html = markdown.markdown(body_md, extensions=["extra"])

    template_name = page.get("template", "home") + ".html"
    template = env.get_template(template_name)

    # Render authors with bold
    for key in ("articles", "preprints"):
        for paper in page.get(key, []):
            if "authors" in paper:
                paper["authors"] = render_authors(paper["authors"])

    # Allow HTML in body for the home page (research description)
    html = template.render(
        config=config,
        page=page,
        body=body_html,
        page_title=page.get("title", "Untitled"),
        active_nav=page.get("active_nav", ""),
    )

    # Output filename: content/index.md -> index.html
    basename = os.path.splitext(os.path.basename(md_path))[0] + ".html"
    output_path = os.path.join(".", basename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✓ {md_path} → {output_path}")


def main():
    if not os.path.exists(CONFIG_FILE):
        print(f"错误：配置文件 {CONFIG_FILE} 不存在")
        sys.exit(1)

    config = load_config()
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=False,  # We handle escaping in templates / content
    )

    # Build one or all
    if len(sys.argv) > 1:
        for path in sys.argv[1:]:
            if path.endswith(".md") and os.path.isfile(path):
                build_page(path, config, env)
            else:
                print(f"跳过：{path}（不是 .md 文件或不存在）")
    else:
        for root, _dirs, files in os.walk(CONTENT_DIR):
            for fname in sorted(files):
                if fname.endswith(".md"):
                    build_page(os.path.join(root, fname), config, env)


if __name__ == "__main__":
    main()
