"""A sound demo for Rubato"""
import sys, os

sys.path.insert(0, os.path.abspath("../"))

import rubato as rb  # pylint: disable=wrong-import-position

rb.init({
    "name": "Sound Test",
    "window_size": rb.Vector(300, 0),
    "res": rb.Vector(0, 0),
})

main_scene = rb.Scene()
rb.Game.scenes.add(main_scene, "main")

rb.Sound.import_sound_folder("sounds")
# rb.Sound.import_sound_folder("sounds/player1", True)
# rb.Sound.import_sound_folder("sounds/player2", True)

click = rb.Sound.get_sound("click")


def update():
    print(bin(click.channels))
    if rb.Input.key_pressed("space"):
        click.play(0)


def input_listener(keyinfo):
    if keyinfo["key"] == "a":
        click.play(20)
    if keyinfo["key"] == "s":
        click.stop()
    if keyinfo["key"] == "p":
        if click.state == rb.Sound.PLAYING:
            click.pause()
        elif click.state == rb.Sound.PAUSED:
            click.resume()


rb.Radio.listen("KEYDOWN", input_listener)

main_scene.update = update

rb.begin()
