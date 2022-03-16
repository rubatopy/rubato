"""A physics demo for Rubato"""
import os
import sys

sys.path.insert(0, os.path.abspath("../"))
# pylint: disable=wrong-import-position
from random import randint, choice
import rubato as rb
from rubato import Game, Vector, Color

rb.init({
    "name": "Physics Demo",
    "fps_cap": 1,
    "physics_timestep": 20,
    "window_size": Vector(600, 600),
    "resolution": Vector(1200, 1200),
})

main_scene = rb.Scene()
Game.scenes.add(main_scene, "main")

top = rb.Sprite({
    "pos": Vector(Game.resolution.x / 2, 0)
}).add(
    rb.Rectangle({
        "width": Game.resolution.x,
        "height": Game.resolution.y / 20,
        "color": Color.gray,
    }))

bottom = rb.Sprite({
    "pos": Vector(Game.resolution.x / 2, Game.resolution.y)
}).add(
    rb.Rectangle({
        "width": Game.resolution.x,
        "height": Game.resolution.y / 20,
        "color": Color.gray,
    }))

left = rb.Sprite({
    "pos": Vector(0, Game.resolution.y / 2)
}).add(
    rb.Rectangle({
        "width": Game.resolution.x / 20,
        "height": Game.resolution.y,
        "color": Color.gray,
    }))

right = rb.Sprite({
    "pos": Vector(Game.resolution.x, Game.resolution.y / 2)
}).add(
    rb.Rectangle({
        "width": Game.resolution.x / 20,
        "height": Game.resolution.y,
        "color": Color.gray,
    }))

for _ in range(60):
    main_scene.add(
        rb.Sprite({
            "pos":
            Vector(
                randint(Game.resolution.x / 20, 19 * Game.resolution.x / 20),
                randint(Game.resolution.y / 20, 19 * Game.resolution.y / 20))
        }).add(
            rb.Circle({
                "radius": Game.resolution.x / 50,
                "color": Color(*choice(
                    list(rb.Configs.color_defaults.values())))
            })).add(
                rb.RigidBody({
                    "bounciness":
                    1,
                    "friction":
                    0.2,
                    "gravity":
                    Vector(0, Game.resolution.x / 8),
                    "velocity":
                    Vector(randint(-100, 100), randint(-100, 100))
                })))

player = rb.Sprite({
    "pos": rb.Vector(50, 50),
    "debug": True
}).add(
    rb.Image({
        "image_location": "testing/Idle/0.png",
        "scale_factor": rb.Vector(10 / 3, 10 / 3)
    }))

player_rb = rb.RigidBody({
    "mass": 0,
    "bounciness": 0.1,
    "max_speed": Vector(1000, 1000),
    "gravity": Vector()
})
player.add(player_rb)

player_hitbox = rb.Polygon({
    "verts":
    rb.Polygon.generate_polygon(4, Game.resolution.x / 25),
    "rotation":
    180,
    "debug":
    True,
})
player.add(player_hitbox)


def custom_update():
    if rb.Input.key_is_pressed("w"):
        player_rb.velocity.y -= Game.resolution.x / 12
    elif rb.Input.key_is_pressed("s"):
        player_rb.velocity.y += Game.resolution.x / 12
    if rb.Input.key_is_pressed("a"):
        player_rb.velocity.x -= Game.resolution.x / 12
    elif rb.Input.key_is_pressed("d"):
        player_rb.velocity.x += Game.resolution.x / 12

    print(f"fps: {rb.Time.smooth_fps()}")


main_scene.add([top, bottom, left, right, player])
main_scene.update = custom_update

rb.radio.listen("resize", lambda: print("hi"))

rb.begin()
