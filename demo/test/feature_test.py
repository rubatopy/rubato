"""A place to test new WIP features"""
import rubato as rb

rb.init(res=(1080, 1080), window_size=(2000, 2000))

main = rb.Scene()
main.add(rb.wrap(rb.Rectangle(200, 200)))


def a():
    rb.Display.save_screenshot("wow")


rb.Radio.listen(rb.Events.KEYDOWN, a)

rb.begin()
