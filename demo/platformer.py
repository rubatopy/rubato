"""
The platformer example tutorial

Requires rubato 2.1.0 or later.
"""
import rubato as rb

# initialize a new game
rb.init(
    name="Platformer Demo",  # Set a name
    res=rb.Vector(1920, 1080),  # Increase the window resolution
)

# Change the global debug level
# rb.Game.debug = True
# rb.Game.show_fps = True

# Tracks the grounded state of the player
grounded = False
# Tracks the number of jumps the player has left
jumps = 0
# size of level
level_size = int(rb.Display.res.x * 1.2)

# create the scene for level one
main = rb.Scene(background_color=rb.Color.cyan.lighter())

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

# define a collision handler
won = False
retry_allowed = True


def player_collide(col_info: rb.Manifold):
    global jumps, grounded, won, retry_allowed
    if col_info.shape_b.tag == "ground" and not grounded and player_body.velocity.y >= 0:
        grounded = True
        jumps = 2
        p_animation.set_state("idle", True)
    if col_info.shape_b.tag == "retry_collider":
        if retry_allowed:
            print("r to retry")
            retry_allowed = False

            def re_allow():
                global retry_allowed
                retry_allowed = True

            rb.Time.delayed_call(re_allow, 2000)
    if col_info.shape_b.tag == "portal":
        if not won:
            print("WIN!")
            won = True


# add a hitbox to the player with the collider
player.add(rb.Rectangle(width=40, height=64, tag="player"))
# add a ground detector
player.add(rb.Rectangle(
    width=34,
    height=2,
    offset=rb.Vector(0, 32),
    trigger=True,
    on_collide=player_collide,
))

# define the player rigidbody
player_body = rb.RigidBody(gravity=rb.Vector(y=rb.Display.res.y * 1.5), pos_correction=1)
player.add(player_body)

# Side boundary
left = rb.GameObject(pos=rb.Display.center_left - rb.Vector(25, 0))
left.add(rb.Rectangle(width=50, height=rb.Display.res.y))
right = rb.GameObject(pos=rb.Display.center_left + rb.Vector(level_size + 25, 0))
right.add(rb.Rectangle(width=50, height=rb.Display.res.y))

# create the ground
ground = rb.GameObject()
ground.add(rb.Rectangle(width=level_size, height=50, color=rb.Color.green, tag="ground"))
ground.get(rb.Rectangle).bottom_left = rb.Display.bottom_left

# create platforms
platforms = [
    rb.GameObject(pos=rb.Vector(
        200,
        rb.Display.bottom - 140,
    )).add(rb.Rectangle(
        width=90,
        height=40,
        tag="ground",
        color=rb.Color.blue,
    )),
    rb.GameObject(pos=rb.Vector(
        400,
        rb.Display.bottom - 340,
    )).add(rb.Rectangle(
        width=150,
        height=40,
        tag="ground",
        color=rb.Color.blue,
    )),
]

# create obstacles
obstacles = [
    rb.GameObject(pos=rb.Vector(700)).add(rb.Rectangle(
        width=90,
        height=500,
        tag="ground",
        color=rb.Color.purple,
    )),
    rb.GameObject(pos=rb.Vector(1200)).add(rb.Rectangle(
        width=70,
        height=450,
        tag="ground",
        color=rb.Color.purple,
    )),
]

for obstacle in obstacles:
    obstacle.get(rb.Rectangle).bottom = rb.Display.bottom - 30

# create triggers
triggers = [
    rb.GameObject(pos=rb.Vector(
        950,
        rb.Display.bottom - 45,
    )).add(rb.Rectangle(
        width=400,
        height=30,
        tag="retry_collider",
        trigger=True,
    )),
]

# Create animation for portal
all_portal_images = rb.Spritesheet(
    path="files/portals/portal1_spritesheet.png",
    sprite_size=rb.Vector(32, 32),
    grid_size=rb.Vector(8, 1),
)

portal_animation = rb.Animation(scale=rb.Vector(4, 4), fps=2)
portal_animation.add_spritesheet("", all_portal_images, to_coord=all_portal_images.end)

# create the end portal
portal = rb.GameObject(pos=rb.Display.bottom_left + rb.Vector(level_size - 50, -100))
portal.add(portal_animation)

portal.add(
    rb.Rectangle(
        trigger=True,
        tag="portal",
        width=portal_animation.anim_frame().get_size().x,
        height=portal_animation.anim_frame().get_size().y,
    )
)

# add them all to the scene
main.add(player, ground, left, right, portal, *platforms, *obstacles, *triggers)


# define a custom update function
# this function is run every frame
def update():
    global grounded

    move_axis = rb.Input.controller_axis(rb.Input.controllers - 1, 0)
    centered = rb.Input.axis_centered(move_axis)

    # check for user directional input
    if rb.Input.key_pressed("a") or (move_axis < 0 and not centered):
        player_body.velocity.x = -300
        p_animation.flipx = True
        if grounded:
            if rb.Input.key_pressed("shift") or rb.Input.key_pressed("s"):
                p_animation.set_state("sneak", True)
            else:
                p_animation.set_state("run", True)
    elif rb.Input.key_pressed("d") or (move_axis > 0 and not centered):
        player_body.velocity.x = 300
        p_animation.flipx = False
        if grounded:
            if rb.Input.key_pressed("shift") or rb.Input.key_pressed("s"):
                p_animation.set_state("sneak", True)
            else:
                p_animation.set_state("run", True)
    else:
        player_body.velocity.x = 0
        if grounded:
            if rb.Input.key_pressed("shift") or rb.Input.key_pressed("s"):
                p_animation.set_state("crouch", True)
            else:
                p_animation.set_state("idle", True)

    if rb.Input.key_pressed("r") or rb.Input.controller_button(rb.Input.controllers - 1, 6):
        player.pos = rb.Display.center_left + rb.Vector(50, 0)
        player.get(rb.RigidBody).velocity = rb.Vector.zero()
        grounded = False

    if rb.Input.key_pressed("space"):
        player_body.ang_vel += 10


# define a custom fixed update function
def fixed_update():
    # have the camera follow the player
    camera_ideal = rb.Math.clamp(
        player.pos.x + rb.Display.res.x / 4, rb.Display.center.x, level_size - rb.Display.res.x / 2
    )
    rb.Game.camera.pos.x = rb.Math.lerp(rb.Game.camera.pos.x, camera_ideal, rb.Time.fixed_delta / 0.4)


# set the scene's update function
main.update = update
main.fixed_update = fixed_update


# define a custom input listener
def handle_keydown(event):
    global jumps, grounded
    if event["key"] == "w" and jumps > 0:
        grounded = False
        player_body.velocity.y = -800
        if jumps == 2:
            p_animation.set_state("jump", freeze=2)
        elif jumps == 1:
            p_animation.set_state("somer", True)
        jumps -= 1
    if event["key"] == "1":
        rb.Game.camera.zoom = 1
    if event["key"] == "2":
        rb.Game.camera.zoom = 2
    if event["key"] == "3":
        rb.Game.camera.zoom = .5


# define a custom controller listener
def handle_controller_button(event):
    if event["button"] == 0:
        handle_keydown({"key": "w"})


rb.Radio.listen(rb.Events.KEYDOWN, handle_keydown)

rb.Radio.listen(rb.Events.JOYBUTTONDOWN, handle_controller_button)

# begin the game
rb.begin()
