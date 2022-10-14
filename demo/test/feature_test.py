"""A place to test new WIP features"""
import rubato as rb

rb.init(res=(100, 100), window_size=(1000, 1000))

rb.Game.show_fps = True


def draw():
    rb.Draw.rect((0, 0), 1, 1, rb.Color.black, 1, rb.Color.purple)


rb.Game.draw = draw

rb.begin()
