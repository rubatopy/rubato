import pgp as PP
from pgp import Sprite, Input, GD
from pgp.scenes import Scene

game = PP.Game()

scene = Scene()
game.scene_manager.add_scene(scene)

sprite = Sprite("./Tinmarr.jpg" ,100, 100, 0)

def custom_update():
    sprite.z_index = 1 - Input.is_pressed("SPACE")

sprite.update = custom_update
scene.sprites.append(sprite)

def test_handler():
    print("Yeet")

game.broadcast.add_listener("test", test_handler)
game.broadcast.add_listener("w_down", test_handler)

game.begin()
