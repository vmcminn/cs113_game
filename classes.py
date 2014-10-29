import pygame

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
