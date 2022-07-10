"""Camera demo"""
from rubato import *

init(res=Vector(500, 500))

main_scene = Scene(name="main")

player = GameObject(pos=Display.center)
player.add(Rectangle(width=50, height=50, color=Color.red))


def mouse_down(_):
    pos = Game.camera.i_transform(Input.get_mouse_pos())
    dot = GameObject(pos=pos).add(Circle(radius=5, color=Color.blue))
    main_scene.add(dot)
    main_scene.camera.pos = pos
Radio.listen(Events.MOUSEDOWN, mouse_down)


main_scene.add(player)

begin()
