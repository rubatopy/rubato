"""Camera demo"""
from rubato import *

init(res=Vector(500, 500))

main_scene = Scene(name="main")

player = GameObject(pos=Display.center)
player.add(Rectangle(width=50, height=50, color=Color.red))

# Radio.listen("")
def update():
    if Input.mouse_pressed():
        pos = main_scene.camera.transform(Input.get_mouse_pos())
        print(pos)
        dot = GameObject(pos=pos).add(Circle(radius=5, color=Color.blue))
        main_scene.add(dot)
        main_scene.camera.set(pos)
        # main_scene.camera

main_scene.add(player)
main_scene.update = update

begin()
