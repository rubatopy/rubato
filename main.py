# pylint: disable=all
import rubato as rb

rb.init({"fps_cap": 20})

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

player = rb.Sprite({
    "pos": rb.Vector(50, 50),
})

player_rb = rb.RigidBody({
    "mass": 100,
    "max_speed": rb.Vector(100, rb.Math.INFINITY),
    "rotation": 0,
    "bounciness": 0.1,
})
player.add_component(player_rb)

player_hitbox = rb.Polygon.generate_rect(32, 32)
player.add_component(player_hitbox)

player_anim = rb.Animation({"fps": 6})

run = rb.Animation.import_animation_folder("testing/Run")
idle = rb.Animation.import_animation_folder("testing/Idle")

player_anim.add_state("idle", idle)
player_anim.add_state("run", run)

player.add_component(player_anim)

main_scene.add_item(player)

spinny = rb.Sprite({"pos": rb.Vector(200, 200)})
spinny_animation = rb.Animation({"fps": 4})
spinny.add_component(spinny_animation)
spinny_animation.add_state(
    "spin", rb.Animation.import_animation_folder("testing/spin"))

main_scene.add_item(spinny)

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

circle1 = rb.Sprite({
    "pos": rb.Vector(200, 50)
}).add_component(rb.Circle(20)).add_component(
    rb.RigidBody({
        "gravity": rb.Vector(0, 0),
        "bounciness": 1
    }))
circle1.get_component(rb.Hitbox).debug = True

main_scene.add_item(circle1)

circle2 = rb.Sprite({
    "pos": rb.Vector(175, 100)
}).add_component(rb.Circle(20)).add_component(
    rb.RigidBody({
        "gravity": rb.Vector(0, 0),
        "bounciness": 1
    }))
circle2.get_component(rb.Hitbox).debug = True

main_scene.add_item(circle2)


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
        # player_anim.set_current_state("idle", True)
        pass
    if rb.Input.is_pressed("right"):
        player_anim.rotation += 1
    if rb.Input.is_pressed("r"):
        rb.Game.window_size = rb.Vector(100, 100)
        rb.Game.state = rb.STATE.RUNNING
    if rb.Input.is_pressed("0"):
        rb.Game.aspect_ratio = 1.5
    if rb.Input.is_pressed("="):
        rb.Game.set_aspect_ratio(rb.Game.get_aspect_ratio() * 1.1)
    elif rb.Input.is_pressed("-"):
        rb.Game.set_aspect_ratio(rb.Game.get_aspect_ratio() / 1.1)
    else:
        player_anim.resize(
            rb.Vector.from_tuple(player_anim.anim_frame.get_size_original()))

    if rb.Input.is_pressed("space"):
        circle1.get_component(rb.RigidBody).add_force(rb.Vector(0, 1000))


def callback(params):
    if params["key"] == "p":
        rb.Game.set_state(rb.STATE.PAUSED if rb.Game.get_state() ==
                          rb.STATE.RUNNING else rb.STATE.RUNNING)


keylistener = rb.radio.listen("keydown", callback)

main_scene.fixed_update = custom_update

rb.begin()
