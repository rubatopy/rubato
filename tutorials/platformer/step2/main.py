"""
Step 2 of the Platformer Tutorial.
"""
import rubato as rb

# Initialize a new game
rb.init(
    {
        "name": "Platformer Demo",  # Set a name
        "window_size": rb.Vector(960, 540),  # Set the window size
        "background_color": rb.Color.cyan.lighter(),  # Set the background color
        "res": rb.Vector(1920, 1080),  # Increase the window resolution
    }
)

# Create a scene
main = rb.Scene()
# Add the scene to the scene manager and give it a name
rb.Game.scenes.add(main, "main")

# Create the player
player = rb.GameObject({
    "pos": rb.Display.center_left + rb.Vector(50, 0),  # Set the starting position of the player
})
dino_image = Image({"rel_path": "sprites/dino/shadow.png", "scale_factor": Vector(4, 4)})


# Add the player to the scene
main.add(player)

# begin the game
rb.begin()
