import PygamePlus as PP
from PygamePlus import Sprite
from PygamePlus.scenes import Scene

game = PP.Game("Amazing Game", 600, 400, True)

scene = Scene()
game.scene_manager.add_scene(scene)

sprite = Sprite(100, 100, "./Tinmarr.jpg")
scene.sprites.append(sprite)

game.begin()
