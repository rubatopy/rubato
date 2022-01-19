from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
environ["PYTHONOPTIMIZE"] = "1" # Makes sure that typechecking is run at the start of runtime instead of all the time
import pygame
from sys import exit
# from typeguard.importhook import install_import_hook
# install_import_hook("rubato")
from rubato.utils import PMath, classproperty, STATE, Display, Vector, Time, Polygon, Circle, SAT, COL_TYPE, Color
from rubato.scenes import SceneManager, Scene, Camera
from rubato.radio import Radio
from rubato.sprite import Sprite, Image, RigidBody, Button, Rectangle, Text, Empty
from rubato.group import Group
from rubato.input import Input

game = None

# TODO Sound manager
# TODO make it so that the 0,0 coordinate is the center of the inital screen and that positive y is up
class Game:
    """
    Main Game object. Controls everything in the game.

    :param options: The :ref:`config <defaultgame>` used to generate the game instance.
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
        pygame.init()
        self.params = Sprite.merge_params(options, Game.default_options)

        self.name = self.params["name"]
        self.window_width = self.params["window_width"]
        self.window_height = self.params["window_height"]
        self.aspect_ratio = self.params["aspect_ratio"]
        self.fps = self.params["fps"]
        self.reset_display = self.params["reset_display"]
        self.use_better_clock = self.params["better_clock"]

        self.state = STATE.STOPPED

        self.clock = pygame.time.Clock()
        Time.set(self.clock)

        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        self.display = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)

        pygame.display.set_caption(self.name)
        if options.get("icon"):
            pygame.display.set_icon(pygame.image.load(options.get("icon")))

        Display.set(self.display)

        self.scenes = SceneManager()
        self.radio = Radio()

    def update(self):
        """Update loop for the game."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.radio.broadcast("EXIT")
                pygame.quit()
                exit(1)
            if event.type == pygame.VIDEORESIZE:
                self.window_width = event.size[0]
                self.window_height = event.size[1]
                self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                self.radio.broadcast(Input.key.name(event.key) + "_down")
            if event.type == pygame.KEYUP:
                self.radio.broadcast(Input.key.name(event.key) + "_up")

        ratio = (self.window_width / self.window_height) < self.aspect_ratio
        width = (self.window_height * self.aspect_ratio, self.window_width)[ratio]
        height = (self.window_height, self.window_width / self.aspect_ratio)[ratio]
        top_right = (((self.window_width - width) // 2, 0), (0, (self.window_height - height) // 2))[ratio]

        self.draw()
        self.screen.blit(pygame.transform.scale(self.display, (int(width), int(height))), top_right)

        Time.process_calls()
        self.scenes.update()

        pygame.display.flip()
        self.radio.events = []

        if self.use_better_clock:
            self.clock.tick_busy_loop(self.fps)
        else:
            self.clock.tick(self.fps)

    def draw(self):
        """Draw loop for the game."""
        self.screen.fill((0, 0, 0))
        if self.reset_display: self.display.fill((255, 255, 255))
        self.scenes.draw(game)
        self.display = Display.display

    def start_loop(self):
        """
        Actually runs the game
        """
        self.state = STATE.RUNNING
        while self.state == STATE.RUNNING:
            self.update()

    @property
    def window_size(self):
        """
        return the size of the game window
        """
        return Vector(self.window_width, self.window_height)


def init(options: dict = {}):
    """
    Initializes rubato.

    :param options: The :ref:`config <defaultgame>` used to generate the game instance.
    """
    global game
    game = Game(options)

def begin():
    """
    Starts the main game loop.
    """
    if game is not None:
        game.start_loop()
    else:
        raise RuntimeError("You have not initialized rubato. Make sure to run rubato.init() right after importing the library")
