"""Generate responsive WebP blog covers while preserving source artwork."""

import hashlib
import re
from io import BytesIO
from pathlib import Path
from urllib.parse import unquote, urlsplit

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
COVER_WIDTHS = (480, 960, 1600)


def prepare_cover(cover, source_path, root=ROOT):
    if not cover or not cover.get('image'):
        return cover
    result = dict(cover)
    url = urlsplit(cover['image'])
    if url.scheme or url.netloc:
        return result
    source = (root / unquote(url.path).lstrip('/') if url.path.startswith('/')
              else Path(source_path).parent / unquote(url.path)).resolve()
    if not source.is_relative_to(root.resolve()):
        raise ValueError(f'Cover must be inside the site repository: {source}')
    if not source.is_file():
        raise ValueError(f'Cover image does not exist: {source}')
    if source.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.webp'}:
        return result

    with Image.open(source) as original:
        if getattr(original, 'n_frames', 1) > 1:
            return result
        oriented = ImageOps.exif_transpose(original)
        has_alpha = 'A' in oriented.getbands() or 'transparency' in oriented.info
        image = oriented.convert('RGBA' if has_alpha else 'RGB')

    relative = source.relative_to(root.resolve()).as_posix()
    key = hashlib.sha256(relative.encode('utf-8')).hexdigest()[:10]
    stem = re.sub(r'[^A-Za-z0-9_-]+', '-', source.stem).strip('-') or 'cover'
    folder = root / 'assets' / 'generated' / 'covers'
    folder.mkdir(parents=True, exist_ok=True)
    variants = []
    generated = set()
    for width in sorted({min(width, image.width) for width in COVER_WIDTHS}):
        height = max(1, round(image.height * width / image.width))
        resized = image.resize((width, height), Image.Resampling.LANCZOS)
        buffer = BytesIO()
        resized.save(buffer, format='WEBP', quality=82, method=6)
        content = buffer.getvalue()
        output = folder / f'{stem}-{key}-{width}.webp'
        generated.add(output)
        if not output.exists() or output.read_bytes() != content:
            output.write_bytes(content)
        # Stable filenames avoid accumulating obsolete output files. A digest
        # in the URL invalidates browser caches when the source image changes.
        digest = hashlib.sha256(content).hexdigest()[:12]
        variants.append((f'/{output.relative_to(root).as_posix()}?v={digest}', width, height))

    for obsolete in folder.glob(f'{stem}-{key}-*.webp'):
        if obsolete not in generated:
            obsolete.unlink()

    largest, width, height = variants[-1]
    result.update(
        image=largest,
        width=width,
        height=height,
        srcset=', '.join(f'{url} {width}w' for url, width, _ in variants),
        sizes='(max-width: 640px) calc(100vw - 32px), (max-width: 816px) calc(100vw - 48px), 768px',
    )
    return result
