"""
The Game class houses the global variable for the game and controls the main
game loop.
"""
import pygame
import sys
from rubato.utils import STATE, Display, Vector, Time
from rubato.scenes import SceneManager
from rubato.radio import Radio
from rubato.sprite import Sprite
import rubato.input as Input


class Game:
    """
    The main game class. It controls everything in the game.

    Attributes:
        scenes (SceneManager): The global scene manager.
        radio (Radio): The global radio system.
        name (str): The title of the game window.
        fps (int): The target fps of the game.
        reset_display (bool): Controls whether or not the display should reset
            every frame.
        state (STATE): The current state of the game.

    Warning:
        Changing most of the above attributes will not update them in the game.
        For all intensive purposes, all the attributes in this class can be
        considered as read only.
    """

    default_options = {
        "name": "Untitled Game",
        "window_width": 600,
        "window_height": 400,
        "aspect_ratio": 1.5,
        "fps": 60,
        "reset_display": True,
        "better_clock": True,
    }

    def __init__(self, options: dict = {}):
        """
        Initializes a game. Should only be called by :meth:`rubato.init`.

        Args:
            options: A game config.
                Defaults to the :ref:`default game options <defaultgame>`.
        """
        pygame.init()
        self._params = Sprite.merge_params(options, Game.default_options)

        self.name: str = self._params["name"]
        self._window_width: int = self._params["window_width"]
        self._window_height: int = self._params["window_height"]
        self._aspect_ratio: float = self._params["aspect_ratio"]
        self.fps: int = self._params["fps"]
        self._reset_display: bool = self._params["reset_display"]
        self._use_better_clock: float = self._params["better_clock"]

        self.state = STATE.STOPPED

        self._clock = pygame.time.Clock()
        Time.set_clock(self._clock)

        self._screen = pygame.display.set_mode(
            (self._window_width, self._window_height), pygame.RESIZABLE)
        self._display = pygame.Surface(
            (self._window_width, self._window_height), pygame.SRCALPHA)

        pygame.display.set_caption(self.name)
        if options.get("icon"):
            pygame.display.set_icon(pygame.image.load(options.get("icon")))

        Display.set(self._display)

        self.scenes = SceneManager()
        self.radio = Radio()

    @property
    def window_size(self):
        """
        The current size of the window

        Returns:
            Vector: A vector with x representing the width and
                y representing the height

        Warning:
            This currently only returns the initial window size
        """
        return Vector(self._window_width, self._window_height)

    def start_loop(self):
        """
        Starts the game loop. Should only be called by :meth:`rubato.begin`
        """
        self.state = STATE.RUNNING
        while self.state == STATE.RUNNING:
            self.update()

    def update(self):
        """The update loop for the game. Called automatically every frame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.radio.broadcast("EXIT")
                pygame.quit()
                sys.exit(1)
            if event.type == pygame.VIDEORESIZE:
                self._window_width = event.size[0]
                self._window_height = event.size[1]
                self._screen = pygame.display.set_mode(
                    (self._window_width, self._window_height),
                    pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                self.radio.broadcast(Input.key.name(event.key) + "_down")
            if event.type == pygame.KEYUP:
                self.radio.broadcast(Input.key.name(event.key) + "_up")

        ratio = (self._window_width / self._window_height) < self._aspect_ratio
        width = (self._window_height * self._aspect_ratio,
                 self._window_width)[ratio]
        height = (self._window_height,
                  self._window_width / self._aspect_ratio)[ratio]
        top_right = (((self._window_width - width) // 2, 0),
                     (0, (self._window_height - height) // 2))[ratio]

        self.draw()
        self._screen.blit(
            pygame.transform.scale(self._display, (int(width), int(height))),
            top_right)

        Time.process_calls()
        self.scenes.update()

        pygame.display.flip()
        self.radio.events = []

        if self._use_better_clock:
            self._clock.tick_busy_loop(self.fps)
        else:
            self._clock.tick(self.fps)

    def draw(self):
        """Draw loop for the game. Called automatically every frame"""
        self._screen.fill((0, 0, 0))
        if self._reset_display: self._display.fill((255, 255, 255))
        self.scenes.draw(self)
        self._display = Display.display
