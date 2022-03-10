# pylint: disable=all
import rubato as rb
from rubato.utils.vector import Vector

rb.init({"fps_cap": 60})

main_scene = rb.Scene()
rb.Game.scenes.add(main_scene, "main")
rb.Game.scenes.set("main")

ground = rb.Sprite({
    "pos": rb.Vector(300, 375)
}).add_component(rb.Polygon.generate_rect(600, 50)).add_component(
    rb.Rectangle({
        "dims": rb.Vector(600, 50),
        "color": rb.Color.green
    }))

main_scene.add_item(ground)

platform = rb.Sprite({
    "pos": rb.Vector(400, 200)
}).add_component(
    rb.Rectangle({
        "dims": rb.Vector(100, 20),
        "color": rb.Color.green
    })).add_component(rb.Polygon.generate_rect(100, 20))

main_scene.add_item(platform)

run = rb.Animation.import_animation_folder("testing/Run")
idle = rb.Animation.import_animation_folder("testing/Idle")

player = rb.Sprite({
    "pos": rb.Vector(50, 50),
})

player_rb = rb.RigidBody({
    "mass": 100,
    "max_speed": rb.Vector(100, rb.Math.INFINITY),
    "rotation": 0,
    "bouncyness": 0.1,
})
player.add_component(player_rb)

player_hitbox = rb.Polygon.generate_rect(32, 32)
player.add_component(player_hitbox)

player_anim = rb.Animation({"fps": 30})

player.add_component(player_anim)
player_anim.add_state("run", run)
player_anim.add_state("idle", idle)

main_scene.add_item(player)

box = rb.Sprite({
    "pos": rb.Vector(300, 325),
}).add_component(rb.RigidBody({
    "mass": 50,
})).add_component(
    rb.Rectangle({
        "dims": rb.Vector(50, 50),
        "color": rb.Color.red
    })).add_component(rb.Polygon.generate_rect(50, 50))
main_scene.add_item(box)


def custom_update():
    if rb.Input.is_pressed("w"):
        player_anim.set_current_state("run")
        player_rb.velocity.y = -200
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
    if rb.Input.is_pressed("r"):
        rb.Game.window_size = rb.Vector(100, 100)
        rb.Game.state = rb.STATE.RUNNING
    if rb.Input.is_pressed("0"):
        rb.Game.aspect_ratio = 1.5
    if rb.Input.is_pressed("="):
        rb.Game.aspect_ratio *= 1.1
        # player_anim.resize(
        #     rb.Vector.from_tuple(player_anim.anim_frame.get_size_original()) *
        #     2)
    elif rb.Input.is_pressed("-"):
        rb.Game.aspect_ratio /= 1.1
        # player_anim.resize(
        #     rb.Vector.from_tuple(player_anim.anim_frame.get_size_original()) /
        #     2)
    else:
        player_anim.resize(
            rb.Vector.from_tuple(player_anim.anim_frame.get_size_original()))


def callback(params):
    if params["key"] == "p":
        rb.Game.set_state(rb.STATE.PAUSED if rb.Game.get_state() ==
                          rb.STATE.RUNNING else rb.STATE.RUNNING)


rb.radio.listen("keydown", callback)

main_scene.fixed_update = custom_update

rb.begin()
