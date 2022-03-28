"""The platformer example tutorial"""
import os
import sys

sys.path.insert(0, os.path.abspath("../"))
# pylint: disable=wrong-import-position

# import rubato
import rubato as rb

# initialize a new game
rb.init(
    {
        "name": "Platformer Demo",
        "window_size": rb.Vector(960, 540),
        "background_color": rb.Color.cyan.lighter(),
        "res": rb.Vector(1920, 1080),
    }
)

# Change the global debug level
rb.Game.debug = False

# create the scene for level one
main = rb.Scene()
rb.Game.scenes.add(main, "main")

# Load various spritesheets
blue_dino_main = rb.Spritesheet(
    {
        "rel_path": "sprites/dino/DinoSprites - blue.png",
        "sprite_size": rb.Vector(24, 24),
        "grid_size": rb.Vector(24, 1)
    }
)
blue_dino_jump = rb.Spritesheet(
    {
        "rel_path": "sprites/dino/jump - blue.png",
        "sprite_size": rb.Vector(24, 24),
        "grid_size": rb.Vector(3, 1),
    }
)
blue_dino_somer = rb.Spritesheet(
    {
        "rel_path": "sprites/dino/somer - blue.png",
        "sprite_size": rb.Vector(24, 24),
        "grid_size": rb.Vector(4, 1),
    }
)

# Tracks the grounded state of the player
grounded = False
# Tracks the number of jumps the player has left
jumps = 0

# create the player
player = rb.GameObject({
    "pos": rb.Display.center_left + rb.Vector(50, 0),
    "z_index": 1,
})

# Add shadow
p_shadow = rb.Image({"rel_path": "sprites/dino/shadow.png", "scale_factor": rb.Vector(4, 4)})
player.add(p_shadow)

# Create animation and initialize states
p_animation = rb.Animation({"scale_factor": rb.Vector(4, 4), "fps": 10})
p_animation.add_spritesheet("idle", blue_dino_main, rb.Vector(0, 0), rb.Vector(3, 0))
p_animation.add_spritesheet("running", blue_dino_main, rb.Vector(4, 0), rb.Vector(7, 0))
p_animation.add_spritesheet("jump", blue_dino_jump, rb.Vector(0, 0), rb.Vector(2, 0))
p_animation.add_spritesheet("somer", blue_dino_somer, rb.Vector(0, 0), rb.Vector(3, 0))
player.add(p_animation)


# define a collision handler
def player_collide(col_info: rb.ColInfo):
    global jumps, grounded
    if col_info.shape_b.tag == "ground":
        grounded = True
        if jumps <= 1:
            p_animation.set_current_state("idle", True)
        jumps = 2


# add a hitbox to the player with the collider
player.add(rb.Rectangle({"width": 64, "height": 80}))
# add a ground detector
player.add(
    rb.Rectangle(
        {
            "width": 80,
            "height": 5,
            "offset": rb.Vector(0, 40),
            "trigger": True,
            "on_collide": player_collide,
        }
    )
)

# define the player rigidbody
player_body = rb.RigidBody({"gravity": rb.Vector(0, 1000)})
player.add(player_body)

# Side boundary
left = rb.GameObject({"pos": rb.Display.center_left - rb.Vector(25, 0)})
left.add(rb.Rectangle({"width": 50, "height": rb.Display.res.y}))

# create the ground
ground = rb.GameObject({"pos": rb.Display.bottom_center})
ground.add(rb.Rectangle({"width": rb.Display.res.x * 4, "height": 50, "color": rb.Color.green, "tag": "ground"}))
ground.get(rb.Rectangle).topleft = rb.Display.bottom_left - rb.Vector(0, 25)

# add them all to the scene
main.add(player, ground, left)


# define a custom update function
def update():
    # check for user directional input
    if rb.Input.key_pressed("a"):
        player_body.velocity.x = -300
        p_animation.flipx = True
        if grounded:
            p_animation.set_current_state("running")
    elif rb.Input.key_pressed("d"):
        player_body.velocity.x = 300
        p_animation.flipx = False
        if grounded:
            p_animation.set_current_state("running")
    else:
        player_body.velocity.x = 0
        if grounded:
            p_animation.set_current_state("idle", True)
    p_shadow.visible = grounded


# define a custom fixed update function
def fixed_update():
    # have the camera follow the player
    camera_ideal = max(0, player.pos.x - rb.Display.res.x / 4)
    rb.Game.camera.pos.x = rb.Math.lerp(rb.Game.camera.pos.x, camera_ideal, rb.Time.fixed_delta / 400)


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


rb.Radio.listen("keydown", handle_keydown)

# begin the game
rb.begin()
