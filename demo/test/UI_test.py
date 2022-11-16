"""
UI demo for rubato
"""
from rubato import *

init()
Game.show_fps = True

main = Scene()

txt = wrap(Text("Hello World!", Font(size=64), rot_offset=25), pos=Display.center + 100, rotation=45)
img = Image("../sprites/spaceship/spaceship.png")

img.set_alpha(30)

main.add(wrap(img, pos=Display.center))


def handle_key():
    img.set_alpha(100)


Radio.listen(Events.KEYDOWN, handle_key)

begin()
