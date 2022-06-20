"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb
import sys, os

sys.path.insert(0, os.path.abspath("../"))

rb.init(
    name="Physics Test",
    physics_fps=60,
    window_size=rb.Vector(600, 600),
    res=rb.Vector(1200, 1200),
    # target_fps=2,
)

rb.Game.show_fps = True
main = rb.Scene()

test = rb.GameObject(pos=rb.Vector(300, 300))
img = rb.Image(rel_path="../sprites/spaceship/spaceship.png")

img.resize(rb.Vector(29 * 2, 26 * 2))
test.add(img)

w = img.get_size().x
h = img.get_size().y


def update():
    global w, h
    if rb.Input.key_pressed("w"):
        w += 1
        h += 1
        img.resize(rb.Vector(w, h))
    if rb.Input.key_pressed("s"):
        w -= 1
        h -= 1
        img.resize(rb.Vector(w, h))
    if rb.Input.key_pressed("a"):
        img.rotation_offset -= 1
    if rb.Input.key_pressed("d"):
        img.rotation_offset += 1


main.add(test)
main.update = update
rb.begin()
