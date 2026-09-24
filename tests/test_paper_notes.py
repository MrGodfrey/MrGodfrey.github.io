import html
import tempfile
import unittest
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from generate import build_blog_reference_index, build_page, render_markdown


class PaperNotesTests(unittest.TestCase):
    def test_tex_survives_markdown(self):
        tex = r"a_i * b_j < c_k \quad \begin{pmatrix}1 & 2 \\ 3 & 4\end{pmatrix}"
        for source in (f"${tex}$", rf"\({tex}\)", f"$$\n{tex}\n$$", "\\[\n" + tex + "\n\\]"):
            with self.subTest(source=source):
                rendered = render_markdown(source, math_enabled=True)
                self.assertIn('class="arithmatex"', rendered)
                self.assertIn(tex, html.unescape(rendered))
                self.assertNotIn("<em>", rendered)

    def test_numbered_equations_and_code(self):
        rendered = render_markdown(
            r"\begin{equation}a=b\label{eq:test}\end{equation}" + "\n\n"
            + r"See $\eqref{eq:test}$." + "\n\n"
            + "`$a_i$`\n\n```tex\n$$x_1$$\n```",
            math_enabled=True,
        )
        self.assertEqual(rendered.count('class="arithmatex"'), 2)
        self.assertIn(r"\label{eq:test}", rendered)
        self.assertIn("<code>$a_i$</code>", rendered)
        self.assertIn('$$x_1$$', rendered)

    def test_math_is_opt_in(self):
        self.assertNotIn('class="arithmatex"', render_markdown("$a_i$"))

    def test_blog_link_follows_paper_links_and_stays_in_same_tab(self):
        env = Environment(loader=FileSystemLoader("templates"))
        index = build_blog_reference_index([
            {"title": "Notes", "slug": "notes", "url": "/blogs/notes/"}
        ])
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "paper.md"
            source.write_text(
                '---\narticles:\n  - title: Test paper\n    authors: "Q. Lü, **Y. Wang**"\n'
                '    blog: notes\n    links:\n      - label: ArXiv\n        url: https://arxiv.org/\n---\n',
                encoding="utf-8",
            )
            output = Path(directory) / "index.html"
            config = {"name_en": "Author", "cv": {"url": "/cv.pdf", "label": "CV"}, "nav": []}
            build_page(str(source), config, env, output_path=str(output), blog_reference_index=index)
            rendered = output.read_text(encoding="utf-8")
            self.assertLess(rendered.index("[ArXiv]"), rendered.index("[Blog]"))
            self.assertIn('id="paper-notes"', rendered)
            self.assertIn('href="/blogs/notes/">', rendered)


if __name__ == "__main__":
    unittest.main()
