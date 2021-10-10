import pgp as pgp
from pgp import Image, Input, Scene, RigidBody, Vector

game = pgp.Game()

scene = Scene()
scene.camera.pos.translate(0, 0)
game.scenes.add(scene)

sprite = Image("./Tinmarr.jpg")


rigidboy = RigidBody({"pos": Vector(100, 0), "mass": 100})

def custom_update():
    # sprite.pos.z = 1 - Input.is_pressed("SPACE")

    if Input.is_pressed("w"):
        scene.camera.zoom = 2
    elif Input.is_pressed("s"):
        scene.camera.zoom = 0.5
    else:
        scene.camera.zoom = 1


sprite.update = custom_update
scene.add(sprite)
bebe = scene.add(rigidboy)


def test_handler():
    rigidboy.velocity.y = -50


game.radio.listen("w_down", test_handler)

game.begin()
