"""A place to test new WIP features"""
import rubato as rb

rb.init(res=(100, 100), window_size=(1000, 1000))
s = rb.Scene()

r = rb.Raster(50, 50)

r.draw_rect((0, 0), (50, 50), rb.Color(255, 255))
r.draw_circle((0, 0), 23, rb.Color(128, 255, 128))
r.draw_poly(rb.Vector.poly(6, 21), (0, 0), rb.Color(0, 128, 255))
r.draw_line((-25, 25), (25, -25), rb.Color(255, 128))
r.draw_point((0, 0), rb.Color(255))

s.add(rb.wrap(r, pos=(0, 0)))
rb.begin()
