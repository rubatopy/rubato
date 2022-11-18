import rubato as rb

# initialize a new game
rb.init(
    name="Platformer Demo",  # Set a name
    res=(1920, 1080),  # Set the window resolution (in pixels).
    fullscreen=True,  # Set the window to be fullscreen
)

import level1

# begin the game
rb.begin()
