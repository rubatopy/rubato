from rubato import *
from pympler import tracker
import psutil, os

tr = tracker.SummaryTracker()

init()


def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


def print_mem():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Overall useage: {process_memory()}\n")
    tr.print_diff()


Time.schedule(ScheduledTask(2000, print_mem))

begin()
