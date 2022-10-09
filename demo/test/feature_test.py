"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb

rb.init(res=(100, 100), window_size=(2000, 2000))

a = rb.KeyResponse(1, "a", "b", 1, 2)
print(a.timestamp)
print(a.keys())

b = {"wow": 1}
print(b.keys())

# rb.begin()
