import pygame
from sys import exit
from random import choice, randint
import os
import pole_funkce
import score_funkce as ScFn
import json
import numpy as np
import time
import math


# Initialize Pygame
os.environ['SDL_VIDEO_CENTERED'] = '1' # Centers the screen on the display
os.environ['SDL_RENDER_SCALE_QUALITY'] = '2' # '0' is the worst quality | '2' is the best quality | '1' is in the middle
                                        # May reduce later
pygame.init()


"""Preassigning variables"""
screen_width, screen_height = 480, 540
screen_width_game, screen_height_game = 100, 100
dw = 10
dh = 50
additional_dw = 0
additional_dh = 0
previous_time = time.time()
remaining_flags = 0
reshuffle_count = 3
field = []
bool_field = []
current_it = 0
cell_size = 30
difficulty = str()
data_list = []

MENU_SCREEN_DIMENSIONS = (480, 540)
fps = 60


screen = pygame.display.set_mode(MENU_SCREEN_DIMENSIONS)
menu_bg_surface = pygame.Surface((screen_width, screen_height))


# Part for loading images
new_game_surf_off = pygame.image.load("surfaces/new_game_button_off.png").convert_alpha() #surfaces of the object
new_game_surf_on = pygame.image.load("surfaces/new_game_button_on.png").convert_alpha() 
load_surf_off = pygame.image.load("surfaces/load_button_off.png").convert_alpha()
load_surf_on = pygame.image.load("surfaces/load_button_on.png").convert_alpha()
back_arrow_surf_on = pygame.image.load("surfaces/back_arrow_flow_on.png").convert_alpha()
back_arrow_surf_off = pygame.image.load("surfaces/back_arrow_flow_off.png").convert_alpha()
back_arrow_surf_on_small = pygame.transform.scale_by(back_arrow_surf_on, 0.7)
back_arrow_surf_off_small = pygame.transform.scale_by(back_arrow_surf_off, 0.7)
easy_surf_on  = pygame.image.load("surfaces/easy_button_on.png").convert_alpha()
easy_surf_off  = pygame.image.load("surfaces/easy_button_off.png").convert_alpha()
medium_surf_on  = pygame.image.load("surfaces/medium_button_on.png").convert_alpha()
medium_surf_off  = pygame.image.load("surfaces/medium_button_off.png").convert_alpha()
hard_surf_on  = pygame.image.load("surfaces/hard_button_on.png").convert_alpha()
hard_surf_off  = pygame.image.load("surfaces/hard_button_off.png").convert_alpha()
box_surf = pygame.image.load("mines/box.png").convert()
one_surf = pygame.image.load("mines/one.png").convert()
two_surf = pygame.image.load("mines/two.png").convert()
three_surf = pygame.image.load("mines/three.png").convert()
four_surf = pygame.image.load("mines/four.png").convert()
five_surf = pygame.image.load("mines/five.png").convert()
six_surf = pygame.image.load("mines/six.png").convert()
null_surf = pygame.image.load("mines/empty.png").convert()
mine_surf = pygame.image.load("mines/mine.png").convert()
mine_purple_surf = pygame.image.load("mines/mine_purple.png").convert()
mine_explode_surf = pygame.image.load("mines/mine_explode.png").convert()
flag_surf = pygame.image.load("mines/flag.png").convert()
seven_surf = pygame.image.load("mines/seven.png").convert()
eight_surf = pygame.image.load("mines/eight.png").convert()

scale_factor = 1
def scale_surface(surface, scale):
    width, height = surface.get_size()
    if scale == 1:
        return surface
    else:
        return pygame.transform.smoothscale(surface, (int(width * scale), int(height * scale)))

one_surf_game = scale_surface(one_surf, scale_factor)
box_surf_game = scale_surface(box_surf, scale_factor)
two_surf_game = scale_surface(two_surf, scale_factor)
three_surf_game = scale_surface(three_surf, scale_factor)
four_surf_game = scale_surface(four_surf, scale_factor)
five_surf_game = scale_surface(five_surf, scale_factor)
six_surf_game = scale_surface(six_surf, scale_factor)
null_surf_game = scale_surface(null_surf, scale_factor)
mine_surf_game = scale_surface(mine_surf, scale_factor)
mine_explode_surf_game = scale_surface(mine_explode_surf, scale_factor)
flag_surf_game = scale_surface(flag_surf, scale_factor)
seven_surf_game = scale_surface(seven_surf, scale_factor)
eight_surf_game = scale_surface(eight_surf, scale_factor)



cell_size *= scale_factor


