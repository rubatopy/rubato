"""
Step 2 of the Platformer Tutorial.
"""
from rubato import *

# Initialize a new game
init(
    {
        "name": "Platformer Demo",  # Set a name
        "window_size": Vector(960, 540),  # Set the window size
        "background_color": Color.cyan.lighter(),  # Set the background color
        "res": Vector(300, 300),  # Increase the window resolution
    }
)

# Create a scene
main = Scene()
# Add the scene to the scene manager and give it a name
Game.scenes.add(main, "main")

# Create the player
player = GameObject({
    "pos": Display.center_left + Vector(50, 0),  # Set the starting position of the player
})
dino_anim = Spritesheet.from_folder("sprites/dino/blue", Vector(24, 24), "run")
dino_anim.fps = 6
player.add(dino_anim)


def update():
    if Input.key_pressed("p"):
        dino_anim.set_current_state("somer", True)


# Add the player to the scene
main.add(player)
main.update = update

# begin the game
begin()
