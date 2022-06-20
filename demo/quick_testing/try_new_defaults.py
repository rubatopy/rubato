from rubato import *

init()

main = Scene("main")

image = Image(rel_path="sprites/dino/blue/crouch.png", scale=Vector(10, 10))
print(image.scale)
# image.scale = Vector(10, 10)

dino = wrap(image, pos=Display.center)

main.add(dino)

begin()
