"""
A classic
"""
import random
from rubato import *

size = 1080
bounds = size // 8
radius = size // 40
level = 0

init(name="asteroids", res=(size, size))

main = Scene()

# background
stars = Surface(size, size)
stars.fill(Color.black)
for i in range(200):
    pos = random.randint(0, size), random.randint(0, size)
    stars.draw_point(pos, Color.white)


# remove asteroids that are out of bounds
class BoundsChecker(Component):

    def update(self):
        if self.gameobj.pos.x < -bounds or self.gameobj.pos.x > size + bounds or \
            self.gameobj.pos.y < -bounds or self.gameobj.pos.y > size + bounds:
            main.delete(self.gameobj)


# asteroid generator
def make_asteroid():
    sides = random.randint(5, 8)

    t = random.randint(0, size)
    topbottom = random.randint(0, 1)
    side = random.randint(0, 1)
    if topbottom:
        pos = t, side * size + (radius if side else -radius)
    else:
        pos = side * size + (radius if side else -radius), t

    dir = (-Display.center.dir_to(pos)).rotate(random.randint(-45, 45))

    main.add(
        wrap(
            [
                Polygon(
                    [
                        Vector.from_radial(random.randint(int(radius * .7), int(radius * 0.95)), i * 360 / sides)
                        for i in range(sides)
                    ],
                    debug=True,
                ),
                RigidBody(velocity=dir * 100, ang_vel=random.randint(-30, 30)),
                BoundsChecker(),
            ],
            "asteroid",
            pos,
            random.randint(0, 360),
        )
    )


Time.schedule(ScheduledTask(1000, make_asteroid, 1000))


class PlayerController(Component):
    """
    A spaceship component.
    """

    def setup(self):
        self.speed = 400
        self.steer = 50

        self.velocity = Vector()

    def fixed_update(self):
        target = Vector(
            Input.controller_axis(Input.controllers - 1, 0),
            Input.controller_axis(Input.controllers - 1, 1),
        )

        d_vel = target * self.speed
        steering = Vector.clamp_magnitude(d_vel - self.velocity, self.steer)

        self.velocity = Vector.clamp_magnitude(self.velocity + steering, self.speed)

        self.gameobj.pos += self.velocity * Time.fixed_delta

        if target != (0, 0):
            self.gameobj.rotation = self.velocity.angle


full = [
    Vector.from_radial(radius, 0),
    Vector.from_radial(radius, 125),
    Vector.from_radial(radius // 4, 180),
    Vector.from_radial(radius, -125),
]
right = [full[0], full[1], full[2]]
left = [full[0], full[2], full[3]]
player_spr = Raster(radius * 2, radius * 2)
player_spr.draw_poly([v + radius for v in full], Color.debug, 2, aa=True)

main.add(
    wrap(
        [
            PlayerController(),
            Polygon(right, trigger=True),
            Polygon(left, trigger=True),
            player_spr,
        ],
        "player",
        Display.center,
    )
)


def background():
    Draw.surf(stars, Display.center)


Game.draw = background

begin()
