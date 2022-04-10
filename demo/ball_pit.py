"""A physics demo for Rubato"""
from random import randint, choice
import rubato as rb

num_balls = 70

rb.init({
    "name": "Ball Pit",
    "physics_fps": 30,
    "window_size": rb.Vector(600, 600),
    "res": rb.Vector(1200, 1200),
})

main_scene = rb.Scene()
rb.Game.scenes.add(main_scene, "main")

top = rb.GameObject({
    "pos": rb.Display.top_center + rb.Vector(0, -30)
}).add(rb.Rectangle({
    "width": rb.Display.res.x + 175,
    "height": rb.Display.res.y / 10,
    "color": rb.Color.gray,
}))

bottom = rb.GameObject({
    "pos": rb.Display.bottom_center + rb.Vector(0, 30)
}).add(rb.Rectangle({
    "width": rb.Display.res.x + 175,
    "height": rb.Display.res.y / 10,
    "color": rb.Color.gray,
}))

left = rb.GameObject({
    "pos": rb.Display.center_left + rb.Vector(-30, 0)
}).add(rb.Rectangle({
    "width": rb.Display.res.x / 10,
    "height": rb.Display.res.y + 175,
    "color": rb.Color.gray,
}))

right = rb.GameObject({
    "pos": rb.Display.center_right + rb.Vector(30, 0)
}).add(rb.Rectangle({
    "width": rb.Display.res.x / 10,
    "height": rb.Display.res.y + 175,
    "color": rb.Color.gray,
}))

main_scene.add(top, bottom, left, right)

for _ in range(num_balls):
    main_scene.add(
        rb.GameObject(
            {
                "pos":
                    rb.Vector(
                        randint(rb.Display.res.x / 20, 19 * rb.Display.res.x / 20),
                        randint(rb.Display.res.y / 20, 19 * rb.Display.res.y / 20)
                    )
            }
        ).add(
            rb.Circle(
                {
                    "radius": rb.Display.res.x / num_balls,
                    "color": rb.Color(*choice(list(rb.Defaults.color_defaults.values())))
                }
            )
        ).add(
            rb.RigidBody(
                {
                    "bounciness": 1,
                    "friction": 0.2,
                    "gravity": rb.Vector(0, 0),
                    "velocity": rb.Vector(randint(-100, 100), randint(-100, 100))
                }
            )
        )
    )

rb.begin()
