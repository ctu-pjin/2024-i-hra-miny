import pygame
from sys import exit
from random import choice, randint
import os
import pole_funkce
import score_funkce as ScFn
import json
import numpy as np
import time


# Initialize Pygame
os.environ['SDL_VIDEO_CENTERED'] = '1' # Centers the screen on the display
os.environ['SDL_RENDER_SCALE_QUALITY'] = '2' # '0' is the worst quality | '2' is the best quality | '1' is in the middle
                                        # May reduce later
pygame.init()


"""Preassigning variables"""
screen_width, screen_height = 480, 600
screen_width_game, screen_height_game = 100, 100
dw = 10
dh = 50
additional_dw = 0
additional_dh = 0
previous_time = time.time()
remaining_flags = 0
reshuffle_count = 3
hint_count = 2
field = []
bool_field = []
current_it = 0
cell_size_gl = 30
difficulty = str()
data_list = []

MENU_SCREEN_DIMENSIONS = (screen_width, screen_height)
fps = 60

screen = pygame.display.set_mode(MENU_SCREEN_DIMENSIONS)
menu_bg_surface = pygame.Surface((screen_width, screen_height))

# Part for loading fonts

karma_font_160 = pygame.font.Font("fonts/KarmaFuture.otf", 160)
karma_font_60 = pygame.font.Font("fonts/KarmaFuture.otf", 60)
karma_suture_font_23 = pygame.font.Font("fonts/KarmaSuture.otf", 23)
karma_suture_font_21 = pygame.font.Font("fonts/KarmaSuture.otf", 21)
karma_suture_font_16 = pygame.font.Font("fonts/KarmaSuture.otf", 16)
karma_suture_font_30 = pygame.font.Font("fonts/KarmaSuture.otf", 30)
karma_font_35 = pygame.font.Font("fonts/KarmaFuture.otf", 35)

# Part for loading texts

text_miny_surf = karma_font_160.render("Miny", False, "Black")
text_miny_rect = text_miny_surf.get_rect(midtop=(screen_width/2, 40))
text_difficulty_surf = karma_font_60.render("Difficulty", False, "Black")
text_difficulty_rect = text_difficulty_surf.get_rect(midtop=(screen_width/2, 70))
text_save_system_surf = karma_font_60.render("Save game", False, "Black")
text_save_system_rect = text_save_system_surf.get_rect(midtop=(screen_width/2, 70))
text_load_system_surf = karma_font_60.render("Load game", False, "Black")
victory_lines = ["Press Space to", "return to main menu", "OR", "Press Enter to", "submit your score"]
loss_lines = ["Press Space to", "return to main menu", "", "Good luck", "next time"]
text_press_space_surfs = [karma_suture_font_23.render(text, False, "White") for text in victory_lines]
text_press_enter_surfs = [karma_suture_font_23.render(text, False, "White") for text in loss_lines]
text_victory_surf = karma_font_35.render("You won!", False, "White")
text_lose_surf = karma_font_35.render("You lost!", False, "White")
text_submit_username_surf = karma_suture_font_21.render("Enter your Username:", False, "Black")
text_this_is_custom_game = karma_suture_font_23.render("Create your custom game field", False, "Black")
text_custom_field_entry_surf = karma_suture_font_21.render("enter width, height, number of mines,", False, "Black")
text_optional_scaling_factor = karma_suture_font_21.render("and optionally the scaling factor", False, "Black")
text_example_for_custom_field_surf = karma_suture_font_21.render("example: 15, 10, 30, 0.7",False, "Black")
lines_scaling_factor_explained = ["if you want to create a larger field, consider adding", "the scaling factor, which makes the cells smaller", "(or potentially larger should you chose so)", "to fit your needs or computer screen better", "if anything goes awry, don't forget", "you can return to menu by pressing the escape button"]
text_scaling_factor_explained = [karma_suture_font_16.render(text, False, "Black") for text in lines_scaling_factor_explained]
text_custom_field_start_game = karma_suture_font_21.render("Press Enter to start the game!", False, "Black")
text_easy_medium_hard = karma_suture_font_23.render("Enter: easy, medium or hard", False, "Black")
text_enter_parameters1 = karma_suture_font_21.render("Or enter the parameters", False, "Black")
text_enter_parameters2 = karma_suture_font_21.render("of your custom game", False, "Black")
text_leaderboards = karma_suture_font_30.render("Leaderboards", False, "Black")
text_example_for_leaderboards = karma_suture_font_21.render("example: 15, 10, 30",False, "Black")

# texts for help screen
text_welcome = karma_suture_font_23.render("Welcome!",False, "Black")
text_mine_sweeper = karma_suture_font_16.render("This is our rendition of the classic Minesweeper", False, "Black")
text_controls = karma_suture_font_16.render("CONTROLS:", False, "Black")
control_lines = ["Left-click: discover a (hopefully) mineless field", "Right-click: place a flag", "Wheel-click: discover the surroundings of a fully", "controlled field", "Esc: return to menu"]
text_control_lines = [karma_suture_font_16.render(text, False, "Black") for text in control_lines]
text_special_features = karma_suture_font_16.render("SPECIAL FEATURES:", False, "Black")
save_lines = ["Save system", "save all your progress by picking", "one of the three slots", "re-write an old save by clicking on it", "or delete it by clicking the garbage can"]
text_save = [karma_suture_font_16.render(text, False, "Black") for text in save_lines]
reshuffle_lines = ["Reshuffle", "changes the positions of undiscovered mines", "to give you another chance when you are lost"]
text_reshuffle = [karma_suture_font_16.render(text, False, "Black") for text in reshuffle_lines]
hint_lines = ["Hint", "reveals the position of one undiscovered mine", "by placing a blue irremovable flag on it"]
text_hint = [karma_suture_font_16.render(text, False, "Black") for text in hint_lines]
text_have_fun = karma_suture_font_23.render("Have fun!", False, "Black")

# Part for loading images

