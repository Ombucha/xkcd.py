"""
MIT License

Copyright (c) 2025 Omkaar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


# pylint: skip-file

import unittest
import xkcd

from xkcd import stream_comics, get_comic_from_date, search_comics

class TestComic(unittest.TestCase):
    def test_latest_comic(self):
        comic = xkcd.Comic()
        self.assertIsInstance(comic.number, int)
        self.assertIsInstance(comic.title, str)
        self.assertTrue(comic.url.startswith("https://xkcd.com/"))
        self.assertIsInstance(comic.image, xkcd.Comic.Image)
        self.assertIsInstance(comic.image.url, str)
        self.assertIsInstance(comic.image.alt, str)
        self.assertIsInstance(comic.image.filename, str)
        self.assertIsInstance(comic.transcript, str)
        self.assertIsInstance(comic.date, object)
        self.assertIsInstance(comic.safe_title, str)
        self.assertIsInstance(comic.wiki_url, str)
        self.assertTrue(comic.wiki_url.startswith("https://explainxkcd.com/"))

    def test_specific_comic(self):
        comic = xkcd.Comic(353)
        self.assertEqual(comic.number, 353)
        self.assertIn("Python", comic.title)

    def test_random_comic(self):
        comic = xkcd.Comic(random=True)
        self.assertIsInstance(comic.number, int)

    def test_image_class(self):
        comic = xkcd.Comic(1)
        img = comic.image
        self.assertIsInstance(img, xkcd.Comic.Image)
        self.assertIsInstance(img.url, str)
        self.assertIsInstance(img.alt, str)
        self.assertIsInstance(img.filename, str)

    def test_invalid_random_and_number(self):
        with self.assertRaises(ValueError):
            xkcd.Comic(1, random=True)

    def test_invalid_number(self):
        # Try a very large number, should raise ValueError
        with self.assertRaises(Exception):
            xkcd.Comic(999999)

    def test_repr(self):
        comic = xkcd.Comic(1)
        rep = repr(comic)
        self.assertIn("Comic", rep)
        self.assertIn("number=1", rep)
        self.assertIn(comic.title, rep)

    def test_stream_comics(self):
        comics = list(stream_comics(1, 2))
        self.assertEqual(len(comics), 2)
        self.assertEqual(comics[0].number, 1)
        self.assertEqual(comics[1].number, 2)

    def test_get_comic_from_date(self):
        comic = xkcd.Comic(1)
        found_gen = get_comic_from_date(comic.date)
        found = None
        for c in found_gen:
            if c.number == 1:
                found = c
                break
        self.assertIsNotNone(found)
        self.assertEqual(found.number, 1)

if __name__ == "__main__":
    unittest.main()
