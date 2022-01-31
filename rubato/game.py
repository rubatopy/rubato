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
        window_width (int): The width of the game window.
        window_height (int): The height of the game window.
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
        params = Sprite.merge_params(options, Game.default_options)

        self.name: str = params["name"]
        self.window_width: int = params["window_width"]
        self.window_height: int = params["window_height"]
        self.__aspect_ratio: float = params["aspect_ratio"]
        self.fps: int = params["fps"]
        self.reset_display: bool = params["reset_display"]
        self.__use_better_clock: float = params["better_clock"]

        self.__state = STATE.STOPPED

        self.__clock = pygame.time.Clock()
        Time.set_clock(self.__clock)

        self.__screen = pygame.display.set_mode(
            (self.window_width, self.window_height), pygame.RESIZABLE)
        self.__display = pygame.Surface(
            (self.window_width, self.window_height), pygame.SRCALPHA)

        pygame.display.set_caption(self.name)
        if options.get("icon"):
            pygame.display.set_icon(pygame.image.load(options.get("icon")))

        Display.set_display(self.__display)

        self.scenes = SceneManager()
        self.radio = Radio()

        self.__saved_dims = [self.window_width, self.window_height]

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, new_state: STATE):
        self.__state = new_state

        if self.__state == STATE.RUNNING:
            self.start_loop()
        if self.__state == STATE.STOPPED:
            pygame.event.post(pygame.QUIT)

    @property
    def window_size(self):
        """
        The current size of the window

        Returns:
            Vector: A vector with x representing the width and
            y representing the height
        """
        return Vector(self.window_width, self.window_height)

    def start_loop(self):
        """
        Starts the game loop. Should only be called by :meth:`rubato.begin`
        """
        self.__state = STATE.RUNNING
        while self.__state == STATE.RUNNING:
            self.update()

    def update(self):
        """The update loop for the game. Called automatically every frame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.radio.broadcast("EXIT")
                pygame.quit()
                sys.exit(1)
            if event.type == pygame.VIDEORESIZE:
                self.window_width = event.size[0]
                self.window_height = event.size[1]
            if event.type == pygame.KEYDOWN:
                self.radio.broadcast(Input.key.name(event.key) + "_down")
            if event.type == pygame.KEYUP:
                self.radio.broadcast(Input.key.name(event.key) + "_up")

        if (self.__saved_dims[0] != self.window_width
                or self.__saved_dims[1] != self.window_height):
            self.__screen = pygame.display.set_mode(
                (self.window_width, self.window_height), pygame.RESIZABLE)

        ratio = (self.window_width / self.window_height) < self.__aspect_ratio
        width = (self.window_height * self.__aspect_ratio,
                 self.window_width)[ratio]
        height = (self.window_height,
                  self.window_width / self.__aspect_ratio)[ratio]
        top_right = (((self.window_width - width) // 2, 0),
                     (0, (self.window_height - height) // 2))[ratio]

        self.draw()
        self.__screen.blit(
            pygame.transform.scale(self.__display, (int(width), int(height))),
            top_right)

        self.__saved_dims = [self.window_width, self.window_height]

        Time.process_calls()
        self.scenes.update()

        pygame.display.flip()
        self.radio.events = []

        if self.__use_better_clock:
            self.__clock.tick_busy_loop(self.fps)
        else:
            self.__clock.tick(self.fps)

    def draw(self):
        """Draw loop for the game. Called automatically every frame"""
        self.__screen.fill((0, 0, 0))
        if self.reset_display: self.__display.fill((255, 255, 255))
        self.scenes.draw(self)
        self.__display = Display.global_display
