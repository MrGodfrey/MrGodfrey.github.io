"""
Site generator — reads Markdown+YAML front matter from content/ and renders
Jinja2 templates into static HTML.

Usage:
    python generate.py                    # build the whole site
    python generate.py content/index.md   # build a single page
"""

import hashlib
import os
import re
import shutil
import sys
import unicodedata
from datetime import date as date_type
from datetime import datetime

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader

# ------------------------------------------------------------------ helpers

CONFIG_FILE = "config.yaml"
CONTENT_DIR = "content"
TEMPLATE_DIR = "templates"
BLOG_SOURCE = os.path.join(CONTENT_DIR, "blog.md")
BLOG_POSTS_DIR = os.path.join(CONTENT_DIR, "blog_posts")
BLOG_OUTPUT_DIR = "blog"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_front_matter(text):
    """Return (front_matter_dict, body_markdown)."""
    m = re.match(r"\A---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)", text, re.DOTALL)
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


def render_markdown(text):
    return markdown.markdown(text, extensions=["extra"])


def normalize_whitespace(text):
    return re.sub(r"\s+", " ", text).strip()


def strip_html(text):
    return re.sub(r"<[^>]+>", "", text)


def excerpt_from_markdown(body_md, limit=180):
    plain_text = normalize_whitespace(strip_html(render_markdown(body_md)))
    if len(plain_text) <= limit:
        return plain_text

    clipped = plain_text[:limit].rsplit(" ", 1)[0]
    return (clipped or plain_text[:limit]).rstrip(" .,;:!?") + "..."


def coerce_datetime(value):
    if isinstance(value, datetime):
        return value
    if isinstance(value, date_type):
        return datetime.combine(value, datetime.min.time())
    if isinstance(value, str):
        cleaned = normalize_whitespace(value)
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%Y/%m/%d %H:%M:%S", "%Y/%m/%d"):
            try:
                return datetime.strptime(cleaned, fmt)
            except ValueError:
                continue
    return None


def format_display_date(value, fallback_ts=None):
    dt = coerce_datetime(value)
    if dt:
        return dt.strftime("%Y-%m-%d")
    if value:
        return normalize_whitespace(str(value))
    if fallback_ts is not None:
        return datetime.fromtimestamp(fallback_ts).strftime("%Y-%m-%d")
    return ""


def sort_date(value, fallback_ts):
    dt = coerce_datetime(value)
    if dt:
        return dt
    return datetime.fromtimestamp(fallback_ts)


def slugify(value):
    ascii_text = (
        unicodedata.normalize("NFKD", value)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-")
    if slug:
        return slug

    unicode_slug = re.sub(r"[^\w]+", "-", value.lower(), flags=re.UNICODE).strip("-")
    if unicode_slug:
        return unicode_slug

    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:10]
    return f"post-{digest}"


def collect_local_assets(body_md):
    assets = []

    for match in re.finditer(r"!\[[^\]]*\]\((.*?)\)", body_md):
        raw_target = match.group(1).strip()
        if raw_target.startswith("<") and ">" in raw_target:
            candidate = raw_target[1:raw_target.index(">")]
        else:
            candidate = raw_target.split()[0] if raw_target else ""
        assets.append(candidate)

    for match in re.finditer(r'<img[^>]+src=["\']([^"\']+)["\']', body_md):
        assets.append(match.group(1).strip())

    local_assets = []
    for asset in assets:
        if not asset:
            continue
        if asset.startswith(("http://", "https://", "/", "data:", "#")) or "://" in asset:
            continue
        local_assets.append(asset)

    return sorted(set(local_assets))


