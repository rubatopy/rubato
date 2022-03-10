"""Physics Demo... basically a ball pit"""
from random import randint
import rubato as rb
from rubato import Game, Vector, Color

num_balls = 50
rb.init({
    "name": "Physics Demo",
    "window_width": 600,
    "window_height": 600,
    "aspect_ratio": 1,
    "fps_cap": 60,
})

main_scene = rb.Scene()
Game.scenes.add(main_scene, "main")
rb.Game.scenes.set("main")

top = rb.Sprite({
    "pos": Vector(300, -25)
}).add_component(
    rb.Polygon({
        "verts": rb.Polygon.generate_rect(600, 100),
        "debug": False,
        "color": Color.maroon,
    }))

bottom = rb.Sprite({
    "pos": Vector(300, 625)
}).add_component(
    rb.Polygon({
        "verts": rb.Polygon.generate_rect(600, 100),
        "debug": False,
        "color": Color.maroon,
    }))

left = rb.Sprite({
    "pos": Vector(-25, 300)
}).add_component(
    rb.Polygon({
        "verts": rb.Polygon.generate_rect(100, 600),
        "debug": False,
        "color": Color.maroon,
    }))

right = rb.Sprite({
    "pos": Vector(625, 300)
}).add_component(
    rb.Polygon({
        "verts": rb.Polygon.generate_rect(100, 600),
        "debug": False,
        "color": Color.maroon,
    }))

balls = []
for i in range(num_balls):
    ball = rb.Sprite({
        "pos": Vector(randint(50, 550), randint(50, 550))
    }).add_component(rb.Circle({
        "radius": 25,
        "color": Color.random
    })).add_component(rb.RigidBody({
        "bounciness": 1,
        "gravity": Vector()
    }))
    balls.append(ball)

player = rb.Sprite({
    "pos": rb.Vector(50, 50),
})

player_rb = rb.RigidBody({
    "mass": 10,
    "bounciness": 1,
    "max_speed": Vector(50, 1000),
    "gravity": Vector()
})
player.add_component(player_rb)

player_hitbox = rb.Polygon({
    "verts": rb.Polygon.generate_rect(32, 32),
    "color": Color.blue,
})
player.add_component(player_hitbox)


def custom_update():
    if rb.Input.is_pressed("w"):
        player_rb.velocity.y -= 100
    elif rb.Input.is_pressed("s"):
        player_rb.velocity.y += 100
    if rb.Input.is_pressed("a"):
        player_rb.velocity.x -= 50
    elif rb.Input.is_pressed("d"):
        player_rb.velocity.x += 50


main_scene.add_item(balls)
main_scene.add_item([top, bottom, left, right, player])
main_scene.update = custom_update

rb.begin()