reshuffle_on_surf = pygame.image.load("surfaces/reshuffle_on.png").convert_alpha()
reshuffle_off_surf = pygame.image.load("surfaces/reshuffle_off.png").convert_alpha()
flag_only_surf = pygame.image.load("surfaces/flag_only.png").convert_alpha()
flag_only_surf_big = pygame.transform.scale_by(flag_only_surf, 1.5)
save_icon_on_surf = pygame.image.load("surfaces/save_icon_on.png").convert_alpha()
save_icon_off_surf = pygame.image.load("surfaces/save_icon_off.png").convert_alpha()
transparent_bg_surf = pygame.image.load("surfaces/transparent_bg_80.png").convert_alpha()
empty_save_surf = pygame.image.load("surfaces/empty_save.png").convert_alpha()
filled_save_surf = pygame.image.load("surfaces/filled_save.png").convert_alpha()
game_save_surfs = [pygame.image.load("surfaces/filled_save.png").convert_alpha() for _ in range(3)]


# Create rectangles
new_game_rect_off = new_game_surf_off.get_rect(midbottom=(screen_width/2, 400)) #rectangle of the surface. Easier to specify an exact location
new_game_rect_on = new_game_surf_on.get_rect(midbottom=(screen_width/2, 400))
load_rect_off = load_surf_off.get_rect(midbottom=(screen_width/2, 500)) 
load_rect_on = load_surf_on.get_rect(midbottom=(screen_width/2, 500))
easy_rect_on = easy_surf_on.get_rect(midbottom=(screen_width/2, 250))
easy_rect_off = easy_surf_off.get_rect(midbottom=(screen_width/2, 250))
medium_rect_on = medium_surf_on.get_rect(midbottom=(screen_width/2, 350))
medium_rect_off = medium_surf_off.get_rect(midbottom=(screen_width/2, 350))
hard_rect_on = hard_surf_on.get_rect(midbottom=(screen_width/2, 450))
hard_rect_off = hard_surf_off.get_rect(midbottom=(screen_width/2, 450))
back_arrow_rect = back_arrow_surf_off.get_rect(topleft = (20, 20))
back_arrow_rect_small = back_arrow_surf_off_small.get_rect(topleft = (10, 15))
reshuffle_rect = reshuffle_on_surf.get_rect(bottomleft = (10, 20))
flag_rect = flag_only_surf.get_rect(bottomright = (screen_width-10, screen_height-10))


save_slot_width = empty_save_surf.get_width()
save_slot_height = empty_save_surf.get_height()
save_slot_rects = []
save_y_offset = 160

for slot in range(3):
    save_slot_rect = pygame.Rect(screen_width/2 - save_slot_width/2, save_y_offset, save_slot_width, save_slot_height)
    save_slot_rects.append(save_slot_rect)
    save_y_offset += 95


"""Functions for mine_menu background generation"""
def random_mine_surf(scale = True):
    if scale is True:
        return choice([box_surf_game] * 30 + [null_surf_game, flag_surf_game] * 5 + [mine_surf_game] * 2 + [one_surf_game] * 4 + [two_surf_game] * 3 + [three_surf_game, four_surf_game, five_surf_game] * 2 + [six_surf_game, seven_surf_game, eight_surf_game])
    else:
        return choice([box_surf] * 30 + [null_surf, flag_surf] * 5 + [mine_surf] * 2 + [one_surf] * 4 + [two_surf] * 3 + [three_surf, four_surf, five_surf] * 2 + [six_surf, seven_surf, eight_surf])


def random_mine_screen_plot(w, h, mine_field):
    random_h, random_w = randint(0, int(h/cell_size)-1), randint(0, int(w/cell_size)-1)
    mine_field[random_h][random_w] = random_mine_surf()
    for hh in range(0, h, cell_size):
            for ww in range(0, w, cell_size):
                screen.blit(mine_field[int(hh/cell_size)][int(ww/cell_size)], (ww, hh))
                

def draw_to_menu_bg(buffer_surface, mine_field, cell_size=30):
    """Draw the entire minefield onto the buffer surface."""
    for row in range(len(mine_field)):
        for col in range(len(mine_field[row])):
            buffer_surface.blit(mine_field[row][col], (col * cell_size, row * cell_size))


def random_mine_screen_generation(w, h, cell_size = 30):
    mine_field = []
    for _ in range(int(h/cell_size)):
        radek = []
        for _ in range(int(w/cell_size)):
            radek.append(random_mine_surf(scale = False))
        mine_field.append(radek)
    return mine_field


