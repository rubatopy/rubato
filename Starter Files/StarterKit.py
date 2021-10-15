# TODO: Make this so that everything runs on it. One Function takes in their screen and makes it as the display.
import pygame, sys, webbrowser
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

text_size = 25
myfont = pygame.font.SysFont('Comic Sans MS', text_size)
cursor = 0
STATES = {
    "Menu": 1,
    "Running": 2,
    "Finished": 3,
}
current_state = STATES["Menu"]
white, black = (255, 255, 255), (0, 0, 0)

def DoMenu():
    MenuText = [
        "ALEXA TURN ON THE 2D PLATFORMER!!!",
        "",
        "Play",
        "About us",
    ]
    # input
    global cursor, current_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            keypressed = pygame.key.get_pressed()
            if keypressed[pygame.K_DOWN]:
                cursor += 1
            if keypressed[pygame.K_UP]:
                cursor -= 1
            if keypressed[pygame.K_RETURN]:
                if cursor == 0:
                    current_state = STATES["Running"]

                if cursor == 1:
                    webbrowser.open("https://curriculum.applied-computing.org/MathAndPythonJamesClass/MMM/ourclass.md")
    if cursor > 1:
        cursor = 0
    if cursor < 0:
        cursor = 1
    # update
    # draw
    screen.fill(white)
    index = 0
    for text in MenuText:
        if index - 2 == cursor:
            text = "> " + text
        text_color = black
        text_image = myfont.render(text, False, text_color)
        screen.blit(text_image, (20, 20 + index * text_size))
        index += 1
    pygame.display.flip()
    pass

def DoEndScreen():
    MenuText = [
        "ALEXA TURN ON THE 2D PLATFORMER!!!",
        "",
        "Congrats on finishing the game!",
        "",
        "Back to main menu",
        "About us",
    ]
    global cursor
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            keypressed = pygame.key.get_pressed()
            if keypressed[pygame.K_DOWN]:
                cursor += 1
            if keypressed[pygame.K_UP]:
                cursor -= 1
            if keypressed[pygame.K_RETURN]:
                if cursor == 0:
                    current_state = STATES["Menu"]
                if cursor == 1:
                    webbrowser.open("https://curriculum.applied-computing.org/MathAndPythonJamesClass/MMM/ourclass.md")
    if cursor > 1:
        cursor = 0
    if cursor < 0:
        cursor = 1
    # update
    # draw
    screen.fill(white)
    index = 0
    for text in MenuText:
        if index - 4 == cursor:
            text = "> " + text
        text_color = black
        text_image = myfont.render(text, False, text_color)
        screen.blit(text_image, (20, 20 + index * text_size))
        index += 1
    pygame.display.flip()
    pass


while True:
    if current_state == STATES["Running"]:
        game()
    if current_state == STATES["Menu"]:
        DoMenu()
    if current_state == STATES["Finished"]:
        DoEndScreen()
