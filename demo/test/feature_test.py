"""A place to test new WIP features"""
import rubato as rb

rb.init(res=(100, 100), window_size=(200, 200))


def listener(event: rb.KeyResponse):
    rb.Radio.broadcast("wow", event.key)


def listener2(event):
    print(event, "wow thats crazy")


rb.Radio.listen(rb.Events.KEYDOWN, listener)
rb.Radio.listen("wow", listener2)
rb.begin()
