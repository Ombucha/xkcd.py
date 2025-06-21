# pylint: skip-file

from pathlib import Path

from setuptools import setup

HERE = Path(__file__).resolve().parent
README = (HERE / "README.rst").read_text()

setup(
    name = "xkcd.py",
    version = "1.2.0",
    description = "A basic API wrapper for xkcd.",
    long_description = README,
    long_description_content_type = "text/x-rst",
    url = "https://github.com/Ombucha/xkcd.py",
    author = "Omkaar",
    author_email = "omkaar.nerurkar@gmail.com",
    license = "MIT",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    python_requires='>= 3.8.0',
    packages = ["xkcd"],
    include_package_data = True,
    install_requires = ["beautifulsoup4", "requests"]
)
