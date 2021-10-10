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

    if Input.is_pressed("="):
        scene.camera.zoom = 2
    elif Input.is_pressed("-"):
        scene.camera.zoom = 0.5
    else:
        scene.camera.zoom = 1


sprite.update = custom_update
scene.add(sprite)
bebe = scene.add(rigidboy)


def w_handler():
    rigidboy.velocity.y = -100

def a_handler():
    rigidboy.velocity.x = -100

def d_handler():
    rigidboy.velocity.x = 100

game.radio.listen("w_down", w_handler)
game.radio.listen("a_down", a_handler)
game.radio.listen("d_down", d_handler)

game.begin()
