import time
from functools import total_ordering


def binary_search(arr, low, high, x):
    # Check base case
    if high >= low:

        mid = (high + low) // 2
        # If element is present at the middle itself
        if arr[mid] == x:
            return mid

        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid] > x:
            return binary_search(arr, low, mid - 1, x)

        # Else the element can only be present in right subarray
        else:
            return binary_search(arr, mid + 1, high, x)

    else:
        # Element is not present in the array
        if high < len(arr)-1:
            return ~(high+1)  # this way it will be negative if it is not present
        else:
            return ~len(arr)
        # 0000 0111


class Action:
    def __init__(self, actions: list = []):
        self.actions = []
        for a in actions:
            self.add(a)

    def add(self, func):
        self.actions.append(func)

    def add_wparam(self, func, param):  # need to implement a list of params
        self.actions.append([func, param])

    def remove(self, func):
        self.actions.remove(func)

    def invoke(self):
        for func in self.actions:
            if isinstance(func, list):
                # func with param
                param = func[1]
                a = func[0]
                eval("a" + "(" + "param" + ")")
            elif isinstance(func, Action):
                func.invoke()
            else:
                func()


@total_ordering
class TimerTask:
    def __init__(self, when, action: Action):
        self.when = when
        self.what: Action = action

    def __lt__(self, other):
        if other.__class__ is self.__class__:
            return self.when > other.when
        else:
            return NotImplemented
        pass

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return self.when == other.when and self.what == other.what

    def __repr__(self):
        return "["+str(self.when) + ", " + str(self.what)+"]"


class Timer(object):
    @property
    def now(self):
        return time.time()

    @property
    def delta_time(self):
        return self._deltatime

    def __init__(self):
        self._last_update_time = self.now
        self._deltatime = 0
        self.tasks: [TimerTask] = []

    def add_task(self, delay, func, params=None):
        '''
            :param delay: delay in seconds until the function is called
            :return: None
        '''
        if not isinstance(func, Action):
            if params:
                temp_action = Action()
                temp_action.add_wparam(func, params)
                task = TimerTask(delay + self.now, temp_action)
            else:
                temp_action = Action()
                temp_action.add(func)
                task = TimerTask(delay + self.now, temp_action)
        else:
            task = TimerTask(delay + self.now, func)

        self.add_task_from_timer(task)

    def add_task_from_timer(self, task:TimerTask):
        proper_index = binary_search(self.tasks, 0, len(self.tasks)-1, task)
        if(proper_index<0):
            proper_index = ~proper_index
        self.tasks.insert(proper_index, task)

    def update(self):
        index = len(self.tasks)-1
        while len(self.tasks) > 0 and self.now > self.tasks[index].when:
            print(self.tasks)
            task: TimerTask = self.tasks[index]
            self.tasks.pop(index)
            task.what.invoke()
            print(self.tasks)
            print("should have called function from timer")
        try:
            self._deltatime = float(self.now) - self._last_update_time
            self._last_update_time = self.now
        except Exception as e:
            print(e)

    def release(self):
        self.tasks.clear()


if __name__ == "__main__":
    timer = Timer()
    thing_to_do = Action()

    def simplefunc():
        time_between_calls = 4
        print(time.time(), f" the next call will be in {time_between_calls} seconds")
        timer.add_task(time_between_calls, thing_to_do)

    thing_to_do.add(simplefunc)
    thing_to_do.invoke()

    while 1:
        timer.update()
    # the timer slows down by ~.00065 seconds each time its called, why?
