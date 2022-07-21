"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb

# initialize a new game
rb.init(
    name="Platformer Demo",  # Set a name
    res=rb.Vector(1920, 1080),  # Increase the window resolution
)

rb.Game.debug = True

grounded = False
# Tracks the number of jumps the player has left
jumps = 2
# size of level
level_size = rb.Display.res.x * 1.2

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
    gravity=rb.Vector(y=rb.Display.res.y * 1.5),
    pos_correction=1,
    friction=0.8,
)
player.add(player_body)


def player_collide(col_info: rb.Manifold):
    global jumps, grounded
    if col_info.shape_b.tag == "ground" and not grounded and player_body.velocity.y >= 0:
        grounded = True
        jumps = 2
        p_animation.set_current_state("idle", True)


# add a hitbox to the player with the collider
player.add(rb.Rectangle(width=64, height=64, tag="player"))  # This line should already be in your code
# add a ground detector
player.add(rb.Rectangle(
    width=10,
    height=2,
    offset=rb.Vector(0, 32),
    trigger=True,
    on_collide=player_collide,
))

# create the ground
ground = rb.GameObject()
ground.add(rb.Rectangle(width=level_size, height=50, color=rb.Color.green, tag="ground"))
ground.get(rb.Rectangle).bottom_left = rb.Display.bottom_left

# create platforms
platforms = [
    rb.GameObject(pos=rb.Vector(200, rb.Display.bottom - 140)
                 ).add(rb.Rectangle(
                     width=90,
                     height=40,
                     tag="ground",
                     color=rb.Color.blue,
                 )),
    rb.GameObject(pos=rb.Vector(400, rb.Display.bottom - 340)
                 ).add(rb.Rectangle(
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

# Side boundary
left = rb.GameObject(pos=rb.Display.center_left - rb.Vector(25, 0))
left.add(rb.Rectangle(width=50, height=rb.Display.res.y))
right = rb.GameObject(pos=rb.Display.center_left + rb.Vector(level_size + 25, 0))
right.add(rb.Rectangle(width=50, height=rb.Display.res.y))

# add them all to the scene
main.add(player, ground, left, right, *platforms, *obstacles)


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
            p_animation.set_current_state("jump", freeze=2)
        elif jumps == 1:
            p_animation.set_current_state("somer", True)
        jumps -= 1


rb.Radio.listen("KEYDOWN", handle_keydown)

# begin the game
rb.begin()
