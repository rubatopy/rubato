"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb

rb.init(res=(100, 100), window_size=(2000, 2000))

rb.Scene()

x = 0


def test(task):
    global x
    print(f"test {x} {rb.Time.now()}")
    x += 1
    if x >= 10:
        task.stop()


rb.Time.scheduled_call(1000, test)

rb.begin()
