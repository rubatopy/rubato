"""A file to time processes easily"""
from time import time

timers = {}
s = 0


def start():  # should be used before a thing to time
    global s
    s = time()


def end(name):  # should be used after a thing to time
    timers[name] = timers.get(name, []) + [time() - s]


def endthenstart(name):  # should be used when chaining time
    end(name)
    start()


def printall():  # should be called when u want to sample the values.
    for key, value in timers.items():
        print(f"{key}: {(sum(value) * 1000) / len(value)}")
