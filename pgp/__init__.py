import pygame
from sys import exit
from pgp.utils import STATE, Display, Vector, Time
from pgp.scenes import SceneManager, Scene
from pgp.radio import Radio
from pgp.sprite import Sprite, Image, RigidBody
from pgp.group import Group
from pgp.input import Input

# TODO Sound manager
class Game:
    """
    Main Game object. Controls everything in the game.

    :param options: The config used to generate the game instance.
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

        self.name = options.get("name", Game.default_options["name"])
        self.window_width = options.get("window_width", Game.default_options["window_width"])
        self.window_height = options.get("window_height", Game.default_options["window_height"])
        self.aspect_ratio = options.get("aspect_ratio", Game.default_options["aspect_ratio"])
        self.fps = options.get("fps", Game.default_options["fps"])
        self.reset_display = options.get("reset_display", Game.default_options["reset_display"])
        self.use_better_clock = options.get("better_clock", Game.default_options["better_clock"])

        self.state = STATE.STOPPED

        self.clock = pygame.time.Clock()
        Time.set(self.clock)

        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        self.display = pygame.Surface((self.window_width, self.window_height))

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
        self.scenes.draw()
        self.display = Display.display()

    def begin(self):
        """
        Actually runs the game
        """
        self.state = STATE.RUNNING
        while self.state == STATE.RUNNING:
            self.update()