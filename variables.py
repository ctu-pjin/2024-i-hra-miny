import pygame
import os

screen_width, screen_height = 480, 600
pygame.display.set_mode((0, 0))
# Initialize Pygame
os.environ['SDL_VIDEO_CENTERED'] = '1' # Centers the screen on the display
os.environ['SDL_RENDER_SCALE_QUALITY'] = '2' # '0' is the worst quality | '2' is the best quality | '1' is in the middle
                                        # May reduce later

class Surf:
    def __init__(self):
        self.script_dir = os.path.abspath(os.path.dirname("variables.py"))
        self.new_game_off = pygame.image.load(self.script_dir + "/surfaces/new_game_button_off.png").convert_alpha() #surfaces of the object
        self.new_game_on = pygame.image.load(self.script_dir + "/surfaces/new_game_button_on.png").convert_alpha() 
        self.load_off = pygame.image.load(self.script_dir + "/surfaces/load_button_off.png").convert_alpha()
        self.load_on = pygame.image.load(self.script_dir + "/surfaces/load_button_on.png").convert_alpha()
        self.scores_off = pygame.image.load(self.script_dir + "/surfaces/scores_button_off.png").convert_alpha()
        self.scores_on = pygame.image.load(self.script_dir + "/surfaces/scores_button_on.png").convert_alpha()
        self.back_arrow_on = pygame.image.load(self.script_dir + "/surfaces/back_arrow_flow_on.png").convert_alpha()
        self.back_arrow_off = pygame.image.load(self.script_dir + "/surfaces/back_arrow_flow_off.png").convert_alpha()
        self.back_arrow_on_small = pygame.transform.scale_by(self.back_arrow_on, 0.7)
        self.back_arrow_off_small = pygame.transform.scale_by(self.back_arrow_off, 0.7)
        self.easy_on  = pygame.image.load(self.script_dir + "/surfaces/easy_button_on.png").convert_alpha()
        self.easy_off  = pygame.image.load(self.script_dir + "/surfaces/easy_button_off.png").convert_alpha()
        self.medium_on  = pygame.image.load(self.script_dir + "/surfaces/medium_button_on.png").convert_alpha()
        self.medium_off  = pygame.image.load(self.script_dir + "/surfaces/medium_button_off.png").convert_alpha()
        self.hard_on  = pygame.image.load(self.script_dir + "/surfaces/hard_button_on.png").convert_alpha()
        self.hard_off  = pygame.image.load(self.script_dir + "/surfaces/hard_button_off.png").convert_alpha()
        self.custom_on = pygame.image.load(self.script_dir + "/surfaces/custom_button_on.png").convert_alpha()
        self.custom_off = pygame.image.load(self.script_dir + "/surfaces/custom_button_off.png").convert_alpha()
        self.box = pygame.image.load(self.script_dir + "/mines/box.png").convert()
        self.null = pygame.image.load(self.script_dir + "/mines/empty.png").convert()
        self.one = pygame.image.load(self.script_dir + "/mines/one.png").convert()
        self.two = pygame.image.load(self.script_dir + "/mines/two.png").convert()
        self.three = pygame.image.load(self.script_dir + "/mines/three.png").convert()
        self.four = pygame.image.load(self.script_dir + "/mines/four.png").convert()
        self.five = pygame.image.load(self.script_dir + "/mines/five.png").convert()
        self.six = pygame.image.load(self.script_dir + "/mines/six.png").convert()
        self.seven = pygame.image.load(self.script_dir + "/mines/seven.png").convert()
        self.eight = pygame.image.load(self.script_dir + "/mines/eight.png").convert()
        self.mine = pygame.image.load(self.script_dir + "/mines/mine.png").convert()
        self.mine_purple = pygame.image.load(self.script_dir + "/mines/mine_purple.png").convert()
        self.mine_explode = pygame.image.load(self.script_dir + "/mines/mine_explode.png").convert()
        self.mine_explode_only = pygame.image.load(self.script_dir + "/mines/mine_explode_only.png").convert_alpha()
        self.flag = pygame.image.load(self.script_dir + "/mines/flag.png").convert()
        self.blue_flag = pygame.image.load(self.script_dir + "/surfaces/flag_blue.png").convert()
        self.reshuffle_on = pygame.image.load(self.script_dir + "/surfaces/reshuffle_on.png").convert()
        self.reshuffle_off = pygame.image.load(self.script_dir + "/surfaces/reshuffle_off.png").convert()
        self.flag_only = pygame.image.load(self.script_dir + "/surfaces/flag_only.png").convert_alpha()
        self.flag_only_big = pygame.transform.scale_by(self.flag_only, 1.5)
        self.save_icon_on = pygame.image.load(self.script_dir + "/surfaces/save_icon_on.png").convert_alpha()
        self.save_icon_off = pygame.image.load(self.script_dir + "/surfaces/save_icon_off.png").convert_alpha()
        self.transparent_bg = pygame.image.load(self.script_dir + "/surfaces/transparent_bg_80.png").convert_alpha()
        self.empty_save = pygame.image.load(self.script_dir + "/surfaces/empty_save.png").convert_alpha()
        self.filled_save = pygame.image.load(self.script_dir + "/surfaces/filled_save.png").convert_alpha()
        self.game_saves = [pygame.image.load(self.script_dir + "/surfaces/filled_save.png").convert_alpha() for _ in range(3)]
        self.hint_on = pygame.image.load(self.script_dir + "/surfaces/hint_on.png").convert()
        self.hint_off = pygame.image.load(self.script_dir + "/surfaces/hint_off.png").convert()
        self.scores_button_on = pygame.image.load(self.script_dir + "/surfaces/scores_button_on.png").convert()
        self.scores_button_off = pygame.image.load(self.script_dir + "/surfaces/scores_button_off.png").convert()
        self.question_mark_off_no_scale = pygame.image.load(self.script_dir + "/surfaces/question_mark_off_spaced.png").convert_alpha()
        self.question_mark_on_no_scale = pygame.image.load(self.script_dir + "/surfaces/question_mark_on.png").convert_alpha()
        self.bin_on_no_scale = pygame.image.load(self.script_dir + "/surfaces/bin_opened.png").convert_alpha()
        self.bin_off_no_scale = pygame.image.load(self.script_dir + "/surfaces/bin_closed.png").convert_alpha()
        self.question_mark_off = pygame.transform.smoothscale(self.question_mark_off_no_scale, (int(self.question_mark_off_no_scale.get_size()[0] * 1.3), int(self.question_mark_off_no_scale.get_size()[1] * 1.3)))
        self.question_mark_on = pygame.transform.smoothscale(self.question_mark_on_no_scale, (int(self.question_mark_on_no_scale.get_size()[0] * 1.3), int(self.question_mark_on_no_scale.get_size()[1] * 1.3)))
        self.bin_on = pygame.transform.smoothscale(self.bin_on_no_scale, (int(self.bin_on_no_scale.get_size()[0] * 1.4), int(self.bin_on_no_scale.get_size()[1] * 1.4)))
        self.bin_off = pygame.transform.smoothscale(self.bin_off_no_scale, (int(self.bin_off_no_scale.get_size()[0] * 1.4), int(self.bin_off_no_scale.get_size()[1] * 1.4)))


