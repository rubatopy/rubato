"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb
from rubato import Vector as V
from rubato.utils.vector import Vector

rb.init(res=V(256, 256), window_size=V(256, 256) * 2)
rb.Game.show_fps = True
s = rb.Scene()

surf = rb.Surface(31, 31, scale=(1 / 8, 1 / 8))
surf.draw_circle((15, 15), 15, fill=rb.Color.red.darker(50))


def movement(p: rb.Particle, dt: float):
    p.pos += p.velocity.lerp(Vector.up() * p.velocity.magnitude, p.age / p.lifespan) * dt
    p.surface.draw_circle(
        (15, 15),
        15,
        fill=rb.Color.red.darker(50).mix(rb.Color.orange.lighter(50), p.age / p.lifespan, "linear"),
    )


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


def update():
    if rb.Input.mouse_pressed():
        particleSytem.start()
        go.pos = rb.Input.get_mouse_pos()
    else:
        particleSytem.stop()


rb.Radio.listen(rb.Events.KEYDOWN, lambda _: print(particleSytem.num_particles))

s.fixed_update = update
s.add(go)
rb.begin()
