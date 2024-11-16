import pygame
from sys import exit
from random import choice, randint
import os
import pole_funkce
import json
import numpy as np

# Initialize Pygame
os.environ['SDL_VIDEO_CENTERED'] = '1' # Centers the screen on the display
os.environ['SDL_RENDER_SCALE_QUALITY'] = '2' # '0' is the worst quality | '2' is the best quality | '1' is in the middle
                                        # May reduce later
pygame.init()

screen_width, screen_height = 480, 540
screen_width_game, screen_height_game = 100, 100
dw = 10
dh = 50
additional_dw = 0

MENU_SCREEN_DIMENSIONS = (480, 540)
GAME_SCREEN_DIMENSIONS = (1024, 768)


screen = pygame.display.set_mode(MENU_SCREEN_DIMENSIONS)
buffer_surface = pygame.Surface((screen_width, screen_height))


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
flag_surf = pygame.image.load("mines/flag.png").convert()
seven_surf = pygame.image.load("mines/seven.png").convert()
eight_surf = pygame.image.load("mines/eight.png").convert()
reshuffle_on_surf = pygame.image.load("surfaces/reshuffle_on.png").convert_alpha()
reshuffle_off_surf = pygame.image.load("surfaces/reshuffle_off.png").convert_alpha()
flag_only_surf = pygame.image.load("surfaces/flag_only.png").convert_alpha()
save_icon_on_surf = pygame.image.load("surfaces/save_icon_on.png").convert_alpha()
save_icon_off_surf = pygame.image.load("surfaces/save_icon_off.png").convert_alpha()
transparent_bg_surf = pygame.image.load("surfaces/transparent_bg_80.png").convert_alpha()


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


"""Functions for mine_menu background generation"""
def random_mine_surf():
    return choice([box_surf] * 30 + [null_surf, flag_surf] * 5 + [mine_surf] * 2 + [one_surf] * 4 + [two_surf] * 3 + [three_surf, four_surf, five_surf] * 2 + [six_surf, seven_surf, eight_surf])


def random_mine_screen_plot(w, h, mine_field):
    random_h, random_w = randint(0, int(h/30)-1), randint(0, int(w/30)-1)
    mine_field[random_h][random_w] = random_mine_surf()
    for hh in range(0, h, 30):
            for ww in range(0, w, 30):
                screen.blit(mine_field[int(hh/30)][int(ww/30)], (ww, hh))
                

def draw_to_buffer(buffer_surface, mine_field, cell_size=30):
    """Draw the entire minefield onto the buffer surface."""
    for row in range(len(mine_field)):
        for col in range(len(mine_field[row])):
            buffer_surface.blit(mine_field[row][col], (col * cell_size, row * cell_size))


def random_mine_screen_generation(w, h, cell_size = 30):
    mine_field = []
    for _ in range(int(h/cell_size)):
        radek = []
        for _ in range(int(w/cell_size)):
            radek.append(random_mine_surf())
        mine_field.append(radek)
    return mine_field


def update_cell(buffer_surface, mine_field, cell_size=30):
    """Randomly update a specific cell in the minefield and redraw it on the buffer."""
    row = randint(0, len(mine_field) - 1)
    col = randint(0, len(mine_field[0]) - 1)
    mine_field[row][col] = random_mine_surf()
    buffer_surface.blit(mine_field[row][col], (col * cell_size, row * cell_size))


def load_save():
    with open("saves.txt") as miny_file:
        while True:
            line = miny_file.readline()
            if line.strip() == "***":
                break
            print(line)
            

# Part for loading fonts
karma_font_160 = pygame.font.Font("fonts/KarmaFuture.otf", 160)
karma_font_60 = pygame.font.Font("fonts/KarmaFuture.otf", 60)
karma_font_26 = pygame.font.Font("fonts/KarmaSuture.otf", 23)
karma_font_35 = pygame.font.Font("fonts/KarmaFuture.otf", 35)

