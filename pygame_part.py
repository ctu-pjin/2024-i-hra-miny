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

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)


# Part for loading images
new_game_surf_off = pygame.image.load("surfaces/yellow_white_border_1.png").convert_alpha() #surfaces of the object
new_game_surf_on = pygame.image.load("surfaces/yellow_white_border_2.png").convert_alpha() 
new_game_rect_off = new_game_surf_off.get_rect(midbottom=(screen_width/2, 400)) #rectangle of the surface. Easier to specify an exact location
new_game_rect_on = new_game_surf_on.get_rect(midbottom=(screen_width/2, 400))
load_surf_off = pygame.image.load("surfaces/yellow_white_border_load_2.png").convert_alpha()
load_surf_on = pygame.image.load("surfaces/yellow_white_border_load_1.png").convert_alpha()
load_rect_off = load_surf_off.get_rect(midbottom=(screen_width/2, 500)) 
load_rect_on = load_surf_on.get_rect(midbottom=(screen_width/2, 500))



# Part for loading fonts
karma_font_160 = pygame.font.Font("fonts/KarmaFuture.otf", 160)
text_miny_surf = karma_font_160.render("Miny", False, "Black")
text_miny_rect = text_miny_surf.get_rect(midtop=(screen_width/2, 40))
screen.blit(text_miny_surf,text_miny_rect)

def main():
    game_active = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
                pygame.quit()
                exit()
        if game_active:
            screen.fill((255, 255, 255))  # Creates a black screen
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
                
        pygame.display.flip()


if __name__ == "__main__":
    main()


