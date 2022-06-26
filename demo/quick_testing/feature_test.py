"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb
import sys, os

sys.path.insert(0, os.path.abspath("../"))

rb.init()

main = rb.Scene()

s = rb.Sprite("../sprites/spaceship/spaceship.png", rb.Vector(10, 10), scale=rb.Vector(5, 5), aa=False)


def update():
    s.render()


main.update = update

rb.begin()
