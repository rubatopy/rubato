"""A particles demo"""
from turtle import width
import rubato as rb
from rubato import Vector as V
from rubato.utils.vector import Vector

rb.init(res=V(256, 256), window_size=V(256, 256) * 2)
rb.Game.show_fps = True
s = rb.Scene()

surf = rb.Surface(scale=(1 / 16, 1 / 16))
surf.draw_circle((16, 16), 16, fill=rb.Color.turquoize)


def movement(p: rb.Particle, dt: float):
    p.velocity = p.velocity.lerp(V(0, -1) * p.velocity.magnitude, p.age / p.lifespan)
    p.surface.set_alpha(round(255 - ((p.age / p.lifespan) * 255)))
    rb.Particle.default_movement(p, dt)


def starting_dir(angle: float):
    return rb.Vector(0, -1).rotate((((angle / 180) - 1) * 60) + 6)


def cursor_make(angle: float):
    return rb.Particle(surf, movement, (0, 0), starting_dir(angle) * 50, (0, 0), 0, 0, 0, 1, 0.4, 1, 0)


particleSytem = rb.ParticleSystem(new_particle=cursor_make, loop=True, duration=0.3, spread=40, density=2)
go = rb.GameObject()
go.add(particleSytem)


def update():
    if rb.Input.mouse_pressed():
        particleSytem.start()
        go.pos = rb.Input.get_mouse_pos()
    else:
        particleSytem.stop()


s.fixed_update = update
s.add(go)
rb.begin()
