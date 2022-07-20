"""
The main game module. It controls everything in the game.
"""
from __future__ import annotations
import sys
import sdl2, sdl2.sdlttf
from typing import TYPE_CHECKING, Dict

from . import Time, Display, Debug, Radio, Events, Font, PrintError, Camera, IdError

if TYPE_CHECKING:
    from . import Scene

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
            use :func:`Game.current.camera <rubato.struct.scene.Scene.camera>` to access the camera directly.

        Returns:
            Camera: The current scene's camera
        """
        return cls.current.camera


# THIS IS A STATIC CLASS
class Game(metaclass=GameProperties):
    """
    The main game class.

    Attributes:
        name (str): The title of the game window.
        debug (bool): Whether to use debug-mode.
        show_fps (bool): Whether to show fps.
        debug_font (Font): What font to draw debug text in.
    """
    RUNNING = 1
    STOPPED = 2
    PAUSED = 3

    name: str = ""

    debug: bool = False
    show_fps: bool = False
    debug_font: Font

    _state: int = STOPPED

    _initialized = False

    _scenes: Dict[str, Scene] = {}
    _scene_id : int = 0
    _current: str = ""

    @classmethod
    @property
    def current(cls) -> Scene:
        """
        The current scene. Get-only.

        Returns:
            The current scene.
        """
        return cls._scenes.get(cls._current)

    @classmethod
    def set_scene(cls, scene_id: str):
        """
        Changes the current scene.

        Args:
            scene_id (str): The id of the new scene.
        """
        cls._current = scene_id

    @classmethod
    def _add(cls, scene: Scene):
        """
        Add a scene to the game. Also set the current scene if this is the first added scene.

        Args:
            scene (Scene): The scene to add.
            scene_id (str): The id of the scene.

        Raises:
            IdError: The given scene id is already used.
        """
        if scene.name is None:
            scene._id = "scene" + str(cls._scene_id) # pylint: disable=protected-access

        if scene.name in cls._scenes:
            raise IdError(f"A scene with name '{scene.name}' has already been added.")

        if not cls._scenes:
            cls.set_scene(scene.name)

        cls._scenes[scene.name] = scene
        cls._scene_id += 1

    @classmethod
    def quit(cls):
        """Quit the game and close the python process."""
        Radio.broadcast(Events.EXIT)
        cls.state = cls.STOPPED
        sys.stdout.flush()
        sdl2.sdlttf.TTF_Quit()
        sdl2.SDL_Quit()
        sys.exit()

    @classmethod
    def constant_loop(cls):  # test: skip
        """
        The constant game loop. Should only be called by :meth:`rubato.begin`.
        """
        cls.state = cls.RUNNING
        try:
            cls.update()
        except KeyboardInterrupt:
            cls.quit()
        except PrintError as e:
            sys.stdout.flush()
            raise e
        except (Exception,) as e:  # add possible exceptions here if there are more needed
            sys.stdout.flush()
            raise type(e)(
                str(e) + "\nRubato Error-ed. Was it our fault? Issue tracker: "
                "https://github.com/rubatopy/rubato/issues"
            ).with_traceback(sys.exc_info()[2])
        finally:
            sys.stdout.flush()

    @classmethod
    def update(cls):  # test: skip
        """
        The update loop for the game. Called automatically every frame.
        Handles the game states.
        Will always process timed calls.
        """
        while True:
            # start timing the update loop
            Time._frame_start = Time.now()  # pylint: disable= protected-access

            # Event handling
            if Radio.pump():
                cls.quit()

            # process delayed calls
            Time.process_calls()

            if cls.current is not None:
                if cls.state == Game.PAUSED:
                    # process user set pause update
                    cls.current.private_paused_update()
                else:
                    # normal update
                    cls.current.private_update()

                    # fixed update
                    Time.physics_counter += Time.delta_time

                    while Time.physics_counter >= Time.fixed_delta:
                        if cls.state != Game.PAUSED:
                            cls.current.private_fixed_update()
                        Time.physics_counter -= Time.fixed_delta

                cls.current.private_draw()

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
            while Time.now() == Time.frame_start:  # pylint: disable= comparison-with-callable
                sdl2.SDL_Delay(1)

            # clock the time the update call took
            Time.delta_time = (Time.now() - Time.frame_start) / 1000  # pylint: disable= comparison-with-callable
