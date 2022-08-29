"""A particles demo"""
import rubato as rb
from rubato import Vector as V
from rubato.utils.vector import Vector

rb.init(res=V(256, 256), window_size=V(256, 256) * 2)
rb.Game.show_fps = True
s = rb.Scene()

surf = rb.Surface(31, 31, scale=(1 / 8, 1 / 8))
surf.draw_circle((15, 15), 15, fill=rb.Color.orange)


def movement(p: rb.Particle, dt: float):
    p.pos += p.velocity.lerp(Vector.up() * p.velocity.magnitude, p.age / p.lifespan) * dt
    p.surface.set_alpha(round((p.age / p.lifespan) * 255))


def start_shape(angle: float):
    return rb.Vector(0, 0)


def starting_dir(angle: float):
    return rb.Vector(0, -1).rotate((((angle / 180) - 1) * 40) + 6)


particleSytem = rb.ParticleSystem(
    surf,
    loop=True,
    lifespan=0.4,
    duration=0.1,
    start_speed=50,
    spread=6,
    movement=movement,
    starting_shape=start_shape,
    starting_dir=starting_dir,
    mode=rb.ParticleSystemMode.RANDOM,
)
go = rb.GameObject()
go.add(particleSytem)

handle = rb.Raster(width=128, height=256, scale=(1 / 20, 1 / 10), offset=(0, 4))
handle.draw_circle((64, 192), 64, fill=rb.Color(165, 42, 42))
handle.draw_rect((0, 64), (128, 128), fill=rb.Color(165, 42, 42))

torch1 = rb.GameObject(pos=(50, 50))
torch1.add(particleSytem.clone())
torch1.add(handle.clone())
torch1.get(rb.ParticleSystem).start()

torch2 = rb.GameObject(pos=rb.Display.top_right + (-50, 50))
torch2.add(particleSytem.clone())
torch2.add(handle.clone())
torch2.get(rb.ParticleSystem).start()


def update():
    if rb.Input.mouse_pressed():
        particleSytem.start()
        go.pos = rb.Input.get_mouse_pos()
    else:
        particleSytem.stop()


s.fixed_update = update
s.add(go, torch1, torch2)
rb.begin()
