"""
The platformer example tutorial

Requires rubato 2.1.0 or later.
"""
import rubato as rb

# initialize a new game
rb.init(
    name="Platformer Demo",  # Set a name
    res=(1920, 1080),  # Increase the window resolution
    window_size=(2880, 1620),  # Set the window size
)

from player import Player
import level1

# Change the global debug level
# rb.Game.debug = True
# rb.Game.show_fps = True

current_scene = level1

##### PLAYER #####

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
    Player(),
)

##### PORTAL #####

# Create animation for portal
all_portal_images = rb.Spritesheet(
    path="files/portals/portal1_spritesheet.png",
    sprite_size=rb.Vector(32, 32),
    grid_size=rb.Vector(8, 1),
)

portal_animation = rb.Animation(scale=rb.Vector(4, 4), fps=2)
portal_animation.add_spritesheet("", all_portal_images, to_coord=all_portal_images.end)

# create the end portal
portal = rb.GameObject(pos=rb.Display.bottom_left + rb.Vector(current_scene.level_size - 50, 100))
portal.add(portal_animation)

portal.add(
    rb.Rectangle(
        trigger=True,
        tag="portal",
        width=portal_animation.anim_frame().size_scaled().x,
        height=portal_animation.anim_frame().size_scaled().y,
        on_collide=lambda col_info: print("You win!") if col_info.shape_b.tag == "player" else None,
    )
)

##### SCENE SETUP #####

level1.scene.add(player, portal)


# define a custom fixed update function
def fixed_update():
    # have the camera follow the player
    camera_ideal = rb.Math.clamp(
        player.pos.x + rb.Display.res.x / 4, rb.Display.center.x, current_scene.level_size - rb.Display.res.x
    )
    rb.Game.current().camera.pos.x = rb.Math.lerp(
        rb.Game.current().camera.pos.x, camera_ideal, rb.Time.fixed_delta / 0.4
    )


# set the scene's update function
level1.scene.fixed_update = fixed_update

# begin the game
rb.begin()
