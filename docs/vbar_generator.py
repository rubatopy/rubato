# A script that generates the sidebar of a page and saves it to a file.
# Must be run from the docs
import json
import requests

dirs = requests.get("https://api.github.com/repos/rubatopy/docs.rubato.app/contents").json()
versions = requests.get("https://api.github.com/repos/rubatopy/rubato/tags").json()

with open("versions.json", "w") as f:
    f.write(json.dumps(versions))

with open("dirs.json", "w") as f:
    f.write(json.dumps(dirs))
