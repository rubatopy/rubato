"""Draw Demo"""
import rubato as rb

rb.init(res=(96, 64), window_size=(960, 640))

c = rb.Camera()

rb.Game.show_fps = True


def draw():
    rb.Draw.queue_pixel((-32, 16), camera=c)
    rb.Draw.queue_line((16, 0), (-16, 32), camera=c)
    rb.Draw.queue_rect((32, 16), 32, 32, fill=rb.Color.red, camera=c)
    rb.Draw.queue_circle((-32, -16), 16, fill=rb.Color.red, camera=c)
    rb.Draw.queue_poly(rb.Vector.poly(5, 16), rb.Vector(0, -16), fill=rb.Color.red, camera=c)


rb.Game.draw = draw

rb.Time.recurrent_call(lambda: print(rb.Draw._cache_size()), 1)

rb.begin()
