# python standard library modules
import os
import sys
import textwrap
import pygbutton

# pygame
import pygame
from pygame.locals import *

# our modules
import globals as GL
from globals import *
from pygbutton import *
from classes import *

selection_box_width = 4

class StartMenu:
    def __init__(self):
        self.bg_image = pygame.image.load('data/background2.png')
        self.start_button = PygButton((325, 395, 140, 40), 'Start')
        self.help_button = PygButton((485, 395, 110, 40), 'Help')
        self.options_button = PygButton((615, 395, 175, 40), 'Options')
        self.exit_button = PygButton((810, 395, 105, 40), 'Exit')
        AUDIO.turn_on_music()
        title_font = pygame.font.Font('data/Kremlin.ttf', 50)
        self.title_font1 = title_font.render('Famished', True, DKRED)
        self.title_font2 = title_font.render('Tournament', True, DKRED)
        self.selection_box_properties = [(325, 395, 140, 40), (485, 395, 110, 40), (615, 395, 175, 40), (810, 395, 105, 40)]
        self.selection_box_i = 0

    def __call__(self):
        self.return_now = False
        while not self.return_now:
            self.draw()
            self.input()
            self.events()
            GL.CLOCK.tick(GL.FPS)

    def draw(self):
        GL.SCREEN.blit(self.bg_image, (0, 0))
        self.start_button.draw(GL.SCREEN)
        self.help_button.draw(GL.SCREEN)
        self.options_button.draw(GL.SCREEN)
        self.exit_button.draw(GL.SCREEN)
        GL.SCREEN.blit(self.title_font1, (495, 120))
        GL.SCREEN.blit(self.title_font2, (450, 175))
        self.selection_box = Rect2(self.selection_box_properties[self.selection_box_i], color=BLUE)
        pygame.draw.rect(GL.SCREEN, self.selection_box.color, self.selection_box, selection_box_width)
        pygame.display.update()

    def input(self):
        GL.INPUT1.refresh()

        if GL.INPUT1.kb_input['K_F12']:
            self.return_now = True
            GL.NEXT_PAGE = 'GameLoop()'

        if GL.INPUT1.SELECT_PRESS_EVENT:
            GL.INPUT1.SELECT_PRESS_EVENT = False

        if GL.INPUT1.B_PRESS_EVENT:
            GL.INPUT1.B_PRESS_EVENT = False

        if GL.INPUT1.START_PRESS_EVENT or GL.INPUT1.A_PRESS_EVENT:

            if GL.INPUT1.START_PRESS_EVENT:
                GL.INPUT1.START_PRESS_EVENT = False

            if GL.INPUT1.A_PRESS_EVENT:
                GL.INPUT1.A_PRESS_EVENT = False

            if self.selection_box_i == 0:
                self.return_now = True
                GL.NEXT_PAGE = 'PlayerSelectPage()'

            elif self.selection_box_i == 1:
                self.return_now = True
                GL.NEXT_PAGE = 'help'

            elif self.selection_box_i == 2:
                self.return_now = True
                GL.NEXT_PAGE = 'options'

            elif self.selection_box_i == 3:
                self.return_now = True
                EXIT_GAME()

        if GL.INPUT1.RIGHT_PRESS_EVENT:
            GL.INPUT1.RIGHT_PRESS_EVENT = False
            self.selection_box_i += 1
            if self.selection_box_i > 3:
                self.selection_box_i = 0

        if GL.INPUT1.LEFT_PRESS_EVENT:
            GL.INPUT1.LEFT_PRESS_EVENT = False
            self.selection_box_i -= 1
            if self.selection_box_i < 0:
                self.selection_box_i = 3

    def events(self):
        for event in pygame.event.get():
            if 'click' in self.start_button.handleEvent(event):
                self.selection_box_i = 0
                self.return_now = True
                GL.NEXT_PAGE = 'PlayerSelectPage()'

            if 'click' in self.help_button.handleEvent(event):
                self.selection_box_i = 1
                self.return_now = True
                GL.NEXT_PAGE = 'help'

            if 'click' in self.options_button.handleEvent(event):
                self.selection_box_i = 2
                self.return_now = True
                GL.NEXT_PAGE = 'options'

            if 'click' in self.exit_button.handleEvent(event):
                self.selection_box_i = 3
                EXIT_GAME()

            if event.type == pygame.QUIT:
                EXIT_GAME()

