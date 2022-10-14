"""
A physics demo for rubato
"""
from random import randint
import rubato as rb
from rubato.utils.hardware.display import Display

# Controls the number of objects in the simulation
num_obj = 60

# Initializes rubato
rb.init(name="rubato physics demo", res=(1980, 1980), window_size=(660, 660))

rb.Game.show_fps = True
# rb.Game.debug = True

main_scene = rb.Scene()  # Create our scene

# Create our four walls
top = rb.GameObject(pos=rb.Display.top_center + rb.Vector(0, 60)).add(
    rb.Rectangle(
        width=rb.Display.res.x + 175,
        height=rb.Display.res.y // 10,
        color=rb.Color.gray,
    )
)

bottom = rb.GameObject(pos=rb.Display.bottom_center + rb.Vector(0, -60)).add(
    rb.Rectangle(
        width=rb.Display.res.x + 175,
        height=rb.Display.res.y // 10,
        color=rb.Color.gray,
    )
)

left = rb.GameObject(pos=rb.Display.center_left + rb.Vector(-60, 0)).add(
    rb.Rectangle(
        width=rb.Display.res.x // 10,
        height=rb.Display.res.y + 175,
        color=rb.Color.gray,
    )
)

right = rb.GameObject(pos=rb.Display.center_right + rb.Vector(60, 0)).add(
    rb.Rectangle(
        width=rb.Display.res.x // 10,
        height=rb.Display.res.y + 175,
        color=rb.Color.gray,
    )
)

# Add the walls to the scene
main_scene.add(top, bottom, left, right)

# Create and add all our objects
for _ in range(num_obj // 2):
    main_scene.add(
        rb.wrap(
            [
                rb.Circle(radius=rb.Display.res.x // num_obj, color=rb.Color.random_default()),
                rb.RigidBody(
                    mass=0.1,
                    bounciness=0.99,
                    friction=0.2,
                    gravity=(0, -80),
                    velocity=(randint(-100, 100), randint(-100, 100)),
                ),
            ],
            pos=Display.top_left + (
                randint(int(rb.Display.res.x / 20), int(19 * rb.Display.res.x / 20)),
                -randint(int(rb.Display.res.y / 20), int(19 * rb.Display.res.y / 20)),
            ),
        )
    )
for _ in range(num_obj // 2):
    main_scene.add(
        rb.wrap(
            [
                rb.Polygon(rb.Vector.poly(randint(3, 9), rb.Display.res.x // num_obj), color=rb.Color.random_default()),
                rb.RigidBody(
                    mass=0.1,
                    bounciness=0.99,
                    friction=0.2,
                    gravity=(0, -80),
                    velocity=(randint(-100, 100), randint(-100, 100)),
                ),
            ],
            pos=Display.top_left + (
                randint(int(rb.Display.res.x / 20), int(19 * rb.Display.res.x / 20)),
                -randint(int(rb.Display.res.y / 20), int(19 * rb.Display.res.y / 20)),
            ),
        )
    )

rb.begin()
