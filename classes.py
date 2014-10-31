import pygame
from pygame.locals import *


class Player(pygame.Rect):

    def __init__(self, left, top, width, height):
        pygame.Rect.__init__(self, left, top, width, height)
        self.initial_topleft = self.topleft


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
        if name == 'left':
            return self.kb_input[K_LEFT] or self.left_right_axis == -1

        elif name == 'right':
            return self.kb_input[K_RIGHT] or self.left_right_axis == +1

        elif name == 'up':
            return self.kb_input[K_UP] or self.up_down_axis == -1

        elif name == 'down':
            return self.kb_input[K_DOWN] or self.up_down_axis == +1

        elif name == 'reset':
            return self.kb_input[K_r] or self.a_button

        elif name in ('space', 'debug'):
            return self.kb_input[K_SPACE] or self.start_button

        elif name in ('q', 'quit'):
            return self.kb_input[K_q] or self.back_button

        else:
            return None
