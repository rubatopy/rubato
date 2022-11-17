import rubato as rb
from player_controller import PlayerController

##### MISC #####

level1_size = int(rb.Display.res.x * 1.2)

##### COLORS #####

platform_color = rb.Color.from_hex("#b8e994")
background_color = rb.Color.from_hex("#82ccdd")
win_color = rb.Color.green.darker(75)

##### PLAYER PREFAB #####

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
    gravity=rb.Vector(y=rb.Display.res.y * -1.5),  # changed to be stronger
    pos_correction=1,
    friction=0.8,
)


player.add(
    # add a hitbox to the player with the collider
    rb.Rectangle(width=40, height=64, tag="player"),
    # add a ground detector
    rb.Rectangle(
        width=34,
        height=2,
        offset=rb.Vector(0, -32),
        trigger=True,
        tag="player_ground_detector",
    ),
    # add a rigidbody to the player
    rb.RigidBody(gravity=rb.Vector(y=rb.Display.res.y * -1.5), pos_correction=1, friction=1),
    # add custom player component
    player_comp := PlayerController(),
)

rb.Game.debug = True

##### SIDE BOUDARIES #####

left = rb.GameObject(pos=rb.Display.center_left - rb.Vector(25, 0)).add(rb.Rectangle(width=50, height=rb.Display.res.y))
right = rb.GameObject().add(rb.Rectangle(width=50, height=rb.Display.res.y))
