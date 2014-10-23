import os
import sys  # some standard libraries we will need
import pygame

# add everything from colors.py into local namespace
from colors import *

# add some commonly used pygame objects into local namespace
from pygame.locals import *

# set window starting position for my desktop which has multiple monitors, this
# is a convenience thing for me.  You guys can add your own setting here if
# it's useful for you

if os.environ['COMPUTERNAME'] == 'BRIAN-DESKTOP':
    os.environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(1920, 150)
# -------------------------------------------------------------------------


class GameLoop:

    def __init__(self):
        def _setup():
            pygame.init()

            # Set the window size - can add the NOFRAME arg if we don't want a
            # window frame but then we have to figure out how to move the
            # window since it won't have a menu bar to grab
            pygame.display.set_mode((1280, 600))

            pygame.display.set_caption('Team Bears!')
            pygame.key.set_repeat(500, 100)  # allow multiple KEYDOWN events

        _setup()

        self.surface = pygame.display.get_surface()

        self.window_border = Rect((0, 0), (1280, 600))
        self.play_area = Rect((65, 0), (1150, 475))
        self.play_area_border = Rect((40, 0), (1200, 500))
        self.player = Rect((200, 300), (50, 50))

        try:
            self.gamepad = pygame.joystick.Joystick(0)
            self.gamepad.init()
            self.gamepad_found = True
        except Exception:
            self.gamepad_found = False

    # ------------------------------------------------------------------------
    def __call__(self):
        while True:
            # fill background dark grey
            self.surface.fill(DGREY)

            # red border of playable movement space
            pygame.draw.rect(self.surface, DKRED, self.play_area_border)

            # playable movement space
            pygame.draw.rect(self.surface, SKYBLUE, self.play_area)

            # creates a thin green rectangle border of surface
            pygame.draw.rect(self.surface, GREEN, self.window_border, 1)

            # placeholder for a playable character; is movable
            pygame.draw.rect(self.surface, LBLUE, self.player)

            self.handle_quit()
            self.handle_keys()
            if self.gamepad_found:
                self.handle_gamepad()

            pygame.display.update()  # necessary to update the display
            pygame.time.delay(50)  # pause for 50 milliseconds

    # -------------------------------------------------------------------------
    def handle_quit(self):
        for event in pygame.event.get():  # loop through all pygame events
            # QUIT event occurs when click X on window bar
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def handle_keys(self):
        # get state of all keyboard buttons - True means key is pressed down
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[K_LEFT]:
            self.player = self.player.move((-3, 0))
        if keys_pressed[K_RIGHT]:
            self.player = self.player.move((+3, 0))
        if keys_pressed[K_UP]:
            self.player = self.player.move((0, -3))
        if keys_pressed[K_DOWN]:
            self.player = self.player.move((0, +3))

    def handle_gamepad(self):
        axis_0 = round(self.gamepad.get_axis(0))
        axis_1 = round(self.gamepad.get_axis(1))
        button_a = self.gamepad.get_button(1)

        if axis_0 == -1:
            self.player = self.player.move((-3, 0))  # left
        if axis_0 == +1:
            self.player = self.player.move((+3, 0))  # right

        if axis_1 == -1:
            self.player = self.player.move((0, -3))  # up
        if axis_1 == +1:
            self.player = self.player.move((0, +3))  # down

        if button_a:
            self.player = Rect((0, 0), (50, 50))  # reset


# -------------------------------------------------------------------------
if __name__ == '__main__':
    GameLoop()()
