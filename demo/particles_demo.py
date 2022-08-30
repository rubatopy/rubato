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
    p.pos += p.velocity.lerp(V(0, -1.25) * p.velocity.magnitude, p.age / p.lifespan) * dt
    p.surface.set_alpha(round(255 - ((p.age / p.lifespan) * 255)))


def starting_dir(angle: float):
    return rb.Vector(0, -1).rotate((((angle / 180) - 1) * 60) + 6)


particleSytem = rb.ParticleSystem(
    surf,
    loop=True,
    lifespan=0.4,
    duration=0.3,
    start_speed=50,
    spread=40,
    movement=movement,
    starting_dir=starting_dir,
    density=2,
)
go = rb.GameObject()
go.add(particleSytem)


def update():
    if rb.Input.mouse_pressed():
        particleSytem.start()
        go.pos = rb.Input.get_mouse_pos()
    else:
        particleSytem.stop()


main_go = rb.GameObject(pos=rb.Display.center)

lifespan = 1
start_speed = 2
start_rotation = 0
start_scale = 1
duration = 2
loop = True
max_particles = rb.Math.INF
spread = 10
density = 1
i = 0
max_i = 10


def make_system():
    global i
    _surf = rb.Surface(scale=(1 / 16, 1 / 16))
    _surf.fill(rb.Color.red.mix(rb.Color.purple, i / max_i))
    args = {
        "surface": _surf.clone(),
        "starting_shape": rb.ParticleSystem.circle_shape(5),
        "starting_dir": rb.ParticleSystem.circle_direction(),
        "z_index": 1,
        ##############################################
        "lifespan": lifespan,
        "start_speed": start_speed,
        "start_rotation": start_rotation,
        "start_scale": start_scale,
        "duration": duration,
        "loop": loop,
        "max_particles": max_particles,
        "spread": spread,
        "density": density,
    }

    _system = rb.ParticleSystem(
        **args,
        mode=rb.ParticleSystemMode.BURST,
        offset=rb.Vector((i - (max_i / 2)) * 20, -80),
    )
    _system2 = rb.ParticleSystem(
        **args,
        mode=rb.ParticleSystemMode.PINGPONG,
        offset=rb.Vector((i - (max_i / 2)) * 20, -30),
    )
    _system3 = rb.ParticleSystem(
        **args,
        mode=rb.ParticleSystemMode.LOOP,
        offset=rb.Vector((i - (max_i / 2)) * 20, 30),
    )
    _system4 = rb.ParticleSystem(
        **args,
        mode=rb.ParticleSystemMode.RANDOM,
        offset=rb.Vector((i - (max_i / 2)) * 20, 80),
    )
    _system.start()
    _system2.start()
    _system3.start()
    _system4.start()
    main_go.add(_system, _system2, _system3, _system4)
    i += 1


make_system()
lifespan *= 2
make_system()
start_speed *= 2
make_system()
start_rotation += 45
make_system()
start_scale *= 2
make_system()
duration *= 2
make_system()
max_particles = 20
make_system()
spread *= 2
make_system()
density *= 2
make_system()
loop = not loop
make_system()

s.fixed_update = update
s.add(go, main_go)
rb.begin()
