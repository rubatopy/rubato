"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb

rb.init(res=(100, 100), window_size=(2000, 2000))

rb.Scene()

x = 0
y = 0


def test(task):
    global x
    print(f"test {x} {rb.Time.now()}")
    x += 1
    if x >= 10:
        task.stop()


def test2():
    global y
    print(f"test2 {y} {rb.Time.now()}")
    y += 1


rb.Time.recurred_call(500, test)
rb.Time.recurred_call(500, test2)

rb.begin()
