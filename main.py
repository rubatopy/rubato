from pgp import Game, Image, Input, Scene, RigidBody, Vector, Time, PMath, Group
from pgp.utils import COL_TYPE

game = Game()

scene = Scene()
scene.camera.pos.translate(0, 0)
game.scenes.add(scene)

group = Group()
scene.add(group)

sprite = Image("./Tinmarr.jpg")
rigid = RigidBody({
    "pos": Vector(100, 0),
    "mass": 1,
    "friction": Vector(0.9, 1),
    "max_speed": Vector(80, PMath.INFINITY),
    "col_type": COL_TYPE.ELASTIC
})

rigid_2 = RigidBody({
    "pos": Vector(200, 300),
    "mass": 1,
    "friction": Vector(1, 1),
    "col_type": COL_TYPE.STATIC,
})


# Sprite
def custom_update():
    if Input.is_pressed("="):
        scene.camera.zoom = 2
    elif Input.is_pressed("-"):
        scene.camera.zoom = 0.5
    else:
        scene.camera.zoom = 1


sprite.update = custom_update
group.add(sprite)


# Rigid
def w_handler():
    rigid.velocity.y = -100


def rigid_update():
    rigid.physics()
    if Input.is_pressed("a"):
        rigid.acceleration.x = -500
    elif Input.is_pressed("d"):
        rigid.acceleration.x = 500
    else:
        rigid.acceleration.x = 0

    if rigid.pos.y > 350:
        rigid.pos.y = 349

    rigid.collider.overlap(rigid_2.collider, False)


rigid.update = rigid_update
rigid.collides_with.append(rigid_2)
game.radio.listen("w_down", w_handler)
group.add(rigid)


# Rigid 2
def rigid_2_update():
    # rigid_2.physics()
    rigid_2.pos = Vector(Input.mouse.get_pos()[0], Input.mouse.get_pos()[1])


rigid_2.update = rigid_2_update
group.add(rigid_2)

game.radio.listen("EXIT", lambda: print("ya-yeet"))

Time.delayed_call(1000, lambda: print("LOL"))

game.begin()
