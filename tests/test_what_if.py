"""MIT License

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


import unittest
import xkcd

class TestWhatIfArticle(unittest.TestCase):
    def test_latest_article(self):
        article = xkcd.WhatIfArticle()
        self.assertIsInstance(article.number, int)
        self.assertIsInstance(article.title, str)
        self.assertIsInstance(article.question, str)
        self.assertIsInstance(article.author, str)
        self.assertTrue(article.url.startswith("https://what-if.xkcd.com/"))
        self.assertIsInstance(article.entry, list)
        # Check entry types (str, Image, Hyperlink, Reference)
        for item in article.entry:
            self.assertTrue(
                isinstance(item, (str, xkcd.WhatIfArticle.Image, xkcd.WhatIfArticle.Hyperlink, xkcd.WhatIfArticle.Reference))
            )

    def test_random_article(self):
        article = xkcd.WhatIfArticle(random=True)
        self.assertIsInstance(article.number, int)

    def test_specific_article(self):
        article = xkcd.WhatIfArticle(1)
        self.assertEqual(article.number, 1)
        self.assertIsInstance(article.title, str)

    def test_image_class(self):
        article = xkcd.WhatIfArticle(1)
        images = [e for e in article.entry if isinstance(e, xkcd.WhatIfArticle.Image)]
        for img in images:
            self.assertIsInstance(img.url, str)
            self.assertIsInstance(img.title, str)
            self.assertIsInstance(img.filename, str)

    def test_hyperlink_class(self):
        article = xkcd.WhatIfArticle(1)
        links = [e for e in article.entry if isinstance(e, xkcd.WhatIfArticle.Hyperlink)]
        for link in links:
            self.assertIsInstance(link.text, str)
            self.assertIsInstance(link.url, str)

    def test_reference_class(self):
        article = xkcd.WhatIfArticle(1)
        refs = [e for e in article.entry if isinstance(e, xkcd.WhatIfArticle.Reference)]
        for ref in refs:
            self.assertIsInstance(ref.number, int)
            self.assertIsInstance(ref.text, str)

    def test_invalid_random_and_number(self):
        with self.assertRaises(ValueError):
            xkcd.WhatIfArticle(1, random=True)

    def test_invalid_number(self):
        # Try a very large number, should raise ValueError
        with self.assertRaises(ValueError):
            xkcd.WhatIfArticle(999999)

if __name__ == "__main__":
    unittest.main()
