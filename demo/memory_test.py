from rubato import *
import psutil, os

init()


def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


Time.schedule(RecurrentTask(1000, lambda: print(f"Overall usage: {process_memory()}\n")))

begin()
