from rubato import *
from pympler import tracker
import os

tr = tracker.SummaryTracker()

init()


def print_mem():
    os.system('cls' if os.name == 'nt' else 'clear')
    tr.print_diff()


Time.schedule(ScheduledTask(2000, print_mem))

begin()