# ----------------------------------------------------------------------------
class HelpPage:
    def __init__(self):
        self.return_button = pygbutton.PygButton((0, 550, 300, 50), 'Main Menu')
        self.section_font = pygame.font.Font('data/Kremlin.ttf', 40)
        self.font = pygame.font.Font('data/arial_narrow_7.ttf', 20)
        self.bg_image = pygame.image.load('data/help.png')
        self.bg_title = self.section_font.render('Background', True, WHITE)
        self.bg_text = textwrap.wrap('Under the tyranny of the dark overlord, the world' +
                                     'is in chaos and all the resources are nearly depleted. ' +
                                     'Entire populations have been subjugated to life in labor ' +
                                     'camps, brutally policed by the overlord\'s military forces. ' +
                                     'As your people\'s champion, you must fight to the death in the ' +
                                     'battle arena to win much needed resources.', width=50)
        self.goals_title = self.section_font.render('Goals', True, WHITE)
        self.goals_text = textwrap.wrap('Ultimately, you want to slay your opponent. ' +
                                        'To become a better fighter, kill the monsters, gain ' +
                                        'experience, and pick up skills. The player to land ' +
                                        'the last hit on the monster will receives the experience ' +
                                        'points. An ultimate boss will spawn every few ' +
                                        'minutes. These bosses drop ultimate skills which ' +
                                        'will help you humiliate and destroy your opponent.', width=50)
        self.selection_box_properties = [(0, 550, 300, 50)]
        self.selection_box_i = 0

    def __call__(self):
        self.return_now = False
        while not self.return_now:
            self.draw()
            self.input()
            self.events()
            GL.CLOCK.tick(GL.FPS)

    def draw(self):
        GL.SCREEN.fill(BLACK)
        GL.SCREEN.blit(self.bg_image, (0, 0))

        GL.SCREEN.blit(self.bg_title, (800, 40))
        for num, text in enumerate(self.bg_text):
            line = self.font.render(text, True, DKRED)
            GL.SCREEN.blit(line, (800, 90 + (num * 20)))

        GL.SCREEN.blit(self.goals_title, (800, 250))
        for num, text in enumerate(self.goals_text):
            line = self.font.render(text, True, DKRED)
            GL.SCREEN.blit(line, (800, 300 + (num * 20)))

        self.return_button.draw(GL.SCREEN)
        self.selection_box = Rect2(self.selection_box_properties[self.selection_box_i], color=BLUE)
        pygame.draw.rect(GL.SCREEN, self.selection_box.color, self.selection_box, selection_box_width)
        pygame.display.update()

    def input(self):
        GL.INPUT1.refresh()

        if GL.INPUT1.START_PRESS_EVENT:
            GL.INPUT1.START_PRESS_EVENT = False
            self.return_now = True
            GL.NEXT_PAGE = 'start'

        if GL.INPUT1.SELECT_PRESS_EVENT:
            GL.INPUT1.SELECT_PRESS_EVENT = False
            self.return_now = True
            GL.NEXT_PAGE = 'start'

        if GL.INPUT1.B_PRESS_EVENT:
            GL.INPUT1.B_PRESS_EVENT = False
            self.return_now = True
            GL.NEXT_PAGE = 'start'

        if GL.INPUT1.A_PRESS_EVENT:
            GL.INPUT1.A_PRESS_EVENT = False
            self.return_now = True
            GL.NEXT_PAGE = 'start'

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EXIT_GAME()
            if 'click' in self.return_button.handleEvent(event):
                self.return_now = True
                GL.NEXT_PAGE = 'start'

