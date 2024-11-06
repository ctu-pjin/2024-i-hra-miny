import pygame
from sys import exit
from time import time, sleep
from random import choice, randint
import os
import math


# Initialize Pygame
os.environ['SDL_VIDEO_CENTERED'] = '1' # Centers the screen on the display
os.environ['SDL_RENDER_SCALE_QUALITY'] = '2' # '0' is the worst quality | '2' is the best quality | '1' is in the middle
                                        # May reduce later
pygame.init()

screen_width, screen_height = 480, 540
screen = pygame.display.set_mode((screen_width, screen_height))
buffer_surface = pygame.Surface((screen_width, screen_height))


# Part for loading images
new_game_surf_off = pygame.image.load("surfaces/yellow_white_border_1.png").convert_alpha() #surfaces of the object
new_game_surf_on = pygame.image.load("surfaces/yellow_white_border_2.png").convert_alpha() 
load_surf_off = pygame.image.load("surfaces/yellow_white_border_load_2.png").convert_alpha()
load_surf_on = pygame.image.load("surfaces/yellow_white_border_load_1.png").convert_alpha()
back_arrow_surf_on = pygame.image.load("surfaces/back_arrow_pressed_200.png").convert_alpha()
back_arrow_surf_off = pygame.image.load("surfaces/back_arrow_200.png").convert_alpha()
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
back_arrow_rect = back_arrow_surf_off.get_rect(topleft = (20, 20))



# Part for loading fonts
karma_font_160 = pygame.font.Font("fonts/KarmaFuture.otf", 160)
karma_font_60 = pygame.font.Font("fonts/KarmaFuture.otf", 60)

# Part for loading texts
text_miny_surf = karma_font_160.render("Miny", False, "Black")
text_miny_rect = text_miny_surf.get_rect(midtop=(screen_width/2, 40))
text_to_delete_new_game_surf = karma_font_60.render("volba obtížnosti", False, "Black")
text_to_delete_new_game_rect = text_to_delete_new_game_surf.get_rect(midtop=(screen_width/2, 120))


clock = pygame.time.Clock()
mine_field = random_mine_screen_generation(screen_width, screen_height)
draw_to_buffer(buffer_surface, mine_field)

def main():
    it = 0
    menu = True
    new_game_menu = False
    while True: 
        for event in pygame.event.get(): # All events are written in this for loop
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if menu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if new_game_rect_on.collidepoint(pygame.mouse.get_pos()):
                            new_game_menu = True
                            menu = False
            if new_game_menu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if back_arrow_rect.collidepoint(pygame.mouse.get_pos()):
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
            screen.fill((255, 255, 255))
            screen.blit(text_to_delete_new_game_surf, text_to_delete_new_game_rect)
            if back_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(back_arrow_surf_on, back_arrow_rect)
            else:
                screen.blit(back_arrow_surf_off, back_arrow_rect)
             
                
        pygame.display.flip()
        clock.tick(60) # Limits the game to 60 fps, better for slower CPU
        it += 1

if __name__ == "__main__":
    main()


