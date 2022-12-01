from rubato import Scene, Color, Text, wrap, Font, Game
import shared

scene = Scene("main_menu", background_color=shared.background_color)

title_font = Font(font=shared.font_name, size=58, color=Color.white)
title = Text("Rubato Platformer Demo", title_font)

play_button = shared.smooth_button_generator(
    (0, -75),
    300,
    100,
    "PLAY",
    lambda: Game.set_scene("level1"),
    Color.gray.darker(100),
)

scene.add(wrap(title, pos=(0, 75)), play_button)