# ----------------------------------------------------------------------------
class PlayerSelectPage:

    def __init__(self):
        def _setup_display():
            self.return_button = pygbutton.PygButton((0, 550, 300, 50), 'Main Menu')
            self.player1_spritesheet = None
            self.player2_spritesheet = None

        def _load_images():
            self.bg_image = pygame.image.load('data/player_select_bkg.png')
            self.humanPortrait = pygame.image.load('data/portrait_human.png')
            self.elfPortrait = pygame.image.load('data/portrait_elf.png')

            self.portraits = [self.humanPortrait, self.elfPortrait]
            self.portraits2 = [self.humanPortrait, self.elfPortrait]

            # show human portrait by default
            self.index = 0
            self.index2 = 0

        def _setup_fonts():
            self.start_font = pygame.font.Font('data/Kremlin.ttf', 50)
            self.start_font_xy = font_position_center(GL.SCREEN.get_rect(), self.start_font, '---------------Press Start when ready---------------')
            self.start_font_rendered = self.start_font.render('---------------Press Start when ready---------------', True, YELLOW)

        def _setup_flags():
            self.ready1 = False
            self.ready2 = False
            self.start = False

            # if there is a second gamepad, there is a second player
            # set ready to false if second player exists
            # if no second player, set ready to true
            if not GL.INPUT2.get_gamepad():
                self.ready2 = True

        _setup_display()
        _setup_fonts()
        _setup_flags()
        _load_images()

    def __call__(self):
        self.return_now = False
        while not self.return_now:
            self.draw()
            self.input()
            self.events()
            GL.CLOCK.tick(GL.FPS)

    def draw(self):
        GL.SCREEN.blit(self.bg_image, (0, 0))
        self.return_button.draw(GL.SCREEN)
        GL.SCREEN.blit(self.portraits[self.index], (167, 106))
        GL.SCREEN.blit(self.portraits2[self.index2], (810, 106))
        if self.ready1 and self.ready2:
            GL.SCREEN.blit(self.start_font_rendered, self.start_font_xy)
        pygame.display.update()

    def input(self):

        def refresh_inputs():
            GL.INPUT1.refresh()
            GL.INPUT2.refresh()

            if GL.INPUT1.SELECT_PRESS_EVENT:
                GL.INPUT1.SELECT_PRESS_EVENT = False
                GL.NEXT_PAGE = 'start'

            if GL.INPUT2.SELECT_PRESS_EVENT:
                GL.INPUT2.SELECT_PRESS_EVENT = False
                GL.NEXT_PAGE = 'start'

        def player_select_inputs():

            def check_other_player(player):
                if player == 'player1':
                    if self.index == self.index2 and self.ready2:  # player 2 is using character, skip index
                        self.index += 1
                        if self.index >= len(self.portraits):
                            self.index = 0
                else:
                    if self.index == self.index2 and self.ready1:  # player 2 is using character, skip index
                        self.index2 += 1
                        if self.index2 >= len(self.portraits2):
                            self.index2 = 0

            def check_left_right(player):
                if player == 'player1':
                    if GL.INPUT1.LEFT_PRESS_EVENT:
                        GL.INPUT1.LEFT_PRESS_EVENT = False
                        self.index -= 1
                        if self.index < 0:
                            self.index = len(self.portraits) - 1

                        check_other_player('player1')


                    elif GL.INPUT1.RIGHT_PRESS_EVENT:
                        GL.INPUT1.RIGHT_PRESS_EVENT = False
                        self.index += 1
                        if self.index >= len(self.portraits):
                            self.index = 0

                        check_other_player('player1')

                elif player == 'player2':
                    if GL.INPUT2.LEFT_PRESS_EVENT:
                        GL.INPUT2.LEFT_PRESS_EVENT = False
                        self.index2 -= 1
                        if self.index2 < 0:
                            self.index2 = len(self.portraits2) - 1

                        check_other_player('player2')

                    elif GL.INPUT2.RIGHT_PRESS_EVENT:
                        GL.INPUT2.RIGHT_PRESS_EVENT = False
                        self.index2 += 1
                        if self.index2 >= len(self.portraits2):
                            self.index2 = 0

                        check_other_player('player2')

            # if player 1/2 is not ready, let them select character
            if not self.ready1:
                check_left_right('player1')
            if not self.ready2:
                check_left_right('player2')

        def player_done_selecting():
            # if player presses A
            # they selected sprite
            # set sprite to player
            # if they pressed select
            # they want to select a different sprite or return to start screen
            if GL.INPUT1.A_PRESS_EVENT or GL.INPUT1.kb_input['K_SPACE']:
                GL.INPUT1.A_PRESS_EVENT = False
                GL.INPUT1.kb_input['K_SPACE'] = False # press space on keyboard to select
                if self.ready2 and self.index2 == self.index:
                    print('Player 2 is using this character. Select a different one.')

                else:
                    print('player 1 ready')
                    self.ready1 = True

            elif GL.INPUT2.A_PRESS_EVENT:
                GL.INPUT2.A_PRESS_EVENT = False
                if self.ready1 and self.index2 == self.index:
                    print('Player 1 is using this character. Select a different one.')

                else:
                    print('player 2 ready')
                    self.ready2 = True

            # if player presses back when previously stated they were ready
            # allow them to reselect player
            # keyboard equivalent of select is 's' key
            elif GL.INPUT1.SELECT_PRESS_EVENT or GL.INPUT1.kb_input['K_s']:
                GL.INPUT1.SELECT_PRESS_EVENT = False
                GL.INPUT1.kb_input['K_s'] = False
                self.ready1 = False

            elif GL.INPUT2.SELECT_PRESS_EVENT:
                GL.INPUT2.SELECT_PRESS_EVENT = False
                self.ready2 = False

            # if player presses back when they were not ready
            # go back to start screen
            elif (GL.INPUT1.SELECT_PRESS_EVENT and not self.ready1 or GL.INPUT1.kb_input['K_s']):
                GL.INPUT1.SELECT_PRESS_EVENT = False
                GL.INPUT1.kb_input['K_s'] = False
                GL.NEXT_PAGE = 'start'

            elif (GL.INPUT2.SELECT_PRESS_EVENT and not self.ready2):
                GL.INPUT2.SELECT_PRESS_EVENT = False
                GL.NEXT_PAGE = 'start'

        def ready_for_start():
            if self.ready1 and self.ready2:

                # if player 1 or player 2 presses start when both players are ready
                # enter game loop
                # if using a keyboard - only one player
                # if keyboard user presses 'A' when he is ready
                # enter game loop
                if (GL.INPUT1.START_PRESS_EVENT or GL.INPUT2.START_PRESS_EVENT) or (GL.INPUT1.kb_input['K_a']):
                    if GL.INPUT1.START_PRESS_EVENT:
                        GL.INPUT1.START_PRESS_EVENT = False
                    if GL.INPUT2.START_PRESS_EVENT:
                        GL.INPUT2.START_PRESS_EVENT = False
                    if GL.INPUT1.kb_input['K_a']:
                        GL.INPUT1.kb_input['K_a'] = False

                    self.start = True
                    print('setting sprites')
                    set_sprites()
                    print('set sprites')
                    print('going to level select screen')
                    GL.NEXT_PAGE = 'LevelSelectPage()'
                    self.return_now = True

        def set_sprites():
            # set spritesheet for player1
            if self.index == 0:  # human
                self.player1_spritesheet = 'data/p1_human.png'
            # elif self.index == 1: #elf
            else:
                self.player1_spritesheet = 'data/p1_elf.png'

            if self.index2 == 0:  # human
                self.player2_spritesheet = 'data/p2_human.png'
            elif self.index2 == 1:  # elf
                self.player2_spritesheet = 'data/p2_elf.png'  # Elf spritesheet 2 if available

            GL.set_player1_spritesheet(self.player1_spritesheet)
            GL.set_player2_spritesheet(self.player2_spritesheet)

        refresh_inputs()
        player_select_inputs()
        player_done_selecting()
        ready_for_start()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EXIT_GAME()
            if 'click' in self.return_button.handleEvent(event):
                self.return_now = True
                GL.NEXT_PAGE = 'start'

