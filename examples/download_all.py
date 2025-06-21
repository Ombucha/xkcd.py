# pylint: skip-file

import xkcd

print("Starting to download all comics...")

for comic in xkcd.stream():
    print(f"Downloading {comic.number} - {comic.title}...")
    comic.download(filename=f"xkcd-{comic.number}.jpg")
    print(f"Downloaded {comic.number} - {comic.title}.")

print("All comics downloaded successfully.")