"""Assumes that this file is fun from the demo folder."""  # pylint: disable=all
from os import environ, getpid, walk
from subprocess import TimeoutExpired, Popen, run

environ["SDL_VIDEODRIVER"] = "dummy"
environ["SDL_AUDIODRIVER"] = "dummy"
environ["SDL_RENDER_DRIVER"] = "software"

for root, dirs, files in walk("."):
    for file in files:
        if file.endswith(".py") and file != "_run_all.py":
            print(f"Running {file}")
            proc = Popen(
                f"python {file}",
                shell=True,
            )
            try:
                proc.wait(timeout=5)
            except TimeoutExpired:
                pass
    break
