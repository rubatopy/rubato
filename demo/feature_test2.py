from rubato import *

init(name="testING", res=Vector(500, 500), window_size=Vector(500, 500), target_fps=30)

main = Scene()

player = GameObject(pos=Display.center)

image = Image(rel_path="sprites/dino/blue/crouch.png", anti_aliasing=False)
player.add(image)

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


saved = []


def main_update():
    # All the mouse presses right now
    get_input()
    if Input.mouse_pressed():
        rect = GameObject(pos=Input.get_mouse_pos())
        rect.add(Rectangle(width=30, height=30))
        saved.append(rect)
        main.add(rect)


def main_draw():
    for rect_go in saved:
        rect = rect_go.get(Rectangle)
        Draw.rect(rect_go.pos + rect.offset, rect.width, rect.height, angle=rect.rotation_offset)


# handle the "shift+w" keypress

main.update = main_update
main.draw = main_draw


# Radio system

def mouse_update(params):
    pass
    # print(params)
    if params["mouse_button"] == "BUTTON_LEFT":
        print("left")


Radio.listen(Events.MOUSEDOWN, mouse_update)

# While loop
begin()
