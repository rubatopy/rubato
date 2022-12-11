"""
The platformer example tutorial
"""
import rubato as rb

# initialize a new game
rb.init(
    name="Platformer Demo",  # Set a name
    res=(1920, 1080),  # Increase the window resolution
    fullscreen=True,  # Set the window to fullscreen
)
rb.Game.debug = True  # Enable debug mode
import main_menu
import level1
import level2
import end_menu

rb.Game.set_scene("main_menu")

# begin the game
rb.begin()
