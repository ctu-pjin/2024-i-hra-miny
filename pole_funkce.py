import numpy as np
import random as rand
import pygame as pg

dr = [-1, 1, 0, 0, -1, -1, 1, 1]
dc = [0, 0, -1, 1, -1, 1, -1, 1]
queue = []

pg.init()

def neighbouring_cells_without_turning(row, column, bool_field):
    empty_cells_to_plot = []
    if bool_field[row, column] == 0:
        empty_cells_to_plot.append([column, row])
    for i in range(8):
        rr = row + dr[i]
        cc = column + dc[i]
        if rr < 0 or rr >= len(bool_field): # výška
            continue
        elif cc < 0 or cc >= len(bool_field[0]): # šířka
            continue
        if bool_field[rr, cc] == 0:
            empty_cells_to_plot.append([cc, rr])
    return empty_cells_to_plot


def verify_amount_of_flags(field, bool_field, row, column):
    sub_array = bool_field[max(0, row-1):row+2, max(0, column-1):column+2]
    if np.count_nonzero(sub_array == 2) == field[row][column]:
        return True
    else:
        return False


def cluster_reveal(field, bool_field, row, column):
    queue.append([row, column])
    reveal_around_zeroes(field, bool_field)
    return field, bool_field


def uncaged_mines(field, bool_field):
    caged_mines = 0
    total_mines = np.count_nonzero(field == 9)
    for i, row in enumerate(field):
        for j, item in enumerate(row):
            if item == 9 and bool_field[i,j] == 2:
                caged_mines += 1
            elif item == 9:
                field[i,j] = -1
    uncaged_mines = total_mines - caged_mines
    return uncaged_mines, field


def reshuffle(field, bool_field):
    number_of_mines_to_shuffle, field = uncaged_mines(field, bool_field)
    undiscovered_fields = []
    mines_positions = set()
    for i, row in enumerate(bool_field):
        for j, item in enumerate(row):
            if item == 0:
                undiscovered_fields.append((i, j))
    for i in range(number_of_mines_to_shuffle):
        position = rand.choice(undiscovered_fields)
        while position in mines_positions:
            position = rand.choice(undiscovered_fields)
        mines_positions.add(position)
        field[position] = 9
    field = count_field(field)
    for i, row in enumerate(field):
        for j, item in enumerate(row):
            if item == 0 and bool_field[i][j] == 1:
                queue.append([i,j])
    reveal_around_zeroes(field, bool_field)
    return field, bool_field


def reveal_around_zeroes(field, bool_field):
    while len(queue) > 0:
        neighbours(queue[0][0], queue[0][1], field, bool_field)
        reveal(queue[0][0], queue[0][1], bool_field)
        queue.pop(0)


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
        elif bool_field[rr, cc] == 2:
            continue
        bool_field[rr, cc] = 1


def random_mine(width, height):
    return rand.randint(0,height-1), rand.randint(0,width-1)


def  update_field(field, bool_field, row, column):
    if field[row][column] == 0:
        queue.append([row, column])
        bool_field[row, column] = 1
        reveal_around_zeroes(field, bool_field)
    else:
        bool_field[row, column] = 1
    return field, bool_field


def count_field(field):
    for i, row in enumerate(field):
            for j, item in enumerate(row):
                if item == 9:
                    continue
                else:
                    sub_array = field[max(0, i-1):i+2, max(0, j-1):j+2]
                    field[i,j] = np.count_nonzero(sub_array == 9)
    return field


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
    neighbour_zero = rand.choice(list(not_mines_positions))
    while neighbour_zero == (row, column):
        neighbour_zero = rand.choice(list(not_mines_positions))
    for i in range(8):
        rr = neighbour_zero[0] + dr[i]
        cc = neighbour_zero[1] + dc[i]
        if rr < 0 or rr >= len(bool_field): # výška
            continue
        elif cc < 0 or cc >= len(bool_field[0]): # šířka
            continue
        not_mines_positions.add((rr, cc))
    mines_position = set()
    for i in range(mines):
        position = random_mine(width,height)
        while position in mines_position or position in not_mines_positions:
            position = random_mine(width,height)
        field[position] = 9
        mines_position.add(position)
    field = count_field(field)
    sub_array = field[max(0,starting_row-1):starting_row+2, max(0,starting_column-1):starting_column+2]
    queue.append([starting_row, starting_column])
    bool_field[starting_row, starting_column] = 1
    reveal_around_zeroes(field, bool_field)
    return field, bool_field
        

def click(x, y, dw, dh, add_dw = 0, cell_size = 30): 
    row = int((y - dh)/cell_size)
    column = int((x-dw-add_dw)/cell_size)
    return row, column