def ensure_parent_dir(path):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def write_output(path, html):
    ensure_parent_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def read_markdown_page(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        raw = f.read()
    return parse_front_matter(raw)


def is_inside(path, directory):
    abs_path = os.path.abspath(path)
    abs_dir = os.path.abspath(directory)
    try:
        return os.path.commonpath([abs_path, abs_dir]) == abs_dir
    except ValueError:
        return False


def is_blog_home(md_path):
    return os.path.abspath(md_path) == os.path.abspath(BLOG_SOURCE)


def is_blog_post(md_path):
    return is_inside(md_path, BLOG_POSTS_DIR)


def render_page(config, env, page, body_html, output_path, source_path, template_name=None, extra_context=None):
    template_file = template_name or (page.get("template", "home") + ".html")
    template = env.get_template(template_file)

    context = {
        "config": config,
        "page": page,
        "body": body_html,
        "page_title": page.get("title", "Untitled"),
        "active_nav": page.get("active_nav", ""),
    }
    if extra_context:
        context.update(extra_context)

    html = template.render(**context)
    write_output(output_path, html)
    print(f"✓ {source_path} → {output_path}")


# ------------------------------------------------------------------ build

def build_page(md_path, config, env, output_path=None, template_name=None, extra_context=None):
    page, body_md = read_markdown_page(md_path)
    body_html = render_markdown(body_md)

    for key in ("articles", "preprints"):
        for paper in page.get(key, []):
            if "authors" in paper:
                paper["authors"] = render_authors(paper["authors"])

    final_output = output_path or (os.path.splitext(os.path.basename(md_path))[0] + ".html")
    render_page(
        config,
        env,
        page,
        body_html,
        final_output,
        md_path,
        template_name=template_name,
        extra_context=extra_context,
    )


def load_blog_posts():
    posts = []
    used_slugs = set()

    if not os.path.isdir(BLOG_POSTS_DIR):
        return posts

    for root, _dirs, files in os.walk(BLOG_POSTS_DIR):
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue

            source_path = os.path.join(root, fname)
            page, body_md = read_markdown_page(source_path)
            file_timestamp = os.path.getmtime(source_path)

            raw_slug = str(page.get("slug") or os.path.splitext(fname)[0])
            slug = slugify(raw_slug)
            base_slug = slug
            suffix = 2
            while slug in used_slugs:
                slug = f"{base_slug}-{suffix}"
                suffix += 1
            used_slugs.add(slug)

            excerpt_source = page.get("excerpt") or page.get("summary") or excerpt_from_markdown(body_md)
            posts.append(
                {
                    "title": normalize_whitespace(str(page.get("title") or os.path.splitext(fname)[0])),
                    "slug": slug,
                    "url": f"/blog/{slug}/",
                    "display_date": format_display_date(page.get("date"), file_timestamp),
                    "sort_date": sort_date(page.get("date"), file_timestamp),
                    "excerpt": normalize_whitespace(str(excerpt_source)),
                    "body_md": body_md,
                    "local_assets": collect_local_assets(body_md),
                    "source_path": source_path,
                    "page": page,
                    "output_path": os.path.join(BLOG_OUTPUT_DIR, slug, "index.html"),
                }
            )

    posts.sort(key=lambda post: (post["sort_date"], post["title"].lower()), reverse=True)
    return posts


def build_blog(config, env):
    if not os.path.isfile(BLOG_SOURCE):
        return

    if os.path.isdir(BLOG_OUTPUT_DIR):
        shutil.rmtree(BLOG_OUTPUT_DIR)

    posts = load_blog_posts()

    build_page(
        BLOG_SOURCE,
        config,
        env,
        output_path=os.path.join(BLOG_OUTPUT_DIR, "index.html"),
        extra_context={"blog_posts": posts},
    )

    for post in posts:
        page = dict(post["page"])
        page.setdefault("title", post["title"])
        page.setdefault("template", "blog_post")
        page.setdefault("active_nav", "Blog")
        render_page(
            config,
            env,
            page,
            render_markdown(post["body_md"]),
            post["output_path"],
            post["source_path"],
            template_name="blog_post.html",
            extra_context={"post": post},
        )
        copy_blog_assets(post)


def copy_blog_assets(post):
    if not post["local_assets"]:
        return

    source_dir = os.path.dirname(post["source_path"])
    output_dir = os.path.dirname(post["output_path"])

    for asset in post["local_assets"]:
        source_asset = os.path.normpath(os.path.join(source_dir, asset))
        target_asset = os.path.normpath(os.path.join(output_dir, asset))

        if not os.path.isfile(source_asset):
            continue
        if not is_inside(target_asset, output_dir):
            continue

        ensure_parent_dir(target_asset)
        shutil.copy2(source_asset, target_asset)


def build_default_site(config, env):
    for root, dirs, files in os.walk(CONTENT_DIR):
        dirs[:] = [d for d in dirs if not is_inside(os.path.join(root, d), BLOG_POSTS_DIR)]
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            path = os.path.join(root, fname)
            if is_blog_home(path):
                continue
            build_page(path, config, env)

    build_blog(config, env)


def build_requested_paths(paths, config, env):
    should_build_blog = False

    for path in paths:
        if not (path.endswith(".md") and os.path.isfile(path)):
            print(f"跳过：{path}（不是 .md 文件或不存在）")
            continue

        if is_blog_home(path) or is_blog_post(path):
            should_build_blog = True
            continue

        build_page(path, config, env)

    if should_build_blog:
        build_blog(config, env)


def main():
    if not os.path.exists(CONFIG_FILE):
        print(f"错误：配置文件 {CONFIG_FILE} 不存在")
        sys.exit(1)

    config = load_config()
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=False,
    )

    if len(sys.argv) > 1:
        build_requested_paths(sys.argv[1:], config, env)
    else:
        build_default_site(config, env)


if __name__ == "__main__":
    main()
