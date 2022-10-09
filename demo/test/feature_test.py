"""A place to test new WIP features"""
import rubato as rb

rb.init(res=(100, 100), window_size=(200, 200))

a = rb.KeyResponse(1, "a", "b", 1, 2)
print(a.timestamp)
print(a.keys())

b = {"wow": 1}
print(b.keys())

# rb.begin()
