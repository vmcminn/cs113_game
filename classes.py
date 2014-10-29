import pygame
from pygame.locals import *


class Player(pygame.Rect):

    def __init__(self, *args, **kargs):
        try:
            pygame.Rect.__init__(self, args)
        except TypeError:
            pygame.Rect.__init__(self, kargs['left'], kargs['top'], kargs['width'], kargs['height'])
            kargs.pop('left')
            kargs.pop('top')
            kargs.pop('width')
            kargs.pop('height')

        for k, v in kargs.items():
            exec('self.{} = {}'.format(k, repr(v)))


class Input:

    def __init__(self):
        try:
            self.gamepad = pygame.joystick.Joystick(0)
            self.gamepad.init()
            self.gamepad_found = True
        except Exception:
            self.gamepad_found = False

    def _get_gamepad_input(self):
        if self.gamepad_found:
            self.left_right_axis = round(self.gamepad.get_axis(0))
            self.up_down_axis = round(self.gamepad.get_axis(1))
            self.button_a = self.gamepad.get_button(1)
        else:
            self.left_right_axis = 0
            self.up_down_axis = 0
            self.button_a = False

    def _get_keyboard_input(self):
        self.kb_input = pygame.key.get_pressed()

    def refresh(self):
        self._get_gamepad_input()
        self._get_keyboard_input()

    def __getattr__(self, name):

        if name == 'left':
            return self.kb_input[K_LEFT] or self.left_right_axis == -1

        elif name == 'right':
            return self.kb_input[K_RIGHT] or self.left_right_axis == +1

        elif name == 'up':
            return self.kb_input[K_UP] or self.up_down_axis == -1

        elif name == 'down':
            return self.kb_input[K_DOWN] or self.up_down_axis == +1

        elif name in ('space', 'debug'):
            return self.kb_input[K_SPACE]

        elif name in ('q', 'quit'):
            return self.kb_input[K_q]
