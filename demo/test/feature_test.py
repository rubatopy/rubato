"""A place to test new WIP features"""
import rubato as rb

rb.init(res=(1080, 1080), window_size=(2000, 2000))

main = rb.Scene()


def on_click():
    print("Button clicked!")


def on_release():
    print("Button released!")


def on_hover():
    print("Mouse entered button!")


def on_exit():
    print("Mouse exited button!")


button = rb.Button(
    50,
    50,
    on_click,
    on_release,
    on_hover,
    on_exit,
)

rect = rb.Raster(50, 50)
rect.fill(rb.Color(255, 0, 0))

go = rb.GameObject()
go.add(button, rect)

main.add(go)
rb.begin()
