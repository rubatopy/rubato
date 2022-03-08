"""
The Game class houses the global variable for the game and controls the main
game loop.
"""
import pygame
from pygame.transform import scale
import sys
from rubato.classes.sprite import Sprite
from rubato.utils import Display, Vector, Time, Configs, Math
from rubato.classes import SceneManager
from rubato.radio import Radio
import rubato.input as Input
from enum import Enum


class STATE(Enum):
    """
    An enum to keep track of the state things
    """
    RUNNING = 1
    STOPPED = 2
    PAUSED = 3


class Game:
    """
    The main game class. It controls everything in the game.
    The Display is where your game lives at a certain aspect ratio,
    The Screen is the actual size of the window which the user interacts with.

    Attributes:
        scenes (SceneManager): The global scene manager.
        radio (Radio): The global radio system.
        name (str): The title of the game window.
        fps (int): The target fps of the game.
        reset_display (bool): Controls whether or not the display should reset
            every frame.
        state (STATE): The current state of the game.
        window_width (int): The width of the game window.
        window_height (int): The height of the game window.
    """

    def __init__(self, options: dict = {}):
        """
        Initializes a game. Should only be called by :meth:`rubato.init`.

        Args:
            options: A game config.
                Defaults to the |default| for `Game`.
        """
        pygame.init()
        params = Configs.merge_params(options, Configs.game_defaults)

        self._phy_ts = 0

        self.name: str = params["name"]
        self._window_width: int = params["window_width"]
        self._window_height: int = params["window_height"]
        self._aspect_ratio: float = params["aspect_ratio"]
        self.fps_cap: int = params["fps_cap"]
        self.physics_timestep: int = params["physics_timestep"]
        self.reset_display: bool = params["reset_display"]
        self._use_better_clock: float = params["better_clock"]

        self._physics_count: float = 0

        self._state = STATE.STOPPED

        self._clock = pygame.time.Clock()
        Time.set_clock(self._clock)

        self._screen = pygame.display.set_mode(
            (self._window_width, self._window_height), pygame.RESIZABLE)
        self._display = pygame.Surface((self._window_width, self._window_height),
                                       pygame.SRCALPHA)

        pygame.display.set_caption(self.name)
        if options.get("icon"):
            pygame.display.set_icon(pygame.image.load(options.get("icon")))

        Display.set_display(self._display)

        self.scenes = SceneManager()
        self.radio = Radio()

        self._saved_dims = [self._window_width, self._window_height]

        infos = pygame.display.Info()
        self._max_screen_size = (infos.current_w, infos.current_h)
    @property
    def physics_timestep(self):
        return self._phy_ts

    @physics_timestep.setter
    def physics_timestep(self, new_ts: int):
        self._phy_ts = new_ts
        Time._fixed_delta_time = new_ts  # pylint: disable=protected-access

    def constant_loop(self):
        """
        The constant game loop. Should only be called by :meth:`rubato.begin`.
        """
        self._state = STATE.RUNNING
        while True:
            self.update()

    def update(self):
        """
        The update loop for the game. Called automatically every frame.
        Handles the game states.
        Will always process timed calls ...
        """
        do_not_do_this_if_paused = True #False if self.state == STATE.PAUSED else True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.radio.broadcast("EXIT")
                pygame.quit()
                sys.exit(1)
            # Game resize
            elif event.type == pygame.VIDEORESIZE:
                self._window_width = event.size[0]
                self._window_height = event.size[1]
            elif event.type == pygame.KEYDOWN and do_not_do_this_if_paused:
                self.radio.broadcast(Input.key.name(event.key) + "_down")
            elif event.type == pygame.KEYUP and do_not_do_this_if_paused:
                self.radio.broadcast(Input.key.name(event.key) + "_up")

        if (self._saved_dims[0] != self._window_width
                or self._saved_dims[1] != self._window_height):
            self._screen = pygame.display.set_mode(
                (self._window_width, self._window_height), pygame.RESIZABLE)

        ratio = (self._window_width / self._window_height) < self._aspect_ratio
        width = (self._window_height * self._aspect_ratio,
                 self._window_width)[ratio]
        height = (self._window_height,
                  self._window_width / self._aspect_ratio)[ratio]
        top_left = (((self._window_width - width) // 2, 0),
                     (0, (self._window_height - height) // 2))[ratio]

        self._saved_dims = [self._window_width, self._window_height]

        if self.state and do_not_do_this_if_paused:
            Time.process_calls()

        self._physics_count += Time.delta_time()

        self._physics_count = Math.clamp(self._physics_count, 0,
                                         self.physics_timestep * 100)

        while self._physics_count > self.physics_timestep:
            self.scenes.fixed_update()
            self._physics_count -= self.physics_timestep

        self.scenes.update()

        self._screen.fill((0, 0, 0))
        if self.reset_display: self._display.fill((255, 255, 255))
        self.scenes.draw()
        self._display = Display.global_display

        self._screen.blit(
            pygame.transform.scale(self._display, (int(width), int(height))),
            top_left)

        pygame.display.flip()
        self.radio.events = []

        if self._use_better_clock:
            self._clock.tick_busy_loop(self.fps_cap)
        else:
            self._clock.tick(self.fps_cap)

    def render(self, sprite: Sprite, surface: pygame.Surface):
        if sprite.z_index <= self.scenes.current_scene.camera.z_index:
            width, height = surface.get_size()

            new_size = (
                round(width * self.scenes.current_scene.camera.zoom),
                round(height * self.scenes.current_scene.camera.zoom),
            )

            Display.update(
                scale(surface, new_size),
                self.scenes.current_scene.camera.transform(
                    Sprite.center_to_tl(sprite.pos, Vector(width, height)) *
                    self.scenes.current_scene.camera.zoom),
            )

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state: STATE):
        self._state = new_state

        if self._state == STATE.STOPPED:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    @property
    def window_width(self):
        """
        Returns:
            The height of the actual window (screen).
        """
        return self._window_width

    @window_width.setter
    def window_width(self, window_width: int) -> None:
        """
        Sets width of actual window (screen).
        Args:
            window_width:
                width clamped between the max display size initialized rubato.init()
        """
        if self._max_screen_size[0] > window_width > 0:
            self._window_width = window_width

    @property
    def window_height(self):
        """
        Returns:
            The width of the actual window (screen).
        """
        return self._window_height

    @window_height.setter
    def window_height(self, window_height: int) -> None:
        """
        Sets height of actual window (screen).
        Args:
            window_height:
                height clamped between the max display size initialized rubato.init()
        """
        if self._max_screen_size[1] > window_height > 0:
            self._window_height = window_height

    @property
    def aspect_ratio(self):
        """
        Returns:
            The aspect ratio of the display (the actual game).
        """
        return self._aspect_ratio

    @aspect_ratio.setter
    def aspect_ratio(self, aspect_ratio: int) -> None:
        """
        Sets the aspect ratio of the display that will be kept no matter the real size of the screen.
        Args:
            aspect_ratio:
        """
        if 100 > aspect_ratio > 0:
            self._aspect_ratio = aspect_ratio

    @property
    def window_size(self):
        """
        The current size of the window

        Returns:
            Vector: A vector with x representing the width and
            y representing the height
        """
        return Vector(self._window_width, self._window_height)

    @window_size.setter
    def window_size(self, window_size: Vector):
        self.window_width = window_size.x
        self.window_height = window_size.y
