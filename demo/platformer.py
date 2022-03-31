"""The platformer example tutorial"""
import os
import sys

sys.path.insert(0, os.path.abspath("../"))
# pylint: disable=wrong-import-position

# import rubato
from rubato import *

# initialize a new game
init(
    {
        "name": "Platformer Demo",
        "window_size": Vector(960, 540),
        "background_color": Color.cyan.lighter(),
        "res": Vector(1920, 1080),
    }
)

# Change the global debug level
Game.debug = True

# Tracks the grounded state of the player
grounded = False
# Tracks the number of jumps the player has left
jumps = 0
# size of level
level_size = Display.res.x * 1.2

# create the scene for level one
main = Scene()
Game.scenes.add(main, "main")

# create the player
player = GameObject({
    "pos": Display.center_left + Vector(50, 0),
    "z_index": 1,
})

# Add shadow
p_shadow = Image({"rel_path": "sprites/dino/shadow.png", "scale_factor": Vector(4, 4)})
player.add(p_shadow)

# Load various spritesheets
blue_dino_main = Spritesheet(
    {
        "rel_path": "sprites/dino/DinoSprites - blue.png",
        "sprite_size": Vector(24, 24),
        "grid_size": Vector(24, 1)
    }
)
blue_dino_jump = Spritesheet(
    {
        "rel_path": "sprites/dino/jump - blue.png",
        "sprite_size": Vector(24, 24),
        "grid_size": Vector(3, 1),
    }
)
blue_dino_somer = Spritesheet(
    {
        "rel_path": "sprites/dino/somer - blue.png",
        "sprite_size": Vector(24, 24),
        "grid_size": Vector(4, 1),
    }
)

# Create animation and initialize states
p_animation = Animation({"scale_factor": Vector(4, 4), "fps": 10})
p_animation.add_spritesheet("idle", blue_dino_main, Vector(0, 0), Vector(3, 0))
p_animation.add_spritesheet("running", blue_dino_main, Vector(4, 0), Vector(7, 0))
p_animation.add_spritesheet("jump", blue_dino_jump, Vector(0, 0), Vector(2, 0))
p_animation.add_spritesheet("somer", blue_dino_somer, Vector(0, 0), Vector(3, 0))
p_animation.add_spritesheet("crouch_idle", blue_dino_main, Vector(17, 0), Vector(19, 0))
p_animation.add_spritesheet("crouch_run", blue_dino_main, Vector(20, 0), Vector(23, 0))
player.add(p_animation)

# define a collision handler
won = False
retry_allowed = True


def player_collide(col_info: ColInfo):
    global jumps, grounded, won, retry_allowed
    if col_info.shape_b.tag == "ground" and not grounded:
        grounded = True
        jumps = 2
        p_animation.set_current_state("idle", True)
    if col_info.shape_b.tag == "retry_collider":
        if retry_allowed:
            print("r to retry")
            retry_allowed = False

            def re_allow():
                global retry_allowed
                retry_allowed = True

            Time.delayed_call(Time.sec_to_milli(2), re_allow)
    if col_info.shape_b.tag == "portal":
        if not won:
            print("WIN!")
            won = True


# add a hitbox to the player with the collider
player.add(Rectangle({"width": 64, "height": 48, "offset": Vector(0, -8), "tag": "player"}))
# add a ground detector
player.add(
    Rectangle({
        "width": 63,
        "height": 5,
        "offset": Vector(0, 16),
        "trigger": True,
        "on_collide": player_collide,
    })
)

# define the player rigidbody
player_body = RigidBody({"gravity": Vector(y=Display.res.y * 1.5), "pos_correction": 1})
player.add(player_body)

# Side boundary
left = GameObject({"pos": Display.center_left - Vector(25, 0)})
left.add(Rectangle({"width": 50, "height": Display.res.y}))
right = GameObject({"pos": Display.center_left + Vector(level_size + 25, 0)})
right.add(Rectangle({"width": 50, "height": Display.res.y}))