# Part for loading texts
text_miny_surf = karma_font_160.render("Miny", False, "Black")
text_miny_rect = text_miny_surf.get_rect(midtop=(screen_width/2, 40))
text_difficulty_surf = karma_font_60.render("Difficulty", False, "Black")
text_difficulty_rect = text_difficulty_surf.get_rect(midtop=(screen_width/2, 70))
victory_lines = ["Press space", "to return", "to main menu"]
text_victory_surfs = [karma_font_26.render(text, False, "White") for text in victory_lines]
text_victory_surf = karma_font_35.render("You won!", False, "White")
text_miny_rect = text_miny_surf.get_rect(midtop=(screen_width/2, 40))



clock = pygame.time.Clock()
mine_field = random_mine_screen_generation(screen_width, screen_height)
draw_to_buffer(buffer_surface, mine_field)


def plot_bool_field(bool_field, field, cell_size = 30): # minefield plotting
    for row in range(len(field)):
        for col in range(len(field[row])):
            match bool_field[row,col]:
                case 0:
                    screen.blit(box_surf, (col*cell_size+dw+additional_dw, row*cell_size+dh))
                case 1:
                    match field[row,col]:
                        case 0:
                            screen.blit(null_surf, (col*cell_size+dw+additional_dw, row*cell_size+dh))
                        case 1: 
                            screen.blit(one_surf, (col*cell_size+dw+additional_dw, row*cell_size+dh))
                        case 2: 
                            screen.blit(two_surf, (col*cell_size+dw+additional_dw, row*cell_size+dh))
                        case 3: 
                            screen.blit(three_surf, (col*cell_size+dw+additional_dw, row*cell_size+dh))
                        case 4: 
                            screen.blit(four_surf, (col*cell_size+dw+additional_dw, row*cell_size+dh))
                        case 5: 
                            screen.blit(five_surf, (col*cell_size+dw+additional_dw, row*cell_size+dh))
                        case 6: 
                            screen.blit(six_surf, (col*cell_size+dw+additional_dw, row*cell_size+dh))
                        case 7: 
                            screen.blit(seven_surf, (col*cell_size+dw+additional_dw, row*cell_size+dh))
                        case 8: 
                            screen.blit(eight_surf, (col*cell_size+dw+additional_dw, row*cell_size+dh))
                        case 9: 
                            screen.blit(mine_surf, (col*cell_size+dw+additional_dw, row*cell_size+dh))
                case 2:
                    screen.blit(flag_surf, (col*cell_size+dw+additional_dw, row*cell_size+dh))

def plot_empty_field(width, height, cell_size = 30):
    for row in range(height):
        for col in range(width):
            screen.blit(box_surf, (col*cell_size+dw+additional_dw, row*cell_size+dh))


