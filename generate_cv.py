"""Build the downloadable English CV from the site's current source data.

Run `uv run python generate_cv.py`, or use the normal site build.
"""

import html
import os
import re
import tempfile
from datetime import date
from pathlib import Path
from urllib.parse import urljoin

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parent
NAVY = colors.HexColor('#000666')
INK = colors.HexColor('#242732')
MUTED = colors.HexColor('#5b6270')


def plain(value):
    """Use the English part of bilingual site labels and strip display markup."""
    text = html.unescape(re.sub(r'<[^>]+>', '', str(value or '')))
    text = re.sub(r'\s*[（(][^()（）]*[\u3400-\u9fff][^()（）]*[)）]', '', text)
    text = text.replace('**', '')
    text = re.sub('[\u2010-\u2015\u2212]', '-', text)
    return re.sub(r'\s+', ' ', text).strip()


def escaped(value):
    return html.escape(plain(value), quote=True)


def build_cv(config, page, profile_md, output_path=None, as_of=None):
    as_of = as_of or date.today()
    output_path = Path(output_path) if output_path else ROOT / config['cv']['url'].lstrip('/')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    font_dir = ROOT / 'assets' / 'fonts' / 'cv'
    for name, file in [('CV', 'DejaVuSans.ttf'), ('CV-Bold', 'DejaVuSans-Bold.ttf')]:
        if name not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont(name, str(font_dir / file)))
    pdfmetrics.registerFontFamily('CV', normal='CV', bold='CV-Bold', italic='CV', boldItalic='CV-Bold')

    styles = {
        'body': ParagraphStyle('body', fontName='CV', fontSize=9.2, leading=12.5, textColor=INK, spaceAfter=4),
        'title': ParagraphStyle('title', fontName='CV-Bold', fontSize=27, leading=33, textColor=NAVY, spaceAfter=5),
        'section': ParagraphStyle('section', fontName='CV-Bold', fontSize=12, leading=17, textColor=NAVY, spaceBefore=14, spaceAfter=7, keepWithNext=True),
        'subsection': ParagraphStyle('subsection', fontName='CV-Bold', fontSize=10, leading=14, textColor=MUTED, spaceBefore=7, spaceAfter=6, keepWithNext=True),
        'entry': ParagraphStyle('entry', fontName='CV-Bold', fontSize=9.5, leading=13.3, textColor=INK, spaceAfter=3),
        'small': ParagraphStyle('small', fontName='CV', fontSize=8.2, leading=11.5, textColor=MUTED, spaceAfter=4),
        'date': ParagraphStyle('date', fontName='CV', fontSize=8.8, leading=13.3, textColor=MUTED, alignment=TA_RIGHT),
    }

    # A missing glyph must fail the build rather than silently corrupt the CV.
    supported = pdfmetrics.getFont('CV').face.charToGlyph
    def paragraph(text, style='body', markup=False):
        visible = plain(text)
        missing = {c for c in visible if not c.isspace() and ord(c) not in supported}
        if missing:
            raise ValueError(f'CV font cannot render {sorted(missing)!r}; add an English source label where needed')
        content = text if markup else escaped(text)
        return Paragraph(content, styles[style])

    site_url = config.get('site_url', '').rstrip('/') + '/'
    def link(label, url):
        return f'<link href="{html.escape(urljoin(site_url, url), quote=True)}" color="#000666">{escaped(label)}</link>'

    def section(title):
        story.append(paragraph(title, 'section'))

    def append_block(block):
        # Include preceding headings in the entry's keep-together group.
        # ReportLab does not chain keepWithNext through nested KeepTogether.
        while story and getattr(story[-1], 'keepWithNext', False):
            block.insert(0, story.pop())
        story.append(KeepTogether(block))

    def dated_entry(title, period, details=()):
        row = Table([[paragraph(title, 'entry'), paragraph(period, 'date')]], colWidths=[width - 112, 112])
        row.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0), ('TOPPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
        block = [row] + [paragraph(item) for item in details if item]
        append_block(block + [Spacer(1, 4)])

    # Account for the default 6pt inner padding on each side of the frame.
    width = A4[0] - 100
    story = [paragraph(config['name_en'], 'title')]
    story.append(paragraph(f"{config['position']} | {config['institution']}"))
    contact = [link(config['email'], 'mailto:' + config['email'])]
    if config['cv'].get('phone'):
        contact.append(escaped(config['cv']['phone']))
    if config['cv'].get('date_of_birth'):
        contact.append('Born ' + escaped(config['cv']['date_of_birth']))
    story.append(paragraph(' | '.join(contact), 'small', markup=True))
    story.append(paragraph(link(site_url.rstrip('/'), site_url), 'small', markup=True))

    section('Research Profile')
    for text in re.split(r'\n\s*\n', profile_md.strip()):
        if text.strip():
            story.append(paragraph(text))
    story.append(paragraph('Research interests: ' + '; '.join(config.get('research_interests', [])), 'small'))

    section('Appointments')
    for item in page.get('experience', []):
        dated_entry(item['role'], item['period'], [item['place'], item.get('extra')])
    section('Education')
    for item in page.get('education', []):
        dated_entry(item['degree'], item['period'], [item['place'], item.get('extra')])

    section('Publications')
    for key, title in [('books', 'Books'), ('articles', 'Journal Articles'), ('preprints', 'Preprints')]:
        entries = page.get(key, [])
        if not entries:
            continue
        story.append(paragraph(title, 'subsection'))
        for number, paper in enumerate(entries, 1):
            authors = html.escape(str(paper.get('authors', '')), quote=True)
            authors = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', authors)
            block = [paragraph(f"{number}. {paper['title']}", 'entry'), paragraph(authors, markup=True)]
            metadata = ', '.join(str(paper[k]) for k in ('journal', 'info', 'status') if paper.get(k))
            links = [link(item['label'], item['url']) for item in paper.get('links', [])]
            if paper.get('blog'):
                links.append(link('Blog', '/blogs/' + paper['blog'] + '/'))
            if metadata or links:
                line = escaped(metadata)
                if links:
                    line += ' &nbsp; ' + ' | '.join(links)
                block.append(paragraph(line, 'small', markup=True))
            append_block(block + [Spacer(1, 4)])

    section('Research Grants')
    for grant in page.get('grants', []):
        details = [grant['source']]
        if grant.get('amount'):
            details.append('Funding: ' + grant['amount'])
        dated_entry(grant['title_en'], grant['period'], details)

    section('Teaching')
    for course in page.get('courses', []):
        dated_entry(course['name'], course['year'])

    section('Academic Service')
    for service in page.get('reviewing', []):
        story.append(paragraph(service))
    if page.get('journals'):
        story.append(paragraph('Journal refereeing', 'subsection'))
        story.append(paragraph('; '.join(page['journals']) + '.'))

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor('#d8dbe3'))
        canvas.line(44, 36, A4[0] - 44, 36)
        canvas.setFont('CV', 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(44, 23, f"{config['name_en']} | Curriculum Vitae")
        canvas.drawCentredString(A4[0] / 2, 23, 'Updated ' + as_of.strftime('%d %b %Y'))
        canvas.drawRightString(A4[0] - 44, 23, str(doc.page))
        canvas.restoreState()

    # Atomic replacement keeps downloads intact while the preview rebuilds.
    with tempfile.NamedTemporaryFile(dir=output_path.parent, suffix='.pdf', delete=False) as tmp:
        temporary_path = Path(tmp.name)
    try:
        document = SimpleDocTemplate(str(temporary_path), pagesize=A4, rightMargin=44, leftMargin=44, topMargin=40, bottomMargin=48, title=f"{config['name_en']} - Curriculum Vitae", author=config['name_en'], invariant=1)
        document.build(story, onFirstPage=footer, onLaterPages=footer)
        os.replace(temporary_path, output_path)
    finally:
        temporary_path.unlink(missing_ok=True)
    print(f'✓ Current homepage data → {output_path}')
    return output_path


def build_from_source():
    from generate import load_config, read_markdown_page
    config = load_config()
    page, profile = read_markdown_page(str(ROOT / 'content' / 'index.md'))
    return build_cv(config, page, profile)


if __name__ == '__main__':
    build_from_source()
