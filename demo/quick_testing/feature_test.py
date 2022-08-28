"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb
from rubato import Vector as V

rb.init(res=V(256, 256), window_size=V(256, 256) * 2)
rb.Game.show_fps = True
s = rb.Scene()

surf = rb.Surface(31, 31, scale=(1 / 8, 1 / 8))
surf.draw_circle((15, 15), 15, fill=rb.Color.blue)

surf2 = surf.clone()
surf2.draw_rect((0, 0), (31, 31), fill=rb.Color.red)


def movement(particle: rb.Particle, dt: float):
    particle.pos += particle.velocity * dt
    # particle.surface.draw_circle((15, 15), 15, fill=rb.Color.blue.mix(rb.Color.red, particle.age / particle.lifespan))


def start_shape(angle: float):
    return rb.Vector((angle / 360) * 32, 0)


def starting_dir(angle: float):
    return rb.Vector(0, -1)


particleSytem = rb.ParticleSystem(
    surf,
    loop=True,
    duration=0.2,
    start_speed=20,
    spread=5,
    movement=movement,
    starting_shape=start_shape,
    starting_dir=starting_dir,
)

particleSytem.start()


def update():
    # particleSytem.rot_offset += rb.Time.fixed_delta * 360
    pass


rb.Radio.listen(rb.Events.KEYDOWN, lambda _: print(particleSytem.num_particles))

s.fixed_update = update
s.add(rb.wrap(particleSytem, pos=rb.Display.center))
rb.begin()
