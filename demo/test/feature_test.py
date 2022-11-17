"""A place to test new WIP features"""
import rubato as rb

rb.init(
    res=(1080, 1080),
    window_size=(2000, 2000),
    fullscreen=True,
    maximize=True,
)

main = rb.Scene()
main.add(rb.wrap(rb.Rectangle(200, 200)))

rb.begin()
