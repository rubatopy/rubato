# pylint: disable=all
from pip import main
import rubato as rb

rb.init()

main_scene = rb.Scene()
rb.game.scenes.add(main_scene)

image = rb.Sprite({
    "pos": rb.Vector(100, 100),
}).add_component(rb.Image({
    "scale": rb.Vector(2, 2),
}))

rect = rb.Sprite({
    "pos": rb.Vector(200, 100),
}).add_component(
    rb.Rectangle({
        "dims": rb.Vector(32, 32),
        "color": rb.Color.red,
    }))

run = rb.Animation.import_animation_folder("testing/Run")
idle = rb.Animation.import_animation_folder("testing/Idle")

player = rb.Sprite({
    "pos": rb.Vector(50, 50),
})

player_rb = rb.RigidBody({
    "mass": 1,
    "friction": rb.Vector(0.95, 0.95),
    "max_speed": rb.Vector(100, rb.Math.INFINITY),
    "hitbox": rb.Polygon.generate_rect(),
    "debug": True,
    "rotation": 0,
    "gravity": 100,
})
player.add_component(player_rb)

player_hitbox = rb.Polygon.generate_rect(32, 32)
player_hitbox.debug = True
player.add_component(player_hitbox)

player_anim = rb.Animation()
player.add_component(player_anim)

player_anim.add_state("run", run)
player_anim.add_state("idle", idle)


def custom_update():
    if rb.Input.is_pressed("w"):
        player_anim.set_current_state("run")
        player_rb.velocity.y = -100
    elif rb.Input.is_pressed("s"):
        player_anim.set_current_state("run")
        player_rb.velocity.y = 100
    if rb.Input.is_pressed("a"):
        player_anim.set_current_state("run")
        player_rb.velocity.x = -100
    elif rb.Input.is_pressed("d"):
        player_anim.set_current_state("run")
        player_rb.velocity.x = 100
    else:
        player_anim.set_current_state("idle", True)
    if rb.Input.is_pressed("right"):
        player_anim.rotation += 1
    if rb.Input.is_pressed("="):
        player_anim.resize(
            rb.Vector.from_tuple(player_anim.anim_frame.get_size_original()) *
            2)
    elif rb.Input.is_pressed("-"):
        player_anim.resize(
            rb.Vector.from_tuple(player_anim.anim_frame.get_size_original()) /
            2)
    else:
        player_anim.resize(
            rb.Vector.from_tuple(player_anim.anim_frame.get_size_original()))


main_scene.add(image)
main_scene.add(rect)
main_scene.add(player)

main_scene.update = custom_update

rb.begin()
