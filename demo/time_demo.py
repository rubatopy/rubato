"""
Demos the time module.
"""
from rubato import *
import time

init()

main = Scene()

go = GameObject(pos=Display.center_left + Vector(50, 0)).add(Rectangle(width=100, height=100, color=Color.red))

interval = 1000
def task():
    go.pos += Vector(50, 0)
    print(f"Scheduled: {time.time()}")


def d_task():
    go.pos += Vector(50, 0)
    print(f"Delayed: {time.time()}")
    Time.delayed_call(interval, d_task)


Time.scheduled_call(interval, task)
Time.delayed_call(interval, d_task)

begin()
