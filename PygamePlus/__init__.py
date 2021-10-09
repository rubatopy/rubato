import pygame
from sys import exit
from PygamePlus.utils import STATE, GD
from PygamePlus.scenes.SceneManager import SceneManager
from PygamePlus.Broadcast import Broadcast
from PygamePlus.Sprite import Sprite
from PygamePlus.Group import Group


class Game:
    """
    Main Game object. Controls everything in the game.

    :param window_width: The starting width of the window.
    :param window_height: The starting height of the window.
    :param reset_display: Whether to clear the display every frame before drawing.
    """

    def __init__(self, window_width: int, window_height: int, reset_display: bool=True):
        pygame.init()

        self.state = STATE.STOPPED
        self.window_width = window_width
        self.window_height = window_height
        self.fps = 60

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
        self.display = pygame.Surface((window_width, window_height))

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

        self.broadcast_system.keys = pygame.key.get_pressed()

        ratio = self.window_width / self.window_height
        height_center = 0
        width_center = 0
        if ratio < 1.5:
            width = self.window_width
            height = self.window_width / 1.5
            height_center = int((self.window_height - height) / 2)
        else:
            height = self.window_height
            width = self.window_height * 1.5
            width_center = int((self.window_width - width) / 2)

        self.draw()
        self.screen.blit(pygame.transform.scale(self.display, (int(width), int(height))), (width_center, height_center))

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

