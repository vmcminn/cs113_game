# python standard library modules
import os
import sys

# pygame
import pygame
from pygame.locals import *

# our modules
from colors import *
from classes import *
from globals import *
from gametime import *

# set window starting position for my desktop which has multiple monitors, this
# is a convenience thing for me.  You guys can add your own setting here if
# it's useful for you
if os.environ['COMPUTERNAME'] == 'BRIAN-DESKTOP':
    os.environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(1920, 90)
if os.environ['COMPUTERNAME'] == 'MAX-LT':
    os.environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(50, 30)

# @PYGAMERUNSPECIAL  setting for my IDE
# -------------------------------------------------------------------------


class GameLoop:
    def __init__(self):
        def _setup_display():
            # set the window size - can add the NOFRAME arg if we don't want a
            # window frame but then we have to figure out how to move the
            # window since it won't have a menu bar to grab
            pygame.display.set_mode((1280, 600))
            pygame.display.set_caption('Famished Tournament')
            self.surface = pygame.display.get_surface()

        def _setup_time():
            self.clock = pygame.time.Clock()
            self.fps = 30
            pygame.time.set_timer(USEREVENT + 1, 250)
            self.game_time = GameTime()

        def _setup_input():
            pygame.key.set_repeat(100, 10)  # allow multiple KEYDOWN events
            self.input = Input()

        def _setup_Rects():
            self.window = self.surface.get_rect()
            self.window_border = Rect((0, 0), (1278, 600))
            self.play_area = Rect((65, 0), (1150, 475))
            self.play_area_border = Rect((40, 0), (1200, 500))
            self.player = Player(left=200, top=150, width=30, height=40)
            self.arena = arena1

        def _setup_fonts():
            self.timer_font = pygame.font.Font('gigi.ttf', 36)
            self.font50 = pygame.font.Font('gigi.ttf', 55)
            self.font50x = ((self.window.w - self.font50.size('100')[0]) // 20) * 1
            self.font50y = ((self.window.h - self.font50.size('100')[1]) // 20) * 19
            self.font200 = pygame.font.SysFont(None, 200)
            self.font200x = ((self.window.w - self.font200.size('-PAUSE-')[0]) // 2) * 1
            self.font200y = ((self.window.h - self.font200.size('-PAUSE-')[1]) // 2) * 1

        pygame.init()
        _setup_display()
        _setup_time()
        _setup_input()
        _setup_Rects()
        _setup_fonts()

    # ------------------------------------------------------------------------
    def __call__(self):
        while True:
            self.handle_player_input()
            self.draw_screen()
            self.handle_event_queue()
            self.clock.tick(self.fps)

    # -------------------------------------------------------------------------
    def handle_player_input(self):

        def _special_input():
            if self.input.DEBUG:
                rendered_font = self.font200.render('-PAUSE-', True, RED)
                self.surface.blit(rendered_font, (self.font200x, self.font200y))
                pygame.display.update()
                try:
                    exec(input('\nEnter something to exec: '))
                except Exception as err:
                    print('>> {}: {} <<'.format(type(err).__name__, err))

            if self.input.EXIT:
                # Add the QUIT event to the pygame event queue to be handled
                # later, at the same time the QUIT event from clicking the
                # window X is handled
                pygame.event.post(pygame.event.Event(QUIT))

        self.input.refresh()
        self.player(self.input, self.arena)
        _special_input()

    # -------------------------------------------------------------------------
    def draw_screen(self):
        def _draw_ui():
            # fill background dark grey
            self.surface.fill(DGREY)
            # thin green border of surface
            pygame.draw.rect(self.surface, GREEN, self.window_border, 1)
            # red border of playable movement space
            pygame.draw.rect(self.surface, DKRED, self.play_area_border)
            # font for health indicator, for testing purposes only
            rendered_font = self.font50.render(str(self.player.hit_points), True, RED)
            self.surface.blit(rendered_font, (self.font50x, self.font50y))

        def _draw_timer():
            time_display = self.timer_font.render(str(self.game_time), True, BLUE)
            self.surface.blit(time_display, (640, 500))

        def _draw_map():
            for rect, rect_color in self.arena:
                pygame.draw.rect(self.surface, rect_color, rect)

        def _draw_players():
            # placeholder for a playable character; is movable
            pygame.draw.rect(self.surface, LBLUE, self.player)

        _draw_ui()
        _draw_timer()
        _draw_map()
        _draw_players()
        pygame.display.update()  # necessary to update the display

    # -------------------------------------------------------------------------
    def handle_event_queue(self):
        # loop through all pygame events
        for event in pygame.event.get():
            # update game timer
            if event.type == USEREVENT + 1:
                self.game_time.inc()

            # QUIT event occurs when click X on window bar
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

# -------------------------------------------------------------------------
if __name__ == '__main__':
    GameLoop()()
