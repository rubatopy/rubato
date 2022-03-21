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
    "target_fps": 0,
    "physics_fps": 30,
    "window_size": Vector(600, 600),
    "resolution": Vector(1200, 1200),
})

main_scene = rb.Scene()
Game.scenes.add(main_scene, "main")

top = rb.Sprite({
    "pos": Game.top_center() + Vector(0, -30)
}).add(
    rb.Rectangle({
        "width": Game.get_width() + 175,
        "height": Game.get_height() / 10,
        "color": Color.gray,
    }))

bottom = rb.Sprite({
    "pos": Game.bottom_center() + Vector(0, 30)
}).add(
    rb.Rectangle({
        "width": Game.get_width() + 175,
        "height": Game.get_height() / 10,
        "color": Color.gray,
    }))

left = rb.Sprite({
    "pos": Game.center_left() + Vector(-30, 0)
}).add(
    rb.Rectangle({
        "width": Game.get_width() / 10,
        "height": Game.get_height() + 175,
        "color": Color.gray,
    }))

right = rb.Sprite({
    "pos": Game.center_right() + Vector(30, 0)
}).add(
    rb.Rectangle({
        "width": Game.get_width() / 10,
        "height": Game.get_height() + 175,
        "color": Color.gray,
    }))

for _ in range(60):
    main_scene.add(
        rb.Sprite({
            "pos":
            Vector(
                randint(Game.get_width() / 20, 19 * Game.get_width() / 20),
                randint(Game.get_height() / 20, 19 * Game.get_height() / 20))
        }).add(
            rb.Circle({
                "radius":
                Game.get_width() / 50,
                "color":
                Color(*choice(list(rb.Defaults.color_defaults.values())))
            })).add(
                rb.RigidBody({
                    "bounciness":
                    1,
                    "friction":
                    0.2,
                    "gravity":
                    Vector(0,
                           Game.get_width() / 8),
                    "velocity":
                    Vector(randint(-100, 100), randint(-100, 100))
                })))

player = rb.Sprite({
    "pos": rb.Vector(50, 50),
    "debug": True
}).add(
    rb.Image({
        "image_location": "testing/Idle/0.png",
        "scale_factor": rb.Vector(2, 2)
    }))

player_rb = rb.RigidBody({
    "mass": 0,
    "bounciness": 0.1,
    "max_speed": Vector(1000, 1000),
    "gravity": Vector()
})
player.add(player_rb)

player_hitbox = rb.Rectangle({
    "width": Game.get_width() / 16,
    "height": Game.get_width() / 16,
    "debug": True,
})
player.add(player_hitbox)


def custom_update():
    if rb.Input.key_pressed("w"):
        player_rb.velocity.y -= 100
    elif rb.Input.key_pressed("s"):
        player_rb.velocity.y += 100
    if rb.Input.key_pressed("a"):
        player_rb.velocity.x -= 100
    elif rb.Input.key_pressed("d"):
        player_rb.velocity.x += 100

    if rb.Input.key_pressed("right"):
        rb.Game.scenes.current.camera.pos.x += 5
    elif rb.Input.key_pressed("left"):
        rb.Game.scenes.current.camera.pos.x -= 5
    if rb.Input.key_pressed("up"):
        rb.Game.scenes.current.camera.pos.y -= 5
    elif rb.Input.key_pressed("down"):
        rb.Game.scenes.current.camera.pos.y += 5

    if rb.Input.key_pressed("-"):
        rb.Game.scenes.current.camera.zoom -= 0.1
    elif rb.Input.key_pressed("="):
        rb.Game.scenes.current.camera.zoom += 0.1
    if rb.Input.key_pressed("0"):
        rb.Game.scenes.current.camera.zoom = 1

    if rb.Input.key_pressed("a", "Shift"):
        print("WOW the secret combo was pressed.")


main_scene.add([top, bottom, left, right, player])
main_scene.update = custom_update

rb.begin()
