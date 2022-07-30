# A script that caches the sidebar of a page and saves it to a file.
import requests

r = requests.get("https://test.rubato.app/version_iframe_generator.html")

with open("version_iframe.html", "w") as f:
    f.write(r.text)
    