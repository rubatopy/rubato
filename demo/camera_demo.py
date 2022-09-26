"""Camera demo"""
from rubato import *

init(res=Vector(500, 500))

main = Scene(name="main")

player = GameObject(pos=Display.center)
player.add(Rectangle(width=50, height=50, color=Color.red))


def update():
    if Input.key_pressed("="):
        main.camera.zoom += 0.05
    if Input.key_pressed("-"):
        main.camera.zoom -= 0.05


def mouse_down(_):
    main.camera.pos += Vector(5, -10)
    main.add(GameObject(pos=world_mouse()).add(Circle(radius=5, color=Color.blue)))
    print(main.camera.zoom)


Radio.listen(Events.MOUSEDOWN, mouse_down)

main.add(player)
main.update = update

begin()
