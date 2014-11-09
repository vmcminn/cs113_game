import pygame

from colors import *
from globals import *

from pygame.locals import *
# -------------------------------------------------------------------------


class Rect2(pygame.Rect):
    def __init__(self, *args, **kargs):
        if args != tuple():
            if all_isinstance(args, tuple) and len(args) is 2:
                super().__init__(args[0], args[1])

            if all_isinstance(args, tuple) and len(args) is 1:
                super().__init__(args[0][0], args[0][1], args[0][2], args[0][3])

            elif all_isinstance(args, int):
                super().__init__(args[0], args[1], args[2], args[3])
        else:
            if all_in('top,left,width,height'.split(','), kargs.keys()):
                super().__init__(kargs['left'], kargs['top'], kargs['width'], kargs['height'])

            elif all_in(('topleft', 'size'), kargs):
                super().__init__(kargs['topleft'], kargs['size'])
# -------------------------------------------------------------------------


class Player(Rect2):
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
        super().move_ip(dxdy)

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

    def _handle_movement(self, arena):
        self.move_ip((self.dx, self.dy))
        for terrain in arena.rects:

            if (terrain.top < self.bottom < terrain.bottom) or (terrain.bottom > self.top > terrain.top):
                if (self.left < terrain.right) and (self.right > terrain.right):
                    self.left = terrain.right
                elif (self.left < terrain.left) and (self.right > terrain.left):
                    self.right = terrain.left

            if (terrain.right > self.left > terrain.left) or (terrain.left < self.right < terrain.right):
                if (self.bottom > terrain.bottom) and (self.top < terrain.bottom):
                    self.top = terrain.bottom
                elif (self.bottom > terrain.top) and (self.top < terrain.top):
                    self.bottom = terrain.top
# -------------------------------------------------------------------------


class Input:
    def __init__(self):
        try:
            self.gamepad = pygame.joystick.Joystick(0)
            self.gamepad.init()
            self.gamepad_found = True
        except pygame.error:
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

        elif name == JUMP:
            return self.kb_input[K_SPACE] or self.a_button

        elif name == RESET:
            return self.kb_input[K_r] or self.y_button

        elif name == DEBUG:
            return self.kb_input[K_F12] or (self.start_button and self.back_button)

        elif name == EXIT:
            return self.kb_input[K_q] or self.kb_input[K_ESCAPE] or self.back_button

        else:
            return None
# -------------------------------------------------------------------------


class Arena:
    def __init__(self, *color_rects):
        self.rects = [Rect2(rect) for rect, color in color_rects]

        self.colors = [color for rect, color in color_rects]
        self.play_area_rect = self.rects[0]
        self.play_area_color = self.colors[0]
        self.rects = self.rects[1:]
        self.colors = self.colors[1:]

    # currently only iterate through to draw the rects
    def __iter__(self):
        for rect, rect_color in zip([self.play_area_rect] + self.rects, [self.play_area_color] + self.colors):
            yield rect, rect_color

arena1 = Arena(
    ((65, 0, 1150, 475), SKYBLUE),  # play_area (must be first)
    ((0, 475, 1280, 50), None),
    ((15, 0, 50, 600), None),
    ((1215, 0, 50, 600), None),
    ((65, 270, 300, 60), DKGREEN),
    ((915, 270, 300, 60), DKGREEN),
    ((610, 150, 60, 230), DKGREEN),
    ((205, 100, 150, 20), DKGREEN),
    ((925, 100, 150, 20), DKGREEN),
)