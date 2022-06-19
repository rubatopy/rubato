"""
Demos the time module.
"""
from rubato import *

init()

main = Scene()

go = GameObject(pos=Display.center_left + Vector(50, 0)).add(Rectangle(width=100, height=100, color=Color.red))


def task():
    go.pos += Vector(50, 0)
    Time.delayed_call(1, task)


task()

begin()
