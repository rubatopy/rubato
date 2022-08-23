"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb
from rubato import Vector as V

width, height = 256, 256
speed = 2

rb.init(res=V(width, height), window_size=V(width, height) * 2)
s = rb.Scene()

rect = rb.Polygon(V.poly(5, width // 6), rb.Color.blue, debug=True, offset=V(48, 0))
go = rb.wrap(rect, pos=rb.Display.center, debug=True)

dropper = rb.Rectangle(20, 20, rb.Color.red, debug=True)
rigidbody = rb.RigidBody(gravity=V(0, 100))
extra = rb.wrap([dropper, rigidbody])

font = rb.Font()
font.size = 10
text = rb.Text("Hello World", font)


def update():
    # go.rotation += speed
    # rect.rot_offset += speed

    text.text = f"go.rotation: {go.rotation:.2f}\nrect.offset.x: {rect.offset.x:.2f}\nrect.rot_offset: {rect.rot_offset:.2f}"


def handler(m_event):
    if m_event["mouse_button"] == "mouse 1":
        e = extra.clone()
        e.pos = V(m_event["x"], m_event["y"])
        s.add(e)


rb.Radio.listen(rb.Events.MOUSEDOWN, handler)

s.add(go, rb.wrap(text, pos=V(50, 20)))
s.fixed_update = update

rb.begin()