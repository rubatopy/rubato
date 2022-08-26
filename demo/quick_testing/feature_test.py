"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb
from rubato import Vector as V

width, height = 256, 256
speed = 2

rb.init(res=V(width, height), window_size=V(width, height) * 2)
s = rb.Scene()

rect = rb.Rectangle(width / 2, height / 2, rb.Color.blue, debug=True)
rect2 = rb.Rectangle(width / 4, height / 4, rb.Color.red, debug=True, offset=rb.Vector(5,5), rot_offset=40)

go = rb.wrap(rect, pos=rb.Display.center, debug=True, name="fatty")
go.add(rect2)
print(rect, go)

group = rb.Group()
go2 = go.clone()
go2.pos += rb.Vector.one() * 30
group.add(go, go2)

font = rb.Font()
font.size = 10
text = rb.Text("Hello World", font)
def switch(data):
    if data["key"] == "h":
        go.hidden = not go.hidden
    elif data["key"] == "i":
        rect2.hidden = not rect2.hidden
    elif data["key"] == "o":
        group.hidden = not group.hidden
rb.Radio.listen(rb.Events.KEYDOWN, switch)
def update():
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


s.add(group, rb.wrap(text, pos=V(50, 20)))
s.fixed_update = update

rb.begin()