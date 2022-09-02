"""A particles demo"""
import rubato as rb
from rubato import Vector as V
from rubato.utils.vector import Vector

rb.init(res=V(128, 128), window_size=V(256, 256) * 2)
rb.Game.show_fps = True
s = rb.Scene()

surf = rb.Surface(scale=(1 / 16, 1 / 16))
surf.draw_circle((16, 16), 16, fill=rb.Color.turquoize)

surf2 = rb.Surface(scale=(1 / 16, 1 / 16))
surf2.draw_circle((16, 16), 16, fill=rb.Color.purple)

surf3 = rb.Surface(scale=(1 / 16, 1 / 16))
surf3.fill(rb.Color.green)


def movement(p: rb.Particle, dt: float):
    p.surface.set_alpha(round(255 * (1 - (p.age / p.lifespan))))
    rb.Particle.default_movement(p, dt)


particleSytem = rb.ParticleSystem(
    new_particle=rb.ParticleSystem.particle_gen(
        surf, movement, acceleration=(0, -75), start_speed=12, lifespan=0.4, z_index=1
    ),
    loop=True,
    duration=0.3,
    spread=5,
    density=2,
    running=True,
)
go = rb.GameObject()
go.add(particleSytem)

go.pos = rb.Display.center

mouse = go.clone()
mouse.get(rb.ParticleSystem).new_particle = rb.ParticleSystem.particle_gen(
    surf2, movement, acceleration=(0, -75), start_speed=12, lifespan=0.4, z_index=1
)

rotator = rb.GameObject(pos=rb.Display.center)

rotatorSystem = rb.ParticleSystem(
    rb.ParticleSystem.particle_gen(surf3, start_speed=50),
    mode=rb.ParticleSystemMode.BURST,
    loop=True,
    running=True,
    duration=0.1,
    spread=60,
    local_space=True,
)

rotator.add(rotatorSystem)


def fixed():
    rotatorSystem.rot_offset += 1
    rotator.rotation -= 0.5

    mouse.pos = rb.Input.get_mouse_pos()
    mouse.get(rb.ParticleSystem).running = rb.Input.mouse_pressed()


def keydown_handler(info):
    if info["key"] == "space":
        rotatorSystem.local_space = not rotatorSystem.local_space


rb.Radio.listen(rb.Events.KEYDOWN, keydown_handler)

s.add(go, mouse, rotator)
s.fixed_update = fixed
rb.begin()
