"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb

# initialize a new game
rb.init(
    name="Platformer Demo",  # Set a name
    window_size=rb.Vector(960, 540),  # Set the window size
    background_color=rb.Color.cyan.lighter(),  # Set the background color
    res=rb.Vector(1920, 1080),  # Increase the window resolution
)

# Create a scene
main = rb.Scene()

# Create the player and set its starting position
player = rb.GameObject(
    pos=rb.Display.center_left + rb.Vector(50, 0),
    z_index=1,
)

# Create animation and initialize states
p_animation = rb.Spritesheet.from_folder(
    rel_path="platformer_files/dino",
    sprite_size=rb.Vector(24, 24),
    default_state="idle",
)
p_animation.scale = rb.Vector(4, 4)
p_animation.fps = 10 # The frames will change 10 times a second
player.add(p_animation) # Add the animation component to the player

# Add the player to the scene
main.add(player)

# begin the game
rb.begin()
