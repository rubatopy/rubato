"""
The platformer example tutorial

Requires rubato 2.1.0 or later.
"""
import rubato as rb

# initialize a new game
rb.init(
    name="Platformer Demo",  # Set a name
    res=(1920, 1080),  # Increase the window resolution
    window_size=(2880, 1620),  # Set the window size
)

import main_menu
import level1
import level2

# Change the global debug level
# rb.Game.debug = True
# rb.Game.show_fps = True
# rb.Game.current().camera.zoom = 1

rb.Game.set_scene("main_menu")

##### SCENE SETUP #####

# begin the game
rb.begin()
