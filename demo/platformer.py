"""The platformer example tutorial"""
import os
import sys

sys.path.insert(0, os.path.abspath("../"))
# pylint: disable=wrong-import-position

jumps = 0

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

# create the scene for level one
main = rb.Scene()
rb.Game.scenes.add(main, "main")

# create the player
player = rb.GameObject({
    "pos": rb.Display.center_left + rb.Vector(50, 0),
})


# define a collision handler
def player_collide(col_info: rb.ColInfo):
    global jumps
    if col_info.shape_b.tag == "ground":
        jumps = 2


# add a hitbox to the player with the collider
player.add(rb.Rectangle({"width": 50, "height": 50, "color": rb.Color.purple.darker()}))
# add a ground detector
player.add(
    rb.Rectangle({
        "width": 50,
        "height": 3,
        "offset": rb.Vector(0, 25),
        "trigger": True,
        "on_collide": player_collide
    })
)

# define the player rigidbody
player_body = rb.RigidBody({"gravity": rb.Vector(0, 1000)})
player.add(player_body)

# create the ground
ground = rb.GameObject({"pos": rb.Display.bottom_center})
ground.add(rb.Rectangle({"width": rb.Display.res.x, "height": 50, "color": rb.Color.green, "tag": "ground"}))

# create the ground
ground = rb.GameObject({"pos": rb.Display.bottom_center})
ground.add(rb.Rectangle({"width": rb.Display.res.x, "height": 50, "color": rb.Color.green, "tag": "ground"}))

# add them all to the scene
main.add(player, ground)


# define a custom update function
def update():
    # have the camera follow the player
    rb.Game.scenes.current.camera.pos.x = max(0, player.pos.x - rb.Display.res.x / 4)

    # check for user directional input
    if rb.Input.key_pressed("a"):
        player_body.velocity.x = -300
    elif rb.Input.key_pressed("d"):
        player_body.velocity.x = 300
    else:
        player_body.velocity.x = 0


# set the scene's update function
main.update = update


# define a custom input listener
def handle_keydown(event):
    global jumps
    if event["key"] == "w" and jumps > 0:
        player_body.velocity.y = -800
        jumps -= 1


rb.Radio.listen("keydown", handle_keydown)

# begin the game
rb.begin()
