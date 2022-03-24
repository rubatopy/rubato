"""
Step 1 of the Platformer Tutorial.
"""
import rubato as rb

# initialize a new game
rb.init(
    {
        "name": "Platformer Demo",  # Set a name
        "window_size": rb.Vector(960, 540),  # Set the window size
        "background_color": rb.Color.cyan.lighter(),  # Set the background color
        "res": rb.Vector(1920, 1080),  # Increase the window resolution
    }
)

# begin the game
rb.begin()
