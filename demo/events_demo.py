"""A file to test all events"""
import rubato as rb

rb.init()

mainScene = rb.Scene()
rad = 50
val = 0


def scroll(data):
    global rad, val
    rad += data["y"]
    val += data["x"]  # trackpad sideways scrolling.


rb.Radio.listen(rb.Events.MOUSEWHEEL, scroll)


def mouse_down(data):
    if data["button"] == 1:
        go = rb.wrap(rb.Circle(color=rb.Color.blue), pos=rb.Input.get_mouse_pos())
        mainScene.add(go)


rb.Radio.listen(rb.Events.MOUSEDOWN, mouse_down)


def draw():
    color = rb.Color.red.mix(rb.Color.blue, val, "linear")

    rb.Draw.circle(rb.Display.center, rad, color)


mainScene.draw = draw

rb.begin()
