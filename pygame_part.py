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

screen_width, screen_height = 500, 550
screen = pygame.display.set_mode((screen_width, screen_height))


# Part for loading images
new_game_surf_off = pygame.image.load("surfaces/yellow_white_border_1.png").convert_alpha() #surfaces of the object
new_game_surf_on = pygame.image.load("surfaces/yellow_white_border_2.png").convert_alpha() 
load_surf_off = pygame.image.load("surfaces/yellow_white_border_load_2.png").convert_alpha()
load_surf_on = pygame.image.load("surfaces/yellow_white_border_load_1.png").convert_alpha()
back_arrow_surf_on = pygame.image.load("surfaces/back_arrow_pressed_200.png").convert_alpha()
back_arrow_surf_off = pygame.image.load("surfaces/back_arrow_200.png").convert_alpha()

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

def main():
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


if __name__ == "__main__":
    main()


