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
        "res": Vector(1920, 1080),  # Increase the window resolution
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
dino_image = Image({"rel_path": "sprites/dino/shadow.png", "scale": Vector(4, 4)})

# Add the player to the scene
main.add(player)

# begin the game
begin()
