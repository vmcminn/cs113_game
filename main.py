import os, sys  # some standard libraries we will need
import pygame
from colors 		import *  # adds all from colors.py into local namespace
from pygame.locals  import *  # adds some commonly used pygame objects into local namespace 

if os.environ['COMPUTERNAME'] == 'BRIAN-DESKTOP':
	os.environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(1920, 150)
#  Sets window starting position for my desktop which has multiple monitors, this is a convenience 
#  thing for me.  You guys can add your own setting here if it's useful for you.


#-------------------------------------------------------------------------------
class GameLoop:
	def __init__(self):
		pygame.init()
		pygame.display.set_mode((1280, 600))  
		# Sets the window size - can add the NOFRAME arg if we don't want a window frame
		# but then we have to figure out how to move the window since it won't have a menu
		# bar to grab
		pygame.display.set_caption('Team Bears!')

		surface 	= pygame.display.get_surface()
		border_rect = Rect((0, 0), (1280, 600))

		while True:		
			surface.fill(DGREY)  
			# fills background dark grey
			
			pygame.draw.rect(surface, GREEN, border_rect, 1)  
			# creates a thin green rectangle border of surface
			
			self.handle_events()

			pygame.display.update()  			# necessary to update the display
			pygame.time.delay(50)  				# pause for 50 milliseconds

	def handle_events(self):
		for event in pygame.event.get():	# loop through all pygame events
			if event.type == QUIT:  		# QUIT event occurs when click X on window bar
				pygame.quit()
				sys.exit()

#-------------------------------------------------------------------------------
if __name__ == '__main__':
	GameLoop()
