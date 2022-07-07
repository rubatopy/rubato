"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb

rb.init()

main = rb.Scene()

s = rb.Sprite("../sprites/spaceship/spaceship.png", scale=rb.Vector(5, 5), aa=False)


def update():
    rb.Draw.sprite(s, rb.Vector(150, 150), 0)


main.update = update

rb.begin()
