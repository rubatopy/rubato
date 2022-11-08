from rubato import Scene, Color, Display, GameObject, Vector, Rectangle, wrap

level_size = int(Display.res.x * 1.2)
portal_location = Vector(Display.left + level_size - 128, 450)

scene = Scene("level1", background_color=Color.cyan.lighter())

# Side boundary
left = GameObject(pos=Display.center_left - Vector(25, 0))
left.add(Rectangle(width=50, height=Display.res.y))
right = GameObject(pos=Display.center_left + Vector(level_size + 25, 0))
right.add(Rectangle(width=50, height=Display.res.y))

# create the ground
ground = GameObject()
ground.add(Rectangle(width=1270, height=50, color=Color.green.darker(40), tag="ground"))
ground.get(Rectangle).bottom_left = Display.bottom_left

# create platforms
platforms = [
    Rectangle(
        150,
        40,
        offset=Vector(-650, -200),
    ),
    Rectangle(
        150,
        40,
        offset=Vector(500, 40),
    ),
    Rectangle(
        150,
        40,
        offset=Vector(800, 200),
    ),
    Rectangle(256, 40, offset=portal_location - (0, 64 + 20))
]

for p in platforms:
    p.tag = "ground"
    p.color = Color.blue.darker(20)

# create pillars
pillars = [
    GameObject(pos=Vector(-260)).add(Rectangle(
        width=100,
        height=650,
    )),
    GameObject(pos=Vector(260)).add(Rectangle(
        width=100,
        height=400,
    )),
]

for pillar in pillars:
    r = pillar.get(Rectangle)
    r.bottom = Display.bottom + 50
    r.tag = "ground"
    r.color = Color.purple

scene.add(ground, left, right, wrap(platforms), *pillars)
