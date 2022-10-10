from rubato import *
import psutil, os

init()


def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


Time.schedule(RecurrentTask(lambda: print(f"Overall usage: {process_memory()}\n"), 1000))

begin()
