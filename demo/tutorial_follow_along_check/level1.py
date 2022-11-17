import shared
from rubato import GameObject, Rectangle, Display, Scene, Vector, wrap

scene = Scene("level1", background_color=shared.background_color)


ground = GameObject().add(ground_rect := Rectangle(width=1270, height=50, color=shared.platform_color, tag="ground"))
ground_rect.bottom_left = Display.bottom_left

end_location = Vector(Display.left + shared.level1_size - 128, 450)

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
    Rectangle(256, 40, offset=end_location - (0, 64 + 20))
]

for p in platforms:
    p.tag = "ground"
    p.color = shared.platform_color

# create pillars, learn to do it with Game Objects too
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
    r.color = shared.platform_color

shared.right.pos = Display.center_left + Vector(shared.level1_size + 25, 0)


scene.add(shared.player, ground, wrap(platforms), *pillars, shared.left, shared.right)