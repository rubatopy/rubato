"""Testing how many things we can draw"""
from rubato import *
import random

init({
    "name": "drawing as much as possible",
    "res": Vector(300, 300),
    "window_size": Vector(600, 600),
})

main_scene = Scene()
Game.scenes.add(main_scene, "main")

image = Image({
    "rel_path": "testing/Run/0.png",
})

group = Group()
amt = 10


def handle_keydown(event):
    global amt
    if event["key"] == "a":
        gos = [
            GameObject({
                "pos": Vector(random.random() * Display.res.x,
                              random.random() * Display.res.y)
            }).add(image.clone()) for _ in range(amt)
        ]
        amt *= 1.1
        amt = int(amt)
        group_mini = Group()
        group_mini.add(*gos)
        group.add(group_mini)
    elif event["key"] == "c":
        print(group.count())
        print(Time.smooth_fps)


Radio.listen("KEYDOWN", handle_keydown)
Radio.listen("KEYHOLD", handle_keydown)

main_scene.add(group)

begin()
