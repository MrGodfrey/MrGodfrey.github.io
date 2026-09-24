import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from generate import (
    build_blog_reference_index, build_page, load_blog_posts, load_config,
    read_markdown_page, sorted_talk_events,
)


class HomepageTests(unittest.TestCase):
    def test_talk_dates_are_sorted_without_changing_full_records(self):
        events = [
            {'date': 'Dec. 10, 2025'}, {'date': 'Aug. 22, 2026'},
            {'date': '2026-05-17'}, {'date': 'July 25, 2025'},
        ]
        original = deepcopy(events)
        self.assertEqual(sorted_talk_events(events), [events[1], events[2], events[0], events[3]])
        self.assertEqual(events, original)
        with self.assertRaises(ValueError):
            sorted_talk_events([{'date': 'invalid'}])

    def test_homepage_limits_each_talk_topic_and_hides_grant_details(self):
        page, _ = read_markdown_page('content/index.md')
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'index.html'
            build_page(
                'content/index.md', load_config(),
                Environment(loader=FileSystemLoader('templates')),
                output_path=str(output),
                blog_reference_index=build_blog_reference_index(load_blog_posts()),
            )
            rendered = output.read_text(encoding='utf-8')
            for topic in page['talks']:
                for i, event in enumerate(sorted_talk_events(topic['events'])):
                    if i < 3:
                        self.assertIn(event['venue'], rendered)
                    else:
                        self.assertNotIn(event['venue'], rendered)
            for grant in page['grants']:
                self.assertIn(grant['title_en'], rendered)
                self.assertNotIn(grant['title_cn'], rendered)
                self.assertNotIn(grant['amount'], rendered)
            self.assertRegex(
                rendered,
                r'<h4[^>]*>\s*<a href="/blogs/null-controllability-analytic-noise/"[^>]*>'
                r'Null Controllability of a Stochastic Parabolic Equation',
            )


if __name__ == '__main__':
    unittest.main()