def update_cell(buffer_surface, mine_field, cell_size=30):
    """Randomly update a specific cell in the minefield and redraw it on the buffer."""
    row = randint(0, len(mine_field) - 1)
    col = randint(0, len(mine_field[0]) - 1)
    mine_field[row][col] = random_mine_surf(scale = False)
    buffer_surface.blit(mine_field[row][col], (col * cell_size, row * cell_size))


"""Save and load functions"""

save_slots = ["save1.json", "save2.json", "save3.json"]


def load_game(slot):
    filename = "saves/" + save_slots[slot]
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                #print(f"Loaded save from {filename}")
                return data
            
        except (json.JSONDecodeError, ValueError) as e:
            #print(f"Error loading {filename}: {e}")
            return None  # Return None if file is invalid
        
    else:
        #print(f"Save file {filename} does not exist.")
        return None  # Return None if file does not exist


def save_game(slot, data):
    filename = "saves/" + save_slots[slot]
    try:
        with open(filename, 'w') as f:
            json.dump(data, f)
            #print(f"Game saved to {filename}")
    except Exception as e:
        ...
        #print(f"Error saving to {filename}: {e}")


# Part for loading fonts
karma_font_160 = pygame.font.Font("fonts/KarmaFuture.otf", 160)
karma_font_60 = pygame.font.Font("fonts/KarmaFuture.otf", 60)
karma_sature_font_23 = pygame.font.Font("fonts/KarmaSuture.otf", 23)
karma_sature_font_21 = pygame.font.Font("fonts/KarmaSuture.otf", 21)
karma_sature_font_30 = pygame.font.Font("fonts/KarmaSuture.otf", 30)
karma_font_35 = pygame.font.Font("fonts/KarmaFuture.otf", 35)

# Part for loading texts
text_miny_surf = karma_font_160.render("Miny", False, "Black")
text_miny_rect = text_miny_surf.get_rect(midtop=(screen_width/2, 40))
text_difficulty_surf = karma_font_60.render("Difficulty", False, "Black")
text_difficulty_rect = text_difficulty_surf.get_rect(midtop=(screen_width/2, 70))
text_save_system_surf = karma_font_60.render("Save system", False, "Black")
text_save_system_rect = text_save_system_surf.get_rect(midtop=(screen_width/2, 70))
text_load_system_surf = karma_font_60.render("Load system", False, "Black")
victory_lines = ["Press Space to", "return to main menu", "OR", "Press Enter to", "submit your score"]
lose_lines = ["Press Space to", "return to main menu", "", "Good luck", "next time"]
text_press_space_surfs = [karma_sature_font_23.render(text, False, "White") for text in victory_lines]
text_press_enter_surfs = [karma_sature_font_23.render(text, False, "White") for text in lose_lines]
text_victory_surf = karma_font_35.render("You won!", False, "White")
text_lose_surf = karma_font_35.render("You lost!", False, "White")
text_miny_rect = text_miny_surf.get_rect(midtop=(screen_width/2, 40))
text_submit_username_surf = karma_sature_font_21.render("Enter your Username:", False, "Black")



clock = pygame.time.Clock()
mine_field = random_mine_screen_generation(screen_width, screen_height)
draw_to_menu_bg(menu_bg_surface, mine_field)
data_list = [load_game(slot) or {} for slot in range(3)]


def plot_bool_field(bool_field, field, cell_size = 30): # minefield plotting
    for row in range(len(field)):
        for col in range(len(field[row])):
            match bool_field[row,col]:
                case 0:
                    screen.blit(box_surf_game, (col*cell_size+dw+additional_dw, row*cell_size+dh+additional_dh))
                case 1:
                    match field[row,col]:
                        case 0:
                            screen.blit(null_surf_game, (col*cell_size+dw+additional_dw, row*cell_size+dh+additional_dh))
                        case 1: 
                            screen.blit(one_surf_game, (col*cell_size+dw+additional_dw, row*cell_size+dh+additional_dh))
                        case 2: 
                            screen.blit(two_surf_game, (col*cell_size+dw+additional_dw, row*cell_size+dh+additional_dh))
                        case 3: 
                            screen.blit(three_surf_game, (col*cell_size+dw+additional_dw, row*cell_size+dh+additional_dh))
                        case 4: 
                            screen.blit(four_surf_game, (col*cell_size+dw+additional_dw, row*cell_size+dh+additional_dh))
                        case 5: 
                            screen.blit(five_surf_game, (col*cell_size+dw+additional_dw, row*cell_size+dh+additional_dh))
                        case 6: 
                            screen.blit(six_surf_game, (col*cell_size+dw+additional_dw, row*cell_size+dh+additional_dh))
                        case 7: 
                            screen.blit(seven_surf_game, (col*cell_size+dw+additional_dw, row*cell_size+dh+additional_dh))
                        case 8: 
                            screen.blit(eight_surf_game, (col*cell_size+dw+additional_dw, row*cell_size+dh+additional_dh))
                        case 9: 
                            screen.blit(mine_surf_game, (col*cell_size+dw+additional_dw, row*cell_size+dh+additional_dh))
                case 2:
                    screen.blit(flag_surf_game, (col*cell_size+dw+additional_dw, row*cell_size+dh+additional_dh))


