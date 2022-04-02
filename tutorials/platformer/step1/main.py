"""
Step 1 of the Platformer Tutorial.
"""
from rubato import *

# initialize a new game
init(
    {
        "name": "Platformer Demo",  # Set a name
        "window_size": Vector(960, 540),  # Set the window size
        "background_color": Color.cyan.lighter(),  # Set the background color
        "res": Vector(1920, 1080),  # Increase the window resolution
    }
)

# begin the game
begin()