class Rect:
    def __init__(self, Surf):
        self.new_game_off = Surf.new_game_off.get_rect(midbottom=(screen_width/2, 350)) #rectangle of the surface. Easier to specify an exact location
        self.new_game_on = Surf.new_game_on.get_rect(midbottom=(screen_width/2, 350))
        self.load_off = Surf.load_off.get_rect(midbottom=(screen_width/2, 450)) 
        self.load_on = Surf.load_on.get_rect(midbottom=(screen_width/2, 450))
        self.scores_off = Surf.scores_off.get_rect(midbottom=(screen_width/2, 550)) 
        self.scores_on = Surf.scores_on.get_rect(midbottom=(screen_width/2, 550))
        self.easy_on = Surf.easy_on.get_rect(midbottom=(screen_width/2, 250))
        self.easy_off = Surf.easy_off.get_rect(midbottom=(screen_width/2, 250))
        self.medium_on = Surf.medium_on.get_rect(midbottom=(screen_width/2, 350))
        self.medium_off = Surf.medium_off.get_rect(midbottom=(screen_width/2, 350))
        self.hard_on = Surf.hard_on.get_rect(midbottom=(screen_width/2, 450))
        self.hard_off = Surf.hard_off.get_rect(midbottom=(screen_width/2, 450))
        self.custom_on = Surf.custom_on.get_rect(midbottom=(screen_width/2, 550))
        self.custom_off = Surf.custom_off.get_rect(midbottom=(screen_width/2, 550))
        self.back_arrow = Surf.back_arrow_off.get_rect(topleft = (20, 20))
        self.back_arrow_small = Surf.back_arrow_off_small.get_rect(topleft = (10, 15))
        self.reshuffle = Surf.reshuffle_on.get_rect(bottomleft = (10, 20))
        self.question_mark = Surf.question_mark_on.get_rect(topright = (screen_width - 15, 15))
        # Creating save slot and bin rectangles
        save_slot_width, save_slot_height = Surf.empty_save.get_width(), Surf.empty_save.get_height() 
        self.save_slots = []
        self.bins = []
        save_y_offset = 160

        for slot in range(3):
            save_slot_rect = pygame.Rect(screen_width/2 - save_slot_width/2 - 15, save_y_offset, save_slot_width, save_slot_height)
            self.save_slots.append(save_slot_rect)
            self.bins.append(pygame.Rect(self.save_slots[slot].x + 10 + self.save_slots[slot].width, self.save_slots[slot].y + 35, Surf.bin_on.get_width(), Surf.bin_on.get_height()))
            save_y_offset += 95


class Font:
    def  __init__(self):
        self.script_dir = os.path.abspath(os.path.dirname("variables.py"))
        self.karma_160 = pygame.font.Font(self.script_dir + "/fonts/KarmaFuture.otf", 160)
        self.karma_60 = pygame.font.Font(self.script_dir + "/fonts/KarmaFuture.otf", 60)
        self.karma_suture_23 = pygame.font.Font(self.script_dir + "/fonts/KarmaSuture.otf", 23)
        self.karma_suture_21 = pygame.font.Font(self.script_dir + "/fonts/KarmaSuture.otf", 21)
        self.karma_suture_16 = pygame.font.Font(self.script_dir + "/fonts/KarmaSuture.otf", 16)
        self.karma_suture_30 = pygame.font.Font(self.script_dir + "/fonts/KarmaSuture.otf", 30)
        self.karma_35 = pygame.font.Font(self.script_dir + "/fonts/KarmaFuture.otf", 35)
        