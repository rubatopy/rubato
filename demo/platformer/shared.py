import rubato as rb
from player import Player

black_32 = rb.Font(size=32)

##### PLAYER #####

# Create the player
player = rb.GameObject(z_index=1)

# Create animation and initialize states
p_animation = rb.Spritesheet.from_folder(
    path="files/dino",
    sprite_size=rb.Vector(24, 24),
    default_state="idle",
)
p_animation.scale = rb.Vector(4, 4)
p_animation.fps = 10  # The frames will change 10 times a second
player.add(p_animation)  # Add the animation component to the player

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
    rb.RigidBody(gravity=rb.Vector(y=rb.Display.res.y * -1.5), pos_correction=1),
    # add custom player component
    player_comp := Player(),
)

##### PORTAL #####

# Create animation for portal
all_portal_images = rb.Spritesheet(
    path="files/portals/portal1_spritesheet.png",
    sprite_size=rb.Vector(32, 32),
    grid_size=rb.Vector(8, 1),
)

portal_animation = rb.Animation(scale=rb.Vector(4, 4), fps=10)
portal_animation.add_spritesheet("", all_portal_images, to_coord=all_portal_images.end)

# create the end portal
portal = rb.GameObject()
portal.add(portal_animation)

portal.add(
    rb.Rectangle(
        trigger=True,
        tag="portal",
        width=portal_animation.anim_frame().size_scaled().x,
        height=portal_animation.anim_frame().size_scaled().y,
    )
)

##### SIDE BOUDARIES #####
left = rb.GameObject(pos=rb.Display.center_left - rb.Vector(25, 0)).add(rb.Rectangle(width=50, height=rb.Display.res.y))
right = rb.GameObject().add(rb.Rectangle(width=50, height=rb.Display.res.y))
