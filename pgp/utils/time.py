from pygame.time import Clock, get_ticks
from pgp.utils import classproperty, check_types


class Time:
    """
    A time class to monitor time and to call functions in the future.
    """
    clock = Clock()
    calls = {}

    @staticmethod
    def delta_time(form: str = "milli") -> int:
        """
        Gets the time since the last frame, in milliseconds.

        :param form: The format the output should be (sec, milli)
        :return: Time since the last frame, in the given form.
        """
        check_types(Time.delta_time, locals())
        if form == "sec":
            return Time.milli_to_sec(Time.clock.get_time())
        elif form == "milli":
            return Time.clock.get_time()
        else:
            raise ValueError(f"Style {form} is not valid")

    @classproperty
    def now(self) -> int:
        """
        Gets the time since the start of the game, in milliseconds.

        :return: Time since the start of the game, in milliseconds.
        """
        return get_ticks()

    @staticmethod
    def set(clock: "Clock"):
        """
        Allows you to set the clock object property to a Pygame Clock object.

        :param clock: A pygame Clock object.
        """
        check_types(Time.set, locals())
        Time.clock = clock

    @staticmethod
    def milli_to_sec(milli: int) -> float:
        """
        Converts milliseconds to seconds.

        :param milli: A number in milliseconds.
        :return: The converted number in seconds.
        """
        check_types(Time.milli_to_sec, locals())
        return milli / 1000

    @staticmethod
    def delayed_call(delta_time: int, func: type(lambda:None)):
        """
        Calls the function func at a later time.

        :param delta_time: The time in milliseconds to run the function at.
        :param func: The function to call.
        """
        check_types(Time.delayed_call, locals())
        run_at = Time.now + delta_time

        if Time.calls.get(run_at):
            Time.calls[run_at].append(func)
        else:
            Time.calls[run_at] = [func]

    @staticmethod
    def process_calls():
        """Processes the calls needed"""
        for call in sorted(Time.calls.keys()):
            if call <= Time.now:
                for func in Time.calls[call]:
                    func()
                del Time.calls[call]
            else:
                break
