"""Physics Demo... basically a ball pit"""
from random import randint
import rubato as rb
from rubato import Game, Vector

num_balls = 20
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
    rb.Rectangle({
        "dims": Vector(600, 100),
        "color": rb.Color.maroon
    })).add_component(rb.Polygon.generate_rect(600, 100))

bottom = rb.Sprite({
    "pos": Vector(300, 625)
}).add_component(
    rb.Rectangle({
        "dims": Vector(600, 100),
        "color": rb.Color.maroon
    })).add_component(rb.Polygon.generate_rect(600, 100))

left = rb.Sprite({
    "pos": Vector(-25, 300)
}).add_component(
    rb.Rectangle({
        "dims": Vector(100, 600),
        "color": rb.Color.maroon
    })).add_component(rb.Polygon.generate_rect(100, 600))

right = rb.Sprite({
    "pos": Vector(625, 300)
}).add_component(
    rb.Rectangle({
        "dims": Vector(100, 600),
        "color": rb.Color.maroon
    })).add_component(rb.Polygon.generate_rect(100, 600))

balls = []
for i in range(num_balls):
    ball = rb.Sprite({
        "pos": Vector(randint(100, 500), randint(100, 500))
    }).add_component(rb.Circle(25)).add_component(
        rb.RigidBody({
            "bouncyness": 1,
            "gravity": Vector()
        }))
    ball.get_component(rb.Hitbox).debug = True
    balls.append(ball)

player = rb.Sprite({
    "pos": rb.Vector(50, 50),
})

player_rb = rb.RigidBody({
    "mass": 10,
    "bouncyness": 1,
    "max_speed": Vector(50, 1000),
    "gravity": Vector()
})
player.add_component(player_rb)

player_hitbox = rb.Polygon.generate_rect(32, 32)
player.add_component(player_hitbox)
player_hitbox.debug = True


def custom_update():
    if rb.Input.is_pressed("w"):
        player_rb.velocity.y = -200
    elif rb.Input.is_pressed("s"):
        player_rb.velocity.y = 200
    if rb.Input.is_pressed("a"):
        player_rb.velocity.x -= 50
    elif rb.Input.is_pressed("d"):
        player_rb.velocity.x += 50


main_scene.add_item(balls)
main_scene.add_item([top, bottom, left, right, player])
main_scene.update = custom_update

rb.begin()
