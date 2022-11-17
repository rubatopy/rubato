"""A place to test new WIP features"""
import rubato as rb

rb.init(
    res=(1080, 1080),
    window_size=(2000, 2000),
    # fullscreen=True,
    # maximize=True,
)

main = rb.Scene()
a = rb.Image("art/avocado.png", offset=(-250, 0))

a.set_alpha(50)
a.set_colorkey(rb.Color.from_hex("#ecf986"))

b = a.clone()
b.offset.x += 500

main.add(rb.wrap([a, b]))

rb.begin()
