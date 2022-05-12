from __future__ import annotations

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
    """

    class Image:

        """
        A class that represents an image.
        """

        def __init__(self, url: str, title: str) -> None:
            self.url = url
            self.title = title
            self.filename = split(urlparse(self.url).path)[1]

    class Hyperlink:

        """
        A class that represents hyperlinked text.
        """

        def __init__(self, text: str, url: str) -> None:
            self.text = text
            self.url = url

    class Reference:

        """
        A class that represents a reference.
        """

        def __init__(self, number: int, text: str) -> None:
            self.number = number
            self.text = text

    def __init__(self, number: Optional[int] = None, *, random = False) -> None:

        if random and number:
            raise ValueError("If 'random' is 'True', 'number' must not be specified.")

        page = Request(WHAT_IF_BASE_URL)
        with urlopen(page) as result:
            soup = BeautifulSoup(result.read(), "html.parser")

        url = [element["href"] for element in soup.find_all("a", href = True)][6]
        latest = int(urlparse(url).path[1:]) + 1
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
        self.author = soup.find("p", {"id": "attribute"}).text
        self.url = f"{WHAT_IF_BASE_URL}{self.number}"
