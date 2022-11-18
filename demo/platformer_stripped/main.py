import rubato as rb

# initialize a new game
rb.init(
    name="Platformer Demo",  # Set a name
    res=(1920, 1080),  # Set the window resolution (in pixels).
    fullscreen=True,  # Set the window to be fullscreen
)

import main_menu
import level1

rb.Game.set_scene("main_menu")

# begin the game
rb.begin()