# ----------------------------------------------------------------------------
class LevelSelectPage:

    def __init__(self):
        def _setup_display():
            self.return_button = pygbutton.PygButton((0, 550, 300, 50), 'Main Menu')
            self.ready = False

        def _load_images():
            self.bg_image = pygame.image.load('data/level_select_bkg.png')
            self.bg_image2 = pygame.image.load('data/level_select_bkg2.png')
            self.humanLevel = pygame.image.load('data/humanLevel.png')
            self.elfLevel = pygame.image.load('data/vinesLevel.png')
            self.androidLevel = pygame.image.load('data/androidLevel.png')
            self.levels = [self.humanLevel, self.elfLevel, self.androidLevel]
            self.outerX = [19, 444, 874]
            self.innerX = [24, 450, 878]
            self.index = 0

        _setup_display()
        _load_images()

    def __call__(self):
        self.return_now = False
        while not self.return_now:
            self.input()
            self.draw()
            self.events()
            GL.CLOCK.tick(GL.FPS)

    def draw(self):
        GL.SCREEN.blit(self.bg_image, (0, 0))
        outer_highlight = Rect2(topleft=(self.outerX[self.index], 184), size = (389, 173), color=(20, 118, 128))
        inner_highlight = Rect2(topleft=(self.innerX[self.index], 190), size=(379, 162), color=(80, 191, 201))
        pygame.draw.rect(GL.SCREEN, outer_highlight.color, outer_highlight)
        pygame.draw.rect(GL.SCREEN, inner_highlight.color, inner_highlight)
        GL.SCREEN.blit(self.bg_image2, (0, 0))
        self.return_button.draw(GL.SCREEN)
        pygame.display.update()

    # only player 1 can select level
    def input(self):
        GL.INPUT1.refresh()

        if GL.INPUT1.LEFT_PRESS_EVENT:
            GL.INPUT1.LEFT_PRESS_EVENT = False
            self.index -= 1
            if self.index < 0:
                self.index = len(self.levels) - 1

        elif GL.INPUT1.RIGHT_PRESS_EVENT:
            GL.INPUT1.RIGHT_PRESS_EVENT = False
            self.index += 1
            if self.index >= len(self.levels):
                self.index = 0

        elif GL.INPUT1.SELECT_PRESS_EVENT or GL.INPUT1.kb_input['K_s']:
            GL.INPUT1.SELECT_PRESS_EVENT = False
            GL.INPUT1.kb_input['K_s'] = False
            GL.NEXT_PAGE = 'PlayerSelectPage()'
            self.return_now = True

        def ready_check():
            if GL.INPUT1.START_PRESS_EVENT or GL.INPUT1.kb_input['K_a']:
                GL.INPUT1.START_PRESS_EVENT = False
                GL.INPUT1.kb_input['K_a'] = False
                print('ready to load')
                self.ready = True
                set_level()
                GL.NEXT_PAGE = 'GameLoop()'
                self.return_now = True

        def set_level():
            print('setting level')
            if self.index == 0:
                arena = arena4
            elif self.index == 1:
                arena = arena3
            elif self.index == 2:
                arena = arena5

            GL.set_level(arena)
            print('set level')

        ready_check()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EXIT_GAME()
            if 'click' in self.return_button.handleEvent(event):
                self.return_now = True
                GL.NEXT_PAGE = 'start'

