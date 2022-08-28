"""
UI demo for rubato
"""
from rubato import *

init()
Game.show_fps = True

main = Scene()

txt = wrap(Text("Hello World!", Font(size=64), rot_offset=25), pos=Display.center + 100, rotation=45)
img = Image("../sprites/spaceship/spaceship.png")
rast = Raster(32, 32)
rast.draw_rect((0, 0), (32, 32), Color.red)

rast.set_alpha(30)

main.add(txt, wrap(img, pos=Display.center), wrap(rast, pos=Display.center - 100))

Game.draw = lambda: Draw.rect(Display.center, 100, 100, Color.red)


def handle_key():
    txt.get(Text).offset += Vector(10, 0)
    img.set_alpha(100)


Radio.listen(Events.KEYDOWN, handle_key)

begin()
