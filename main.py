from rubato import Game, Image, Input, Scene, RigidBody, Vector, Time, PMath, Group, Polygon, SAT
from rubato.utils import COL_TYPE

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
    "col_type": COL_TYPE.ELASTIC,
    "hitbox": Polygon.generate_polygon(4, 16)
})

ground = RigidBody({
    "pos": Vector(0, 400-16),
    "mass": 1,
    "friction": Vector(1, 1),
    "col_type": COL_TYPE.ELASTIC,
    "scale": Vector(600/16, 1),
    "box": [0, 0, 600, 16],
    "gravity": 0,
    "hitbox": Polygon.generate_polygon(4, 100)
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


rigid.update = rigid_update
rigid.collides_with.append(ground)
game.radio.listen("w_down", w_handler)
group.add(rigid)
group.add(ground)

game.radio.listen("EXIT", lambda: print("ya-yeet"))

Time.delayed_call(1000, lambda: print("LOL"))

game.begin()