# ----------------------------------------------------------------------------
class OptionsPage:
    def __init__(self):
        self.bg_image = pygame.image.load('data/background2.png')
        self.active_colors = BLACK, DKRED
        self.inactive_colors = DKRED, BLACK
        self.music_on_button = pygbutton.PygButton((650, 200, 60, 50), 'ON')
        self.music_off_button = pygbutton.PygButton((730, 200, 80, 50), 'OFF')
        self.effects_on_button = pygbutton.PygButton((650, 260, 60, 50), 'ON')
        self.effects_off_button = pygbutton.PygButton((730, 260, 80, 50), 'OFF')
        self.return_button = pygbutton.PygButton((0, 550, 300, 50), 'Main Menu')
        font = pygame.font.Font('data/Kremlin.ttf', 40)
        self.bg_font = font.render('Music:', True, DKRED)
        self.se_font = font.render('Sound:', True, DKRED)

        main_menu = (0, 550, 300, 50)
        sound_on = (650, 260, 60, 50)
        music_on = (650, 200, 60, 50)
        music_off = (730, 200, 80, 50)
        sound_off = (730, 260, 80, 50)

        self.selection_box_row_properties = [[main_menu, sound_on, music_on], [main_menu, sound_off, music_off]]

        row1_initial = 0 if AUDIO.sound_on else 1
        row2_initial = 0 if AUDIO.music_on else 1

        self.selection_box_col_indices = [0, row1_initial, row2_initial]
        self.selection_box_row = 0

    def __call__(self):
        self.return_now = False
        while not self.return_now:
            self.draw()
            self.input()
            self.events()
            GL.CLOCK.tick(GL.FPS)

    def draw(self):
        if AUDIO.music_on:
            self.music_on_button.fgcolor, self.music_on_button.bgcolor = self.active_colors
            self.music_off_button.fgcolor, self.music_off_button.bgcolor = self.inactive_colors
        else:
            self.music_on_button.fgcolor, self.music_on_button.bgcolor = self.inactive_colors
            self.music_off_button.fgcolor, self.music_off_button.bgcolor = self.active_colors

        if AUDIO.sound_on:
            self.effects_on_button.fgcolor, self.effects_on_button.bgcolor = self.active_colors
            self.effects_off_button.fgcolor, self.effects_off_button.bgcolor = self.inactive_colors
        else:
            self.effects_on_button.fgcolor, self.effects_on_button.bgcolor = self.inactive_colors
            self.effects_off_button.fgcolor, self.effects_off_button.bgcolor = self.active_colors

        GL.SCREEN.blit(self.bg_image, (0, 0))
        GL.SCREEN.blit(self.bg_font, (450, 200))
        GL.SCREEN.blit(self.se_font, (450, 260))
        self.music_on_button.draw(GL.SCREEN)
        self.music_off_button.draw(GL.SCREEN)
        self.effects_on_button.draw(GL.SCREEN)
        self.effects_off_button.draw(GL.SCREEN)

        self.return_button.draw(GL.SCREEN)
        row = self.selection_box_row
        col = self.selection_box_col_indices[row]
        self.selection_box = Rect2(self.selection_box_row_properties[col][row], color=BLUE)
        pygame.draw.rect(GL.SCREEN, self.selection_box.color, self.selection_box, selection_box_width)
        pygame.display.update()

    def input(self):
        GL.INPUT1.refresh()
        if GL.INPUT1.START_PRESS_EVENT:
            GL.INPUT1.START_PRESS_EVENT = False
            if self.selection_box_row == 0:
                self.return_now = True
                GL.NEXT_PAGE = 'start'

        if GL.INPUT1.SELECT_PRESS_EVENT:
            GL.INPUT1.SELECT_PRESS_EVENT = False
            self.return_now = True
            GL.NEXT_PAGE = 'start'

        if GL.INPUT1.B_PRESS_EVENT:
            GL.INPUT1.B_PRESS_EVENT = False
            self.return_now = True
            GL.NEXT_PAGE = 'start'

        if GL.INPUT1.A_PRESS_EVENT:
            GL.INPUT1.A_PRESS_EVENT = False
            if self.selection_box_row == 0:
                self.return_now = True
                GL.NEXT_PAGE = 'start'

        if GL.INPUT1.UP_PRESS_EVENT:
            GL.INPUT1.UP_PRESS_EVENT = False
            self.selection_box_row += 1
            if self.selection_box_row > 2:
                self.selection_box_row = 0

        if GL.INPUT1.DOWN_PRESS_EVENT:
            GL.INPUT1.DOWN_PRESS_EVENT = False
            self.selection_box_row -= 1
            if self.selection_box_row < 0:
                self.selection_box_row = 2

        if GL.INPUT1.LEFT_PRESS_EVENT or GL.INPUT1.RIGHT_PRESS_EVENT:

            if GL.INPUT1.LEFT_PRESS_EVENT:
                GL.INPUT1.LEFT_PRESS_EVENT = False

            if GL.INPUT1.RIGHT_PRESS_EVENT:
                GL.INPUT1.RIGHT_PRESS_EVENT = False

            curr_col = self.selection_box_col_indices[self.selection_box_row]
            new_col = 1 if curr_col == 0 else 0
            self.selection_box_col_indices[self.selection_box_row] = new_col

            if self.selection_box_row == 1:
                if new_col == 0:
                    AUDIO.turn_on_effects()
                elif new_col == 1:
                    AUDIO.turn_off_effects()

            elif self.selection_box_row == 2:
                if new_col == 0:
                    AUDIO.turn_on_music()
                elif new_col == 1:
                    AUDIO.turn_off_music()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EXIT_GAME()

            if 'click' in self.music_on_button.handleEvent(event):
                self.selection_box_row = 2
                self.selection_box_col_indices[self.selection_box_row] = 0
                AUDIO.turn_on_music()

            if 'click' in self.music_off_button.handleEvent(event):
                self.selection_box_row = 2
                self.selection_box_col_indices[self.selection_box_row] = 1
                AUDIO.turn_off_music()

            if 'click' in self.effects_on_button.handleEvent(event):
                self.selection_box_row = 1
                self.selection_box_col_indices[self.selection_box_row] = 0
                AUDIO.turn_on_effects()

            if 'click' in self.effects_off_button.handleEvent(event):
                self.selection_box_row = 1
                self.selection_box_col_indices[self.selection_box_row] = 1
                AUDIO.turn_off_effects()

            if 'click' in self.return_button.handleEvent(event):
                self.selection_box_row = 0
                self.return_now = True
                GL.NEXT_PAGE = 'start'

