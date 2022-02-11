"""
This is a demo file :)

WARNING: THIS ENTIRE FILE DOESN'T WORK AS IT USES THE OLD SYSTEM
"""
# pylint: disable=all

import rubato as rb
from rubato import Group, Scene, Vector, Input, Configs, Animation

rb.init()

main_scene = Scene()

# To see any Rubato Class's default options, you can print them
print(Configs.rect_defaults)


rb.game.scenes.add(main_scene)
group = Group()
main_scene.add(group)

sprite = rb.Rectangle({
    "pos": Vector(300, 200),
    "dims": Vector(100, 100),
    "color": rb.Colour.yellow
})
empty = rb.Empty()

run = Animation.import_animation_folder("testing/Run")
idle = Animation.import_animation_folder("testing/Idle")

player_anim = Animation({"pos": Vector(50, 50)})
player_anim.add_state("idle", idle)
player_anim.add_state("run", run)
main_scene.add(player_anim)

def custom_update():
    # if Input.is_pressed("w"):
    #     sprite.pos += Vector(0, -5)
    # if Input.is_pressed("s"):
    #     sprite.pos += Vector(0, 5)
    # if Input.is_pressed("a"):
    #     sprite.pos += Vector(-5, 0)
    # if Input.is_pressed("d"):
    #     sprite.pos += Vector(5, 0)
    if Input.is_pressed("w"):
        player_anim.set_current_state("run")
        player_anim.pos += Vector(0, -5)
    elif Input.is_pressed("s"):
        player_anim.set_current_state("run")
        player_anim.pos += Vector(0, 5)
    elif Input.is_pressed("a"):
        player_anim.set_current_state("run")
        player_anim.pos += Vector(-5, 0)
    elif Input.is_pressed("d"):
        player_anim.set_current_state("run")
        player_anim.pos += Vector(5, 0)
    else:
        player_anim.set_current_state("idle")
    if Input.is_pressed("right"):
        player_anim.rotation += 1
    if Input.is_pressed("="):
        player_anim.resize(Vector.from_tuple(player_anim.anim_frame.get_size_original()) * 2)
    elif Input.is_pressed("-"):
        player_anim.resize(Vector.from_tuple(player_anim.anim_frame.get_size_original()) / 2)
    else:
        player_anim.resize(Vector.from_tuple(player_anim.anim_frame.get_size_original()))


empty.update = custom_update
group.add(sprite)


text = rb.Text({"text": "hi", "onto_surface": sprite.image})
group.add(text)

main_scene.add(group)
main_scene.add(empty)

rb.begin()
