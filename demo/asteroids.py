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
        wrap([
            Polygon([
                Vector.from_radial(random.randint(int(radius * .7), int(radius * 0.95)), i * 360 / sides)
                for i in range(sides)
            ], Color.white),
            RigidBody(velocity=dir * 100, ang_vel=random.randint(-30, 30)),
            BoundsChecker(),
        ], "asteroid", pos, random.randint(0, 360))
    )


Time.schedule(ScheduledTask(1000, make_asteroid, 1000))


class PlayerController(Component):
    """
    A spaceship component.
    """

    def setup(self):
        self.speed = .2
        self.steer = .02

        self.velocity = Vector()

    def fixed_update(self):
        target = world_mouse()
        dir = (target - self.gameobj.pos).normalized()

        acc = Vector.clamp_magnitude((dir * self.speed - self.velocity) * self.steer, self.steer)

        self.velocity = Vector.clamp_magnitude(self.velocity + acc * Time.sec_to_milli(Time.fixed_delta), self.speed)
        self.gameobj.pos += self.velocity * Time.sec_to_milli(Time.fixed_delta)

        if not self.gameobj.pos.within(target, radius):
            self.gameobj.rotation = self.velocity.angle


main.add(
    wrap([PlayerController(), Polygon(Vector.poly(3, radius), Color.green, trigger=True)], "player", Display.center)
)


def background():
    Draw.surf(stars, Display.center)


Game.draw = background

begin()
