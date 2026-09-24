import tempfile
import unittest
import json
import shutil
from datetime import date
from pathlib import Path

from pypdf import PdfReader

from generate import load_config, read_markdown_page
from generate_cv import build_cv, plain


class CVTests(unittest.TestCase):
    def test_current_sources_appear_in_pdf_with_grant_amounts_but_without_talks(self):
        config = load_config()
        page, profile = read_markdown_page('content/index.md')
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'cv.pdf'
            build_cv(config, page, profile, output, as_of=date(2026, 9, 24))
            reader = PdfReader(output)
            text = ' '.join(' '.join(p.extract_text() for p in reader.pages).split())
            for group in ('books', 'articles', 'preprints'):
                for paper in page[group]:
                    self.assertIn(plain(paper['title']), text)
            for grant in page['grants']:
                self.assertIn(plain(grant['title_en']), text)
                self.assertIn('Funding: ' + grant['amount'], text)
                self.assertIn(grant['source'], text)
            self.assertNotIn('Invited Talks', text)
            for topic in page['talks']:
                for event in topic['events']:
                    self.assertNotIn(event['venue'], text)
            self.assertIn('ϕ-null', text)
            self.assertIn('Updated 24 Sep 2026', text)
            urls = [
                annotation.get_object().get('/A', {}).get('/URI', '')
                for pdf_page in reader.pages
                for annotation in pdf_page.get('/Annots', [])
            ]
            self.assertIn(config['site_url'] + '/blogs/null-controllability-analytic-noise/', urls)

    def test_source_updates_propagate_and_rebuild_is_stable(self):
        config = load_config()
        page, profile = read_markdown_page('content/index.md')
        page['grants'][0]['amount'] = 'RMB 123K'
        page['preprints'].insert(0, {'title': 'New source paper', 'authors': '**Y. Wang**', 'status': 'Submitted'})
        page['talks'].append({'title': 'Excluded talk', 'events': [{'venue': 'Excluded venue'}]})
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'cv.pdf'
            build_cv(config, page, profile, output, as_of=date(2026, 9, 24))
            first = output.read_bytes()
            text = ' '.join(p.extract_text() for p in PdfReader(output).pages)
            self.assertIn('Funding: RMB 123K', text)
            self.assertIn('New source paper', text)
            self.assertNotIn('Excluded', text)
            build_cv(config, page, profile, output, as_of=date(2026, 9, 24))
            self.assertEqual(output.read_bytes(), first)

    def test_date_changes_only_when_cv_content_changes_and_survives_a_fresh_checkout(self):
        config = load_config()
        page, profile = read_markdown_page('content/index.md')
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'cv.pdf'
            state = output.with_suffix('.meta.json')
            build_cv(config, page, profile, output, as_of=date(2026, 9, 24))
            first, first_state = output.read_bytes(), state.read_bytes()
            first_mtime = output.stat().st_mtime_ns
            # Changes to excluded fields must not advance the CV date.
            page['talks'].append({'title': 'A new invited talk'})
            page['grants'][0]['title_cn'] = '仅修改中文标题'
            build_cv(config, page, profile, output, as_of=date(2026, 10, 1))
            self.assertEqual(output.read_bytes(), first)
            self.assertEqual(state.read_bytes(), first_state)
            self.assertEqual(output.stat().st_mtime_ns, first_mtime)

            fresh = Path(directory) / 'fresh' / 'cv.pdf'
            fresh.parent.mkdir()
            shutil.copyfile(state, fresh.with_suffix('.meta.json'))
            # A missing PDF is regenerated using the committed content date.
            build_cv(config, page, profile, fresh, as_of=date(2026, 10, 2))
            self.assertEqual(fresh.read_bytes(), first)

            page['grants'][0]['amount'] = 'RMB 150K'
            build_cv(config, page, profile, output, as_of=date(2026, 10, 3))
            text = ' '.join(p.extract_text() for p in PdfReader(output).pages)
            self.assertIn('Updated 03 Oct 2026', text)
            self.assertIn('Funding: RMB 150K', text)
            self.assertNotEqual(output.read_bytes(), first)
            self.assertEqual(json.loads(state.read_text())['updated_on'], '2026-10-03')


if __name__ == '__main__':
    unittest.main()
