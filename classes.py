import pygame

from colors import *
from globals import *

from pygame.locals import *


class Player(pygame.Rect):
    def __init__(self, left, top, width, height):
        super().__init__(left, top, width, height)
        self.topleft_initial = self.topleft
        self.speed = 5
        self.facing_direction = RIGHT
        self.hit_points = 100
        self.hit_points_max = 100

    def copy(self):
        return Player(self.left, self.top, self.width, self.height)

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
            return self.kb_input[K_F12] or self.start_button

        elif name == EXIT:
            return self.kb_input[K_q] or self.kb_input[K_ESCAPE] or self.back_button

        else:
            return None


class Arena:
    def __init__(self, *color_rects):
        self.rects = [pygame.Rect(rect) for rect, color in color_rects]
        self.colors = [color for rect, color in color_rects]
        self.play_area_rect = self.rects[0]

    def __iter__(self):
        for rect, rect_color in zip(self.rects, self.colors):
            yield rect, rect_color

arena1 = Arena(
    ((65, 0, 1150, 475), SKYBLUE),
    ((65, 270, 300, 60), DKGREEN),
    ((915, 270, 300, 60), DKGREEN),
    ((610, 150, 60, 230), DKGREEN),
    ((205, 100, 150, 20), DKGREEN),
    ((925, 100, 150, 20), DKGREEN),
)
