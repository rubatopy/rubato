# pylint: disable=all
import rubato as rb
from rubato.utils.vector import Vector

rb.init({"fps_cap": 60})

main_scene = rb.Scene()
rb.game.scenes.add(main_scene)

ground = rb.Sprite({
    "pos": rb.Vector(300, 375)
}).add_component(rb.Polygon.generate_rect(600, 50)).add_component(
    rb.Rectangle({
        "dims": rb.Vector(600, 50),
        "color": rb.Color.green
    }))

main_scene.add(ground)

platform = rb.Sprite({
    "pos": rb.Vector(400, 200)
}).add_component(
    rb.Rectangle({
        "dims": rb.Vector(100, 20),
        "color": rb.Color.green
    })).add_component(rb.Polygon.generate_rect(100, 20))

main_scene.add(platform)

run = rb.Animation.import_animation_folder("testing/Run")
idle = rb.Animation.import_animation_folder("testing/Idle")

player = rb.Sprite({
    "pos": rb.Vector(50, 50),
})

player_rb = rb.RigidBody({
    "mass": 20,
    "max_speed": rb.Vector(100, rb.Math.INFINITY),
    "debug": True,
    "rotation": 0,
})
player.add_component(player_rb)

player_hitbox = rb.Polygon.generate_rect(32, 32)
player_hitbox.debug = True
player.add_component(player_hitbox)

player_anim = rb.Animation()
player.add_component(player_anim)

player_anim.add_state("run", run)
player_anim.add_state("idle", idle)

main_scene.add(player)

box = rb.Sprite({
    "pos": rb.Vector(300, 325),
}).add_component(rb.RigidBody({
    "mass": 50,
})).add_component(
    rb.Rectangle({
        "dims": rb.Vector(50, 50),
        "color": rb.Color.red
    })).add_component(rb.Polygon.generate_rect(50, 50))
box.get_component(rb.Hitbox).debug = True
main_scene.add(box)


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
        rb.game.window_size = rb.Vector(100,100)
        rb.game.state = rb.STATE.RUNNING
    if rb.Input.is_pressed("0"):
        rb.game.aspect_ratio = 1.5
    if rb.Input.is_pressed("="):
        rb.game.aspect_ratio *= 1.1
        # player_anim.resize(
        #     rb.Vector.from_tuple(player_anim.anim_frame.get_size_original()) *
        #     2)
    elif rb.Input.is_pressed("-"):
        rb.game.aspect_ratio /= 1.1
        # player_anim.resize(
        #     rb.Vector.from_tuple(player_anim.anim_frame.get_size_original()) /
        #     2)
    else:
        player_anim.resize(
            rb.Vector.from_tuple(player_anim.anim_frame.get_size_original()))

    player_hitbox.collide(ground.get_component(rb.Hitbox))
    player_hitbox.collide(platform.get_component(rb.Hitbox))
    player_hitbox.collide(box.get_component(rb.Hitbox))

    box.get_component(rb.Hitbox).collide(ground.get_component(rb.Hitbox))

def callback(params):
    if params["key"] == "p":
        print("ouch")
        rb.game.state = rb.STATE.PAUSED if rb.game.state == rb.STATE.RUNNING else rb.STATE.RUNNING

rb.game.radio.listen("keydown", callback)

main_scene.fixed_update = custom_update

rb.begin()
