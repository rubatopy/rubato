from rubato import *

init()

main = Scene("main")

Image = Image(
    {
        "rel_path": "sprites/dino/blue/crouch.png"
    }
    # rel_path="sprites/dino/blue/crouch.png",
)
dino = GameObject({
    "pos": Display.center
}).add(Image)

main.add(dino)

begin()
