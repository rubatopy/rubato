from rubato import Scene, Color, Display, GameObject, Vector, Rectangle, wrap, Radio, Events, Game, Time
import shared

scene = Scene("level1", background_color=shared.background_color)

end_location = Vector(Display.left + shared.level1_size - 128, 450)

# create the ground
ground = GameObject().add(ground_rect := Rectangle(width=1270, height=50, color=shared.platform_color, tag="ground"))
ground_rect.bottom_left = Display.bottom_left

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
    r.color = shared.platform_color

has_won = False


def won():
    global click_listener, has_won
    if not has_won:
        has_won = True
        scene.add_ui(shared.win_text)


def switch():
    global has_won
    shared.player.pos = Display.bottom_left + Vector(50, 80)
    shared.player_comp.initial_pos = shared.player.pos.clone()

    shared.right.pos = Display.center_left + Vector(shared.level1_size + 25, 0)

    shared.flag.pos = end_location
    shared.flag.get(Rectangle).on_enter = lambda col_info: won() if col_info.shape_b.tag == "player" else None

    scene.remove_ui(shared.win_text)

    has_won = False
    shared.start_time = Time.now()

    scene.camera.pos = Vector(0, 0)


scene.on_switch = switch

scene.add(ground, wrap(platforms), *pillars, shared.player, shared.left, shared.right, shared.flag)
