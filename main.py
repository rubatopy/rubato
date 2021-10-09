import pgp as PP
from pgp import Sprite, Input, GD
from pgp.scenes import Scene

game = PP.Game()

scene = Scene()
game.scene_manager.add_scene(scene)

sprite = Sprite(100, 100, "./Tinmarr.jpg")

def custom_update():
    sprite.state["show"] = Input.is_pressed("SPACE")

def custom_draw():
    if sprite.state.get("show"): GD.update(sprite.image, sprite.position)

sprite.update = custom_update
sprite.draw = custom_draw
scene.sprites.append(sprite)

def test_handler():
    print("Yeet")

game.broadcast.add_listener("test", test_handler)
game.broadcast.add_listener("w_down", test_handler)

game.begin()
