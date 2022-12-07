import rubato as rb

rb.init()

scene = rb.Scene()

text = rb.Text("Hello World!", font := rb.Font(size=32))
text_go = rb.wrap(text)


def update():
    if rb.Input.mouse_pressed():
        text_go.pos = rb.Input.get_mouse_pos()
        font.color = rb.Color.random()


scene.update = update

scene.add(text_go)

rb.begin()
