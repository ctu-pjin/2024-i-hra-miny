import numpy as np
import random as rand


def random_mine(width,height):
    return rand.randint(0,height-1), rand.randint(0,width-1)

def field_description(width, height, mines):
    mines_position = []
    field = np.zeros((height, width), dtype=int)
    bool_field = np.zeros((height, width), dtype=int)
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
    print(field)

field_description(5,7,10)