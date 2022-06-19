"""
UI demo for rubato
"""
from rubato import *

init()
Game.show_fps = True

main = Scene()

text = GameObject(pos=Display.center).add(Text(text="Hello World!", ))

main.add(text)

begin()
