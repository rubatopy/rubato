"""Physics Demo... basically a ball pit"""
import os
import sys

sys.path.insert(0, os.path.abspath("../"))
# pylint: disable=wrong-import-position
from random import randint
import rubato as rb
from rubato import Game, Vector, Color

num_balls = 100
rb.init({
    "name": "Physics Demo",
    "fps_cap": 60,
    "window_size": Vector(600, 600),
    "resolution": Vector(600, 600),
})

main_scene = rb.Scene()
Game.scenes.add(main_scene, "main")
rb.Game.scenes.set("main")

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

balls = []
for i in range(num_balls):
    balls.append(rb.Sprite({
        "pos":
        Vector(randint(Game.resolution.x / 20, 19 * Game.resolution.x / 20),
               randint(Game.resolution.y / 20, 19 * Game.resolution.y / 20))
    }).add(
        rb.Circle({
            "radius": Game.resolution.x / 40,
            "color": Color.random
        })
    ).add(
        rb.RigidBody({
            "bounciness": 1,
            "gravity": Vector(0, Game.resolution.x / 10)
        })
    ))

player = rb.Sprite({
    "pos": rb.Vector(50, 50),
}).add(rb.Image({"image_location": "testing/Idle/0.png"}))

player_rb = rb.RigidBody({
    "mass": 10,
    "bounciness": 0.1,
    "max_speed": Vector(50, 1000),
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
        player_rb.velocity.y -= Game.resolution.x * (1 / 12)
    elif rb.Input.key_is_pressed("s"):
        player_rb.velocity.y += Game.resolution.x * (1 / 12)
    if rb.Input.key_is_pressed("a"):
        player_rb.velocity.x -= Game.resolution.x * (1 / 12)
    elif rb.Input.key_is_pressed("d"):
        player_rb.velocity.x += Game.resolution.x * (1 / 12)

    #print(f"fps: {rb.Time.clock.get_fps()}")


main_scene.add(balls)
main_scene.add([top, bottom, left, right, player])
main_scene.update = custom_update

rb.begin()
