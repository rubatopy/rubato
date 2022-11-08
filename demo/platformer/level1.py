from rubato import Scene, Color, Display, GameObject, Vector, Rectangle

level_size = int(Display.res.x * 1.2)

scene = Scene("level1", background_color=Color.cyan.lighter())

# Side boundary
left = GameObject(pos=Display.center_left - Vector(25, 0))
left.add(Rectangle(width=50, height=Display.res.y))
right = GameObject(pos=Display.center_left + Vector(level_size + 25, 0))
right.add(Rectangle(width=50, height=Display.res.y))

# create the ground
ground = GameObject()
ground.add(Rectangle(width=level_size, height=50, color=Color.green, tag="ground"))
ground.get(Rectangle).bottom_left = Display.bottom_left

# create platforms
platforms = [
    GameObject(pos=Vector(
        -760,
        Display.bottom + 140,
    )).add(Rectangle(
        width=90,
        height=40,
        tag="ground",
        color=Color.blue,
    )),
    GameObject(pos=Vector(
        -560,
        Display.bottom + 340,
    )).add(Rectangle(
        width=150,
        height=40,
        tag="ground",
        color=Color.blue,
    )),
]

# create obstacles
obstacles = [
    GameObject(pos=Vector(-260)).add(Rectangle(
        width=90,
        height=500,
        tag="ground",
        color=Color.purple,
    )),
    GameObject(pos=Vector(240)).add(Rectangle(
        width=70,
        height=450,
        tag="ground",
        color=Color.purple,
    )),
]

for obstacle in obstacles:
    obstacle.get(Rectangle).bottom = Display.bottom + 30

# create triggers
triggers = [
    GameObject(pos=Vector(
        -10,
        Display.bottom + 45,
    )).add(Rectangle(
        width=400,
        height=30,
        tag="retry_collider",
        trigger=True,
    )),
]

scene.add(ground, left, right, *platforms, *obstacles, *triggers)
