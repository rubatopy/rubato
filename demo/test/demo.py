from rubato import *

init(res=Vector(500, 500))

main = Scene()

player = GameObject(name="player", pos=Display.center)
image = Image(rel_path="art/Player1.png")
player.add(image)
main.add(player)


class Coin(Component):
    def __init__(self):
        super().__init__()
        self.image = None

    def setup(self):
        self.image = self.gameobj.get(Image)

    # def update(self):
    #     self.image.offset = Vector(100, 100)


player.add(Coin()).add(Image(rel_path="art/Silver Coin.png", offset=Vector(100, 100)))

speed = 40


def input_update():
    if Input.key_pressed("a"):
        player.pos.x -= speed * Time.delta_time
    if Input.key_pressed("d"):
        player.pos.x += speed * Time.delta_time
    if Input.key_pressed("w"):
        player.pos.y -= speed * Time.delta_time
    if Input.key_pressed("s"):
        player.pos.y += speed * Time.delta_time


def draw_update():
    for i in range(0, Display.res.x, 20):
        Draw.circle(Vector(i, 50))

main.update = input_update
main.draw = draw_update

begin()
