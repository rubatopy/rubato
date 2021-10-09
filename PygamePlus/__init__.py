import pygame
from sys import exit
from PygamePlus.utils import STATE, GD
from PygamePlus.scenes.scene_manager import SceneManager
from PygamePlus.broadcast import Broadcast
from PygamePlus.sprite import Sprite
from PygamePlus.group import Group


class Game:
    """
    Main Game object. Controls everything in the game.

    :param name: The name of the window.
    :param window_width: The starting width of the window.
    :param window_height: The starting height of the window.
    :param reset_display: Whether to clear the display every frame before drawing.
    """

    def __init__(self, name: str, window_width: int, window_height: int, reset_display: bool = True):
        pygame.init()

        self.name = name

        self.state = STATE.STOPPED
        self.window_width = window_width
        self.window_height = window_height
        self.aspect_ratio = 1.5
        self.fps = 60

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
        self.display = pygame.Surface((window_width, window_height))
        pygame.display.set_caption(name)

        GD.set(self.display)

        self.scene_manager = SceneManager()
        self.reset_display = reset_display
        self.broadcast_system = Broadcast()

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

        ratio = (self.window_width / self.window_height) < self.aspect_ratio
        width = (self.window_height * self.aspect_ratio, self.window_width)[ratio]
        height = (self.window_height, self.window_width / self.aspect_ratio)[ratio]
        top_right = (((self.window_width - width) // 2, 0), (0, (self.window_height - height) // 2))[ratio]

        self.draw()
        self.screen.blit(pygame.transform.scale(self.display, (int(width), int(height))), top_right)

        self.broadcast_system.handle_events()

        self.scene_manager.update()

        pygame.display.flip()
        self.clock.tick(self.fps)
        self.broadcast_system.events = []

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