def main():
    it = 0
    menu = True
    first_click = False
    new_game_menu = False
    end_game_screen = False
    game = False
    global screen, screen_height_game, screen_width_game, additional_dw
    load_save()
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
            
            elif new_game_menu:  
                if event.type == pygame.MOUSEBUTTONUP:  
                    if event.button == 1: 
                        if easy_rect_on.collidepoint(pygame.mouse.get_pos()):
                            width, height, pocet_min = 8, 8, 10
                        elif medium_rect_on.collidepoint(pygame.mouse.get_pos()):
                            width, height, pocet_min = 15, 12, 40
                        elif hard_rect_on.collidepoint(pygame.mouse.get_pos()):
                            width, height, pocet_min = 41, 20, 200
                        elif back_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                            screen = pygame.display.set_mode(MENU_SCREEN_DIMENSIONS)
                            menu = True
                            new_game_menu = False
                            continue  # Skip the rest of this loop iteration if going back to menu

                        # Set up the game if a difficulty button was clicked
                        if easy_rect_on.collidepoint(pygame.mouse.get_pos()) or medium_rect_on.collidepoint(pygame.mouse.get_pos()) or hard_rect_on.collidepoint(pygame.mouse.get_pos()):
                            if width*30 + dw + 10 < 200:
                                additional_dw = (200 - width*30 - dw - 10)/2 
                            mines_rect = pygame.Rect(dw + additional_dw, dh, width*30, height*30)
                            screen_width_game = max(width*30 + dw + 10, 200)
                            screen_height_game = height*30 + 2*dh + 10
                            
                            screen = pygame.display.set_mode((screen_width_game, screen_height_game))
                            new_game_menu = False
                            game = True
                            first_click = True

                    
                            
            elif game:
                if first_click is True:
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1 and back_arrow_rect_small.collidepoint(pygame.mouse.get_pos()):
                            game = False
                            new_game_menu = True
                            first_click = True
                            screen = pygame.display.set_mode(MENU_SCREEN_DIMENSIONS)
                    elif event.type == pygame.MOUSEBUTTONDOWN:  
                        if event.button == 1 and mines_rect.collidepoint(pygame.mouse.get_pos()):
                            x_click, y_click = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] 
                            row, column = pole_funkce.click(x_click, y_click, dw, dh, additional_dw)
                            first_click = False
                            field, bool_field = pole_funkce.field_description(width, height, pocet_min, row, column)
                else:
                    flag_count = np.count_nonzero(bool_field == 2)
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1 and back_arrow_rect_small.collidepoint(pygame.mouse.get_pos()):
                            game = False
                            new_game_menu = True
                            first_click = True
                            screen = pygame.display.set_mode(MENU_SCREEN_DIMENSIONS)
                    elif event.type == pygame.MOUSEBUTTONDOWN:  
                        if event.button == 1 and 15 < pygame.mouse.get_pos()[0] < 55 and screen_height_game - 50 < pygame.mouse.get_pos()[1] < screen_height_game - 10:
                            field, bool_field = pole_funkce.reshuffle(field, bool_field)
                        elif event.button == 1 and mines_rect.collidepoint(pygame.mouse.get_pos()):
                            x_click, y_click = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] 
                            row, column = pole_funkce.click(x_click, y_click, dw, dh, additional_dw)
                            # pole_funkce.update_field(row, collumn)
                            if bool_field[row][column] == 2:
                                continue
                            if field[row][column] == 9:
                                ...
                                #exit()
                            field, bool_field = pole_funkce.update_field(field, bool_field, row, column)
                        elif event.button == 2 and mines_rect.collidepoint(pygame.mouse.get_pos()):
                            x_click, y_click = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                            row, column = pole_funkce.click(x_click, y_click, dw, dh, additional_dw)
                            if bool_field[row][column] == 1 and pole_funkce.verify_amount_of_flags(field, bool_field, row, column):
                                field, bool_field = pole_funkce.cluster_reveal(field, bool_field, row, column)
                        elif event.button == 3 and mines_rect.collidepoint(pygame.mouse.get_pos()):
                            x_click, y_click = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] 
                            row, column = pole_funkce.click(x_click, y_click, dw, dh, additional_dw)
                            if bool_field[row][column] == 0  and (pocet_min - flag_count) > 0:
                                bool_field[row][column] = 2
                            elif bool_field[row][column] == 2:
                                bool_field[row][column] = 0
            elif end_game_screen:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        end_game_screen = False
                        menu = True
                        screen = pygame.display.set_mode(MENU_SCREEN_DIMENSIONS)

        # This part is for drawing pictures on the screen         
        if menu:  # this is drawn, while menu is active
            screen.fill((255, 255, 255))  # Creates a white screen (to erase the previos iteration)
            #pygame.draw.rect(screen, (255, 0, 0), (0, 0, 80, 80))  # Draw a red rectangle
            update_cell(buffer_surface, mine_field)
            screen.blit(buffer_surface, (0, 0))
            if new_game_rect_on.collidepoint(pygame.mouse.get_pos()):
                screen.blit(new_game_surf_on, new_game_rect_on)
            else:
                screen.blit(new_game_surf_off, new_game_rect_off)
            if load_rect_on.collidepoint(pygame.mouse.get_pos()):
                screen.blit(load_surf_on, load_rect_on)
            else:
                screen.blit(load_surf_off, load_rect_off)

            screen.blit(text_miny_surf,text_miny_rect)

        if new_game_menu: # this is drawn, while new game menu is active
            screen.fill((200, 200, 200))
            update_cell(buffer_surface, mine_field)
            screen.blit(buffer_surface, (0, 0))
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
        if game:
            if first_click is True:
                screen.fill((140, 140, 140))
                pygame.draw.rect(screen, (195, 195, 195), (5, 5, max(width*30 + dw, 190), height*30+dh*2))
                plot_empty_field(width, height)

                if 15 < pygame.mouse.get_pos()[0] < 55 and screen_height_game - 50 < pygame.mouse.get_pos()[1] < screen_height_game - 10:
                    screen.blit(reshuffle_on_surf, (15, screen_height_game-50))
                else:
                    screen.blit(reshuffle_off_surf, (15, screen_height_game-50))

                screen.blit(flag_only_surf, (screen_width_game-30, screen_height_game-30))

                if back_arrow_rect_small.collidepoint(pygame.mouse.get_pos()):
                    screen.blit(back_arrow_surf_on_small, back_arrow_rect_small)
                else:
                    screen.blit(back_arrow_surf_off_small, back_arrow_rect_small)

                if screen_width_game - 46 < pygame.mouse.get_pos()[0] < screen_width_game - 10 and 10 < pygame.mouse.get_pos()[1] < 46:
                    screen.blit(save_icon_on_surf, (screen_width_game - 46, 10))
                else:
                    screen.blit(save_icon_off_surf, (screen_width_game - 46, 10))
            else:
                screen.fill((140, 140, 140))
                pygame.draw.rect(screen, (195, 195, 195), (5, 5, max(width*30 + dw, 190), height*30+dh*2))
                plot_bool_field(bool_field, field)
                if 15 < pygame.mouse.get_pos()[0] < 55 and screen_height_game - 50 < pygame.mouse.get_pos()[1] < screen_height_game - 10:
                    screen.blit(reshuffle_on_surf, (15, screen_height_game-50))
                else:
                    screen.blit(reshuffle_off_surf, (15, screen_height_game-50))
                screen.blit(flag_only_surf, (screen_width_game-30, screen_height_game-30))
                if back_arrow_rect_small.collidepoint(pygame.mouse.get_pos()):
                    screen.blit(back_arrow_surf_on_small, back_arrow_rect_small)
                else:
                    screen.blit(back_arrow_surf_off_small, back_arrow_rect_small)
                if screen_width_game - 46 < pygame.mouse.get_pos()[0] < screen_width_game - 10 and 10 < pygame.mouse.get_pos()[1] < 46:
                    screen.blit(save_icon_on_surf, (screen_width_game - 46, 10))
                else:
                    screen.blit(save_icon_off_surf, (screen_width_game - 46, 10))



                if np.count_nonzero(bool_field == 1) >= width * height - pocet_min:
                    for radek in range((len(bool_field))):
                        for sloupec in range((len(bool_field[0]))):
                            if field[radek][sloupec] == 9:
                                bool_field[radek][sloupec] = 1
                    end_game_screen = True
                    game = False
                    first_click = True
                    plot_bool_field(bool_field, field)
                    print("Výhra")
                    screen.blit(transparent_bg_surf, (0, 0))
            
        if end_game_screen:
            y_offset = 52
            add_y_offset = max(0, (screen_height_game - (2*dh+35))/2)
            screen.blit(text_victory_surf, (screen_width_game/2-text_victory_surf.get_width()/2, 5 + add_y_offset))
            for text_surf in text_victory_surfs:   
                screen.blit(text_surf, (screen_width_game/2-text_surf.get_width()/2, y_offset + add_y_offset))
                y_offset += text_surf.get_height()

        pygame.display.flip()
        clock.tick(60) # Limits the game to 60 fps, better for slower CPU
        it += 1

if __name__ == "__main__":
    main()


