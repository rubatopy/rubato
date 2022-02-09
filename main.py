# pylint: disable=all
from rubato import (
    Image,
    Input,
    Scene,
    RigidBody,
    Vector,
    Time,
    Math,
    Group,
    Polygon,
    SAT,
    COL_TYPE,
    Radio,
)
import rubato as rb

rb.init()

scene = Scene()
scene.camera.pos.translate(0, 0)
rb.game.scenes.add(scene)

group = Group()
scene.add(group)

sprite = Image({"image_location": "", "pos": Vector(300, 200)})
rigid = RigidBody({
    "pos": Vector(200, 0),
    "mass": 1,
    "friction": Vector(1, 1),
    "max_speed": Vector(100, Math.INFINITY),
    "col_type": COL_TYPE.ELASTIC,
    "hitbox": Polygon.generate_rect(),
    "debug": True,
    "rotation": 0,
})

ground = RigidBody({
    "pos": Vector(300, 400 - 8),
    "mass": 1,
    "friction": Vector(1, 1),
    "col_type": COL_TYPE.STATIC,
    "scale": Vector(600 / 16, 1),
    "gravity": 0,
    "hitbox": Polygon.generate_rect(600, 16),
    "debug": True,
})

triangle = RigidBody({
    "pos":
    Vector(200, 200),
    "mass":
    1,
    "friction":
    Vector(1, 1),
    "col_type":
    COL_TYPE.STATIC,
    "hitbox":
    Polygon([Vector(40, 40), Vector(40, -100),
             Vector(0, 40)], rotation=46),
    "img":
    "empty",
    "debug":
    True,
    "gravity":
    0,
})

# triangle = RigidBody({
#     "pos": Vector(200, 200),
#     "mass": 1,
#     "friction": Vector(1, 1),
#     "col_type": COL_TYPE.ELASTIC,
#     "hitbox": Polygon([Vector(40, 40), Vector(40, -100), Vector(0, 40),  Vector(0, 50)], rotation=46),
#     "img": "empty",
#     "debug": True,
#     "gravity": 0,
# })


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

    if Input.is_pressed("space"):
        rb.game.window_width = 800
        rb.game.window_height = 800

    rigid.bounce(triangle)
    rigid.bounce(ground)


rigid.update = rigid_update

rb.game.radio.listen("w_down", w_handler)
group.add(rigid)

group.add(ground)

group.add(triangle)

rb.game.radio.listen("EXIT", lambda: print("exit event"))

Time.delayed_call(1000, lambda: print("1 second"))
Time.delayed_call(1000, lambda: print("1 second(2)"))
Time.delayed_call(5, lambda: print("5 millis"))

rb.Sound.import_sound("urmom.mp3", "urmom")
rb.Sound.play_sound("urmom", 1)

rb.begin()
