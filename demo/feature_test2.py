from rubato import *


init(name="testING", res=Vector(500, 500), window_size=Vector(500, 500), target_fps=30)

main = Scene()
Debug = True

player = GameObject(pos=Display.center)

image = Image(rel_path="sprites/dino/blue/crouch.png", anti_aliasing=False)
player.add(image)
image.resize(Vector(600, 100))

main.add(player)

speed = 3
def get_input():
    # All the keys being pressed right now
    if Input.key_pressed("a"):
        player.pos.x -= speed

    if Input.key_pressed("w"):
        player.pos.y -= speed

    if Input.key_pressed("s"):
        player.pos.y += speed

    if Input.key_pressed("d"):
        player.pos.x += speed
def main_update():
    # All the mouse presses right now
    get_input()
    if Input.mouse_pressed():
        print("hi")
        rect = GameObject(pos=Input.get_mouse_pos())
        rect.add(Rectangle())
        main.add(rect)


# handle the "shift+w" keypress

main.update = main_update

# While loop
begin()
