import numpy as np
import random as rand
import pygame as pg

dr = [-1, 1, 0, 0, -1, -1, 1, 1]
dc = [0, 0, -1, 1, -1, 1, -1, 1]
queue = []

pg.init()

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
        bool_field[rr, cc] = 1

def random_mine(width, height):
    return rand.randint(0,height-1), rand.randint(0,width-1)

def pre_start(width, height, pocet_min):
    ...

def  update_field(field, bool_field, row, column):
    if field[row][column] == 0:
        queue.append([row, column])
        bool_field[row, column] = 1
        while len(queue) > 0:
            neighbours(queue[0][0], queue[0][1], field, bool_field)
            reveal(queue[0][0], queue[0][1], bool_field)
            queue.pop(0)
    elif field[row][column] == 9:
        # to write
        bool_field[row, column] = 1
    else:
        bool_field[row, column] = 1
    return field, bool_field


def field_description(width, height, mines, row, column):
    starting_row, starting_column = row, column
    not_mines_positions = set()
    field = np.zeros((height, width), dtype=int)
    bool_field = np.zeros((height, width), dtype=int)
    not_mines_positions.add((starting_row, starting_column))
    for i in range(8):
        rr = row + dr[i]
        cc = column + dc[i]
        if rr < 0 or rr >= len(bool_field): # výška
            continue
        elif cc < 0 or cc >= len(bool_field[0]): # šířka
            continue
        not_mines_positions.add((rr, cc))
    print(not_mines_positions)
    while True:
        field = np.zeros((height, width), dtype=int)
        bool_field = np.zeros((height, width), dtype=int)
        mines_position = set()
        for i in range(mines):
            position = random_mine(width,height)
            while position in mines_position or position in not_mines_positions:
                position = random_mine(width,height)
            field[position] = 9
            mines_position.add(position)
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

def start(width, height, mines, row, column): # prozatimní
    field, bool_field, mines_position = field_description(width, height, mines, row, column)
    return field, bool_field


