import pgp as pgp
from pgp import Image, Input, Scene, RigidBody, Vector, Time

game = pgp.Game()

scene = Scene()
scene.camera.pos.translate(0, 0)
game.scenes.add(scene)

sprite = Image("./Tinmarr.jpg")
rigid = RigidBody({"pos": Vector(100, 0), "mass": 1, "friction":Vector(0.9, 1)})

def custom_update():
    # sprite.pos.z = 1 - Input.is_pressed("SPACE")

    if Input.is_pressed("="):
        scene.camera.zoom = 2
    elif Input.is_pressed("-"):
        scene.camera.zoom = 0.5
    else:
        scene.camera.zoom = 1

sprite.update = custom_update
scene.add(sprite)
bebe = scene.add(rigid)

def w_handler():
    rigid.velocity.y = -100

def rigid_update():
    rigid.physics()
    if Input.is_pressed("a"):
        rigid.velocity.x = -100
    elif Input.is_pressed("d"):
        rigid.velocity.x = 100
        
    if rigid.pos.y > 350:
        rigid.pos.y = 349

rigid.update = rigid_update
game.radio.listen("w_down", w_handler)

game.radio.listen("EXIT", lambda: print("ya-yeet"))

Time.delayed_call(1000, lambda: print("LOL"))

game.begin()
