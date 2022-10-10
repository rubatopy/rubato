"""Draw Demo"""  # pylint: disable=all
import rubato as rb

rb.init(res=(96, 64), window_size=(960, 640))

c = rb.Camera()

rb.Game.show_fps = True


def draw():
    rb.Draw.queue_point((16, 16), camera=c)
    rb.Draw.queue_line((32, 0), (64, 31), camera=c)
    rb.Draw.queue_rect((64 + 16, 16), 32, 32, fill=rb.Color.red, camera=c)
    rb.Draw.queue_circle((16, 32 + 16), 16, fill=rb.Color.red, camera=c)
    rb.Draw.queue_poly(rb.Vector.poly(5, 16), rb.Vector(32 + 16, 32 + 16), fill=rb.Color.red, camera=c)


rb.Game.draw = draw

rb.Time.recurred_call(1000, lambda: print(rb.Draw._cache_size()))

rb.begin()