new_game_surf_off = pygame.image.load("surfaces/new_game_button_off.png").convert_alpha() #surfaces of the object
new_game_surf_on = pygame.image.load("surfaces/new_game_button_on.png").convert_alpha() 
load_surf_off = pygame.image.load("surfaces/load_button_off.png").convert_alpha()
load_surf_on = pygame.image.load("surfaces/load_button_on.png").convert_alpha()
scores_surf_off = pygame.image.load("surfaces/scores_button_off.png").convert_alpha()
scores_surf_on = pygame.image.load("surfaces/scores_button_on.png").convert_alpha()
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
custom_surf_on = pygame.image.load("surfaces/custom_button_on.png").convert_alpha()
custom_surf_off = pygame.image.load("surfaces/custom_button_off.png").convert_alpha()
box_surf = pygame.image.load("mines/box.png").convert()
null_surf = pygame.image.load("mines/empty.png").convert()
one_surf = pygame.image.load("mines/one.png").convert()
two_surf = pygame.image.load("mines/two.png").convert()
three_surf = pygame.image.load("mines/three.png").convert()
four_surf = pygame.image.load("mines/four.png").convert()
five_surf = pygame.image.load("mines/five.png").convert()
six_surf = pygame.image.load("mines/six.png").convert()
seven_surf = pygame.image.load("mines/seven.png").convert()
eight_surf = pygame.image.load("mines/eight.png").convert()
mine_surf = pygame.image.load("mines/mine.png").convert()
mine_purple_surf = pygame.image.load("mines/mine_purple.png").convert()
mine_explode_surf = pygame.image.load("mines/mine_explode.png").convert()
mine_explode_only_surf = pygame.image.load("mines/mine_explode_only.png").convert_alpha()
pygame.display.set_icon(mine_explode_only_surf)
flag_surf = pygame.image.load("mines/flag.png").convert()
blue_flag_surf = pygame.image.load("surfaces/flag_blue.png").convert()

reshuffle_on_surf = pygame.image.load("surfaces/reshuffle_on.png").convert()
reshuffle_off_surf = pygame.image.load("surfaces/reshuffle_off.png").convert()
flag_only_surf = pygame.image.load("surfaces/flag_only.png").convert_alpha()
flag_only_surf_big = pygame.transform.scale_by(flag_only_surf, 1.5)
save_icon_on_surf = pygame.image.load("surfaces/save_icon_on.png").convert_alpha()
save_icon_off_surf = pygame.image.load("surfaces/save_icon_off.png").convert_alpha()
transparent_bg_surf = pygame.image.load("surfaces/transparent_bg_80.png").convert_alpha()
empty_save_surf = pygame.image.load("surfaces/empty_save.png").convert_alpha()
filled_save_surf = pygame.image.load("surfaces/filled_save.png").convert_alpha()
game_save_surfs = [pygame.image.load("surfaces/filled_save.png").convert_alpha() for _ in range(3)]
hint_on_surf = pygame.image.load("surfaces/hint_on.png").convert()
hint_off_surf = pygame.image.load("surfaces/hint_off.png").convert()
scores_button_on_surf = pygame.image.load("surfaces/scores_button_on.png").convert()
scores_button_off_surf = pygame.image.load("surfaces/scores_button_off.png").convert()
question_mark_surf_off = pygame.image.load("surfaces/question_mark_off_spaced.png").convert_alpha()
question_mark_surf_on = pygame.image.load("surfaces/question_mark_on.png").convert_alpha()
bin_on_surf = pygame.image.load("surfaces/bin_opened.png").convert_alpha()
bin_off_surf = pygame.image.load("surfaces/bin_closed.png").convert_alpha()


scale_factor = 1
def scale_surface(surface, scale):
    width, height = surface.get_size()
    if scale == 1: # Does not need to be scaled (žádná komprese)
        return surface
    else:
        return pygame.transform.smoothscale(surface, (int(width * scale), int(height * scale)))

# Creating scaled surfaces for game items
def scale_game_field(scale_factor):
    global one_surf_game, box_surf_game, two_surf_game, three_surf_game, four_surf_game, five_surf_game, six_surf_game, seven_surf_game, eight_surf_game, null_surf_game, mine_surf_game, mine_explode_surf_game, flag_surf_game, cell_size_gl, blue_flag_surf_game
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
    blue_flag_surf_game = scale_surface(blue_flag_surf, scale_factor)
    cell_size_gl *= scale_factor

cell_size_gl *= scale_factor

question_mark_surf_off = scale_surface(question_mark_surf_off, 1.3)
question_mark_surf_on = scale_surface(question_mark_surf_on, 1.3)
bin_off_surf = scale_surface(bin_off_surf, 1.4)
bin_on_surf = scale_surface(bin_on_surf, 1.4)

# Create rectangles
new_game_rect_off = new_game_surf_off.get_rect(midbottom=(screen_width/2, 350)) #rectangle of the surface. Easier to specify an exact location
new_game_rect_on = new_game_surf_on.get_rect(midbottom=(screen_width/2, 350))
load_rect_off = load_surf_off.get_rect(midbottom=(screen_width/2, 450)) 
load_rect_on = load_surf_on.get_rect(midbottom=(screen_width/2, 450))
scores_rect_off = scores_surf_off.get_rect(midbottom=(screen_width/2, 550)) 
scores_rect_on = scores_surf_on.get_rect(midbottom=(screen_width/2, 550))
easy_rect_on = easy_surf_on.get_rect(midbottom=(screen_width/2, 250))
easy_rect_off = easy_surf_off.get_rect(midbottom=(screen_width/2, 250))
medium_rect_on = medium_surf_on.get_rect(midbottom=(screen_width/2, 350))
medium_rect_off = medium_surf_off.get_rect(midbottom=(screen_width/2, 350))
hard_rect_on = hard_surf_on.get_rect(midbottom=(screen_width/2, 450))
hard_rect_off = hard_surf_off.get_rect(midbottom=(screen_width/2, 450))
custom_rect_on = custom_surf_on.get_rect(midbottom=(screen_width/2, 550))
custom_rect_off = custom_surf_off.get_rect(midbottom=(screen_width/2, 550))
back_arrow_rect = back_arrow_surf_off.get_rect(topleft = (20, 20))
back_arrow_rect_small = back_arrow_surf_off_small.get_rect(topleft = (10, 15))
reshuffle_rect = reshuffle_on_surf.get_rect(bottomleft = (10, 20))
question_mark_rect = question_mark_surf_on.get_rect(topright = (screen_width - 15, 15))

# Creating save slot and bin rectangles
save_slot_width, save_slot_height = empty_save_surf.get_width(), empty_save_surf.get_height() 
save_slot_rects = []
bin_rects = []
save_y_offset = 160

for slot in range(3):
    save_slot_rect = pygame.Rect(screen_width/2 - save_slot_width/2 - 15, save_y_offset, save_slot_width, save_slot_height)
    save_slot_rects.append(save_slot_rect)
    bin_rects.append(pygame.Rect(save_slot_rects[slot].x + 10 + save_slot_rects[slot].width, save_slot_rects[slot].y + 35, bin_on_surf.get_width(), bin_on_surf.get_height()))
    save_y_offset += 95


"""Functions for mine_menu background generation"""
def random_mine_surf(scale = True): # Takes random mine_filed surface
    if scale is True:
        return choice([box_surf_game] * 30 + [null_surf_game, flag_surf_game] * 5 + [mine_surf_game] * 2 + [one_surf_game] * 4 + [two_surf_game] * 3 + [three_surf_game, four_surf_game, five_surf_game] * 2 + [six_surf_game, seven_surf_game, eight_surf_game])
    else:
        return choice([box_surf] * 30 + [null_surf, flag_surf] * 5 + [mine_surf] * 2 + [one_surf] * 4 + [two_surf] * 3 + [three_surf, four_surf, five_surf] * 2 + [six_surf, seven_surf, eight_surf])


