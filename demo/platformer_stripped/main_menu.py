import rubato as rb

scene = rb.Scene("main_menu", background_color=rb.Color.black)  # make a new scene

title_font = rb.Font(size=64, styles=["bold"], color=rb.Color.white)
title = rb.Text(text="PLATFORMER DEMO!", font=title_font)

play_button = rb.GameObject(pos=(0, -75)).add(
    rb.Button(
        width=300,
        height=100,
        onrelease=lambda: rb.Game.set_scene("level1"),
    ),
    rb.Text(
        "PLAY",
        rb.Font(size=32, color=rb.Color.white),
    ),
    r := rb.Raster(
        width=300,
        height=100,
        z_index=-1,
    ),
)
r.fill(color=rb.Color.gray.darker(100))

scene.add_ui(
    rb.wrap(title, pos=(0, 75)),
    play_button,
)
