#COLOR = (RRR, GGG, BBB)

BLACK = (0, 0, 0)
DGREY = (64, 64, 64)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
DKRED = (128, 0, 0)
DKGREEN = (0, 128, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LBLUE = (0, 128, 255)
SKYBLUE = (128, 223, 223)

YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
ORANGE = (255, 153, 0)

LEFT = 'LEFT'
RIGHT = 'RIGHT'
UP = 'UP'
DOWN = 'DOWN'
JUMP = 'JUMP'
ATTACK = 'ATTACK'
DEBUG = 'DEBUG'
EXIT = 'EXIT'
RESET = 'RESET'


def all_in(items_want_inside, container_being_checked):
    for thingy in items_want_inside:
        if thingy not in container_being_checked:
            return False
    return True


def all_isinstance(items_checking, instance_wanted):
    for thingy in items_checking:
        if isinstance(thingy, instance_wanted) is False:
            return False
    return True


def font_position_center(center_within_size, font, text):
    x = (center_within_size[0] - font.size(text)[0]) // 2
    y = (center_within_size[1] - font.size(text)[1]) // 2
    return x, y