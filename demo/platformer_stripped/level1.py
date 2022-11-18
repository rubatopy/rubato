import shared
import rubato as rb

scene = rb.Scene("level1", background_color=shared.background_color)

# create the ground
ground = rb.GameObject().add(
    ground_rect := rb.Rectangle(
        width=1270,
        height=50,
        color=shared.platform_color,
        tag="ground",
    )
)
ground_rect.bottom_left = rb.Display.bottom_left

end_location = rb.Vector(rb.Display.left + shared.level1_size - 128, 450)

# create platforms
platforms = [
    rb.Rectangle(
        150,
        40,
        offset=rb.Vector(-650, -200),
    ),
    rb.Rectangle(
        150,
        40,
        offset=rb.Vector(500, 40),
    ),
    rb.Rectangle(
        150,
        40,
        offset=rb.Vector(800, 200),
    ),
    rb.Rectangle(256, 40, offset=end_location - (0, 64 + 20))
]

for p in platforms:
    p.tag = "ground"
    p.color = shared.platform_color

# create pillars
pillars = [
    rb.GameObject(pos=rb.Vector(-260)).add(rb.Rectangle(
        width=100,
        height=650,
    )),
    rb.GameObject(pos=rb.Vector(260)).add(rb.Rectangle(
        width=100,
        height=400,
    )),
]

for pillar in pillars:
    r = pillar.get(rb.Rectangle)
    r.bottom = rb.Display.bottom + 50
    r.tag = "ground"
    r.color = shared.platform_color

# program the right boundary
shared.right.pos = rb.Display.center_left + (shared.level1_size + 25, 0)

scene.add(
    shared.player,
    ground,
    rb.wrap(platforms),
    *pillars,
    shared.left,
    shared.right,
)
