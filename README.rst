.. image:: https://raw.githubusercontent.com/Ombucha/xkcd.py/main/banner.png

.. image:: https://img.shields.io/pypi/v/xkcd.py
    :target: https://pypi.python.org/pypi/xkcd.py
    :alt: PyPI version
.. image:: https://static.pepy.tech/personalized-badge/xkcd.py?period=total&left_text=downloads&left_color=grey&right_color=red
    :target: https://pypi.python.org/pypi/xkcd.py
    :alt: PyPI downloads
.. image:: https://sloc.xyz/github/Ombucha/xkcd.py?lower=True
    :target: https://github.com/Ombucha/xkcd.py/graphs/contributors
    :alt: Lines of code
.. image:: https://img.shields.io/github/repo-size/Ombucha/xkcd.py?color=yellow
    :target: https://github.com/Ombucha/xkcd.py
    :alt: Repository size

A Python wrapper for the XKCD webcomic API. Because sometimes you need comics in your code.

Features
--------

- Get XKCD comics by number, or just ask for the latest and hope it's not about Python.
- Search comics by title or transcript (for when you remember the joke but not the number).
- Pythonic interface, because we like snakes.
- Type hints, so your editor can feel smart.
- Error handling, because the internet is a scary place.
- Documentation and examples, so you don't have to read the source (unless you want to).

Requirements
------------

- **Python 3.8 or higher** (older Pythons are like old comics: fun, but not supported)
- `requests <https://pypi.python.org/pypi/requests>`_ (for talking to the internet)

Installation
------------

To install the latest stable version:

.. code-block:: sh

    # Unix / macOS
    python3 -m pip install "xkcd.py"

    # Windows
    py -m pip install "xkcd.py"

To install the development version (for people who like living on the edge):

.. code-block:: sh

    git clone https://github.com/Ombucha/xkcd.py
    cd xkcd.py
    python3 -m pip install -e .

Getting Started
---------------

1. **Install the package** (see above).
2. **Start coding!** (see below)

Quick Example
-------------

.. code-block:: python

    import xkcd

    # Get the latest comic (fingers crossed it's not about regular expressions)
    comic = xkcd.get_latest()
    print(f"{comic.num}: {comic.title} - {comic.img}")

    # Get a specific comic by number (353 is a classic)
    comic = xkcd.get_comic(353)
    print(f"{comic.num}: {comic.title} - {comic.alt}")

    # Search for comics about Python (the language, not the snake)
    results = xkcd.search("Python")
    for comic in results:
        print(f"{comic.num}: {comic.title}")

Links
-----

- `xkcd <https://xkcd.com/>`_ (the source of all stick-figure wisdom)
- `Official API <https://xkcd.com/json.html>`_ (for robots)
- `Documentation <https://xkcd.readthedocs.io/>`_ (for humans)

Contributing
------------

Pull requests, issues, and stick-figure diagrams welcome! See the `contributing guide <https://github.com/Ombucha/xkcd.py/blob/main/CONTRIBUTING.md>`_.

License
-------

MIT License. Because sharing is caring. See the `LICENSE <https://github.com/Ombucha/xkcd.py/blob/main/LICENSE>`_ file for details.
