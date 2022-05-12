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
    """

    class Image:

        """
        A class that represents an image.
        """

        def __init__(self, url: str, title: str) -> None:
            self.url = url
            self.title = title
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
