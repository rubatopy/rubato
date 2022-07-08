"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb

# initialize a new game
rb.init(
    name="Platformer Demo",  # Set a name
    window_size=rb.Vector(960, 540),  # Set the window size
    res=rb.Vector(1920, 1080),  # Increase the window resolution
)

rb.Game.debug = True

# Tracks the number of jumps the player has left
jumps = 2

# Create a scene
main = rb.Scene(background_color=rb.Color.cyan.lighter())

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
p_animation.fps = 10  # The frames will change 10 times a second
player.add(p_animation)  # Add the animation component to the player

# define the player rigidbody
player_body = rb.RigidBody(
    gravity=rb.Vector(y=rb.Display.res.y * 0.05),
    pos_correction=1,
    friction=0.8,
)
player.add(player_body)

# add a hitbox to the player with the collider
player.add(rb.Rectangle(
    width=64,
    height=64,
    tag="player",
))

# Add the player to the scene
main.add(player)


# define a custom update function
# this function is run every frame
def update():
    if rb.Input.key_pressed("a"):
        player_body.velocity.x = -300
        p_animation.flipx = True
    elif rb.Input.key_pressed("d"):
        player_body.velocity.x = 300
        p_animation.flipx = False
    else:
        player_body.velocity.x = 0

    if rb.Input.key_pressed("space"):
        player_body.ang_vel += 10


main.update = update


# define a custom input listener
def handle_keydown(event):
    global jumps
    if event["key"] == "w" and jumps > 0:
        player_body.velocity.y = -200
        if jumps == 2:
            p_animation.set_current_state("jump", freeze=2)
        elif jumps == 1:
            p_animation.set_current_state("somer", True)
        jumps -= 1


rb.Radio.listen("KEYDOWN", handle_keydown)

# begin the game
rb.begin()
