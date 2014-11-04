import os
import sys
import pygame

# add everything from colors.py into local namespace
from colors import *
from classes import *
from globals import *
from gametime import *

# add some commonly used pygame objects into local namespace
from pygame.locals import *

# set window starting position for my desktop which has multiple monitors, this
# is a convenience thing for me.  You guys can add your own setting here if
# it's useful for you
if os.environ['COMPUTERNAME'] == 'BRIAN-DESKTOP':
    os.environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(1920, 90)
# @PYGAMERUNSPECIAL
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
            pygame.key.set_repeat(500, 100)  # allow multiple KEYDOWN events
            self.input = Input()

        def _setup_Rects():
            self.window = self.surface.get_rect()
            self.window_border = Rect((0, 0), (1280, 600))
            self.play_area = Rect((65, 0), (1150, 475))
            self.play_area_border = Rect((40, 0), (1200, 500))
            self.player = Player(left=200, top=300, width=30, height=40, speed=5)
            self.projectile = Player(left=self.play_area.right, top=self.play_area.centery, width=10, height=10, speed=8)

        def _setup_fonts():
            self.timer_font = pygame.font.SysFont('gigi', 36)
            self.font50 = pygame.font.SysFont('gigi', 55)
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
            self.handle_timer_based_events()
            self.handle_player_input()
            self.handle_npcs()
            self.detect_collisions()
            self.take_damage()
            self.draw_screen()
            self.check_if_game_over()
            self.handle_event_queue()
            self.clock.tick(self.fps)

    # -------------------------------------------------------------------------
    def handle_timer_based_events(self):
        def _health_regen():
            pass

        def _energy_regen():
            pass

        def _spawn_npc():
            pass
        pass

    # -------------------------------------------------------------------------
    def handle_player_input(self):
        def _move_character():
            # create a copy of player, move the copy, and test if the copy
            # is fully contained within the playable area rectangle.  If
            # it is, then move the player to same position as the copy
            temp_player = self.player.copy()
            if self.input.LEFT:
                temp_player.move_ip(LEFT)  # left

            if self.input.RIGHT:
                temp_player.move_ip(RIGHT)  # right

            if self.input.UP:
                temp_player.move_ip(UP)  # up

            if self.input.DOWN:
                temp_player.move_ip(DOWN)  # down

            if self.input.RESET:
                # 'a' button or 'r' key
                temp_player.topleft = self.player.initial_topleft

            if self.play_area.contains(temp_player):
                self.player.topleft = temp_player.topleft

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

        def _use_skills():
            pass

        self.input.refresh()
        _move_character()
        _special_input()

    # -------------------------------------------------------------------------
    def handle_npcs(self):
        def _move_npcs():
            self.projectile.move_ip(LEFT)

        def _use_skills_npcs():
            pass
        _move_npcs()

    # -------------------------------------------------------------------------
    def detect_collisions(self):
        def _player_terrain():
            pass

        def _player_particle():
            pass

        def _player_player():
            pass

        def _player_npc():
            pass

        def _npc_particle():
            pass

        def _particle_particle():
            pass
        if self.projectile.colliderect(self.player):
            self.player.health -= 5
        pass

    # -------------------------------------------------------------------------
    def take_damage(self):
        def _player():
            pass

        def _npcs():
            pass

        def _temp_terrains():
            pass
        pass

    # -------------------------------------------------------------------------
    def draw_screen(self):
        def _draw_ui():
            # fill background dark grey
            self.surface.fill(DGREY)
            # red border of playable movement space
            pygame.draw.rect(self.surface, DKRED, self.play_area_border)
            # font for health indicator, for testing purposes only
            rendered_font = self.font50.render(str(self.player.health), True, RED)
            self.surface.blit(rendered_font, (self.font50x, self.font50y))

        def _draw_timer():
            time_display = self.timer_font.render(str(self.game_time), True, BLUE)
            self.surface.blit(time_display, (640, 500))

        def _draw_map():
            # playable movement space
            pygame.draw.rect(self.surface, SKYBLUE, self.play_area)
            # creates a thin green rectangle border of surface
            pygame.draw.rect(self.surface, GREEN, self.window_border, 1)

        def _draw_players():
            # placeholder for a playable character; is movable
            pygame.draw.rect(self.surface, LBLUE, self.player)

        def _draw_npcs():
            pygame.draw.rect(self.surface, RED, self.projectile)

        def _draw_particles():
            pass

        _draw_ui()
        _draw_timer()
        _draw_map()
        _draw_players()
        _draw_npcs()
        pygame.display.update()  # necessary to update the display

    # -------------------------------------------------------------------------
    def check_if_game_over(self):
        pass

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
