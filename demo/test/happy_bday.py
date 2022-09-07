"""using rubato's particle effects to make a happy birthday card"""
# pylint: disable=all
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
        self.accell = V(0, 3)
        self.rast = None

    def setup(self):
        self.rast = self.gameobj.get(rb.Raster)
    def update(self):
        self.vel += self.accell * rb.Time.delta_time
        self.rast.offset += self.vel * rb.Time.delta_time
        if self.rast.offset.y > self.range and self.vel.y > 0:
            self.vel.y *= -1
        if self.rast.offset.y < -self.range and self.vel.y < 0:
            self.vel.y *= -1

def balloon_gen():
    height = 30
    radius = 16
    pos = V(rb.Math.lerp(radius*2, rb.Display.res.x-radius*2, random.random()), random.random() * rb.Display.res.y / 4 + radius * 3)
    pos.round()
    go = rb.wrap(rast := rb.Raster(height=32 + height), pos=pos)
    go.add(Balloon())
    rast.draw_circle((radius, radius), radius, fill=rb.Color.random())
    offset = V.down() * (radius + height / 2) + V.right() * radius
    for i in range(height):
        rast.draw_point(offset + V(i%3, i), rb.Color.black)
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
        part.velocity = V.from_radial(random.random() * 10+5, angle)
        part.velocity*=2
        # print(part.velocity, angle)
        perpendicular = angle + 90
        part.pos += V.from_radial(rb.Math.lerp(-10, 10, random.random()), perpendicular)
        return part
    return dir_func
# def right(angle):
#     part = rb.Particle(surf.clone(), velocity=V(1,0)*10, lifespan=4)
#     return part

def system(angle, lifespan):
    return rb.ParticleSystem(
        new_particle=dir_func_gen(angle, lifespan),
        loop=True,
        running=True,
    )

# bday.add(rb.wrap(system(90, 5), pos=rb.Display.center))
# f = open("instructions.txt", "w")
# def update(info):
#     if info["button"] == "mouse 1":
#         bday.add(rb.wrap(system(180, 10/2), pos=(info["x"], info["y"])))
#         f.write(f"bday.add(rb.wrap(system(180, 10/2), pos=({info['x']}, {info['y']})))")
#     if info["button"] == "mouse 2":
#         bday.add(rb.wrap(system(180, 5/2), pos=(info["x"], info["y"])))
#         f.write(f"bday.add(rb.wrap(system(180, 5/2), pos=({info['x']}, {info['y']})))")
#     if info["button"] == "mouse 3":
#         bday.add(rb.wrap(system(90, 5/2), pos=(info["x"], info["y"])))
#         f.write(f"bday.add(rb.wrap(system(90, 5/2), pos=({info['x']}, {info['y']})))")
# rb.Radio.listen(rb.Events.MOUSEDOWN, update)

f = open("instructions.txt", "r")
l = f.readlines()
for line in l:
    exec(line)

rb.begin()

