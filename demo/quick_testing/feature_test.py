"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb

rb.init(fullscreen="desktop")

main = rb.Scene()


def update():
    rb.Draw.indexed_circle(rb.Display.center, 100, rb.Color.red, 0, rb.Color.green)
    if rb.Input.key_pressed("1"):
        rb.Display.set_fullscreen(True, "desktop")
    elif rb.Input.key_pressed("2"):
        rb.Display.set_fullscreen(True, "exclusive")
    elif rb.Input.key_pressed("3"):
        rb.Display.set_fullscreen(False)


main.update = update

rb.begin()
