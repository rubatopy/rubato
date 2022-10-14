"""A simple tetris game built with Rubato"""
from rubato import *
from rubato import Vector as V

init(name="tetris", res=Vector(22, 42), window_size=(220, 420))


def incScore(add):
    global score
    score += add
    Display.window_name = f"tetris - score: {score}"


score = 0
incScore(0)

field = [[0] * 10] * 20

block_size = 2

i_piece = [
    [0, 0, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0],
]
j_piece = [
    [0, 1, 0],
    [0, 1, 0],
    [1, 1, 0],
]
l_piece = [
    [0, 1, 0],
    [0, 1, 0],
    [0, 1, 1],
]
t_piece = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 0, 0],
]
s_piece = [
    [0, 1, 1],
    [1, 1, 0],
    [0, 0, 0],
]
z_piece = [
    [1, 1, 0],
    [0, 1, 1],
    [0, 0, 0],
]
o_piece = [
    [1, 1],
    [1, 1],
]

current = z_piece
pos = V(1, 0)


def draw_block(pos, color):
    Draw.rect(
        center=Display.top_left + ((pos * block_size) + (1 + block_size / 2, -1 - block_size / 2)),
        width=block_size,
        height=block_size,
        border=None,
        fill=color,
    )


def draw_scene():
    Draw.clear(Color.darkgray)

    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j]:
                draw_block(V(j, -i), Color.magenta)
            else:
                draw_block(V(j, -i), Color.black.lighter())

    for i in range(len(current)):
        for j in range(len(current[i])):
            if current[i][j]:
                draw_block(pos + V(j, i), Color.red)


def moveDown():
    pos.y -= 1
    incScore(1)


Game.draw = draw_scene

Time.schedule(RecurrentTask(moveDown, 1000, 1000))

begin()
