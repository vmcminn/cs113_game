LEFT = 'LEFT'
RIGHT = 'RIGHT'
UP = 'UP'
DOWN = 'DOWN'
JUMP = 'JUMP'

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
