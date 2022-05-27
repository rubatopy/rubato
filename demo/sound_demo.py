"""
A sound demo for rubato

Requires rubato 2.1.0 or later.
"""
import rubato as rb

rb.init(
    name="Sound Test",
    window_size=rb.Vector(300, 0),
    res=rb.Vector(0, 0),
)

main_scene = rb.Scene()

rb.Sound.import_sound_folder("sounds", recursive=False)  # Import the sound folder shallowly

click = rb.Sound.get_sound("click")  # Get sound instance
music = rb.Sound.get_sound("music")

sound = rb.Sound("sounds/bark.wav", "barkyboi")

# player 1 and 2 have duplicate file names so we must use the absolute path as a key
rb.Sound.import_sound_folder("sounds/player1", True)
rb.Sound.import_sound_folder("sounds/player2", True)

player1_intro = rb.Sound.get_sound("sounds/player1/intro")
player1_intro.play()


def update():
    print(f"click: {bin(click.channels)}   music: {bin(music.channels)}")  # Prints the active channels
    if rb.Input.key_pressed("space"):
        click.play(0)


def input_listener(keyinfo):
    if keyinfo["key"] == "m":
        music.play()
    if keyinfo["key"] == "a":
        click.play(20)
    if keyinfo["key"] == "s":
        click.stop()
        music.stop()
    if keyinfo["key"] == "p":
        if click.state == rb.Sound.PLAYING:
            click.pause()
        elif click.state == rb.Sound.PAUSED:
            click.resume()
        if music.state == rb.Sound.PLAYING:
            music.pause()
        elif music.state == rb.Sound.PAUSED:
            music.resume()


rb.Radio.listen("KEYDOWN", input_listener)

main_scene.update = update

rb.begin()
