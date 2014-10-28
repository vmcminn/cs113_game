import os
import sys
import pygame

# add everything from colors.py into local namespace
from colors import *

# add some commonly used pygame objects into local namespace
from pygame.locals import *

# set window starting position for my desktop which has multiple monitors, this
# is a convenience thing for me.  You guys can add your own setting here if
# it's useful for you
if os.environ['COMPUTERNAME'] == 'BRIAN-DESKTOP':
    os.environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(1920, 90)
# -------------------------------------------------------------------------


class GameLoop:

    def __init__(self):
        def _setup_screen():
            # set the window size - can add the NOFRAME arg if we don't want a
            # window frame but then we have to figure out how to move the
            # window since it won't have a menu bar to grab
            pygame.display.set_mode((1280, 600))

            pygame.display.set_caption('Team Bears!')

        def _setup_input():
            pygame.key.set_repeat(500, 100)  # allow multiple KEYDOWN events
            try:
                self.gamepad = pygame.joystick.Joystick(0)
                self.gamepad.init()
                self.gamepad_found = True
            except Exception:
                self.gamepad_found = False

        def _draw_initial():
            self.surface = pygame.display.get_surface()
            self.window_border = Rect((0, 0), (1280, 600))
            self.play_area = Rect((65, 0), (1150, 475))
            self.play_area_border = Rect((40, 0), (1200, 500))
            self.player = Rect((200, 300), (30, 40))

        pygame.init()
        _setup_screen()
        _setup_input()
        _draw_initial()

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
            self.check_if_window_closed()

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
        def _handle_keyboard_input():
            # get state of all keyboard buttons - True if key pressed down
            keys_pressed = pygame.key.get_pressed()

            if keys_pressed[K_LEFT]:
                self.player.move_ip((-5, 0))  # left
            if keys_pressed[K_RIGHT]:
                self.player.move_ip((+5, 0))  # right
            if keys_pressed[K_UP]:
                self.player.move_ip((0, -5))  # up
            if keys_pressed[K_DOWN]:
                self.player.move_ip((0, +5))  # down

            if keys_pressed[K_SPACE]:  # debug
                while True:
                    try:
                        exec(input('\nEnter something to exec: '))
                        break
                    except Exception as err:
                        print('>> {}: {} <<'.format(type(err).__name__, err))

            if keys_pressed[K_q]:  # quit
                # Add the QUIT event to the pygame event queue to be handled
                # later, at the same time the QUIT event from clicking the
                # window X is handled
                pygame.event.post(pygame.event.Event(QUIT))

        def _handle_gamepad_input():
            if self.gamepad_found:
                axis_0 = round(self.gamepad.get_axis(0))
                axis_1 = round(self.gamepad.get_axis(1))
                button_a = self.gamepad.get_button(1)

                if axis_0 == -1:
                    self.player.move_ip((-5, 0))  # left
                if axis_0 == +1:
                    self.player.move_ip((+5, 0))  # right

                if axis_1 == -1:
                    self.player.move_ip((0, -5))  # up
                if axis_1 == +1:
                    self.player.move_ip((0, +5))  # down

                if button_a:
                    self.player = Rect((0, 0), (30, 40))  # reset

        def _get_keys_pressed():
            pass

        def _get_keys_depressed():
            pass

        def _move_character():
            pass

        def _use_skills():
            pass

        _handle_keyboard_input()
        _handle_gamepad_input()

    # -------------------------------------------------------------------------
    def handle_npcs(self):
        def _move_npcs():
            pass

        def _use_skills_npcs():
            pass
        pass

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

        def _draw_map():
            # playable movement space
            pygame.draw.rect(self.surface, SKYBLUE, self.play_area)
            # creates a thin green rectangle border of surface
            pygame.draw.rect(self.surface, GREEN, self.window_border, 1)

        def _draw_players():
            # placeholder for a playable character; is movable
            pygame.draw.rect(self.surface, LBLUE, self.player)
            pass

        def _draw_npcs():
            pass

        def _draw_particles():
            pass

        _draw_ui()
        _draw_map()
        _draw_players()
        pygame.display.update()  # necessary to update the display
        pygame.time.delay(50)  # pause for 50 milliseconds

    # -------------------------------------------------------------------------
    def check_if_game_over(self):
        pass

    # -------------------------------------------------------------------------
    def check_if_window_closed(self):
        for event in pygame.event.get():  # loop through all pygame events
            # QUIT event occurs when click X on window bar
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

# -------------------------------------------------------------------------
if __name__ == '__main__':
    GameLoop()()
