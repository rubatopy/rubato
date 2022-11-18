import rubato as rb

# initialize a new game
rb.init(
    name="Platformer Demo",  # Set a name
    res=(1920, 1080),  # Set the window resolution (in pixels).
    fullscreen=True,  # Set the window to be fullscreen
)

import shared

main = rb.Scene(background_color=rb.Color.cyan.lighter())

# Add the player to the scene
main.add(shared.player)

# begin the game
rb.begin()
