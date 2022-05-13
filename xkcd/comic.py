from datetime import datetime
from html import unescape
from os.path import split
from random import randint
from urllib.parse import urlparse
from typing import Optional

from requests import get


XKCD_BASE_URL = "https://xkcd.com/"
XKCD_WIKI_BASE_URL = "https://explainxkcd.com/"


class Comic:

    """
    A class that represents a comic.

    :param number: The comic's number.
    :type number: Optional[:class:`int`]
    :param random: Whether to choose a random comic, or not.
    :type random: Optional[:class:`bool`]

    .. note::

        If ``random`` is ``True``, ``number`` must not be specified.

    :ivar date: The comic's date.
    :ivar image: The URL of the comic's image.
    :ivar number: The number of the comic.
    :ivar title: The comic's title.
    :ivar safe_title: A safe form of the comic's title.
    :ivar transcript: The trascript of the comic.
    :ivar wiki_url: The URL of the comic's wiki.
    :ivar url: The comic's URL.
    """

    class Image:

        """
        A class that represents an image.

        :ivar url: The image's URL.
        :ivar title: The image's title (Alt Text).
        :ivar filename: The filename of the image.
        """

        def __init__(self, _url: str, _title: str) -> None:
            self.url = _url
            self.title = _title
            self.filename = split(urlparse(self.url).path)[1]

    def __init__(self, number: Optional[int] = None, *, random: Optional[bool] = False) -> None:

        if random and number is None:
            raise ValueError("If 'random' is 'True', 'number' must not be specified.")

        if random:
            response = get(f"{XKCD_BASE_URL}info.0.json").json()
            latest = int(response["num"])
            self.number = randint(1, latest)
            response = get(f"{XKCD_BASE_URL}{self.number}/info.0.json").json()
        else:
            request_url = f"{XKCD_BASE_URL}info.0.json" if number is None else f"{XKCD_BASE_URL}{number}/info.0.json"
            response = get(request_url).json()
            self.number = int(response["num"])
        self.date = datetime(int(response["year"]), int(response["month"]), int(response["day"]))
        self.safe_title = response["safe_title"]
        self.title = response["title"]
        self.transcript = unescape(response["transcript"])
        self.image = self.Image(response["url"], response["alt"])

        self.wiki_url = f"{XKCD_WIKI_BASE_URL}{self.number}"
        self.url = f"{XKCD_BASE_URL}{self.number}"
