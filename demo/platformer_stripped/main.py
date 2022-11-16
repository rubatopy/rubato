"""
The platformer example tutorial
"""
import rubato as rb

# initialize a new game
rb.init(
    name="Platformer Demo",  # Set a name
    res=(1920, 1080),  # Increase the window resolution
    fullscreen="desktop",  # Set the window to fullscreen
)

import main_menu
import level1

# Change the global debug level
# rb.Game.debug = True
# rb.Game.show_fps = True
# rb.Game.current().camera.zoom = 1

rb.Game.set_scene("main_menu")

# begin the game
rb.begin()
