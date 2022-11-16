from rubato import Scene, Color, Game, Display, Time, Text, GameObject
import shared, time

scene = Scene("end_menu", background_color=Color.black)

restart_button = shared.smooth_button_generator(
    (0, -75),
    600,
    100,
    "RESTART",
    lambda: Game.set_scene("main_menu"),
    Color.gray.darker(100),
)

screenshot_button = shared.smooth_button_generator(
    (0, -200),
    600,
    100,
    "SAVE SCREENSHOT",
    lambda: Display.save_screenshot((f"platformer time {time.asctime()}").replace(" ", "-")),
    Color.gray.darker(100),
)

time_text = GameObject(pos=(0, 100)).add(Text("", shared.white_32))


def on_switch():
    final_time = Time.now() - shared.start_time
    time_text.get(Text).text = f"Final time: {round(final_time, 2)} seconds"


scene.on_switch = on_switch
scene.add_ui(restart_button, screenshot_button, time_text)
