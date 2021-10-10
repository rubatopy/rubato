import pgp as pgp
from pgp import Image, Input, Scene, RigidBody, Point

game = pgp.Game()

scene = Scene()
scene.camera.pos.translate(0, 0)
game.scenes.add(scene)

sprite = Image("./Tinmarr.jpg")

rigidboy = RigidBody({"pos": Point(100, 0, 0), "mass": 100})

def custom_update():
    # sprite.pos.z = 1 - Input.is_pressed("SPACE")

    if Input.is_pressed("w"):
        scene.camera.scale_zoom(1.01)
    elif Input.is_pressed("s"):
        scene.camera.scale_zoom(0.99)


sprite.update = custom_update
scene.add(sprite)
scene.add(rigidboy)

game.begin()
