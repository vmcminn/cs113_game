import pygame

from globals import *

from pygame.locals import *


class Player(pygame.Rect):

    def __init__(self, left, top, width, height, speed):
        pygame.Rect.__init__(self, left, top, width, height)
        self.initial_topleft = self.topleft
        self.speed = speed
        self.health = 100

    def copy(self):
        return Player(self.left, self.top, self.width, self.height, self.speed)

    def move_ip(self, direction):
        di = {LEFT: (-self.speed, 0), RIGHT: (+self.speed, 0),
              UP: (0, -self.speed), DOWN: (0, +self.speed), }
        if direction in di.keys():
            pygame.Rect.move_ip(self, di[direction])


class Input:

    def __init__(self):
        try:
            self.gamepad = pygame.joystick.Joystick(0)
            self.gamepad.init()
            self.gamepad_found = True
        except Exception:
            self.gamepad_found = False

    def refresh(self):
        def _get_gamepad_input():
            if self.gamepad_found:
                self.left_right_axis = round(self.gamepad.get_axis(0))
                self.up_down_axis = round(self.gamepad.get_axis(1))
                self.a_button = self.gamepad.get_button(1)
                self.y_button = self.gamepad.get_button(3)
                self.start_button = self.gamepad.get_button(9)
                self.back_button = self.gamepad.get_button(8)

        def _get_keyboard_input():
            self.kb_input = pygame.key.get_pressed()

        _get_gamepad_input()
        _get_keyboard_input()

    def __getattr__(self, name):
        if name == LEFT:
            return self.kb_input[K_LEFT] or self.left_right_axis == -1

        elif name == RIGHT:
            return self.kb_input[K_RIGHT] or self.left_right_axis == +1

        elif name == UP:
            return self.kb_input[K_UP] or self.up_down_axis == -1

        elif name == DOWN:
            return self.kb_input[K_DOWN] or self.up_down_axis == +1

        elif name == RESET:
            return self.kb_input[K_r] or self.a_button

        elif name == DEBUG:
            return self.kb_input[K_SPACE] or self.start_button

        elif name == EXIT:
            return self.kb_input[K_q] or self.back_button

        else:
            return None
