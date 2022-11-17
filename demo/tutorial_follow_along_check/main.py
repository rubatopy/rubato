import rubato as rb

rb.init(
    name="Platformer Demo",  # Set a name
    res=rb.Vector(1920, 1080),  # Set the window resolution (pixel length and height).
    fullscreen="desktop",  # Set the window to be fullscreen
)

import level1

# begin the game
rb.begin()