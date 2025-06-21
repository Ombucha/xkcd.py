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
from typing import Optional

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag


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
        :ivar title: The image's title (Alt Text).
        :ivar filename: The filename of the image.
        """

        def __init__(self, url: str, title: str) -> None:
            self.url = url
            self.title = title
            self.filename = split(urlparse(self.url).path)[1]

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

        def __init__(self, _number: int, _text: str) -> None:
            self.number = _number
            self.text = _text

        def __int__(self) -> int:
            return self.number

        def __str__(self) -> str:
            return self.text

        def __repr__(self) -> str:
            return f"<Reference number={self.number!r} text={self.text!r}>"

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
                    raise ValueError("You have chosen a comic after the latest one.")
                self.number = number

        page = Request(f"{WHAT_IF_BASE_URL}{self.number}")
        with urlopen(page) as result:
            soup = BeautifulSoup(result.read(), "html.parser")

        self.entry = []
        for tag in soup.find_all():
            identifier = not "id" in tag.attrs.keys()
            if tag.parent.name == "article" and identifier:
                children = list(tag.children)
                if tag.name == "p" and len(children) > 0:
                    for child in children:
                        if isinstance(child, NavigableString):
                            self.entry.append(str(child))
                        elif isinstance(child, Tag) and child.name == "a":
                            self.entry.append(self.Hyperlink(child.text, child.attrs["href"]))
                        elif isinstance(child, Tag) and child.name == "span":
                            _children = list(child.children)
                            self.entry.append(self.Reference(int(_children[0].text[1:-1]), _children[1].text))
                elif tag.name == "img":
                    self.entry.append(self.Image(tag.attrs["src"], tag.attrs["title"]))

        self.title = soup.find("h2", {"id": "title"}).a.text
        self.question = soup.find("p", {"id": "question"}).text
        self.author = soup.find("p", {"id": "attribute"}).text[1:]
        self.url = f"{WHAT_IF_BASE_URL}{self.number}"
