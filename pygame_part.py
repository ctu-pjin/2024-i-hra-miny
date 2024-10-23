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
to_delete_surf = pygame.image.load("surfaces/to_delete.jpg") #surfaces of the object
to_delete_rect = to_delete_surf.get_rect(topright=(screen_width, 0)) #rectangle of the surface. Easier to specify an exact location
#
#



def main():
    game_active = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
                pygame.quit()
                exit()
        if game_active:
            screen.fill((0, 0, 0))  # Creates a black screen
            pygame.draw.rect(screen, (255, 0, 0), (0, 0, 80, 80))  # Draw a red rectangle
            screen.blit(to_delete_surf, to_delete_rect)
        pygame.display.flip()


if __name__ == "__main__":
    main()


