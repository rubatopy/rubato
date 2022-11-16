from rubato import Scene, Color, Text, wrap, Font, Game, Text, Raster, Button, GameObject
import shared

scene = Scene("main_menu", background_color=Color.black)

title_font = Font(size=64, styles=["bold"], color=Color.white)
title = Text("PLATFORMER DEMO!", title_font)

play_button = GameObject(pos=(0, -75)).add(
    Button(300, 100, onrelease=lambda: Game.set_scene("level1")),
    Text("PLAY", shared.white_32.clone()),
    r := Raster(300, 100, z_index=-1),
)
r.fill(Color.gray.darker(100))

scene.add_ui(wrap(title, pos=(0, 75)), play_button)
