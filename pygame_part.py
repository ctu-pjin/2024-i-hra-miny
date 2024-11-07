import pygame
from sys import exit
from time import time, sleep
from random import choice, randint
import os
import math
import pole_funkce

# Initialize Pygame
os.environ['SDL_VIDEO_CENTERED'] = '1' # Centers the screen on the display
os.environ['SDL_RENDER_SCALE_QUALITY'] = '2' # '0' is the worst quality | '2' is the best quality | '1' is in the middle
                                        # May reduce later
pygame.init()

screen_width, screen_height = 480, 540

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



# Part for loading fonts
karma_font_160 = pygame.font.Font("fonts/KarmaFuture.otf", 160)
karma_font_60 = pygame.font.Font("fonts/KarmaFuture.otf", 60)

# Part for loading texts
text_miny_surf = karma_font_160.render("Miny", False, "Black")
text_miny_rect = text_miny_surf.get_rect(midtop=(screen_width/2, 40))
text_difficulty_surf = karma_font_60.render("Difficulty", False, "Black")
text_difficulty_rect = text_difficulty_surf.get_rect(midtop=(screen_width/2, 70))




clock = pygame.time.Clock()
mine_field = random_mine_screen_generation(screen_width, screen_height)
draw_to_buffer(buffer_surface, mine_field)


def plot_bool_field(bool_field, field, cell_size = 30): # minefield plotting
    dw = 10
    dh = 100
    for row in range(len(field)):
        for col in range(len(field[row])):
            match bool_field[row,col]:
                case 0:
                    screen.blit(box_surf, (col*cell_size+dw, row*cell_size+dh))
                case 1:
                    match field[row,col]:
                        case 0:
                            screen.blit(null_surf, (col*cell_size+dw, row*cell_size+dh))
                        case 1: 
                            screen.blit(one_surf, (col*cell_size+dw, row*cell_size+dh))
                        case 2: 
                            screen.blit(two_surf, (col*cell_size+dw, row*cell_size+dh))
                        case 3: 
                            screen.blit(three_surf, (col*cell_size+dw, row*cell_size+dh))
                        case 4: 
                            screen.blit(four_surf, (col*cell_size+dw, row*cell_size+dh))
                        case 5: 
                            screen.blit(five_surf, (col*cell_size+dw, row*cell_size+dh))
                        case 6: 
                            screen.blit(six_surf, (col*cell_size+dw, row*cell_size+dh))
                        case 7: 
                            screen.blit(seven_surf, (col*cell_size+dw, row*cell_size+dh))
                        case 8: 
                            screen.blit(eight_surf, (col*cell_size+dw, row*cell_size+dh))
                        case 9: 
                            screen.blit(mine_surf, (col*cell_size+dw, row*cell_size+dh))
                case 2:
                    screen.blit(flag_surf, (col*cell_size+dw, row*cell_size+dh))


def main():
    it = 0
    menu = True
    new_game_menu = False
    game = False
    global screen
    while True: 
        for event in pygame.event.get(): # All events are written in this for loop
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if menu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if new_game_rect_on.collidepoint(pygame.mouse.get_pos()):
                            screen = pygame.display.set_mode(MENU_SCREEN_DIMENSIONS)
                            new_game_menu = True
                            menu = False
            if new_game_menu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if easy_rect_on.collidepoint(pygame.mouse.get_pos()):
                            width, height, pocet_min = 15, 10, 20
                            screen = pygame.display.set_mode((width*30+20, height*30 + 110))
                            new_game_menu = False
                            game = True
                            if pygame.MOUSEBUTTONUP:
                                if pygame.mouse.get_pressed()[0]:
                                    field, bool_field = pole_funkce.start(width, height, pocet_min)
                        elif back_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                            screen = pygame.display.set_mode(MENU_SCREEN_DIMENSIONS)
                            menu = True
                            new_game_menu = False
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
            screen.fill((100, 100, 100))
            pygame.draw.rect(screen, (180, 180, 180), (5, 5, width*30+10, height*30+100))
            plot_bool_field(bool_field, field)
                
        pygame.display.flip()
        clock.tick(60) # Limits the game to 60 fps, better for slower CPU
        it += 1

if __name__ == "__main__":
    main()


