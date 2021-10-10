import pgp as pgp
from pgp import Image, Input, Scene, RigidBody, Vector

game = pgp.Game()

scene = Scene()
scene.camera.pos.translate(0, 0)
game.scenes.add(scene)

sprite = Image("./Tinmarr.jpg")

rigidboy = RigidBody({"pos": Vector(100, 0), "mass": 100})

def custom_update():
    sprite.pos.z = 1 - Input.is_pressed("SPACE")


sprite.update = custom_update
scene.add(sprite)
scene.add(rigidboy)

def test_handler():
    print("Yeet")


game.radio.listen("test", test_handler)
game.radio.listen("w_down", test_handler)

game.begin()
