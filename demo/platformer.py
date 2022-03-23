"""The platformer example tutorial"""
import os
import sys

sys.path.insert(0, os.path.abspath("../"))
# pylint: disable=wrong-import-position

# import rubato
import rubato as rb

# initialize a new game
rb.init()

# create the scene for level one
main = rb.Scene()
rb.Game.scenes.add(main, "main")

# create the player
player = rb.Sprite()
player.add(rb.Rectangle({"width": 50, "height": 50, "color": rb.Color.purple}))

# define the player rigidbody
player_body = rb.RigidBody({"max_speed": rb.Vector(150, rb.Math.INFINITY), "friction": 0.1})
player.add(player_body)

# create the ground
ground = rb.Sprite({"pos": rb.Display.bottom_center})
ground.add(rb.Rectangle({"width": rb.Display.resolution.x, "height": 50, "color": rb.Color.green}))

# add them all to the scene
main.add(player, ground)


# define a custom update function
def update():
    # have the camera follow the player
    rb.Game.scenes.current.camera.pos.x = max(0, player.pos.x - rb.Display.resolution.x / 4)

    # check for user directional input
    if rb.Input.key_pressed("a"):
        player_body.velocity.x -= 40
    if rb.Input.key_pressed("d"):
        player_body.velocity.x += 40


# set the scene's update function
main.update = update

# begin the game
rb.begin()
