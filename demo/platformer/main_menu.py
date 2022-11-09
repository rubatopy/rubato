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


play_button = GameObject(pos=(0, -75)).add(
    Button(
        300,
        100,
        onhover=lambda: Time.recurrent_call(increase_font_size, 3),
        onexit=lambda: Time.recurrent_call(decrease_font_size, 3),
        onclick=lambda: Game.set_scene("level1"),
    ),
    Raster(300, 100),
    Text("PLAY", shared.black_32),
)
play_button.get(Raster).fill(Color.gray.lighter(100))

scene.add_ui(wrap(title, pos=(0, 75)), play_button)
