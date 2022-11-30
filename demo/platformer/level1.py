from rubato import Tilemap, Display, Vector, Rectangle, wrap, Radio, Events, Game, Time
import shared

scene = shared.DataScene("level1", background_color=shared.background_color)
scene.level_size = int(Display.res.x * 1.2)

end_location = Vector(Display.left + scene.level_size - 128, -416)

tilemap = Tilemap("files/level1.tmx", (8, 8), "ground")
has_won = False


def won():
    global click_listener, has_won
    if not has_won:
        has_won = True
        click_listener = Radio.listen(Events.MOUSEUP, go_to_next)
        scene.add_ui(shared.win_text, shared.win_sub_text)


def go_to_next():
    Game.set_scene("level2")
    click_listener.remove()


def switch():
    global has_won
    shared.player.pos = Display.bottom_left + Vector(50, 160)
    shared.player_comp.initial_pos = shared.player.pos.clone()
    shared.right.pos = Display.center_left + Vector(scene.level_size + 25, 0)
    shared.flag.pos = end_location
    shared.flag.get(Rectangle).on_enter = lambda col_info: won() if col_info.shape_b.tag == "player" else None
    scene.remove_ui(shared.win_text, shared.win_sub_text)
    has_won = False
    shared.start_time = Time.now()
    scene.camera.pos = Vector(0, 0)


scene.on_switch = switch

shared.cloud_generator(scene, 10, True)

scene.add(wrap(tilemap, pos=(192, 0)), shared.player, shared.left, shared.right, shared.flag)  #, shared.vignette)
