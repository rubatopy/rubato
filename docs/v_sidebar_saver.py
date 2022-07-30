# A script that caches the sidebar of a page and saves it to a file.
# Must be run from the docs
import requests

r = requests.get("https://test.rubato.app/version_iframe_generator.html")

import urllib.request
with urllib.request.urlopen('http://python.org/') as response:
    html = response.read()

with open("version_iframe.html", "w", encoding="utf-8") as f:
    f.write(html.decode("utf-8"))
