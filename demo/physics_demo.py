"""
A physics demo for rubato

This code simulates a ball pit with no gravity. This file only depends on rubato 2.1.0 or later.
"""
from random import randint, choice
import rubato as rb

# Controls the number of objects in the simulation
num_objs = 70

# Initializes rubato
rb.init({
    "name": "rubato Physics Demo",
    "window_size": rb.Vector(600, 600),
    "res": rb.Vector(1200, 1200),
})

rb.Game.show_fps = True

main_scene = rb.Scene()  # Create our scene

# Create our four walls
top = rb.GameObject(pos=rb.Display.top_center + rb.Vector(0, -30)).add(
    rb.Rectangle({
        "width": rb.Display.res.x + 175,
        "height": rb.Display.res.y / 10,
        "color": rb.Color.gray,
    })
)

bottom = rb.GameObject(pos=rb.Display.bottom_center + rb.Vector(0, 30)).add(
    rb.Rectangle({
        "width": rb.Display.res.x + 175,
        "height": rb.Display.res.y / 10,
        "color": rb.Color.gray,
    })
)

left = rb.GameObject(pos=rb.Display.center_left + rb.Vector(-30, 0)).add(
    rb.Rectangle({
        "width": rb.Display.res.x / 10,
        "height": rb.Display.res.y + 175,
        "color": rb.Color.gray,
    })
)

right = rb.GameObject(pos=rb.Display.center_right + rb.Vector(30, 0)).add(
    rb.Rectangle({
        "width": rb.Display.res.x / 10,
        "height": rb.Display.res.y + 175,
        "color": rb.Color.gray,
    })
)

# Add the walls to the scene
main_scene.add(top, bottom, left, right)

# Create and add all our objects
for _ in range(num_objs):
    main_scene.add(
        rb.GameObject(
            {
                "pos": # Set a random position
                    rb.Vector(
                        randint(rb.Display.res.x / 20, 19 * rb.Display.res.x / 20),
                        randint(rb.Display.res.y / 20, 19 * rb.Display.res.y / 20)
                    )
            }
        ).add(
            rb.Circle(
                {
                    "radius": rb.Display.res.x / num_objs,
                    "color": rb.Color(*choice(list(rb.Defaults.color_defaults.values())))
                }
            )
        ).add(
            rb.RigidBody(
                {
                    "density": 0.1,
                    "bounciness": 1,
                    "friction": 0.2,
                    "velocity": rb.Vector(randint(-100, 100), randint(-100, 100)),
                    "advanced": True,
                }
            )
        )
    )

rb.begin()