# create the ground
ground = GameObject()
ground.add(Rectangle({"width": level_size, "height": 50, "color": Color.green, "tag": "ground"}))
ground.get(Rectangle).bottom_left = Display.bottom_left

# create platforms
platforms = [
    GameObject({
        "pos": Vector(200, Display.bottom - 140)
    }).add(Rectangle({
        "width": 90,
        "height": 40,
        "tag": "ground",
        "color": Color.blue
    })),
    GameObject({
        "pos": Vector(400, Display.bottom - 340)
    }).add(Rectangle({
        "width": 150,
        "height": 40,
        "tag": "ground",
        "color": Color.blue
    })),
]

# create obstacles
obstacles = [
    GameObject({
        "pos": Vector(700)
    }).add(Rectangle({
        "width": 90,
        "height": 500,
        "tag": "ground",
        "color": Color.purple
    })),
    GameObject({
        "pos": Vector(1200)
    }).add(Rectangle({
        "width": 70,
        "height": 450,
        "tag": "ground",
        "color": Color.purple
    })),
]

# create triggers

triggers = [
    GameObject({
        "pos": Vector(950, Display.bottom - 45),
    }).add(Rectangle({
        "width": 400,
        "height": 30,
        "tag": "retry_collider",
        "trigger": True
    })),
]

for obstacle in obstacles:
    obstacle.get(Rectangle).bottom = Display.bottom - 30

# Create animation for portal
all_portal_images = Spritesheet(
    {
        "rel_path": "sprites/portals/portal1_spritesheet.png",
        "sprite_size": Vector(32, 32),
        "grid_size": Vector(8, 1)
    }
)
portal_animation = Animation({"scale_factor": Vector(4, 4), "fps": 2})
portal_animation.add_spritesheet("", all_portal_images, to_coord=all_portal_images.end)

# create the end portal
portal = GameObject({"pos": Display.bottom_left + Vector(level_size - 50, -100)})
portal.add(portal_animation)

portal.add(
    Rectangle(
        {
            "trigger": True,
            "tag": "portal",
            "width": portal_animation.anim_frame.get_size().x,
            "height": portal_animation.anim_frame.get_size().y,
        }
    )
)

# add them all to the scene
main.add(player, ground, left, right, portal, *platforms, *obstacles, *triggers)


# define a custom update function
def update():
    global grounded
    # check for user directional input
    if Input.key_pressed("a"):
        player_body.velocity.x = -300
        p_animation.flipx = True
        if grounded:
            if Input.key_pressed("shift") or Input.key_pressed("s"):
                p_animation.set_current_state("crouch_run", True)
            else:
                p_animation.set_current_state("running")
    elif Input.key_pressed("d"):
        player_body.velocity.x = 300
        p_animation.flipx = False
        if grounded:
            if Input.key_pressed("shift") or Input.key_pressed("s"):
                p_animation.set_current_state("crouch_run", True)
            else:
                p_animation.set_current_state("running")
    else:
        player_body.velocity.x = 0
        if grounded:
            if Input.key_pressed("shift") or Input.key_pressed("s"):
                p_animation.set_current_state("crouch_idle", True)
            else:
                p_animation.set_current_state("idle", True)

    if Input.key_pressed("r"):
        player.pos = Display.center_left + Vector(50, 0)
        player.get(RigidBody).velocity = Vector.zero
        grounded = False

    p_shadow.visible = grounded


# define a custom fixed update function
def fixed_update():
    # have the camera follow the player
    camera_ideal = max(0, min(player.pos.x - Display.res.x / 4, level_size - Display.res.x))
    Game.camera.pos.x = Math.lerp(Game.camera.pos.x, camera_ideal, Time.fixed_delta / 400)


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


Radio.listen("keydown", handle_keydown)

# begin the game
begin()
