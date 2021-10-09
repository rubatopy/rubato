import pygame
from sys import exit
from pgp.utils import STATE, GD, Point
from pgp.scenes import SceneManager, Scene
from pgp.broadcast import Broadcast
from pgp.sprite import Sprite, Image
from pgp.group import Group
from pgp.input import Input


class Game:
    """
    Main Game object. Controls everything in the game.

    :param options: The config used to generate the game instance.
    """

    def __init__(self, options: dict = {}):
        pygame.init()

        self.name = options.get("name") or "Untitled Game"
        self.window_width = options.get("window_width") or 600
        self.window_height = options.get("window_height") or 400
        self.aspect_ratio = options.get("aspect_ratio") or 1.5
        self.fps = options.get("fps") or 60
        self.reset_display = options.get("reset_display") or True

        self.state = STATE.STOPPED
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        self.display = pygame.Surface((self.window_width, self.window_height))
        pygame.display.set_caption(self.name)
        if options.get("icon"):
            pygame.display.set_icon(pygame.image.load(options.get("icon")))

        GD.set(self.display)

        self.scene_manager = SceneManager()
        self.broadcast = Broadcast()

    def update(self):
        """Update loop for the game."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # TODO Pass and handle quit event through broadcast system first
                exit(1)
            if event.type == pygame.VIDEORESIZE:
                self.window_width = event.size[0]
                self.window_height = event.size[1]
                self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                self.broadcast.broadcast_event(Input.key.name(event.key)+"_down")
            if event.type == pygame.KEYUP:
                self.broadcast.broadcast_event(Input.key.name(event.key)+"_up")

        ratio = (self.window_width / self.window_height) < self.aspect_ratio
        width = (self.window_height * self.aspect_ratio, self.window_width)[ratio]
        height = (self.window_height, self.window_width / self.aspect_ratio)[ratio]
        top_right = (((self.window_width - width) // 2, 0), (0, (self.window_height - height) // 2))[ratio]

        self.draw()
        self.screen.blit(pygame.transform.scale(self.display, (int(width), int(height))), top_right)

        self.scene_manager.update()

        pygame.display.flip()
        self.clock.tick(self.fps)
        self.broadcast.events = []

    def draw(self):
        """Draw loop for the game."""
        if self.reset_display: self.display.fill((255, 255, 255))
        self.screen.fill((0, 0, 0))
        self.scene_manager.draw()
        self.display = GD.display()

    def begin(self):
        """
        Actually runs the game
        """
        self.state = STATE.RUNNING
        while self.state == STATE.RUNNING:
            self.update()
