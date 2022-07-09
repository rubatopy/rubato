"""A place to test new WIP features"""  # pylint: disable=all
from ast import In
import rubato as rb
from rubato.utils.rb_input import Input

rb.init(fullscreen="desktop")

main = rb.Scene()


def update():
    rb.Draw.circle(rb.Display.center, 100, rb.Color.red, 0, rb.Color.green)
    if rb.Input.key_pressed("1"):
        rb.Display.set_fullscreen(True, "desktop")
    elif rb.Input.key_pressed("2"):
        rb.Display.set_fullscreen(True, "exclusive")
    elif rb.Input.key_pressed("3"):
        rb.Display.set_fullscreen(False)


main.update = update

rb.begin()
