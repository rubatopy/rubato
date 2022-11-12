from rubato import Display, Vector, Color, Rectangle, wrap, GameObject, Radio, Events, Game, Raster
from data_scene import DataScene
from moving_platform import MovingPlatform
import shared

scene = DataScene("level2", background_color=Color.cyan.lighter())
scene.level_size = int(Display.res.x * 2)

end_location = Vector(Display.left + scene.level_size - 128, 0)

platforms = [
    GameObject(pos=Vector(-885, -50)).add(Rectangle(150, 40)),
    GameObject(pos=Vector(-735, -50)).add(Rectangle(150, 40), MovingPlatform(100, "r", 400, 2)),
    GameObject(pos=Vector(-185, -450)).add(Rectangle(150, 40), MovingPlatform(150, "u", 980, 0)),
    GameObject(pos=Vector(0, 300)).add(Rectangle(150, 40), MovingPlatform(200, "r", 500, 0)),
    GameObject(pos=Vector(1300, 0)).add(Rectangle(150, 40), MovingPlatform(100, "l", 500, 1)),
    GameObject(pos=Vector(1700, -400)).add(Rectangle(150, 40), MovingPlatform(1000, "u", 400, 0)),
    GameObject(pos=Vector(2215, 100)).add(Rectangle(150, 40)),
    GameObject(pos=Vector(2730, -84)).add(Rectangle(300, 40)),
]

for p in platforms:
    if MovingPlatform in p:
        p.get(Rectangle).tag = "moving_ground"
    else:
        p.get(Rectangle).tag = "ground"
    p.get(Rectangle).color = Color.blue.darker(20)

shared.cloud_generator(scene, 20)

has_won = False


def won():
    global click_listener, has_won
    if not has_won:
        has_won = True
        click_listener = Radio.listen(Events.MOUSEUP, go_to_next)
        scene.add_ui(shared.win_text, shared.win_sub_text)


def go_to_next():
    Game.set_scene("end_menu")
    click_listener.remove()


def switch():
    shared.player.pos = Vector(Display.left + 50, 0)
    shared.player_comp.initial_pos = shared.player.pos.clone()
    shared.right.pos = Display.center_left + Vector(scene.level_size + 25, 0)
    shared.end.pos = end_location
    shared.end.get(Rectangle).on_enter = lambda col_info: won() if col_info.shape_b.tag == "player" else None


scene.on_switch = switch
scene.add(*platforms, shared.player, shared.left, shared.right, shared.end)
