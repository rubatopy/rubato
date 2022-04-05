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


def handle_keydown(event):
    if event["key"] == "a":
        GOs = [GameObject({"pos": Vector(random.random() * Display.res.x, random.random() * Display.res.y)}).add(
            image.clone())
               for _ in range(10)]
        group.add(*GOs)
    elif event["key"] == "c":
        print(len(group.game_objects))




Radio.listen("KEYDOWN", handle_keydown)

main_scene.add(group)

begin()
