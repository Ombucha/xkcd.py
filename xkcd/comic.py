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


from datetime import date, datetime
from html import unescape
from os.path import split
from random import randint
from urllib.parse import urlparse
from typing import Optional, Generator, Union
from subprocess import run
from platform import system
from concurrent.futures import ThreadPoolExecutor, as_completed

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
    :ivar image: The comic's image.
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
        :ivar title: The image's Alt text.
        :ivar filename: The filename of the image.
        """

        def __init__(self, url: str, alt: str) -> None:
            self.url = url
            self.alt = alt
            self.filename = split(urlparse(self.url).path)[1]

        def __repr__(self) -> str:
            return f"<Image url={self.url!r} alt={self.alt!r}>"

    def __init__(self, number: Optional[int] = None, *, random: Optional[bool] = False) -> None:

        if random and number:
            raise ValueError("If 'random' is 'True', 'number' must not be specified.")

        try:
            if random:
                response = get(f"{XKCD_BASE_URL}info.0.json").json()
                latest = int(response["num"])
                self.number = randint(1, latest)
                response = get(f"{XKCD_BASE_URL}{self.number}/info.0.json").json()
            else:
                request_url = f"{XKCD_BASE_URL}info.0.json" if number is None else f"{XKCD_BASE_URL}{number}/info.0.json"
                response = get(request_url).json()
                self.number = int(response["num"])
        except Exception as e:
            raise RuntimeError(f"Failed to fetch comic data: {e}") from e

        self.date = date(int(response["year"]), int(response["month"]), int(response["day"]))
        self.safe_title = response["safe_title"]
        self.title = response["title"]
        self.transcript = unescape(response["transcript"])
        self.image = self.Image(response["img"], response["alt"])
        self.wiki_url = f"{XKCD_WIKI_BASE_URL}{self.number}"
        self.url = f"{XKCD_BASE_URL}{self.number}"

    def __repr__(self) -> str:
        return f"<Comic number={self.number} title={self.title!r} date={self.date}>"

    def __str__(self) -> str:
        return self.transcript

    def __int__(self) -> int:
        return self.number

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Comic):
            return NotImplemented
        return self.number == other.number

    def download(self, *, filename: Optional[str] = None, path: Optional[str] = None) -> str:
        """
        Downloads the comic image.

        :param filename: The name of the file to save the image as. If not specified, uses the image's filename.
        :param path: The path to save the image to. If not specified, saves in the current directory.
        :return: The full path of the saved image.
        """
        if not filename:
            filename = self.image.filename
        if path:
            filename = f"{path}/{filename}"
        else:
            filename = f"./{filename}"

        with open(filename, "wb") as file:
            file.write(get(self.image.url).content)

        return filename

    def show(self, *, filename: Optional[str] = None, path: Optional[str] = None) -> None:
        """
        Downloads the comic and opens the image in the default image viewer.

        :param filename: The name of the file to save the image as. If not specified, uses the image's filename.
        :param path: The path to save the image to. If not specified, saves in the current directory.
        """
        run(['open' if system() == 'Darwin' else 'xdg-open' if system() == 'Linux' else 'start', self.download(filename=filename, path=path)], shell=True, check=False)

def stream_comics(start: int = 1, end: Optional[int] = None) -> Generator[Comic, None, None]:
    """
    Streams comics from the specified start to end comic number.

    :param start: The starting comic number.
    :param end: The ending comic number. If not specified, streams until the latest comic.
    """
    response = get(f"{XKCD_BASE_URL}info.0.json").json()
    latest = int(response["num"])
    if start < 1 or (end is not None and end < start) or (end is not None and end > latest):
        raise ValueError(f"Invalid range: start={start}, end={end}")

    if end is None:
        end = latest
    for number in range(start, end + 1):
        yield Comic(number)

def get_comic_from_date(release_date: Union[datetime, date], *, max_workers: Optional[int] = 32) -> Optional[Generator[Comic, None, None]]:
    """
    Gets a comic by its date if it exists.

    .. note::

        The comics returned may not be in chronological order due to multithreading.

    :param release_date: The date of the comic to fetch.
    :type release_date: :class:`datetime.datetime` or :class:`datetime.date`
    :param max_workers: The maximum number of threads to use for fetching comics.
    :type max_workers: Optional[:class:`int`]
    """
    if isinstance(release_date, datetime):
        release_date = release_date.date()
    latest = get(f"{XKCD_BASE_URL}info.0.json").json()["num"]
    maximum = None

    def try_comic(number: int):
        nonlocal maximum

        if maximum and number > maximum:
            return None

        try:
            comic = Comic(number)
            if comic.date > release_date:
                maximum = number - 1
            if comic.date == release_date:
                return comic
        except RuntimeError:
            pass

        return None

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(try_comic, n) for n in range(1, latest + 1)]
        for future in as_completed(futures):
            result = future.result()
            if result:
                yield result

def search_comics(query: str, *, max_workers: Optional[int] = 32) -> Generator[Comic, None, None]:
    """
    Searches for comics by title or alt text.

    .. note::

        The comics returned may not be in chronological order due to multithreading.

    :param query: The search query.
    :type query: :class:`str`
    :param max_workers: The maximum number of threads to use for fetching comics.
    :type max_workers: Optional[:class:`int`]
    """
    if not query:
        raise ValueError("Query must not be empty.")

    def try_comic(number: int):
        try:
            comic = Comic(number)
            if query.lower() in "".join([str(comic.number), str(comic.date), comic.title, comic.safe_title, comic.image.url, comic.image.alt, comic.transcript, comic.url, comic.wiki_url]).lower():
                return comic
        except RuntimeError:
            pass
        return None

    latest = get(f"{XKCD_BASE_URL}info.0.json").json()["num"]
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(try_comic, n) for n in range(1, latest + 1)]
        for future in as_completed(futures):
            result = future.result()
            if result:
                yield result