# ----------------------------------------------------------------------------
class PauseMenu:
    def __init__(self):
        self.menu_box = Rect2(topleft=(320, 120), size=(640, 240), color=BLACK)
        main_font = 'data/Kremlin.ttf'
        pause_font = pygame.font.Font(main_font, 100)
        self.pause_font_xy = font_position_center(self.menu_box, pause_font, '-PAUSE-')
        self.pause_font_rendered = pause_font.render('-PAUSE-', True, RED)

        self.continue_button_properties = (395, 270, 200, 50)
        self.quit_button_properties = (730, 270, 100, 50)

        self.continue_button = pygbutton.PygButton(self.continue_button_properties, 'Continue')
        self.quit_button = pygbutton.PygButton(self.quit_button_properties, 'Quit')
        self.selection_box_properties = [self.continue_button_properties, self.quit_button_properties]
        self.selection_box_i = 0

    def __call__(self):
        self.return_now = False
        while not self.return_now:
            self.draw()
            self.input()
            self.events()
            GL.CLOCK.tick(GL.FPS)

    def draw(self):
        pygame.draw.rect(GL.SCREEN, WHITE, self.menu_box)
        pygame.draw.rect(GL.SCREEN, self.menu_box.color, self.menu_box, 4)
        GL.SCREEN.blit(self.pause_font_rendered, (self.pause_font_xy[0], self.menu_box.top))
        self.continue_button.draw(GL.SCREEN)
        self.quit_button.draw(GL.SCREEN)
        self.selection_box = Rect2(self.selection_box_properties[self.selection_box_i], color=BLUE)
        pygame.draw.rect(GL.SCREEN, self.selection_box.color, self.selection_box, selection_box_width)
        pygame.display.update()

    def input(self):
        GL.INPUT1.refresh_during_pause()
        # if GL.INPUT1.START_PRESS_EVENT:
        #     GL.INPUT1.START_PRESS_EVENT = False
        #     self.return_now = True
        #     GL.NEXT_PAGE = 'GL.CURR_GAME'

        if GL.INPUT1.SELECT_PRESS_EVENT:
            GL.INPUT1.SELECT_PRESS_EVENT = False
            self.return_now = True
            GL.NEXT_PAGE = 'GL.CURR_GAME'

        if GL.INPUT1.START_PRESS_EVENT or GL.INPUT1.A_PRESS_EVENT:

            if GL.INPUT1.START_PRESS_EVENT:
                GL.INPUT1.START_PRESS_EVENT = False

            if GL.INPUT1.A_PRESS_EVENT:
                GL.INPUT1.A_PRESS_EVENT = False

            if self.selection_box_i == 0:
                self.return_now = True
                GL.NEXT_PAGE = 'GL.CURR_GAME'

            if self.selection_box_i == 1:
                self.return_now = True
                GL.NEXT_PAGE = 'start'

        if GL.INPUT1.RIGHT_PRESS_EVENT:
            GL.INPUT1.RIGHT_PRESS_EVENT = False
            self.selection_box_i += 1
            if self.selection_box_i > 1:
                self.selection_box_i = 0

        if GL.INPUT1.LEFT_PRESS_EVENT:
            GL.INPUT1.LEFT_PRESS_EVENT = False
            self.selection_box_i -= 1
            if self.selection_box_i < 0:
                self.selection_box_i = 1

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EXIT_GAME()

            if 'click' in self.continue_button.handleEvent(event):
                self.return_now = True
                GL.NEXT_PAGE = 'GL.CURR_GAME'

            if 'click' in self.quit_button.handleEvent(event):
                self.return_now = True
                GL.NEXT_PAGE = 'start'
