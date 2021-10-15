from rubato import Game, Image, Input, Scene, RigidBody, Vector, Time, PMath, Group, Polygon, SAT
from rubato.utils import COL_TYPE

game = Game()

scene = Scene()
scene.camera.pos.translate(0, 0)
game.scenes.add(scene)

group = Group()
scene.add(group)

sprite = Image("./Tinmarr.jpg", Vector(300,200))
rigid = RigidBody({
    "pos": Vector(100, 0),
    "mass": 1,
    "friction": Vector(0.9, 1),
    "max_speed": Vector(80, PMath.INFINITY),
    "col_type": COL_TYPE.ELASTIC,
    "hitbox": Polygon([Vector(-8, 8), Vector(8, 8), Vector(8, -8), Vector(-8, -8)]),
    "debug": False
})

ground = RigidBody({
    "pos": Vector(300, 400-8),
    "mass": 1,
    "friction": Vector(1, 1),
    "col_type": COL_TYPE.STATIC,
    "scale": Vector(600/16, 1),
    "gravity": 0,
    "hitbox": Polygon([Vector(-300, 8), Vector(300, 8), Vector(300, -8), Vector(-300, -8)])
})

triangle = RigidBody({
    "pos": Vector(200, 200),
    "mass": 1,
    "friction": Vector(1, 1),
    "col_type": COL_TYPE.STATIC,
    "scale": Vector(5, 5),
    "hitbox": Polygon([Vector(40, 40), Vector(40, -40), Vector(-40, 40)]),
    "img": "rubato/static/default_triangle.png",
    "debug": True,
    "gravity": 0,
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
# rigid.collides_with.append(ground)
rigid.collides_with.append(triangle)
game.radio.listen("w_down", w_handler)
group.add(rigid)

# group.add(ground)

# triangle.collides_with.append(ground)
group.add(triangle)

game.radio.listen("EXIT", lambda: print("ya-yeet"))

Time.delayed_call(1000, lambda: print("LOL"))

game.begin()