def draw_to_menu_bg(buffer_surface, mine_field, cell_size=30): # Draws entire minefiled onto the screen as background
    for row in range(len(mine_field)):
        for col in range(len(mine_field[row])):
            buffer_surface.blit(mine_field[row][col], (col * cell_size, row * cell_size))


def random_mine_screen_generation(w, h, cell_size = 30): # Creates the mine_field values for background
    mine_field = []
    for _ in range(int(h/cell_size)):
        radek = []
        for _ in range(int(w/cell_size)):
            radek.append(random_mine_surf(scale = False))
        mine_field.append(radek)
    return mine_field


def update_cell(buffer_surface, mine_field, cell_size=30): # updates the minefiled background with 1 new random cell
    row = randint(0, len(mine_field) - 1)
    col = randint(0, len(mine_field[0]) - 1)
    mine_field[row][col] = random_mine_surf(scale = False)
    buffer_surface.blit(mine_field[row][col], (col * cell_size, row * cell_size))


"""Save and load functions"""
save_slots = ["save1.json", "save2.json", "save3.json"]

def load_game(slot): # Loads the game data from save_X.json file to a variable
    filename = "saves/" + save_slots[slot]
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                return data
            
        except (json.JSONDecodeError, ValueError) as e:
            return None  # Return None if file is invalid
    else:
        return None  # Return None if file does not exist


def save_game(slot, data): # Saves the game data to save_X.json file
    filename = "saves/" + save_slots[slot]
    try:
        with open(filename, 'w') as f: 
            json.dump(data, f)
    except Exception as e:
        ...
        #print(f"Error saving to {filename}: {e}")


def delete_game(slot): # Deletes the selected game save file
    if any(rect.collidepoint(pygame.mouse.get_pos()) for rect in bin_rects):
        if bin_rects[0].collidepoint(pygame.mouse.get_pos()):
            slot = 0
        elif bin_rects[1].collidepoint(pygame.mouse.get_pos()):
            slot = 1
        elif bin_rects[2].collidepoint(pygame.mouse.get_pos()):
            slot = 2
        if load_game(slot) is None:
            return False
        
        filename = "saves/" + save_slots[slot]
        try:
            os.remove(filename) # Removes the save file completely
        except:
            print("Deletion Failed")

# Function for creating basic rectangles with id, name and time written on it
def create_rect_surf(id, name, time, color = (180, 180, 180), width = 380, height = 28):
    surf = pygame.Surface((width, height))
    surf.fill((160, 160, 160))  # Fill the surface with the background color

    text_left = f"{id}. {name}" # Text alligned to the left and right sides of the surf
    text_right = f"{time}s"

    # Transforming text to the surface
    text_left_surface = karma_suture_font_21.render(text_left, True, BLACK)
    text_right_surface = karma_suture_font_21.render(text_right, True, BLACK)

    # Blit the text onto the surface¨
    pygame.draw.rect(surf, color, (2, 2, width-4, height-4))
    surf.blit(text_left_surface, (5, 2))
    surf.blit(text_right_surface, (surf.get_width()-text_right_surface.get_width()-5, 2))
    return surf

"""Plotting/Drawing functions"""
def plot_bool_field(bool_field, field, cell_size = 30): # minefield plotting based on the bool_field and field values
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
                case 3:
                    screen.blit(blue_flag_surf_game, (col*cell_size+dw+additional_dw, row*cell_size+dh+additional_dh))

def plot_empty_field(width, height, cell_size = 30): # plots empty field in game before the first click
    for row in range(height):
        for col in range(width):
            screen.blit(box_surf_game, (col*cell_size+dw+additional_dw, row*cell_size+dh+additional_dh))

"""Event functions"""
def leave_game(game, menu, first_click, screen, cell_size_gl, scale_factor): # Handles transition from game to menu
    game = False
    menu = True
    first_click = True
    screen = pygame.display.set_mode(MENU_SCREEN_DIMENSIONS)
    cell_size_gl = 30
    scale_factor = 1.0
    return game, menu, first_click, screen, cell_size_gl, scale_factor

def back_to_menu_from_scores(menu, scores_menu, scores_input_text, score_data_to_blit, score_data_to_blit_bool):
    menu = True                      # Handles transition from scores_menu to menu
    scores_menu = False
    scores_input_text = ""
    score_data_to_blit = dict()
    score_data_to_blit_bool = False
    return menu, scores_menu, scores_input_text, score_data_to_blit, score_data_to_blit_bool

def game_over(row, column, bool_field, field, cell_size_gl, screen, transparent_bg_surf, end_screen, game, first_click, scale_factor):
    for radek in range((len(bool_field))): 
        for sloupec in range((len(bool_field[0]))):
            if field[radek][sloupec] == 9: # marks all mines as revealed if game was lost
                bool_field[radek][sloupec] = 1
    plot_bool_field(bool_field, field, cell_size_gl)
    screen.blit(mine_explode_surf_game, (column*cell_size_gl+dw+additional_dw, row*cell_size_gl+dh+additional_dh)) # culprit of loss is red
    pygame.display.flip()
    time.sleep(1.5)
    screen.blit(transparent_bg_surf, (0, 0))
    end_screen = True
    game = False
    first_click = True
    cell_size_gl = 30
    scale_factor = 1.0
    return end_screen, game, first_click, cell_size_gl, scale_factor

"""Other surf drawing functions"""
def draw_surf_on_off(surf_on, surf_off, rect_on, rect_off): # draw an object differently when mouse hovers over it
    if rect_on.collidepoint(pygame.mouse.get_pos()):
        screen.blit(surf_on, rect_on)
    else:
        screen.blit(surf_off, rect_off)

def x_center(screen, surf): # center drawn object
    x = screen.get_size()[0]/2 - surf.get_size()[0]/2
    return x

def wrong_input_to_box_red(screen, box, box_active, wrong_input): # Border of an input box goes red to indicate wrong input
    if wrong_input:
        pygame.draw.rect(screen, (176, 96, 91), box, 3) 
    else:
        pygame.draw.rect(screen, GRAY if box_active else WHITE, box, 3)

clock = pygame.time.Clock() # Clock is used to tick with a specific fps, so the game runs stable
mine_field = random_mine_screen_generation(screen_width, screen_height)
draw_to_menu_bg(menu_bg_surface, mine_field)
data_list = [load_game(slot) or {} for slot in range(3)]

# Input Boxes
username_box = pygame.Rect(40, 90, 220, 40)
username_text = ""
username_button_active = False

custom_mine_field_box = pygame.Rect(120, 170, 240, 40)
custom_mine_field_text = ""
custom_mine_field_box_active = False

