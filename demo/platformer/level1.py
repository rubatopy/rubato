from rubato import Scene, Color, Display, GameObject, Vector, Rectangle, wrap, Font, Text, Radio, Events, Game, Time
import shared
from data_scene import DataScene

scene = DataScene("level1", background_color=Color.cyan.lighter())
scene.level_size = int(Display.res.x * 1.2)

portal_location = Vector(Display.left + scene.level_size - 128, 450)

# create the ground
ground = GameObject().add(ground_rect := Rectangle(width=1270, height=50, color=Color.green.darker(40), tag="ground"))
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

# level win screen
win_font = Font(size=128, color=Color.green.darker(75), styles=["bold"])
win_text = GameObject(z_index=2).add(Text("YOU WIN!", win_font, anchor=(0, 0.5)))
win_sub_text = GameObject(pos=(0, -100), z_index=2).add(Text("Click anywhere to move on", shared.black_32))

has_won = False


def won():
    global click_listener, has_won
    if not has_won:
        has_won = True
        click_listener = Radio.listen(Events.MOUSEDOWN, go_to_next)
        scene.add_ui(win_text, win_sub_text)


def go_to_next():
    Game.set_scene("level2")
    click_listener.remove()


def switch():
    shared.player.pos = Display.bottom_left + Vector(50, 50)
    shared.player_comp.initial_pos = shared.player.pos.clone()
    shared.right.pos = Display.center_left + Vector(scene.level_size + 25, 0)
    shared.portal.pos = portal_location
    shared.portal.get(Rectangle).on_enter = lambda col_info: won() if col_info.shape_b.tag == "player" else None


scene.on_switch = switch
scene.add(ground, wrap(platforms), *pillars, shared.player, shared.left, shared.right, shared.portal)
