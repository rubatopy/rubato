# TODO: Make this so that everything runs on it. One Function takes in their screen and makes it as the display.
import pygame, sys
from pygame.locals import *

mainClock = pygame.time.Clock()
pygame.init()
WINDOWWIDTH = 600
WINDOWHEIGHT = 400
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),pygame.RESIZABLE)
display = pygame.Surface((300,200))


def resize(event):
    global WINDOWWIDTH, WINDOWHEIGHT
    if event.type == pygame.VIDEORESIZE:
        WINDOWWIDTH = event.size[0]
        WINDOWHEIGHT = event.size[1]
        return pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE)


def game():
    global screen, display
    display.fill((255, 255, 255))
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            screen = resize(event)
        if event.type == KEYDOWN:
            pass

    ratio = WINDOWWIDTH / WINDOWHEIGHT
    height_center = 0
    width_center = 0
    if ratio < 1.5:
        width = WINDOWWIDTH
        height = WINDOWWIDTH / 1.5
        height_center = int((WINDOWHEIGHT - height) / 2)
    else:
        height = WINDOWHEIGHT
        width = WINDOWHEIGHT * 1.5
        width_center = int((WINDOWWIDTH - width) / 2)
    screen.blit(pygame.transform.scale(display, (int(width), int(height))), (width_center, height_center))
    pygame.display.update()
    mainClock.tick(40)


while True:
    game()
