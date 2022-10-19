"""A place to test new WIP features"""
import rubato as rb

rb.init(res=(100, 100), window_size=(1000, 1000))

rb.Game.show_fps = True


def update():
    print(rb.Input.get_mouse_pos())


rb.Game.update = update

rb.begin()
