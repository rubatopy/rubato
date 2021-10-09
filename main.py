import PygamePlus as PP
from PygamePlus import Sprite, Input
from PygamePlus.scenes import Scene

game = PP.Game()

scene = Scene()
game.scene_manager.add_scene(scene)

sprite = Sprite(100, 100, "./Tinmarr.jpg")

def custom_update():
    if Input.is_pressed("SPACE"):
        game.broadcast.broadcast_event("test")

sprite.update = custom_update
scene.sprites.append(sprite)

def test_handler():
    print("Yeet")

game.broadcast.add_listener("test", test_handler)
game.broadcast.add_listener("w_down", test_handler)

game.begin()
