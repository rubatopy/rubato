"""using rubato's particle effects to make a happy birthday card"""
import rubato as rb

from rubato import Vector as V
import random

rb.init(physics_fps=30)

bday = rb.Scene()


class Balloon(rb.Component):

    def __init__(self):
        super().__init__()
        self.range = random.randint(5, 20)
        self.vel = V(0, 0)
        self.acc = V(0, 3)
        self.rast: rb.Raster

    def setup(self):
        self.rast = self.gameobj.get(rb.Raster)

    def update(self):
        self.vel += self.acc * rb.Time.delta_time
        self.rast.offset += self.vel * rb.Time.delta_time
        if self.rast.offset.y > self.range and self.vel.y > 0:
            self.vel.y *= -1
        if self.rast.offset.y < -self.range and self.vel.y < 0:
            self.vel.y *= -1


def balloon_gen():
    height = 30
    radius = 16
    pos = V(
        rb.Math.lerp(radius * 2, rb.Display.res.x - radius * 2, random.random()),
        random.random() * rb.Display.res.y / 4 + radius * 3
    )
    pos.round()
    rast = rb.Raster(height=32 + height)
    go = rb.wrap(rast, pos=pos)
    go.add(Balloon())
    rast.draw_circle((radius, radius), radius, fill=rb.Color.random())
    offset = V.down() * (radius + height / 2) + V.right() * radius
    for i in range(height):
        rast.draw_point(offset + V(i % 3, i), rb.Color.black)
    rast.scale = V.one() * (random.random() * 2 + 1)
    bday.add(go)


for _ in range(15):
    balloon_gen()

surf = rb.Surface()
surf.draw_circle((16, 16), 16, fill=rb.Color.black)


def dir_func_gen(angle, lifespan):

    def dir_func(_):
        cpy = surf.clone()
        cpy.fill(rb.Color.random_default(1))
        cpy.scale = V.one() * (random.random() * 0.5)
        part = rb.Particle(cpy, lifespan=lifespan)
        part.velocity = V.from_radial(random.random() * 10 + 5, angle)
        part.velocity *= 2
        perpendicular = angle + 90
        part.pos += V.from_radial(rb.Math.lerp(-10, 10, random.random()), perpendicular)
        return part

    return dir_func


def system(angle, lifespan):
    return rb.ParticleSystem(
        new_particle=dir_func_gen(angle, lifespan),
        loop=True,
        running=True,
    )


bday.add(rb.wrap(system(180, 10 / 2), pos=(92, 450)))
bday.add(rb.wrap(system(180, 10 / 2), pos=(170, 454)))
bday.add(rb.wrap(system(180, 10 / 2), pos=(266, 456)))
bday.add(rb.wrap(system(180, 10 / 2), pos=(336, 460)))
bday.add(rb.wrap(system(180, 10 / 2), pos=(420, 472)))
bday.add(rb.wrap(system(90, 5 / 2), pos=(418, 470)))
bday.add(rb.wrap(system(180, 10 / 2), pos=(554, 468)))
bday.add(rb.wrap(system(90, 5 / 2), pos=(554, 468)))
bday.add(rb.wrap(system(180, 5 / 2), pos=(682, 460)))
bday.add(rb.wrap(system(180, 5 / 2), pos=(758, 460)))
bday.add(rb.wrap(system(90, 5 / 2), pos=(682, 528)))
bday.add(rb.wrap(system(180, 5 / 2), pos=(722, 534)))
bday.add(rb.wrap(system(90, 5 / 2), pos=(94, 520)))
bday.add(rb.wrap(system(90, 5 / 2), pos=(272, 466)))
bday.add(rb.wrap(system(90, 5 / 2), pos=(270, 526)))
bday.add(rb.wrap(system(180, 5 / 2), pos=(482, 474)))
bday.add(rb.wrap(system(90, 5 / 2), pos=(424, 540)))
bday.add(rb.wrap(system(180, 5 / 2), pos=(624, 466)))
bday.add(rb.wrap(system(90, 5 / 2), pos=(552, 536)))
bday.add(rb.wrap(system(180, 10 / 2), pos=(112, 672)))
bday.add(rb.wrap(system(90, 5 / 2), pos=(112, 672)))
bday.add(rb.wrap(system(180, 10 / 2), pos=(250, 662)))
bday.add(rb.wrap(system(90, 5 / 2), pos=(250, 664)))
bday.add(rb.wrap(system(180, 10 / 2), pos=(186, 676)))
bday.add(rb.wrap(system(90, 5 / 2), pos=(116, 744)))
bday.add(rb.wrap(system(90, 5 / 2), pos=(112, 806)))
bday.add(rb.wrap(system(180, 10 / 2), pos=(322, 670)))
bday.add(rb.wrap(system(90, 5 / 2), pos=(254, 806)))
bday.add(rb.wrap(system(180, 10 / 2), pos=(390, 666)))
bday.add(rb.wrap(system(90, 5 / 2), pos=(394, 670)))
bday.add(rb.wrap(system(180, 5 / 2), pos=(526, 660)))
bday.add(rb.wrap(system(180, 5 / 2), pos=(606, 666)))
bday.add(rb.wrap(system(180, 10 / 2), pos=(460, 678)))
bday.add(rb.wrap(system(90, 5 / 2), pos=(392, 736)))
bday.add(rb.wrap(system(90, 5 / 2), pos=(532, 728)))
bday.add(rb.wrap(system(180, 5 / 2), pos=(560, 734)))

rb.begin()
