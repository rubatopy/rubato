import rubato as rb
from player_controller import PlayerController
# Create the player and set its starting position
player = rb.GameObject(
    pos=rb.Display.center_left + rb.Vector(50, 0),
    z_index=1,
)

# Create animation and initialize states
p_animation = rb.Spritesheet.from_folder(
    path="files/dino",
    sprite_size=rb.Vector(24, 24),
    default_state="idle",
)
p_animation.scale = rb.Vector(4, 4)
p_animation.fps = 10  # The frames will change 10 times a second
player.add(p_animation)  # Add the animation component to the player

# define the player rigidbody
player_body = rb.RigidBody(
    gravity=rb.Vector(y=rb.Display.res.y * -0.05),
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
player.add(player_comp := PlayerController())
rb.Game.debug = True