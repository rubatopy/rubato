"""A place to test new WIP features"""  # pylint: disable=all
import sys, os

sys.path.insert(0, os.path.abspath("../"))

import rubato as rb

rb.init({"res": rb.Vector(600, 600)})

main = rb.Scene()
rb.Game.scenes.add(main, "main")

player = rb.GameObject({
    "pos": rb.Display.center_left + rb.Vector(50, 0),
    "z_index": 1,
})

# Add shadow
p_shadow = rb.Image({"rel_path": "sprites/dino/shadow.png", "scale_factor": rb.Vector(4, 4)})
player.add(p_shadow)

# Load various spritesheets
blue_dino_main = rb.Spritesheet(
    {
        "rel_path": "sprites/dino/DinoSprites - blue.png",
        "sprite_size": rb.Vector(24, 24),
        "grid_size": rb.Vector(24, 1)
    }
)

# Create animation and initialize states
p_animation = rb.Spritesheet.from_folder("sprites/dino/blue", rb.Vector(24, 24))
p_animation.add_spritesheet("crouch_idle", blue_dino_main, rb.Vector(17, 0), rb.Vector(19, 0))
p_animation.add_spritesheet("crouch_run", blue_dino_main, rb.Vector(20, 0), rb.Vector(23, 0))
p_animation.scale(rb.Vector(4, 4))
p_animation.fps = 10
player.add(p_animation)


def update():
    pass


def listener(info):
    if info["key"] == "space":
        main.add(player)


rb.Radio.listen("KEYDOWN", listener)

main.update = update

rb.begin()
