import pygame, sys
from PygamePlus.utils import STATE


class Game:
    """
    Main Game object. Controls everything in the game
    """

    def __init__(self, window_width, window_height):
        pygame.init()

        self.state = STATE.RUNNING
        self.window_width = window_width
        self.window_height = window_height

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
        self.display = pygame.Surface((window_width / 2, window_height / 2))

    def update(self):
        """
        Update loop for the game
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(1)
            if event.type == pygame.VIDEORESIZE:
                self.window_width = event.size[0]
                self.window_height = event.size[1]
                self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)

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
        self.screen.blit(pygame.transform.scale(self.display, (int(width), int(height))), (width_center, height_center))

        self.draw()

        pygame.display.flip()
        self.clock.tick(40)

    def draw(self):
        """
        Draw loop for the game
        """
        self.display.fill((255, 255, 255))
        self.screen.fill((0, 0, 0))

        pygame.draw.rect(self.screen, (255,255,0), [100, 100, 100, 100])

    def runGame(self):
        """
        Actually runs the game
        """
        while self.state == STATE.RUNNING:
            self.update()
