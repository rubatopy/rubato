"""
This is a demo file :)
"""

import rubato as rb
from rubato import Group, Scene, Vector, Input

rb.init()

main_scene = Scene()

# To see any Rubato Class's default options, you can print them
print(rb.Text.default_options)


rb.game.scenes.add(main_scene)
group = Group()
main_scene.add(group)

sprite = rb.Rectangle({
    "pos": Vector(300, 200),
    "dims": Vector(100, 100),
    "color": rb.color.yellow
})
empty = rb.Empty()


def custom_update():
    if Input.is_pressed("w"):
        sprite.pos += Vector(0, -5)
    if Input.is_pressed("s"):
        sprite.pos += Vector(0, 5)
    if Input.is_pressed("a"):
        sprite.pos += Vector(-5, 0)
    if Input.is_pressed("d"):
        sprite.pos += Vector(5, 0)
    if Input.is_pressed("="):
        main_scene.camera.zoom = 2
    elif Input.is_pressed("-"):
        main_scene.camera.zoom = 0.5
    else:
        main_scene.camera.zoom = 1


empty.update = custom_update
group.add(sprite)


text = rb.Text({"text": "hi", "onto_surface": sprite.image})
group.add(text)

main_scene.add(group)
main_scene.add(empty)

rb.begin()
