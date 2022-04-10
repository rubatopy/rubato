"""Text demo for rubato"""
import rubato as rb

rb.init()

main = rb.Scene()
rb.Game.scenes.add(main, "main")

text = rb.Text({
    "font": rb.Font({
        "font": "Fredoka",
        "size": 64,
        "color": rb.Color.white,
    }),
    "text": "hello world",
})

rect = rb.Rectangle({"width": 400, "height": 70, "color": rb.Color.red})

rotating = False


def onclick():
    global rotating
    rotating = True


def onrelease():
    global rotating
    rotating = False


def onhover():
    rect.color = rb.Color.green


def onexit():
    rect.color = rb.Color.red


button = rb.Button(
    {
        "width": rect.width,
        "height": rect.height,
        "onclick": onclick,
        "onrelease": onrelease,
        "onhover": onhover,
        "onexit": onexit,
    }
)

ui = rb.UIElement({"pos": rb.Display.center}).add(rect).add(text).add(button)

main.add(ui)


def update():
    if rotating:
        ui.rotation += 1


main.update = update

rb.begin()
