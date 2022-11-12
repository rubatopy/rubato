from rubato import Scene, Color, Text, wrap, Font, GameObject, Button, Raster, Time, RecurrentTask, Vector, Game
import shared

scene = Scene("main_menu", background_color=Color.white)

title_font = Font(size=64, styles=["bold"])
title = Text("PLATFORMER DEMO!", title_font)

font_changing: RecurrentTask | None = None


def increase_font_size(task: RecurrentTask):
    global font_changing

    if font_changing is not None and font_changing != task:
        font_changing.stop()
    play_button.get(Text).font_size += 1
    if play_button.get(Text).font_size >= 64:
        task.stop()
        font_changing = None
        play_button.get(Text).font_size = 64
    else:
        font_changing = task


def decrease_font_size(task: RecurrentTask):
    global font_changing

    if font_changing is not None and font_changing != task:
        font_changing.stop()
    play_button.get(Text).font_size -= 1
    if play_button.get(Text).font_size <= 32:
        task.stop()
        font_changing = None
        play_button.get(Text).font_size = 32
    else:
        font_changing = task


play_button = shared.smooth_button_generator(
    (0, -75),
    300,
    100,
    "PLAY",
    lambda: Game.set_scene("end_menu"),
    Color.gray.lighter(100),
)

scene.add_ui(wrap(title, pos=(0, 75)), play_button)
