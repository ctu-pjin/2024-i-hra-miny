import numpy as np
import random as rand
import pygame as pg

dr = [-1, 1, 0, 0, -1, -1, 1, 1]
dc = [0, 0, -1, 1, -1, 1, -1, 1]
queue = []

def neighbours(row , column, field, bool_field): # variace na BFS
    global dr, dc, queue
    for i in range(8):
        rr = row + dr[i]
        cc = column + dc[i]
        if rr < 0 or rr >= len(field): # výška
            continue
        elif cc < 0 or cc >= len(field[0]): # šířka
            continue
        if field[rr, cc] == 0:
            if bool_field[rr, cc] != 1:
                bool_field[rr, cc] = 1
                queue.append([rr, cc])

def reveal(row, column, bool_field):
    for i in range(8):
        rr = row + dr[i]
        cc = column + dc[i]
        if rr < 0 or rr >= len(bool_field): # výška
            continue
        elif cc < 0 or cc >= len(bool_field[0]): # šířka
            continue
        bool_field[rr, cc] = 1;

def random_mine(width, height):
    return rand.randint(0,height-1), rand.randint(0,width-1)

def field_description(width, height, mines):
    xy = pg.mouse.get_pos()
    starting_row, starting_column = click(xy[0], xy[1])
    while True:
        field = np.zeros((height, width), dtype=int)
        bool_field = np.zeros((height, width), dtype=int)
        mines_position = []
        for i in range(mines):
            position = random_mine(width,height)
            while position in mines_position:
                position = random_mine(width,height)
            field[position] = 9
            mines_position.append(position)
        for i, row in enumerate(field):
            for j, item in enumerate(row):
                if item == 9:
                    continue
                else:
                    sub_array = field[max(0, i-1):i+2, max(0, j-1):j+2]
                    field[i,j] = np.count_nonzero(sub_array == 9)
        sub_array = field[max(0,starting_row-1):starting_row+2, max(0,starting_column-1):starting_column+2]
        if field[starting_row,starting_column] == 0 and np.count_nonzero(sub_array == 0) > 1:
            queue.append([starting_row, starting_column])
            bool_field[starting_row, starting_column] = 1
            while len(queue) > 0:
                neighbours(queue[0][0], queue[0][1], field, bool_field)
                reveal(queue[0][0], queue[0][1], bool_field)
                queue.pop(0)
            break
    return field, bool_field, mines_position
        

def click(x, y, cell_size = 30): 
    dh = 100
    dw = 10
    row = int((y - dh)/cell_size)
    column = int((x-dw)/cell_size)
    return row, column

def start(width, height, mines): # prozatimní
    field, bool_field = field_description(width, height, mines)



start(10,10,10)