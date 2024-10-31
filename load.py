import pygame
from collections import namedtuple

# Mohlo by se hodit do budoucna pro přehlednost kódu, zatím neaktivní řešení

# Define a named tuple for storing surfaces and rectangles
ImageAssets = namedtuple("ImageAssets", [
    "new_game_surf_off", "new_game_surf_on", "new_game_rect_off", "new_game_rect_on",
    "load_surf_off", "load_surf_on", "load_rect_off", "load_rect_on"
])

def load_images(screen_width, screen_height):
    # Load images
    new_game_surf_off = pygame.image.load("surfaces/yellow_white_border_1.png").convert_alpha()
    new_game_surf_on = pygame.image.load("surfaces/yellow_white_border_2.png").convert_alpha()
    load_surf_off = pygame.image.load("surfaces/yellow_white_border_load_2.png").convert_alpha()
    load_surf_on = pygame.image.load("surfaces/yellow_white_border_load_1.png").convert_alpha()

    # Create rects with specified positions
    new_game_rect_off = new_game_surf_off.get_rect(midbottom=(screen_width / 2, 400))
    new_game_rect_on = new_game_surf_on.get_rect(midbottom=(screen_width / 2, 400))
    load_rect_off = load_surf_off.get_rect(midbottom=(screen_width / 2, 500))
    load_rect_on = load_surf_on.get_rect(midbottom=(screen_width / 2, 500))

    # Return all assets as a named tuple
    return ImageAssets(
        new_game_surf_off, new_game_surf_on, new_game_rect_off, new_game_rect_on,
        load_surf_off, load_surf_on, load_rect_off, load_rect_on
    )