"""A simple script to generate a sitemap from your file system."""
from pathlib import PurePath
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString, Document
from os import walk, environ

url = environ.get("URL", "https://rubato.app/")
root = ET.Element("urlset", {"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"})

ignored_dirs = ["temp"]
ignored_files = ["404.html"]

for path, dirs, files in walk("."):
    if "robots.txt" in files:
        ignored_dirs.append(PurePath(path))
        continue
    p = PurePath(path)
    if any(p.is_relative_to(i) for i in ignored_dirs):
        continue
    loc = url + (p.as_posix() + "/" if p.as_posix() != "." else "")
    for file in files:
        if file.endswith(".html") and file not in ignored_files:
            item = ET.SubElement(root, "url")
            if file != "index.html":
                ET.SubElement(item, "loc").text = loc + file
            else:
                ET.SubElement(item, "loc").text = loc

with open("sitemap.xml", "w", encoding="utf-8") as f:
    parsed: Document = parseString(ET.tostring(root, encoding="unicode"))
    f.write(parsed.toprettyxml(indent="    "))
