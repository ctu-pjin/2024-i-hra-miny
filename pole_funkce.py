import numpy as np
import random as rand
import pygame as pg

dr = [-1, 1, 0, 0, -1, -1, 1, 1]
dc = [0, 0, -1, 1, -1, 1, -1, 1]
queue = []

pg.init()

def separate_string_by_commas(string):
    string = string.strip()  # Strip leading and trailing spaces
    string_split = [s.strip() for s in string.split(",")]
    return string_split

def is_it_integer(list_of_strings): # tests if input is an integer
    for string in list_of_strings:
        try:
            int(string)
        except:
            return False
    return True

def is_it_float(list_of_floats):
    print(list_of_floats)
    for string in list_of_floats:
        try:
            float(string)
        except:
            print("Float se nezdařil")
            return False
    return True

def field_creation_conditions(list_of_strings): # checks if it's possible to create a field from custom input, used for custom fields
    width, height, pocet_min = int(list_of_strings[0]), int(list_of_strings[1]), int(list_of_strings[2])
    if pocet_min <= 0 or width <= 0 or height <= 0 or pocet_min > width*height - 15:
        return False
    return True


def current_mines_positions(field, bool_field): # returns positions of undiscovered mines, used in hint
    current_mines = []
    for i, row in enumerate(field):
        for j, item in enumerate(row):
            if item == 9 and bool_field[i][j] == 0:
                current_mines.append((i,j))
    return current_mines


def hint(field, bool_field): # hint functions that picks a random undiscoverd mine and places a flag on it
    current_mines = current_mines_positions(field, bool_field)
    if len(current_mines) == 0:
        return bool_field
    hint = rand.choice(current_mines)
    bool_field[hint[0],hint[1]] = 3
    return bool_field


def neighbouring_cells_without_turning(row, column, bool_field): # for middle click, if an undiscovered cell is around the place where we clicked, it will show as an empty field, plotting in pygamepart
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


def verify_amount_of_flags(field, bool_field, row, column): # for middle click, checks if the field's surroundings are controlled or not, returns true if yes
    sub_array = bool_field[max(0, row-1):row+2, max(0, column-1):column+2]
    if (np.count_nonzero(sub_array == 2) + np.count_nonzero(sub_array == 3)) == field[row][column]:
        return True
    else:
        return False


def cluster_reveal(field, bool_field, row, column): # revealing field automatically, in case of zeros BFS to reveal around all of them
    queue.append([row, column])
    reveal_around_zeroes(field, bool_field)
    return field, bool_field


def uncaged_mines(field, bool_field): # counting unflagged mines, for reshuffle
    caged_mines = 0
    total_mines = np.count_nonzero(field == 9)
    for i, row in enumerate(field):
        for j, item in enumerate(row):
            if item == 9 and (bool_field[i,j] == 2 or bool_field[i,j] == 3):
                caged_mines += 1
            elif item == 9:
                field[i,j] = -1
    uncaged_mines = total_mines - caged_mines
    return uncaged_mines, field


def reshuffle(field, bool_field): # changes positions of unflagged mines
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
    reveal_around_zeroes(field, bool_field) # if no mines are near a discovered field and it turns into a zero, it is necessary to discover its surroundings, a zero musn't be at the border
    return field, bool_field


def reveal_around_zeroes(field, bool_field): # reveals the surroundings of previously queued zeros, checking their surroundings for more zeroes, a chain reaction
    while len(queue) > 0:
        neighbours(queue[0][0], queue[0][1], field, bool_field)
        reveal(queue[0][0], queue[0][1], bool_field)
        queue.pop(0)


def neighbours(row , column, field, bool_field): # BFS, checks for zeroes in neighbourhoods, putting them into the queue
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


def reveal(row, column, bool_field): # assigns "revealed" marker to the surroundings of a cell
    for i in range(8):
        rr = row + dr[i]
        cc = column + dc[i]
        if rr < 0 or rr >= len(bool_field): # výška
            continue
        elif cc < 0 or cc >= len(bool_field[0]): # šířka
            continue
        elif bool_field[rr, cc] == 2 or bool_field[rr,cc] == 3:
            continue
        bool_field[rr, cc] = 1


def random_mine(width, height): #chooses a random position for a mine in the field
    return rand.randint(0,height-1), rand.randint(0,width-1)


def update_field(field, bool_field, row, column): # ran after clicking, updates what we did into the field and bool_field
    if field[row][column] == 0: # checks for zeroes
        queue.append([row, column]) 
        bool_field[row, column] = 1
        reveal_around_zeroes(field, bool_field) # starting a chain reaction to reveal a cluster if necessary
    else:
        bool_field[row, column] = 1
    return field, bool_field


def count_field(field): # counts the numbers in cells based on how many mines they share a border with
    for i, row in enumerate(field):
            for j, item in enumerate(row):
                if item == 9:
                    continue
                else:
                    sub_array = field[max(0, i-1):i+2, max(0, j-1):j+2]
                    field[i,j] = np.count_nonzero(sub_array == 9)
    return field


def field_description(width, height, mines, row, column): # field generated after first click
    starting_row, starting_column = row, column
    not_mines_positions = set()
    field = np.zeros((height, width), dtype=int)
    bool_field = np.zeros((height, width), dtype=int)
    not_mines_positions.add((starting_row, starting_column)) # to create an "island" with first click 
    for i in range(8): # starting click has to be on a zero field
        rr = row + dr[i]
        cc = column + dc[i]
        if rr < 0 or rr >= len(bool_field): # výška
            continue
        elif cc < 0 or cc >= len(bool_field[0]): # šířka
            continue
        not_mines_positions.add((rr, cc))
    neighbour_zero = rand.choice(list(not_mines_positions)) # starting click has to have at least one zero neighbour
    while neighbour_zero == (row, column):
        neighbour_zero = rand.choice(list(not_mines_positions))
    for i in range(8):
        rr = neighbour_zero[0] + dr[i]
        cc = neighbour_zero[1] + dc[i]
        if rr < 0 or rr >= len(bool_field): # výška
            continue
        elif cc < 0 or cc >= len(bool_field[0]): # šířka
            continue
        not_mines_positions.add((rr, cc)) # their surroundings added to the "island"
    mines_position = set()
    for i in range(mines):
        position = random_mine(width,height) # random positions for mines from the rest of the field
        while position in mines_position or position in not_mines_positions:
            position = random_mine(width,height)
        field[position] = 9
        mines_position.add(position)
    field = count_field(field) # get values for all cells based on mine positions
    queue.append([starting_row, starting_column])
    bool_field[starting_row, starting_column] = 1 # assigning revealed status
    reveal_around_zeroes(field, bool_field)
    return field, bool_field
        

def click(x, y, dw, dh, add_dw = 0, add_dh = 0, cell_size = 30): # transforms coordinates from pygame into row and column of the field
    row = int((y - dh-add_dh)/cell_size)
    column = int((x-dw-add_dw)/cell_size)
    return row, column