def plot_empty_field(width, height, cell_size = 30):
    for row in range(height):
        for col in range(width):
            screen.blit(box_surf_game, (col*cell_size+dw+additional_dw, row*cell_size+dh+additional_dh))


"""Provizorni"""
# Input Box
username_box = pygame.Rect(40, 90, 220, 40)
username_text = ""
username_button_active = False

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)


def main():
    empty_cells_to_plot = []
    it = 0
    menu = True
    first_click = False
    new_game_menu = False
    win_screen = False
    game = False
    load_screen = False
    save_screen = False
    end_screen = False
    submit_score_screen = False
    global screen, screen_height_game, screen_width_game, additional_dw, additional_dh, previous_time, remaining_flags, data_list, current_it, scale_factor
    global username_text, username_button_active
    mines_rect = pygame.Rect(0, 0, 0, 0)

    while True: 
        for event in pygame.event.get():  # All events are written in this for loop
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            if menu:
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1: # To check if it is a left mouse click
                        if new_game_rect_on.collidepoint(pygame.mouse.get_pos()):
                            screen = pygame.display.set_mode(MENU_SCREEN_DIMENSIONS)
                            new_game_menu = True
                            menu = False
                        elif load_rect_on.collidepoint(pygame.mouse.get_pos()):
                            menu = False
                            load_screen = True
                            data_list = [load_game(slot) or {} for slot in range(3)]

            elif new_game_menu:  
                if event.type == pygame.MOUSEBUTTONUP:  
                    if event.button == 1: 
                        if easy_rect_on.collidepoint(pygame.mouse.get_pos()):
                            width, height, pocet_min, difficulty = 11, 11, 17, "Easy"
                        elif medium_rect_on.collidepoint(pygame.mouse.get_pos()):
                            width, height, pocet_min, difficulty = 15, 12, 35, "Medium"
                        elif hard_rect_on.collidepoint(pygame.mouse.get_pos()):
                            #width, height, pocet_min, difficulty = 28, 20, 100, "Hard"
                            width, height, pocet_min, difficulty = 50, 34, 270, "Hard"
                        elif back_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                            screen = pygame.display.set_mode(MENU_SCREEN_DIMENSIONS)
                            menu = True
                            new_game_menu = False
                            continue  # Skip the rest of this loop iteration if going back to menu

                        # Set up the game if a difficulty button was clicked
                        if easy_rect_on.collidepoint(pygame.mouse.get_pos()) or medium_rect_on.collidepoint(pygame.mouse.get_pos()) or hard_rect_on.collidepoint(pygame.mouse.get_pos()):
                            additional_dw = max(0, (260 - width*cell_size - dw*2)/2) # 260 je stejná jako o 3 řádky níže
                            additional_dh = max(0, (280 - height*cell_size - dw*2-90)/2)
                            reshuffle_count = 3
                            mines_rect = pygame.Rect(dw + additional_dw, dh + additional_dh, width*cell_size, height*cell_size)
                            screen_width_game = max(width*cell_size + dw * 2, 260) # Zde
                            screen_height_game = max(height*cell_size + 2*dh + 10, 280)
                            
                            screen = pygame.display.set_mode((screen_width_game, screen_height_game))
                            new_game_menu = False
                            game = True
                            first_click = True
                            all_scores = ScFn.update_or_add_game_data(width, height, pocet_min)
                            key = str((width, height, pocet_min))
                            game_scores = all_scores[key]
               
            elif game:
                if first_click is True:
                    remaining_flags = pocet_min
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1 and back_arrow_rect_small.collidepoint(pygame.mouse.get_pos()):
                            game = False
                            menu = True
                            first_click = True
                            screen = pygame.display.set_mode(MENU_SCREEN_DIMENSIONS)

                    elif event.type == pygame.MOUSEBUTTONDOWN:  
                        if event.button == 1 and mines_rect.collidepoint(pygame.mouse.get_pos()):
                            x_click, y_click = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] 
                            row, column = pole_funkce.click(x_click, y_click, dw, dh, additional_dw, additional_dh, cell_size)
                            first_click = False
                            game_time = 0
                            field, bool_field = pole_funkce.field_description(width, height, pocet_min, row, column)

                else:
                    flag_count = np.count_nonzero(bool_field == 2)
                    remaining_flags = pocet_min - flag_count
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1 and back_arrow_rect_small.collidepoint(pygame.mouse.get_pos()):
                            game = False
                            menu = True
                            first_click = True
                            screen = pygame.display.set_mode(MENU_SCREEN_DIMENSIONS)

                        elif event.button == 2 and mines_rect.collidepoint(pygame.mouse.get_pos()):
                            x_click, y_click = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                            up_row, up_column = pole_funkce.click(x_click, y_click, dw, dh, additional_dw, additional_dh, cell_size)
                            if bool_field[up_row][up_column] == 1 and pole_funkce.verify_amount_of_flags(field, bool_field, up_row, up_column) and up_row == down_row and up_column == down_column:
                                field, bool_field = pole_funkce.cluster_reveal(field, bool_field, up_row, up_column)
                                for i in empty_cells_to_plot:
                                    if field[i[1]][i[0]] == 9:
                                        for radek in range((len(bool_field))):
                                            for sloupec in range((len(bool_field[0]))):
                                                if field[radek][sloupec] == 9:
                                                    bool_field[radek][sloupec] = 1
                                        plot_bool_field(bool_field, field, cell_size)
                                        pygame.display.flip()
                                        time.sleep(1.5)
                                        screen.blit(transparent_bg_surf, (0, 0))
                                        end_screen = True
                                        game = False
                                        first_click = True
                            empty_cells_to_plot.clear()
                        
                        elif event.button == 1 and (screen_width_game - 46 < pygame.mouse.get_pos()[0] < screen_width_game - 10 and 10 < pygame.mouse.get_pos()[1] < 46):
                            screen = pygame.display.set_mode(MENU_SCREEN_DIMENSIONS)
                            save_screen = True
                            game = False

                    elif event.type == pygame.MOUSEBUTTONDOWN:  
                        if (event.button == 1 and 15 < pygame.mouse.get_pos()[0] < 55 and screen_height_game - 50 < pygame.mouse.get_pos()[1] < screen_height_game - 10) and (reshuffle_count > 0):
                            field, bool_field = pole_funkce.reshuffle(field, bool_field)
                            reshuffle_count -= 1

                        elif event.button == 1 and mines_rect.collidepoint(pygame.mouse.get_pos()):
                            x_click, y_click = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] 
                            row, column = pole_funkce.click(x_click, y_click, dw, dh, additional_dw, additional_dh, cell_size)
                            # pole_funkce.update_field(row, collumn)
                            if bool_field[row][column] == 2:
                                continue
                            if field[row][column] == 9:
                                for radek in range((len(bool_field))):
                                    for sloupec in range((len(bool_field[0]))):
                                        if field[radek][sloupec] == 9:
                                            bool_field[radek][sloupec] = 1
                                plot_bool_field(bool_field, field, cell_size)
                                screen.blit(mine_explode_surf_game, (column*cell_size+dw+additional_dw, row*cell_size+dh+additional_dh))
                                pygame.display.flip()
                                time.sleep(1.5)
                                screen.blit(transparent_bg_surf, (0, 0))
                                end_screen = True
                                game = False
                                first_click = True
                            
                            field, bool_field = pole_funkce.update_field(field, bool_field, row, column)

                        elif event.button == 2 and mines_rect.collidepoint(pygame.mouse.get_pos()):
                            x_click, y_click = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                            down_row, down_column = pole_funkce.click(x_click, y_click, dw, dh, additional_dw, additional_dh, cell_size)
                            empty_cells_to_plot = pole_funkce.neighbouring_cells_without_turning(down_row, down_column, bool_field)

                        elif event.button == 3 and mines_rect.collidepoint(pygame.mouse.get_pos()):
                            x_click, y_click = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] 
                            row, column = pole_funkce.click(x_click, y_click, dw, dh, additional_dw, additional_dh, cell_size)
                            if bool_field[row][column] == 0  and remaining_flags > 0:
                                bool_field[row][column] = 2
                            elif bool_field[row][column] == 2:
                                bool_field[row][column] = 0

            elif win_screen:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        win_screen = False
                        end_screen = False
                        if event.key == pygame.K_SPACE:
                            menu = True
                            screen = pygame.display.set_mode(MENU_SCREEN_DIMENSIONS)
                        else:      
                            submit_score_screen = True
                            screen = pygame.display.set_mode((10*30, 8*30))
            
            elif end_screen:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        menu = True
                        screen = pygame.display.set_mode(MENU_SCREEN_DIMENSIONS)
                        win_screen = False
                        end_screen = False

            elif load_screen:
                if event.type == pygame.MOUSEBUTTONUP:  
                    if event.button == 1: 
                        if back_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                            screen = pygame.display.set_mode(MENU_SCREEN_DIMENSIONS)
                            menu = True
                            load_screen = False
                        elif any(rect.collidepoint(pygame.mouse.get_pos()) for rect in save_slot_rects):
                            if save_slot_rects[0].collidepoint(pygame.mouse.get_pos()):
                                slot = 0
                            elif save_slot_rects[1].collidepoint(pygame.mouse.get_pos()):
                                slot = 1
                            elif save_slot_rects[2].collidepoint(pygame.mouse.get_pos()):
                                slot = 2
                            if load_game(slot) is None:
                                continue
                            data = load_game(slot)
                            field = np.array(data["field"])
                            bool_field = np.array(data["boolField"])
                            width = len(field[0])
                            height = len(field)
                            reshuffle_count = data["reshuffleCount"]
                            game_time = data["timePlayed"]
                            pocet_min = data["mineCount"]
                            difficulty = data["difficulty"]
                            remaining_flags = data["remainingFlags"]
                            first_click = False
                            load_screen = False
                            game = True
                            additional_dw = max(0, (200 - width*cell_size - dw - 10)/2)
                            mines_rect = pygame.Rect(dw + additional_dw, dh, width*cell_size, height*cell_size)
                            screen_width_game = max(width*cell_size + dw * 2, 200)
                            screen_height_game = height*cell_size + 2*dh + 10
                            screen = pygame.display.set_mode((screen_width_game, screen_height_game))
            elif save_screen:
                if event.type == pygame.MOUSEBUTTONUP:  
                    if event.button == 1: 
                        if back_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                            screen = pygame.display.set_mode((screen_width_game, screen_height_game))
                            game = True
                            save_screen = False
                        elif any(rect.collidepoint(pygame.mouse.get_pos()) for rect in save_slot_rects):
                            if save_slot_rects[0].collidepoint(pygame.mouse.get_pos()):
                                slot = 0
                            elif save_slot_rects[1].collidepoint(pygame.mouse.get_pos()):
                                slot = 1
                            elif save_slot_rects[2].collidepoint(pygame.mouse.get_pos()):
                                slot = 2   
                            data_list[slot] = {
                                "boolField":  bool_field.tolist(),
                                "field": field.tolist(),
                                "timePlayed": game_time,
                                "reshuffleCount": reshuffle_count,
                                "mineCount": pocet_min,
                                "difficulty": difficulty,
                                "remainingFlags": remaining_flags
                            }
                            save_game(slot, data_list[slot])        

            elif submit_score_screen:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the input box was clicked
                    if username_box.collidepoint(event.pos):
                        username_button_active = True
                    else:
                        username_button_active = False

                elif event.type == pygame.KEYDOWN and username_button_active:
                    if event.key == pygame.K_RETURN: # User pressed enter and validated his game username
                        if username_text.strip():
                            game_scores = ScFn.add_user_score(width, height, pocet_min, username_text.strip(), game_time)
                            print(f"Score submitted for {username_text.strip()}.")
                            submit_score_screen = False
                            menu = True
                            screen = pygame.display.set_mode(MENU_SCREEN_DIMENSIONS)
                            username_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        username_text = username_text[:-1]
                    else:
                        if len(username_text) < 17:
                            username_text += event.unicode                   

        # This part is for drawing pictures on the screen         
        if menu:  # this is drawn, while menu is active
            screen.fill((255, 255, 255))  # Creates a white screen (to erase the previos iteration)
            #pygame.draw.rect(screen, (255, 0, 0), (0, 0, 80, 80))  # Draw a red rectangle
            update_cell(menu_bg_surface, mine_field)
            screen.blit(menu_bg_surface, (0, 0))

            if new_game_rect_on.collidepoint(pygame.mouse.get_pos()):
                screen.blit(new_game_surf_on, new_game_rect_on)
            else:
                screen.blit(new_game_surf_off, new_game_rect_off)

            if load_rect_on.collidepoint(pygame.mouse.get_pos()):
                screen.blit(load_surf_on, load_rect_on)
            else:
                screen.blit(load_surf_off, load_rect_off)

            screen.blit(text_miny_surf,text_miny_rect)

        elif new_game_menu: # this is drawn, while new game menu is active
            screen.fill((200, 200, 200))
            update_cell(menu_bg_surface, mine_field)
            screen.blit(menu_bg_surface, (0, 0))
            pygame.draw.rect(screen, (50, 50, 50), (screen_width/2-160, 50, 320, 420))
            pygame.draw.rect(screen, (130, 130, 130), (screen_width/2-155, 55, 310, 410))
            screen.blit(text_difficulty_surf, text_difficulty_rect)

            if easy_rect_on.collidepoint(pygame.mouse.get_pos()):
                screen.blit(easy_surf_on, easy_rect_on)
            else:
                screen.blit(easy_surf_off, easy_rect_off)

            if medium_rect_on.collidepoint(pygame.mouse.get_pos()):
                screen.blit(medium_surf_on, medium_rect_on)
            else:
                screen.blit(medium_surf_off, medium_rect_off)

            if hard_rect_on.collidepoint(pygame.mouse.get_pos()):
                screen.blit(hard_surf_on, hard_rect_on)
            else:
                screen.blit(hard_surf_off, hard_rect_off)

            if back_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(back_arrow_surf_on, back_arrow_rect)
            else:
                screen.blit(back_arrow_surf_off, back_arrow_rect)

        elif game:
            if first_click is True:
                remaining_flags_surf = karma_sature_font_23.render(str(remaining_flags), False, "Black")
                reshuffle_count_surf = karma_sature_font_23.render(str(reshuffle_count), False, "Black")
                screen.fill((140, 140, 140))
                pygame.draw.rect(screen, (195, 195, 195), (5, 5, screen_width_game-10, screen_height_game-10))
                plot_empty_field(width, height, cell_size)

                if (15 < pygame.mouse.get_pos()[0] < 55 and screen_height_game - 50 < pygame.mouse.get_pos()[1] < screen_height_game - 10) or (reshuffle_count == 0):
                    screen.blit(reshuffle_on_surf, (15, screen_height_game-50))
                else:
                    screen.blit(reshuffle_off_surf, (15, screen_height_game-50))

                screen.blit(reshuffle_count_surf, (60, screen_height_game-40))

                screen.blit(flag_only_surf_big, (screen_width_game-37, screen_height_game-42))
                screen.blit(remaining_flags_surf, (screen_width_game - 42 - remaining_flags_surf.get_width(), screen_height_game - 40))

                if back_arrow_rect_small.collidepoint(pygame.mouse.get_pos()):
                    screen.blit(back_arrow_surf_on_small, back_arrow_rect_small)
                else:
                    screen.blit(back_arrow_surf_off_small, back_arrow_rect_small)

                if screen_width_game - 46 < pygame.mouse.get_pos()[0] < screen_width_game - 10 and 10 < pygame.mouse.get_pos()[1] < 46:
                    screen.blit(save_icon_on_surf, (screen_width_game - 46, 10))
                else:
                    screen.blit(save_icon_off_surf, (screen_width_game - 46, 10))

            else:
                reshuffle_count_surf = karma_sature_font_23.render(str(reshuffle_count), False, "Black")
                if it%fps == 0:
                    game_time += 1

                game_time_surf = karma_sature_font_23.render(str(game_time), False, "Black")
                remaining_flags_surf = karma_sature_font_23.render(str(remaining_flags), False, "Black")
                screen.fill((140, 140, 140))
                pygame.draw.rect(screen, (195, 195, 195), (5, 5, screen_width_game-10, screen_height_game-10))
                plot_bool_field(bool_field, field, cell_size)

                if (15 < pygame.mouse.get_pos()[0] < 55 and screen_height_game - 50 < pygame.mouse.get_pos()[1] < screen_height_game - 10) or (reshuffle_count == 0):
                    screen.blit(reshuffle_on_surf, (15, screen_height_game-50))
                else:
                    screen.blit(reshuffle_off_surf, (15, screen_height_game-50))
                screen.blit(reshuffle_count_surf, (60, screen_height_game-40))

                screen.blit(flag_only_surf_big, (screen_width_game-37, screen_height_game-42))
                screen.blit(remaining_flags_surf, (screen_width_game - 42 - remaining_flags_surf.get_width(), screen_height_game - 40))

                if back_arrow_rect_small.collidepoint(pygame.mouse.get_pos()):
                    screen.blit(back_arrow_surf_on_small, back_arrow_rect_small)
                else:
                    screen.blit(back_arrow_surf_off_small, back_arrow_rect_small)
                if screen_width_game - 46 < pygame.mouse.get_pos()[0] < screen_width_game - 10 and 10 < pygame.mouse.get_pos()[1] < 46:
                    screen.blit(save_icon_on_surf, (screen_width_game - 46, 10))
                else:
                    screen.blit(save_icon_off_surf, (screen_width_game - 46, 10))

                screen.blit(game_time_surf, (screen_width_game/2 - game_time_surf.get_width()/2, 10))

                if len(empty_cells_to_plot) > 0:
                    for i in empty_cells_to_plot:
                        screen.blit(null_surf_game, (i[0]*cell_size+dw+additional_dw, i[1]*cell_size+dh+additional_dh))

                if np.count_nonzero(bool_field == 1) >= width * height - pocet_min:
                    win_screen = True
                    game = False
                    first_click = True
                    plot_bool_field(bool_field, field, cell_size)
                    screen.blit(transparent_bg_surf, (0, 0))
                
        elif win_screen or end_screen:
            y_offset = 52
            add_y_offset = max(0, (screen_height_game - (2*dh+35)-additional_dh*2)/2)
            if win_screen:
                screen.blit(text_victory_surf, (screen_width_game/2-text_victory_surf.get_width()/2, 5 + add_y_offset))
                for text_surf in text_press_space_surfs:   
                    screen.blit(text_surf, (screen_width_game/2-text_surf.get_width()/2, y_offset + add_y_offset))
                    y_offset += text_surf.get_height()
            else:
                screen.blit(text_lose_surf, (screen_width_game/2-text_lose_surf.get_width()/2, 5 + add_y_offset))
                for text_surf in text_press_enter_surfs:   
                    screen.blit(text_surf, (screen_width_game/2-text_surf.get_width()/2, y_offset + add_y_offset))
                    y_offset += text_surf.get_height()

        elif load_screen or save_screen:
            screen.fill((200, 200, 200))
            update_cell(menu_bg_surface, mine_field)
            screen.blit(menu_bg_surface, (0, 0))
            pygame.draw.rect(screen, (50, 50, 50), (screen_width/2-190, 50, 380, 420))
            pygame.draw.rect(screen, (130, 130, 130), (screen_width/2-185, 55, 370, 410))
            if load_screen:
                screen.blit(text_load_system_surf, text_save_system_rect)
            else:
                screen.blit(text_save_system_surf, text_save_system_rect)

            if back_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(back_arrow_surf_on, back_arrow_rect)
            else:
                screen.blit(back_arrow_surf_off, back_arrow_rect)

            for slot in range(3):
                if load_game(slot) is None:
                    screen.blit(empty_save_surf, save_slot_rects[slot])
                else:
                    game_save_surfs[slot].blit(pygame.image.load("surfaces/filled_save.png").convert_alpha(), (0, 0))
                    game_save_surfs[slot].blit(karma_sature_font_30.render(data_list[slot]["difficulty"], False, "Black"), (10, 10))
                    game_save_surfs[slot].blit(flag_only_surf, (game_save_surfs[slot].get_width() - flag_only_surf.get_width() - 10, 15))
                    game_save_surfs[slot].blit(karma_sature_font_23.render(str(data_list[slot]["remainingFlags"]), False, "Black"), (game_save_surfs[slot].get_width() - karma_sature_font_23.render(str(data_list[slot]["remainingFlags"]),  False, "Black").get_width() - flag_only_surf.get_width() - 15, 11))
                    game_save_surfs[slot].blit(karma_sature_font_23.render(str(len(data_list[slot]["field"])) + "x" + str(len(data_list[slot]["field"][0])),  False, "Black"), (10, 45))
                    game_save_surfs[slot].blit(karma_sature_font_23.render(str(data_list[slot]["timePlayed"]) + " s", False, "Blue"), (game_save_surfs[slot].get_width() - karma_sature_font_23.render(str(data_list[slot]["timePlayed"]) + " s", False, "Blue").get_width() - 10, 45))
                    screen.blit(game_save_surfs[slot], save_slot_rects[slot]) 

        elif submit_score_screen:
            screen.fill((200, 200, 200))
            update_cell(menu_bg_surface, mine_field)
            screen.blit(menu_bg_surface, (0, 0))
            pygame.draw.rect(screen, (100, 100, 100), (30, 30, 8*30, 6*30))
            pygame.draw.rect(screen, (150, 150, 150), (35, 35, 8*30 - 10, 6*30 - 10))
            screen.blit(text_submit_username_surf, (screen.get_size()[0]/2 - text_submit_username_surf.get_size()[0]/2, 50))
            pygame.draw.rect(screen, GRAY if username_button_active else WHITE, username_box, 2)
            username_input_surface = karma_sature_font_21.render(username_text, True, BLACK)
            screen.blit(username_input_surface, (username_box.x + 5, username_box.y + 5))

        pygame.display.flip()
        clock.tick(fps) # Limits the game to 60 fps, better for slower CPU
        it += 1


if __name__ == "__main__":
    main()


