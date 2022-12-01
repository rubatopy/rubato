from rubato import Display, Vector, Rectangle, GameObject, Radio, Events, Game, Spritesheet, SimpleTilemap, Surface
from moving_platform import MovingPlatform
import shared

scene = shared.DataScene("level2", background_color=shared.background_color)
scene.level_size = int(Display.res.x * 2)

end_location = Vector(Display.left + scene.level_size - 128, 0)

tileset = Spritesheet("files/cavesofgallet_tiles.png", (8, 8))

platforms = [
    GameObject(pos=Vector(-885, -50)),
    GameObject(pos=Vector(-735, -50)).add(MovingPlatform(100, "r", 400, 2)),
    GameObject(pos=Vector(-185, -450)).add(MovingPlatform(150, "u", 980, 0)),
    GameObject(pos=Vector(0, 300)).add(MovingPlatform(200, "r", 500, 0)),
    GameObject(pos=Vector(1300, 0)).add(MovingPlatform(100, "l", 500, 1)),
    GameObject(pos=Vector(1700, -400)).add(MovingPlatform(1000, "u", 400, 0)),
    GameObject(pos=Vector(2215, 100)),
    GameObject(pos=Vector(2730, -84)).add(
        Rectangle(320, 40, tag="ground"),
        SimpleTilemap(
            [[0, 0, 0, 0, 0, 0, 0, 0]],
            [tileset.get(4, 1)],
            (8, 8),
            scale=(5, 5),
        )
    ),
]

platform = SimpleTilemap([[0, 0, 0, 0]], [tileset.get(4, 1)], (8, 8), scale=(5, 5))
for p in platforms:
    if len(p.get_all(Rectangle)) == 0:
        p.add(r := Rectangle(160, 40))
        if MovingPlatform in p:
            r.tag = "moving_ground"
        else:
            r.tag = "ground"
    p.add(platform.clone())

shared.cloud_generator(scene, 10)

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
    global has_won
    shared.player.pos = Vector(Display.left + 50, 0)
    shared.player_comp.initial_pos = shared.player.pos.clone()
    shared.right.pos = Display.center_left + Vector(scene.level_size + 25, 0)
    shared.flag.pos = end_location
    shared.flag.get(Rectangle).on_enter = lambda col_info: won() if col_info.shape_b.tag == "player" else None
    scene.remove_ui(shared.win_text, shared.win_sub_text)
    has_won = False
    scene.camera.pos = Vector(0, 0)


scene.on_switch = switch
scene.add(*platforms, shared.player, shared.left, shared.right, shared.flag, shared.vignette)
