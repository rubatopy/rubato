"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb
from rubato import Vector as V

rb.init(res=V(256, 256), window_size=V(256, 256) * 2)
s = rb.Scene()

surf = rb.Surface(5, 5)
surf.draw_rect(V(0, 0), V(32, 32), fill=rb.Color.blue)

particleSytem = rb.ParticleSystem(
    surf,
    loop=True,
    duration=0.1,
    start_speed=20,
    spread=10,
)

particleSytem.start()


def update():
    # return
    particleSytem.rot_offset += 1


s.update = update
s.add(rb.wrap(particleSytem, pos=rb.Display.center))
rb.begin()
