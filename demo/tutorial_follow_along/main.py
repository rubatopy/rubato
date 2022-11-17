import rubato as rb

# initialize a new game
main = rb.Scene(background_color=rb.Color.cyan.lighter())

rb.init(
    name="Platformer Demo",  # Set a name
    res=rb.Vector(1920, 1080),  # Set the window resolution (pixel length and height).
    # note that since we didn't also specify a window size,
    # the window will be automatically resized to half of the resolution.
)

import shared

# Add the player to the scene
main.add(shared.player)
# begin the game
rb.begin()
