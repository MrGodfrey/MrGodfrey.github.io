import tempfile
import unittest
from pathlib import Path
from urllib.parse import urlsplit

from PIL import Image

from generate_images import prepare_cover


class CoverImageTests(unittest.TestCase):
    def test_responsive_sizes_preserve_source_ratio_and_are_stable(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            source = root / 'cover.png'
            Image.new('RGB', (1800, 1000), '#eef4ff').save(source)
            original = source.read_bytes()
            cover = {'image': '/cover.png', 'alt': 'Test cover'}
            result = prepare_cover(cover, root / 'post.md', root)
            outputs = sorted((root / 'assets/generated/covers').glob('*.webp'))
            self.assertEqual(len(outputs), 3)
            sizes = set()
            for output in outputs:
                with Image.open(output) as image:
                    sizes.add(image.size)
            self.assertEqual(sizes, {(480, 267), (960, 533), (1600, 889)})
            self.assertEqual(source.read_bytes(), original)
            self.assertEqual(cover['image'], '/cover.png')
            self.assertEqual(result['alt'], 'Test cover')
            mtimes = {p: p.stat().st_mtime_ns for p in outputs}
            self.assertEqual(prepare_cover(cover, root / 'post.md', root), result)
            self.assertEqual({p: p.stat().st_mtime_ns for p in outputs}, mtimes)

            Image.new('RGB', (1800, 1000), '#f0a010').save(source)
            changed = prepare_cover(cover, root / 'post.md', root)
            self.assertEqual(urlsplit(changed['image']).path, urlsplit(result['image']).path)
            self.assertNotEqual(changed['image'], result['image'])
            self.assertEqual(len(list(outputs[0].parent.glob('*.webp'))), 3)

            Image.new('RGBA', (200, 100), (30, 60, 90, 100)).save(source)
            small = prepare_cover(cover, root / 'post.md', root)
            remaining = list(outputs[0].parent.glob('*.webp'))
            self.assertEqual(len(remaining), 1)
            with Image.open(remaining[0]) as image:
                self.assertEqual(image.size, (200, 100))
                self.assertIn('A', image.getbands())
            self.assertEqual(small['width'], 200)

    def test_remote_images_are_unchanged_and_missing_local_covers_fail_clearly(self):
        cover = {'image': 'https://example.com/cover.png'}
        self.assertEqual(prepare_cover(cover, 'post.md'), cover)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            with self.assertRaisesRegex(ValueError, 'does not exist'):
                prepare_cover({'image': '/missing.png'}, root / 'post.md', root)


if __name__ == '__main__':
    unittest.main()
