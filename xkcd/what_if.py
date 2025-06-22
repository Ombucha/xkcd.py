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


from os.path import split
from random import randint
from urllib.parse import urlparse
from urllib.request import urlopen, Request
from typing import Optional, Generator, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from bs4 import BeautifulSoup
from bs4.element import Tag


WHAT_IF_BASE_URL = "https://what-if.xkcd.com/"


class WhatIfArticle:

    """
    A class that represents a What If article.

    :param number: The article's number.
    :type number: Optional[:class:`int`]
    :param random: Whether to choose a random article, or not.
    :type random: Optional[:class:`bool`]

    .. note::

        If ``random`` is ``True``, ``number`` must not be specified.

    :ivar entry: The article entry. It is a list of :class:`str`, :class:`Image`, :class:`Hyperlink` and :class:`Reference`.
    :ivar number: The number of the article.
    :ivar title: The article's title.
    :ivar question: The question of the article.
    :ivar author: The author of the article.
    :ivar url: The article's URL.
    """

    class Image:

        """
        A class that represents an image.

        :ivar url: The image's URL.
        :ivar alt: The image's Alt text.
        :ivar filename: The filename of the image.
        """

        def __init__(self, url: str, alt: str) -> None:
            self.url = url
            self.alt = alt
            self.filename = split(urlparse(self.url).path)[1]

        def __repr__(self):
            return f"<Image url={self.url!r} alt={self.alt!r}>"

    class Hyperlink:

        """
        A class that represents hyperlinked text.

        :ivar url: The URL that hyperlink leads to.
        :ivar text: The text shown on the hyperlink.
        """

        def __init__(self, text: str, url: str) -> None:
            self.text = text
            self.url = url

        def __str__(self) -> str:
            return self.text

        def __repr__(self) -> str:
            return f"<Hyperlink text={self.text!r} url={self.url!r}>"

    class Reference:

        """
        A class that represents a reference.

        :ivar number: The reference's number.
        :ivar text: The text shown upon hovering over the reference.
        """

        def __init__(self, number: int, text: List[str]) -> None:
            self.number = number
            self.text = text

        def __int__(self) -> int:
            return self.number

        def __str__(self) -> str:
            return "".join([str(item) for item in self.text])

        def __repr__(self) -> str:
            return f"<Reference number={self.number!r} text={str(self)!r}>"

    def __init__(self, number: Optional[int] = None, *, random = False) -> None:

        if random and number:
            raise ValueError("If 'random' is 'True', 'number' must not be specified.")

        page = Request(f"{WHAT_IF_BASE_URL}archive")
        with urlopen(page) as result:
            soup = BeautifulSoup(result.read(), "html.parser")

        entries = soup.find_all("div", {"class": "archive-entry"})
        latest = int(entries[-1].a.attrs["href"].split("/")[-1])
        if random:
            self.number = randint(1, latest)
        else:
            if number is None:
                self.number = latest
            else:
                if number > latest:
                    raise ValueError("You have chosen an article after the latest one.")
                self.number = number

        page = Request(f"{WHAT_IF_BASE_URL}{self.number}")
        with urlopen(page) as result:
            soup = BeautifulSoup(result.read(), "html.parser")

        self.entry = []
        for item in soup.find("article", {"id": "entry"}).children:
            if isinstance(item, Tag) and "id" not in item.attrs:
                if item.name == "img":
                    self.entry.append(self.Image(item.attrs["src"], item.attrs.get("alt", "")))
                if item.name in ["p", "div"]:
                    for tag in item.children:
                        if tag.name == "a":
                            self.entry.append(self.Hyperlink(tag.text, tag.attrs["href"]))
                        elif tag.name == "span" and tag.attrs.get("class")[0] == "ref":
                            ref_number = int(tag.find("span", {"class": "refnum"}).text[1:-1])
                            ref_text_tag = tag.find("span", {"class": "refbody"})
                            ref_text = []
                            for child in ref_text_tag.children:
                                if isinstance(child, Tag) and child.name == "a":
                                    ref_text.append(self.Hyperlink(child.text, child.attrs["href"]))
                                else:
                                    if len(ref_text) > 0 and isinstance(ref_text[-1], str):
                                        ref_text[-1] += child.text
                                    else:
                                        ref_text.append(child.text)
                            self.entry.append(self.Reference(ref_number, ref_text))
                        else:
                            if len(self.entry) > 0 and isinstance(self.entry[-1], str):
                                self.entry[-1] += tag.text
                            else:
                                self.entry.append(tag.text)

        self.title = soup.find("h2", {"id": "title"}).a.text.strip()
        self.question = soup.find("p", {"id": "question"}).text.strip()

        try:
            self.author = soup.find("p", {"id": "attribute"}).text.strip("—").strip()
        except AttributeError:
            self.author = None

        self.url = f"{WHAT_IF_BASE_URL}{self.number}"

    def __repr__(self) -> str:
        return f"<WhatIfArticle number={self.number} title={self.title!r}>"

    def __str__(self) -> str:
        paragraphs = []
        current_paragraph = []
        for item in self.entry:
            if isinstance(item, str):
                current_paragraph.append(item.strip())
            elif isinstance(item, WhatIfArticle.Image):
                if current_paragraph:
                    paragraphs.append(" ".join(current_paragraph).strip())
                    current_paragraph = []
            elif isinstance(item, WhatIfArticle.Hyperlink):
                current_paragraph.append(item.text)
        if current_paragraph:
            paragraphs.append(" ".join(current_paragraph).strip())
        return "\n\n".join(p for p in paragraphs if p)

    def __int__(self) -> int:
        return self.number

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WhatIfArticle):
            return NotImplemented
        return self.number == other.number

def stream_articles(start: Optional[int] = 1, end: Optional[int] = None) -> Generator[WhatIfArticle, None, None]:
    """
    A generator that yields What If articles.

    :param start: The starting article number.
    :type start: Optional[:class:`int`]
    :param end: The ending article number. If None, it will stream until the latest article.
    :type end: Optional[:class:`int`]
    """
    if end is None:
        end = WhatIfArticle().number

    if start < 1 or end < start:
        raise ValueError("Invalid range for articles.")

    for number in range(start, end + 1):
        yield WhatIfArticle(number)

def search_articles(query: str, *, max_workers: Optional[int] = 32) -> Generator[WhatIfArticle, None, None]:
    """
    Searches for articles by title or question.

    .. note::

        The articles returned may not be in chronological order due to multithreading.

    :param query: The search query.
    :type query: :class:`str`
    :param max_workers: The maximum number of threads to use for searching.
    :type max_workers: Optional[:class:`int`]
    """
    if not query:
        raise ValueError("Query must not be empty.")

    def try_article(number: int):
        try:
            article = WhatIfArticle(number)
            data = "".join([str(article.number), article.title, article.question, article.author if article.author else "", article.url]).lower()

            for item in article.entry:
                if isinstance(item, WhatIfArticle.Image):
                    data += item.alt.lower() + item.url.lower()
                elif isinstance(item, WhatIfArticle.Hyperlink):
                    data += item.text.lower() + item.url.lower()
                elif isinstance(item, WhatIfArticle.Reference):
                    data += str(item).lower() + str(item.number).lower()
                else:
                    data += item.lower()

            if query.lower() in data:
                return article
        except RuntimeError:
            pass
        return None

    latest = WhatIfArticle().number
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(try_article, n) for n in range(1, latest + 1)]
        for future in as_completed(futures):
            result = future.result()
            if result:
                yield result
