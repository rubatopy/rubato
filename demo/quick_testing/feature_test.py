"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb
from rubato import Vector as V

width, height = 256, 256
speed = 2
reset = False

rb.init(res=V(width, height), window_size=V(width, height) * 2)
s = rb.Scene()

rect = rb.Rectangle(width / 2, height / 2, rb.Color.blue, debug=True)

go = rb.wrap(rect, pos=rb.Display.center, debug=True)

font = rb.Font()
font.size = 10
text = rb.Text("Hello World", font)


def update():
    global reset
    if rb.Input.key_pressed("q"):
        go.rotation -= speed
    elif rb.Input.key_pressed("e"):
        go.rotation += speed
    elif rb.Input.key_pressed("a"):
        rect.offset.x -= speed
    elif rb.Input.key_pressed("d"):
        rect.offset.x += speed
    elif rb.Input.key_pressed("z"):
        rect.rot_offset -= speed
    elif rb.Input.key_pressed("x"):
        rect.rot_offset += speed

    text.text = f"go.rotation: {go.rotation:.2f}\nrect.offset.x: {rect.offset.x:.2f}\nrect.rot_offset: {rect.rot_offset:.2f}"

    if rb.Input.key_pressed("escape"):
        rb.init()


s.add(go, rb.wrap(text, pos=V(50, 20)))
s.fixed_update = update

rb.begin()