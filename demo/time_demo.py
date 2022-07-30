"""
Demos the time module.
"""
from rubato import *
import time

init()

main = Scene()

go = wrap(Rectangle(width=100, height=100, color=Color.red), pos=Display.center_left + Vector(50, 0))
main.add(go)

interval = 1000
def task():
    go.pos += Vector(50, 0)
    print(f"Scheduled: {time.time() - st}")
    if time.time() - st > 6:
        sched_task.stop()


def d_task():
    go.pos += Vector(50, 0)
    print(f"Delayed: {time.time() - st}")
    Time.delayed_call(interval, d_task)

st = time.time()

sched_task = ScheduledTask(interval, task)
Time.schedule(sched_task)

Time.delayed_call(interval, d_task)

begin()