scores_input_box = pygame.Rect(50, 115, screen_width-100, 40)
scores_input_text = ""
scores_input_box_active = False

WHITE = (255, 255, 255) # Defying basic colors
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)


def main():
    global screen, screen_height_game, screen_width_game, additional_dw, additional_dh, previous_time, remaining_flags, data_list, current_it, scale_factor, cell_size_gl, scale_factor
    global username_text, username_button_active, custom_mine_field_text, custom_mine_field_box_active, scores_input_box, scores_input_box_active, scores_input_text
    # All these variables are set to False 
    wrong_custom_input, wrong_score_input, first_click, score_data_to_blit_bool = False, False, False, False
    new_game_menu, win_screen, game, load_screen, save_screen, scores_menu, end_screen, submit_score_screen, custom_mine_field_screen, help_screen = False,False,False,False,False,False,False,False,False,False
    # Preassigning other variables
    empty_cells_to_plot = []
    score_data_to_blit = dict()
    it = 0  # Used for counting game time
    cell_size_gl = 30 
    menu = True # Menu is the first screen that is being drawn
    mines_rect = pygame.Rect(0, 0, 0, 0)
    
    if os.path.exists('saves'): # save system needs this directory, and if there were no saves in it, github would delete it, so this checks if it exists
        pass
    else:
        os.mkdir('saves') # or creates it if needed 

    while True:  # Main while true loop, that runs on every fps, every tick is the screen redrawn
        for event in pygame.event.get():  # All events are written in this for loop
            if event.type == pygame.QUIT: # If the close button is pressed, the window closes
                pygame.quit()
                exit()
            # Only one screen is being drawn at the same time: menu, newgame menu, scores menu, game, win or lose screen...   
            if menu: # specifies the active screen and what can occur while its active
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1: # To check if it is a left mouse click
                        if new_game_rect_on.collidepoint(pygame.mouse.get_pos()): # specifies which of the defined buttons was clicked on
                            new_game_menu = True # what happens when the button gets clicked, this case changes actiive screens
                            menu = False
                        elif load_rect_on.collidepoint(pygame.mouse.get_pos()):
                            menu = False
                            load_screen = True
                            data_list = [load_game(slot) or {} for slot in range(3)]
                        elif scores_rect_on.collidepoint(pygame.mouse.get_pos()):
                            menu = False
                            scores_menu = True
                            scores_input_box_active = True
                        elif question_mark_rect.collidepoint(pygame.mouse.get_pos()):
                            help_screen = True
                            menu = False

            elif new_game_menu:  # EVENTS in Menu for choosing a game difficulty 
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  
                    if easy_rect_on.collidepoint(pygame.mouse.get_pos()): # set the game parameters if clickled on any difficulty button
                        width, height, pocet_min, difficulty = 12, 10, 18, "Easy"
                    elif medium_rect_on.collidepoint(pygame.mouse.get_pos()):
                        width, height, pocet_min, difficulty = 16, 13, 37, "Medium"
                    elif hard_rect_on.collidepoint(pygame.mouse.get_pos()):
                        width, height, pocet_min, difficulty = 29, 20, 100, "Hard"
                    elif custom_rect_on.collidepoint(pygame.mouse.get_pos()): # If clicked on custom difficulty 
                        custom_mine_field_box_active = True
                        custom_mine_field_screen = True
                        new_game_menu = False
                        wrong_custom_input = False
                    elif back_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                        menu = True
                        new_game_menu = False
                        continue  # Skip the rest of this loop iteration if going back to menu

                    # Set up the game if a difficulty button was clicked
                    if easy_rect_on.collidepoint(pygame.mouse.get_pos()) or medium_rect_on.collidepoint(pygame.mouse.get_pos()) or hard_rect_on.collidepoint(pygame.mouse.get_pos()):
                        # Creates all parameters of the game field
                        cell_size_gl = 30
                        scale_factor = 1.0
                        new_game_menu = False
                        scale_game_field(scale_factor)
                        additional_dw = max(0, (260 - width*cell_size_gl - dw*2)/2) # 260 je stejná jako o 3 řádky níže
                        additional_dh = max(0, (280 - height*cell_size_gl - dw*2-90)/2)
                        mines_rect = pygame.Rect(dw + additional_dw, dh + additional_dh, width*cell_size_gl, height*cell_size_gl)
                        screen_width_game = max(width*cell_size_gl + dw * 2, 260) # Zde
                        screen_height_game = max(height*cell_size_gl + 2*dh + 10, 280)
                        screen = pygame.display.set_mode((screen_width_game, screen_height_game))
                        reshuffle_count = 3
                        hint_count = 2
                        game = True
                        first_click = True
                        # Creates or add scores for the game parameters 
                        all_scores = ScFn.update_or_add_game_data(width, height, pocet_min)
                        key = str((width, height, pocet_min))
                        game_scores = all_scores[key]

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu = True
                        new_game_menu = False

            elif custom_mine_field_screen:   # EVENTS in Custom menu
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  
                    if back_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                        new_game_menu = True
                        custom_mine_field_screen = False
                        custom_mine_field_text = ""
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the input box was clicked
                    if custom_mine_field_box.collidepoint(event.pos):
                        custom_mine_field_box_active = True
                        wrong_custom_input = False
                    else:
                        custom_mine_field_box_active = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                            new_game_menu = True
                            custom_mine_field_screen = False
                            custom_mine_field_text = ""
                    elif custom_mine_field_box_active:
                        if event.key == pygame.K_RETURN: # User pressed enter and validated his game username
                            custom_entry = pole_funkce.separate_string_by_commas(custom_mine_field_text)
                            if len(custom_entry) == 3: # If user did not enter the scale parameter, it will assign it 1.0
                                custom_entry.append("1.0")
                            if len(custom_entry) == 4:
                                if pole_funkce.is_it_integer(custom_entry[0:3]) is False or pole_funkce.is_it_float([custom_entry[3]]) is False:
                                    pass # Checks if the input is correct
                                elif len(custom_entry) == 4 and pole_funkce.field_creation_conditions(custom_entry[0:3]): # Checks if the field can be created
                                    # Creates all parameters of the game field
                                    width, height, pocet_min, scale_factor = int(custom_entry[0]), int(custom_entry[1]), int(custom_entry[2]), float(custom_entry[3])
                                    difficulty = "Custom"
                                    custom_mine_field_screen = False
                                    custom_mine_field_text = ""
                                    scale_game_field(scale_factor)
                                    additional_dw = max(0, (260 - width*cell_size_gl - dw*2)/2) # 260 je stejná jako o 3 řádky níže
                                    additional_dh = max(0, (280 - height*cell_size_gl - dw*2-90)/2)
                                    mines_rect = pygame.Rect(dw + additional_dw, dh + additional_dh, width*cell_size_gl, height*cell_size_gl)
                                    screen_width_game = max(width*cell_size_gl + dw * 2, 260) # Zde
                                    screen_height_game = max(height*cell_size_gl + 2*dh + 10, 280) 
                                    screen = pygame.display.set_mode((screen_width_game, screen_height_game))
                                    reshuffle_count = 3
                                    hint_count = 2
                                    game = True
                                    first_click = True
                                    all_scores = ScFn.update_or_add_game_data(width, height, pocet_min)
                                    key = str((width, height, pocet_min))
                                    game_scores = all_scores[key]
                                
                            # If an error occurs, this happens
                            custom_mine_field_text = ""
                            custom_mine_field_box_active = False
                            wrong_custom_input = True

                        elif event.key == pygame.K_BACKSPACE:
                            custom_mine_field_text = custom_mine_field_text[:-1]
                        else: # Adds a character from user input and checks for maximum length
                            if len(custom_mine_field_text) < 20:
                                custom_mine_field_text += event.unicode 

            elif scores_menu:  # EVENTS in Scores menu 
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if back_arrow_rect.collidepoint(pygame.mouse.get_pos()): # Goes back to the menu
                        menu, scores_menu, scores_input_text, score_data_to_blit, score_data_to_blit_bool = back_to_menu_from_scores(menu, scores_menu, scores_input_text, score_data_to_blit, score_data_to_blit_bool)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the input box was clicked
                    if scores_input_box.collidepoint(event.pos):
                        scores_input_box_active = True
                        wrong_score_input = False
                    else:
                        scores_input_box_active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu, scores_menu, scores_input_text, score_data_to_blit, score_data_to_blit_bool = back_to_menu_from_scores(menu, scores_menu, scores_input_text, score_data_to_blit, score_data_to_blit_bool)
                    elif scores_input_box_active:
                        if event.key == pygame.K_RETURN: # User pressed enter and validated his game username

                            # Checking if the input is easy, medium or hard and changing it to its parameters
                            if ScFn.check_for_difficulty(scores_input_text):
                                if scores_input_text.strip().lower() == "easy":
                                    scores_input_text = "12, 10, 18"
                                else:
                                    scores_input_text = "16, 13, 37" if scores_input_text.strip().lower() == "medium" else "29, 20, 100"

                            # Checking if the input parameters of any field exists        
                            scores_entry = pole_funkce.separate_string_by_commas(scores_input_text)
                            if pole_funkce.is_it_integer(scores_entry) is False:
                                wrong_score_input = True
                            elif len(scores_entry) == 3:
                                try:
                                    key = ScFn.create_str_key(scores_entry)
                                    scores_input_text = ""
                                    game_scores = ScFn.get_data()[key]
                                    score_data_to_blit = ScFn.show_data(game_scores)
                                    print(score_data_to_blit)
                                    score_data_to_blit_bool = True
                                except:
                                    wrong_score_input = True
                                    
                            else:
                                wrong_score_input = True
                                score_data_to_blit = dict()
                                score_data_to_blit_bool = False
                            # If an error occurs, this happens
                            scores_input_text = ""
                            scores_input_box_active = False


                        elif event.key == pygame.K_BACKSPACE:
                            scores_input_text = scores_input_text[:-1]
                        else: # Adds a character from user input and checks for maximum length
                            if len(scores_input_text) < 20:
                                scores_input_text += event.unicode 
            
            elif help_screen:   # EVENTS in Help screen
                if event.type == pygame.MOUSEBUTTONUP:  
                    if event.button == 1: 
                        if back_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                            menu = True
                            help_screen = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                            menu = True
                            help_screen = False

            elif game:  # EVENTS in Game 
                # evets for leaving the game
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and back_arrow_rect_small.collidepoint(pygame.mouse.get_pos()):
                        game, menu, first_click, screen, cell_size_gl, scale_factor = leave_game(game, menu, first_click, screen, cell_size_gl, scale_factor)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game, menu, first_click, screen,cell_size_gl, scale_factor = leave_game(game, menu, first_click, screen, cell_size_gl, scale_factor)


                if first_click is True: # The user has not clicked yet
                    remaining_flags = pocet_min
                    if event.type == pygame.MOUSEBUTTONDOWN:  # This creates the field and ensures the save first click
                        if event.button == 1 and mines_rect.collidepoint(pygame.mouse.get_pos()):
                            x_click, y_click = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] 
                            row, column = pole_funkce.click(x_click, y_click, dw, dh, additional_dw, additional_dh, cell_size_gl)
                            first_click = False
                            game_time = 0
                            field, bool_field = pole_funkce.field_description(width, height, pocet_min, row, column)

                elif first_click is False: # The user already clicked, new events
                    flag_count = np.count_nonzero(bool_field == 2) + np.count_nonzero(bool_field == 3)
                    remaining_flags = pocet_min - flag_count
                    if event.type == pygame.MOUSEBUTTONUP: 
                        if event.button == 2 and mines_rect.collidepoint(pygame.mouse.get_pos()): # handle events if user wheel-clicked
                            x_click, y_click = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                            up_row, up_column = pole_funkce.click(x_click, y_click, dw, dh, additional_dw, additional_dh, cell_size_gl)
                            if bool_field[up_row][up_column] == 1 and pole_funkce.verify_amount_of_flags(field, bool_field, up_row, up_column) and up_row == down_row and up_column == down_column:
                                field, bool_field = pole_funkce.cluster_reveal(field, bool_field, up_row, up_column)
                                for i in empty_cells_to_plot:
                                    if field[i[1]][i[0]] == 9: #End the game if the mine was revealed
                                        end_screen, game, first_click, cell_size_gl, scale_factor = game_over(i[1], i[0], bool_field, field, cell_size_gl, screen, transparent_bg_surf, end_screen, game, first_click, scale_factor)
                                        break         
                            empty_cells_to_plot.clear()
                        
                        elif event.button == 1 and (screen_width_game - 46 < pygame.mouse.get_pos()[0] < screen_width_game - 10 and 10 < pygame.mouse.get_pos()[1] < 46):
                            screen = pygame.display.set_mode(MENU_SCREEN_DIMENSIONS)
                            save_screen = True
                            game = False

                    elif event.type == pygame.MOUSEBUTTONDOWN:  
                        if (event.button == 1 and 15 < pygame.mouse.get_pos()[0] < 55 and screen_height_game - 50 < pygame.mouse.get_pos()[1] < screen_height_game - 10) and (reshuffle_count > 0):
                            field, bool_field = pole_funkce.reshuffle(field, bool_field)
                            reshuffle_count -= 1

                        elif event.button == 1 and hint_on_rect.collidepoint(pygame.mouse.get_pos()) and hint_count > 0:
                            bool_field = pole_funkce.hint(field, bool_field)
                            hint_count -= 1

                        elif event.button == 1 and mines_rect.collidepoint(pygame.mouse.get_pos()):
                            x_click, y_click = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] 
                            row, column = pole_funkce.click(x_click, y_click, dw, dh, additional_dw, additional_dh, cell_size_gl)
                            # pole_funkce.update_field(row, collumn)
                            if bool_field[row][column] == 2 or bool_field[row][column] == 3:
                                continue
                            if field[row][column] == 9: #Ends the game if the mine was revealed
                                end_screen, game, first_click, cell_size_gl, scale_factor = game_over(row, column, bool_field, field, cell_size_gl, screen, transparent_bg_surf, end_screen, game, first_click, scale_factor)
                            field, bool_field = pole_funkce.update_field(field, bool_field, row, column)

                        elif event.button == 2 and mines_rect.collidepoint(pygame.mouse.get_pos()):
                            x_click, y_click = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                            down_row, down_column = pole_funkce.click(x_click, y_click, dw, dh, additional_dw, additional_dh, cell_size_gl)
                            empty_cells_to_plot = pole_funkce.neighbouring_cells_without_turning(down_row, down_column, bool_field)

                        elif event.button == 3 and mines_rect.collidepoint(pygame.mouse.get_pos()): # Events with placing and removing flags
                            x_click, y_click = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] 
                            row, column = pole_funkce.click(x_click, y_click, dw, dh, additional_dw, additional_dh, cell_size_gl)
                            if bool_field[row][column] == 0  and remaining_flags > 0:
                                bool_field[row][column] = 2
                            elif bool_field[row][column] == 2:
                                bool_field[row][column] = 0

            elif win_screen:   # EVENTS in Win screen
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        win_screen = False
                        end_screen = False
                        if event.key == pygame.K_SPACE:
                            menu = True
                            screen = pygame.display.set_mode(MENU_SCREEN_DIMENSIONS)
                        else:   
                            username_button_active = True   
                            submit_score_screen = True
                            screen = pygame.display.set_mode((10*30, 8*30))
            
            elif end_screen:   # EVENTS in Lose screen
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    menu = True
                    screen = pygame.display.set_mode(MENU_SCREEN_DIMENSIONS)
                    win_screen = False
                    end_screen = False

            elif load_screen:   # EVENTS in Load screen
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  
                    if back_arrow_rect.collidepoint(pygame.mouse.get_pos()):
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
                        data = load_game(slot) # Assigns the values from the json file to game field variables
                        field = np.array(data["field"])
                        bool_field = np.array(data["boolField"])
                        width = len(field[0])
                        height = len(field)
                        reshuffle_count = data["reshuffleCount"]
                        hint_count = data["hintCount"]
                        game_time = data["timePlayed"]
                        pocet_min = data["mineCount"]
                        difficulty = data["difficulty"]
                        remaining_flags = data["remainingFlags"]
                        scale_factor = data["scaleFactor"]
                        scale_game_field(scale_factor)
                        first_click = False
                        load_screen = False
                        game = True
                        additional_dw = max(0, (260 - width*cell_size_gl - dw - 10)/2)
                        additional_dh = max(0, (280 - height*cell_size_gl - dw*2-90)/2)
                        mines_rect = pygame.Rect(dw + additional_dw, dh, width*cell_size_gl, height*cell_size_gl)
                        screen_width_game = max(width*cell_size_gl + dw * 2, 260)
                        screen_height_game = max(height*cell_size_gl + 2*dh + 10, 280)
                        screen = pygame.display.set_mode((screen_width_game, screen_height_game))

                    elif any(rect.collidepoint(pygame.mouse.get_pos()) for rect in bin_rects): # Deletes the clicked save file
                        delete_game(bin_rects)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        load_screen = False
                        menu = True

            elif save_screen:   # EVENTS in Save screen
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  
                    if back_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                        game = True
                        save_screen = False
                        screen = pygame.display.set_mode((screen_width_game, screen_height_game))

                    elif any(rect.collidepoint(pygame.mouse.get_pos()) for rect in save_slot_rects):
                        # Creates or updates the json save file with game parameters
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
                            "hintCount": hint_count,
                            "mineCount": pocet_min,
                            "difficulty": difficulty,
                            "remainingFlags": remaining_flags,
                            "scaleFactor": scale_factor
                        }
                        save_game(slot, data_list[slot])  

                    elif any(rect.collidepoint(pygame.mouse.get_pos()) for rect in bin_rects):
                        delete_game(bin_rects)    

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    save_screen = False
                    game = True 
                    screen = pygame.display.set_mode((screen_width_game, screen_height_game))

            elif submit_score_screen:   # EVENTS in Submit score screen
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
                            
                            # Shows the leaderboard of finished game
                            scores_menu = True
                            key_string = str(f"{width}, {height}, {pocet_min}")
                            separated_key_string = pole_funkce.separate_string_by_commas(key_string)
                            key = ScFn.create_str_key(separated_key_string)
                            game_scores = ScFn.get_data()[key]
                            score_data_to_blit = ScFn.show_data(game_scores)
                            score_data_to_blit_bool = True                            
                            screen = pygame.display.set_mode(MENU_SCREEN_DIMENSIONS)
                            username_text = ""

                    elif event.key == pygame.K_BACKSPACE:
                        username_text = username_text[:-1]
                    else:
                        if len(username_text) < 19:
                            username_text += event.unicode    


        # This part is for drawing pictures on the screen         
        if menu:  # this is drawn, while menu is active
            screen.fill((255, 255, 255))  # Creates a white screen (to erase the previos iteration)
            #pygame.draw.rect(screen, (255, 0, 0), (0, 0, 80, 80))  # Draw a red rectangle
            update_cell(menu_bg_surface, mine_field) # shifting cells in the background of the menus
            screen.blit(menu_bg_surface, (0, 0))
            # draw buttons that change appearance with mouse over them
            draw_surf_on_off(new_game_surf_on, new_game_surf_off, new_game_rect_on, new_game_rect_off)
            draw_surf_on_off(load_surf_on, load_surf_off, load_rect_on, load_rect_off)
            draw_surf_on_off(scores_surf_on, scores_surf_off, scores_rect_on, scores_rect_off)
            draw_surf_on_off(question_mark_surf_on, question_mark_surf_off, question_mark_rect, question_mark_rect)
            # draw text
            screen.blit(text_miny_surf,text_miny_rect)

        elif new_game_menu: # this is drawn, while new game menu is active
            screen.fill((200, 200, 200))
            update_cell(menu_bg_surface, mine_field)
            screen.blit(menu_bg_surface, (0, 0))
            pygame.draw.rect(screen, (50, 50, 50), (screen_width/2-160, 50, 320, 520))
            pygame.draw.rect(screen, (130, 130, 130), (screen_width/2-155, 55, 310, 510))
            screen.blit(text_difficulty_surf, text_difficulty_rect)

            # draw buttons
            draw_surf_on_off(easy_surf_on, easy_surf_off, easy_rect_on, easy_rect_off)
            draw_surf_on_off(medium_surf_on, medium_surf_off, medium_rect_on, medium_rect_off)
            draw_surf_on_off(hard_surf_on, hard_surf_off, hard_rect_on, hard_rect_off)
            draw_surf_on_off(custom_surf_on, custom_surf_off, custom_rect_on, custom_rect_off)
            draw_surf_on_off(back_arrow_surf_on, back_arrow_surf_off, back_arrow_rect, back_arrow_rect)

        elif scores_menu:
            screen.fill((200, 200, 200))
            update_cell(menu_bg_surface, mine_field)
            screen.blit(menu_bg_surface, (0, 0))
            pygame.draw.rect(screen, (50, 50, 50), (30, 60, screen_width-60, screen_height-90))
            pygame.draw.rect(screen, (130, 130, 130), (35, 65, screen_width-70, screen_height-100))
            pygame.draw.rect(screen, (190, 190, 190), (42, 162, screen_width-84, screen_height-204))
            pygame.draw.rect(screen, (220, 220, 220), (45, 165, screen_width-90, screen_height-210))

            draw_surf_on_off(back_arrow_surf_on, back_arrow_surf_off, back_arrow_rect, back_arrow_rect)

            pygame.draw.rect(screen, GRAY if scores_input_box_active else WHITE, scores_input_box, 3)
            wrong_input_to_box_red(screen, scores_input_box, scores_input_box_active, wrong_score_input)

            scores_input_surface = karma_suture_font_21.render(scores_input_text, True, BLACK)
            screen.blit(scores_input_surface, (scores_input_box.x + 5, scores_input_box.y + 5))
            screen.blit(text_leaderboards, (screen_width/2 - text_leaderboards.get_width()/2, 72))
            

            if score_data_to_blit_bool: # If there are data to draw, this will happen
                y_offset = 0
                for user, _ in enumerate(score_data_to_blit):
                    position = user + 1
                    if position < 4:
                        if position == 1:
                            color_i = (239, 191, 4)
                        else:
                            color_i = (202, 202, 215) if position == 2 else (205, 127, 50)
                        surf_to_blit = create_rect_surf(str(position), score_data_to_blit[user]["username"], score_data_to_blit[user]["time"], color = color_i)
                    else:
                        surf_to_blit = create_rect_surf(str(position), score_data_to_blit[user]["username"], score_data_to_blit[user]["time"])
                    screen.blit(surf_to_blit, (50, 170 + y_offset))
                    y_offset += 31
                    if position == 12:
                        break
            else: # Otherwise only text surfaces will be drawn
                screen.blit(text_easy_medium_hard, (x_center(screen, text_easy_medium_hard), 168))
                screen.blit(text_enter_parameters1, (x_center(screen, text_enter_parameters1), 200))
                screen.blit(text_enter_parameters2, (x_center(screen, text_enter_parameters2), 232))
                screen.blit(text_example_for_leaderboards, (x_center(screen, text_example_for_leaderboards), 264))

        elif game:
            # This part is being drawn always (before and after first click)
            hint_on_rect = hint_on_surf.get_rect(midbottom = (screen_width_game/2, screen_height_game - 10))
            remaining_flags_surf = karma_suture_font_23.render(str(remaining_flags), False, "Black")
            reshuffle_count_surf = karma_suture_font_23.render(str(reshuffle_count), False, "Black")
            hint_count_surf = karma_suture_font_23.render(str(hint_count), False, "Black")
            screen.fill((140, 140, 140))
            pygame.draw.rect(screen, (195, 195, 195), (5, 5, screen_width_game-10, screen_height_game-10))
            if (15 < pygame.mouse.get_pos()[0] < 55 and screen_height_game - 50 < pygame.mouse.get_pos()[1] < screen_height_game - 10) or (reshuffle_count == 0):
                screen.blit(reshuffle_on_surf, (15, screen_height_game-50))
            else:
                screen.blit(reshuffle_off_surf, (15, screen_height_game-50))

            screen.blit(reshuffle_count_surf, (60, screen_height_game-40))
            screen.blit(hint_count_surf, (screen_width_game/2+25, screen_height_game-40))

            draw_surf_on_off(hint_on_surf, hint_off_surf, hint_on_rect, hint_on_rect)

            screen.blit(flag_only_surf_big, (screen_width_game-37, screen_height_game-42))
            screen.blit(remaining_flags_surf, (screen_width_game - 42 - remaining_flags_surf.get_width(), screen_height_game - 40))

            draw_surf_on_off(back_arrow_surf_on_small, back_arrow_surf_off_small, back_arrow_rect_small, back_arrow_rect_small)

            if screen_width_game - 46 < pygame.mouse.get_pos()[0] < screen_width_game - 10 and 10 < pygame.mouse.get_pos()[1] < 46:
                screen.blit(save_icon_on_surf, (screen_width_game - 46, 10))
            else:
                screen.blit(save_icon_off_surf, (screen_width_game - 46, 10))

            # This is drawn before the first click
            if first_click is True: 
                plot_empty_field(width, height, cell_size_gl)
            else: # This is being drawn after the first click
                game_time_surf = karma_suture_font_23.render(str(game_time), False, "Black")
                screen.blit(game_time_surf, (x_center(screen, game_time_surf), 10))
                plot_bool_field(bool_field, field, cell_size_gl)
                screen.blit(game_time_surf, (x_center(screen, game_time_surf), 10))

                if len(empty_cells_to_plot) > 0: # This draws 3x3 grid when the user wheel-clicks on the field
                    for i in empty_cells_to_plot:
                        screen.blit(null_surf_game, (i[0]*cell_size_gl+dw+additional_dw, i[1]*cell_size_gl+dh+additional_dh))

                if np.count_nonzero(bool_field == 1) >= width * height - pocet_min:
                    cell_size_gl = 30
                    win_screen = True
                    game = False
                    first_click = True
                    plot_bool_field(bool_field, field, cell_size_gl)
                    screen.blit(transparent_bg_surf, (0, 0))

                if it%fps == 0:  # Calculates the game time
                    game_time += 1
                
        elif win_screen or end_screen: # Draws the win or end screen 
            y_offset = 52
            add_y_offset = max(0, (screen_height_game - (2*dh+35)-additional_dh*2)/2)
            if win_screen:
                screen.blit(text_victory_surf, (x_center(screen, text_victory_surf), 5 + add_y_offset))
                for text_surf in text_press_space_surfs:   
                    screen.blit(text_surf, (x_center(screen, text_surf), y_offset + add_y_offset))
                    y_offset += text_surf.get_height()
            else:
                screen.blit(text_lose_surf, (x_center(screen, text_lose_surf), 5 + add_y_offset))
                for text_surf in text_press_enter_surfs:   
                    screen.blit(text_surf, (x_center(screen, text_surf), y_offset + add_y_offset))
                    y_offset += text_surf.get_height()

        elif load_screen or save_screen: # Draws the load and save screen
            update_cell(menu_bg_surface, mine_field)
            screen.blit(menu_bg_surface, (0, 0))
            pygame.draw.rect(screen, (50, 50, 50), (screen_width/2-190, 50, 380, 420))
            pygame.draw.rect(screen, (130, 130, 130), (screen_width/2-185, 55, 370, 410))
            if load_screen:
                screen.blit(text_load_system_surf, text_save_system_rect)
            else:
                screen.blit(text_save_system_surf, text_save_system_rect)

            draw_surf_on_off(back_arrow_surf_on, back_arrow_surf_off, back_arrow_rect, back_arrow_rect)

            for slot in range(3): # This draws the individual save/load files.
                if load_game(slot) is None:    # On each game_save_surf are being drawn the game parameters (ukazatele)
                    screen.blit(empty_save_surf, save_slot_rects[slot])   # And those game_save_surfs are then being drawn on the screen
                else:
                    game_save_surfs[slot].blit(pygame.image.load("surfaces/filled_save.png").convert_alpha(), (0, 0))
                    game_save_surfs[slot].blit(karma_suture_font_30.render(data_list[slot]["difficulty"], False, "Black"), (10, 10))
                    game_save_surfs[slot].blit(flag_only_surf, (game_save_surfs[slot].get_width() - flag_only_surf.get_width() - 10, 15))
                    game_save_surfs[slot].blit(karma_suture_font_23.render(str(data_list[slot]["remainingFlags"]), False, "Black"), (game_save_surfs[slot].get_width() - karma_suture_font_23.render(str(data_list[slot]["remainingFlags"]),  False, "Black").get_width() - flag_only_surf.get_width() - 15, 11))
                    game_save_surfs[slot].blit(karma_suture_font_23.render(str(len(data_list[slot]["field"])) + "x" + str(len(data_list[slot]["field"][0])),  False, "Black"), (10, 45))
                    game_save_surfs[slot].blit(karma_suture_font_23.render(str(data_list[slot]["timePlayed"]) + " s", False, "Blue"), (game_save_surfs[slot].get_width() - karma_suture_font_23.render(str(data_list[slot]["timePlayed"]) + " s", False, "Blue").get_width() - 10, 45))
                    
                    if bin_rects[slot].collidepoint(pygame.mouse.get_pos()):
                        screen.blit(bin_on_surf, bin_rects[slot])
                    else:
                        screen.blit(bin_off_surf, bin_rects[slot])
                    screen.blit(game_save_surfs[slot], save_slot_rects[slot]) 

        elif submit_score_screen: # Draws the submit score screen
            screen.fill((200, 200, 200))
            update_cell(menu_bg_surface, mine_field)
            screen.blit(menu_bg_surface, (0, 0))
            pygame.draw.rect(screen, (100, 100, 100), (30, 30, 8*30, 6*30))
            pygame.draw.rect(screen, (150, 150, 150), (35, 35, 8*30 - 10, 6*30 - 10))
            screen.blit(text_submit_username_surf, (x_center(screen, text_submit_username_surf), 50))
            pygame.draw.rect(screen, GRAY if username_button_active else WHITE, username_box, 2)
            username_input_surface = karma_suture_font_21.render(username_text, True, BLACK)
            screen.blit(username_input_surface, (username_box.x + 5, username_box.y + 5))

        elif custom_mine_field_screen: # Draws the Custom difficulty screen
            screen.fill((200, 200, 200))
            update_cell(menu_bg_surface, mine_field)
            screen.blit(menu_bg_surface, (0, 0))
            pygame.draw.rect(screen, (100, 100, 100), (30, 60, 14*30, 15*30))
            pygame.draw.rect(screen, (150, 150, 150), (35, 65, 14*30 - 10, 15*30 - 10))
            screen.blit(text_this_is_custom_game, (x_center(screen, text_this_is_custom_game), 80))
            screen.blit(text_custom_field_entry_surf, (x_center(screen, text_custom_field_entry_surf), 109))
            screen.blit(text_optional_scaling_factor, (x_center(screen, text_optional_scaling_factor), 135))
            
            wrong_input_to_box_red(screen, custom_mine_field_box, custom_mine_field_box_active, wrong_custom_input)

            custom_field_input_surface = karma_suture_font_21.render(custom_mine_field_text, True, BLACK)
            screen.blit(custom_field_input_surface, (custom_mine_field_box.x + 5, custom_mine_field_box.y + 5))
            screen.blit(text_example_for_custom_field_surf, (x_center(screen, text_example_for_custom_field_surf), 218))
            y_offset = 243
            for text in text_scaling_factor_explained:
                screen.blit(text, (x_center(screen, text), y_offset))
                y_offset += 20
            screen.blit(text_custom_field_start_game, (x_center(screen, text_custom_field_start_game), y_offset+5))

            draw_surf_on_off(back_arrow_surf_on, back_arrow_surf_off, back_arrow_rect, back_arrow_rect)

        elif help_screen: # Draws the help screen (just a bunch of text)
            screen.fill((200, 200, 200))
            update_cell(menu_bg_surface, mine_field)
            screen.blit(menu_bg_surface, (0, 0))
            pygame.draw.rect(screen, (130, 130, 130), (30, 60, screen_width-60, screen_height-90))
            pygame.draw.rect(screen, (200, 200, 200), (35, 65, screen_width-70, screen_height-100))
            screen.blit(text_welcome, (x_center(screen, text_welcome), 75))
            screen.blit(text_mine_sweeper, (x_center(screen, text_mine_sweeper),100))
            screen.blit(text_controls, (40, 130))
            y_offset = 150
            for text in text_control_lines:
                screen.blit(text, (45, y_offset))
                y_offset += 20
            screen.blit(text_special_features, (40, y_offset + 10))
            screen.blit(save_icon_off_surf, (45, y_offset + 30))
            y_offset += 30
            for text in text_save:
                screen.blit(text, (90, y_offset))
                y_offset += 20
            y_offset += 10
            screen.blit(reshuffle_off_surf, (45, y_offset))
            for text in text_reshuffle:
                screen.blit(text, (90, y_offset))
                y_offset += 20
            y_offset += 10
            screen.blit(hint_off_surf, (45, y_offset))
            for text in text_hint:
                screen.blit(text, (90, y_offset))
                y_offset += 20
            screen.blit(text_have_fun, (x_center(screen, text_have_fun), y_offset + 10))
            draw_surf_on_off(back_arrow_surf_on, back_arrow_surf_off, back_arrow_rect, back_arrow_rect)

        # This happens every iteration
        pygame.display.flip() 
        clock.tick(fps) # Limits the game to 60 fps
        it += 1


if __name__ == "__main__":
    main()


