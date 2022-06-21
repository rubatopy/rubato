"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb
import sys, os

sys.path.insert(0, os.path.abspath("../"))

rb.init()

main = rb.Scene()

test = rb.Rectangle(width=20)

main.add(rb.GameObject(pos=rb.Vector(300, 300)).add(test))

def update():
    print(test.get_aabb())

main.update = update

rb.begin()
