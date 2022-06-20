"""
The main game module. It controls everything in the game.
"""
from __future__ import annotations
import sys
import sdl2, sdl2.ext, sdl2.sdlttf
from typing import TYPE_CHECKING

from . import Time, Display, Debug, Color, Radio, Events, Font, Draw, PrintError

if TYPE_CHECKING:
    from . import SceneManager, Camera


class GameProperties(type):
    """
    Defines static property methods for Game.

    Warning:
        This is only a metaclass for the class below it, so you wont be able to access this class.
        To use the property methods here, simply access them as you would any other Game property.
    """

    @property
    def state(cls) -> int:
        """
        The state of the game.

        The game states are::

            Game.RUNNING
            Game.STOPPED
            Game.PAUSED
        """
        return cls._state

    @state.setter
    def state(cls, new: int):
        cls._state = new

        if cls._state == Game.STOPPED:
            sdl2.SDL_PushEvent(sdl2.SDL_Event(sdl2.SDL_QUIT))

    @property
    def camera(cls) -> Camera:
        """
        A shortcut getter allowing easy access to the current camera.
        This is a get-only property.

        Note:
            Returns a pointer to the current camera object.
            This is so you can access/change the current camera properties faster, but you'd still need to
            use :func:`Game.scenes.current.camera <rubato.classes.scene.Scene.camera>` to access the camera directly.

        Returns:
            Camera: The current scene's camera
        """
        return cls.scenes.current.camera


# THIS IS A STATIC CLASS
class Game(metaclass=GameProperties):
    """
    The main game class.

    Attributes:
        name (str): The title of the game window.
        scenes (SceneManager): The global scene manager.
        background_color (Color): The background color of the window.
        border_color (Color): The color of the borders of the window.
        debug (bool): Turn on debug rendering for everything in the game.
    """
    RUNNING = 1
    STOPPED = 2
    PAUSED = 3

    name: str = ""
    border_color: Color = Color(0, 0, 0)
    background_color: Color = Color(255, 255, 255)

    debug: bool = False
    show_fps: bool = False
    debug_font: Font

    _state: int = STOPPED
    scenes: SceneManager = None

    initialized = False

    @classmethod
    def constant_loop(cls):  # test: skip
        """
        The constant game loop. Should only be called by :meth:`rubato.begin`.
        """
        cls.state = cls.RUNNING
        try:
            while True:
                cls.update()
        except PrintError as e:
            raise e
        except KeyboardInterrupt:
            Radio.broadcast(Events.EXIT)
            sdl2.sdlttf.TTF_Quit()
            sdl2.SDL_Quit()
            sys.exit()
        except (Exception,) as e:  # add possible exceptions here if there are more needed
            raise type(e)(
                str(e) + "\nRubato Error-ed. Was it our fault? Issue tracker: "
                "https://github.com/rubatopy/rubato/issues"
            ).with_traceback(sys.exc_info()[2])

    @classmethod
    def update(cls):  # test: skip
        """
        The update loop for the game. Called automatically every frame.
        Handles the game states.
        Will always process timed calls.
        """
        # start timing the update loop
        frame_start = sdl2.SDL_GetTicks64()

        # Event handling
        Radio.pump()

        # process delayed calls
        Time.process_calls()

        if cls.state == Game.PAUSED:
            # process user set pause update
            cls.scenes.paused_update()
        else:
            # normal update
            cls.scenes.update()

            # fixed update
            Time.physics_counter += Time.delta_time

            while Time.physics_counter >= Time.fixed_delta:
                if cls.state != Game.PAUSED:
                    cls.scenes.fixed_update()
                Time.physics_counter -= Time.fixed_delta

        Draw.clear(cls.border_color, cls.background_color)

        cls.scenes.draw()

        Draw.dump()

        if cls.show_fps:
            Debug.draw_fps(cls.debug_font)

        # update renderers
        Display.renderer.present()

        # use delay to cap the fps if need be
        if Time.capped:
            delay = Time.normal_delta - (1000 * Time.delta_time)
            if delay > 0:
                sdl2.SDL_Delay(int(delay))

        # dont allow updates to occur more than once in a millisecond
        # this will likely never occur but is a failsafe
        while sdl2.SDL_GetTicks64() == frame_start:
            sdl2.SDL_Delay(1)

        # clock the time the update call took
        Time.delta_time = (sdl2.SDL_GetTicks64() - frame_start) / 1000
