import pygame

from colors import *
from globals import *

from pygame.locals import *


class Player(pygame.Rect):
    def __init__(self, left, top, width, height):
        super().__init__(left, top, width, height)
        self.topleft_initial = self.topleft

        self.dx, self.dy = 0, 4
        self.dx_max, self.dy_max = 15, 15

        self.dx_increase = 2  # when pushing down button
        self.dx_decrease = 0.5  # always.  this is basically friction

        self.dy_increase = 35  # when jump
        self.dy_decrease = 4  # always.  this is basically gravity

        self.facing_direction = RIGHT
        self.hit_points = 100
        self.hit_points_max = 100

    def copy(self):
        return Player(self.left, self.top, self.width, self.height)

    def move_ip(self, dxdy):
        pygame.Rect.move_ip(self, dxdy)

    def __call__(self, input, arena_map):
        self._handle_acceleration(input)
        self._handle_movement(arena_map)

    def _handle_acceleration(self, input):

        def _apply_accel_left_right_input(input):
            if input.LEFT:
                self.dx -= self.dx_increase
            elif input.RIGHT:
                self.dx += self.dx_increase

        def _apply_decel_friction():
            if self.dx > 0:
                self.dx -= self.dx_decrease
            elif self.dx < 0:
                self.dx += self.dx_decrease

        def _apply_accel_jump_input(input):
            if input.JUMP:
                self.dy -= self.dy_increase

        def _apply_decel_gravity():
            self.dy += self.dy_decrease

        def _apply_limits():
            self.dx = eval('{:+}'.format(self.dx)[0] + str(min(abs(self.dx), self.dx_max)))
            self.dy = eval('{:+}'.format(self.dy)[0] + str(min(abs(self.dy), self.dy_max)))

        _apply_accel_left_right_input(input)
        _apply_decel_friction()
        _apply_accel_jump_input(input)
        _apply_decel_gravity()
        _apply_limits()

    def _handle_movement(self, arena_map):

        def _move_is_legal(dxdy):
            # 1 - create a copy of player
            copy = self.copy()
            # 2 - move the copy
            copy.move_ip(dxdy)
            # 3 - test if copy is fully contained within the playable area Rect
            not_out_of_bounds = arena_map.play_area_rect.contains(copy)
            # 4 - test if copy is not overlapping any terrain Rect's
            not_inside_terrain = copy.collidelist(arena_map.rects[1:]) == -1
            return not_out_of_bounds == not_inside_terrain is True

        if _move_is_legal((self.dx, 0)):
            self.move_ip((self.dx, 0))
        else:
            self.dx = 0

        if _move_is_legal((0, self.dy)):
            self.move_ip((0, self.dy))
        else:
            self.dy = 0


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
