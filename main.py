import pgp as pgp
from pgp import Image, Input, Scene

game = pgp.Game()

scene = Scene()
scene.camera.pos.translate(-100, -100)
game.scene_manager.add_scene(scene)

sprite = Image("./Tinmarr.jpg")


def custom_update():
    sprite.pos.z = 1 - Input.is_pressed("SPACE")


sprite.update = custom_update
scene.add(sprite)


def test_handler():
    print("Yeet")


game.broadcast.add_listener("test", test_handler)
game.broadcast.add_listener("w_down", test_handler)

game.begin()
