import os, sys  # some standard libraries we will need
import pygame
from colors 		import *  # adds everything from colors.py into local namespace
from pygame.locals  import *  # adds some commonly used pygame objects into local namespace 

if os.environ['COMPUTERNAME'] == 'BRIAN-DESKTOP':
	os.environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(1920, 150)
#  ^ Sets window starting position for my desktop which has multiple monitors, this is a convenience 
#  thing for me.  You guys can add your own setting here if it's useful for you.


#-------------------------------------------------------------------------------
class GameLoop:
	def __init__(self):
		def _setup():
			pygame.init()
			pygame.display.set_mode((1280, 600))  
			# ^ Sets the window size - can add the NOFRAME arg if we don't want a window frame
			# but then we have to figure out how to move the window since it won't have a menu
			# bar to grab
			pygame.display.set_caption('Team Bears!')
			pygame.key.set_repeat(500, 100)  # allows multiple KEYDOWN events

		_setup()
		self.surface 		= pygame.display.get_surface()
		self.border_rect 	= Rect((0, 0), (1280, 600))
		self.small_rect		= Rect((0, 0), (50, 50))
		self.gamepad 		= pygame.joystick.Joystick(0)
		self.gamepad.init()


	#-------------------------------------------------------------------------------
	def __call__(self):
		while True:		
			self.surface.fill(DGREY)  
			# ^ fills background dark grey
			pygame.draw.rect(self.surface, GREEN, self.border_rect, 1)
			# ^ creates a thin green rectangle border of surface
			pygame.draw.rect(self.surface, LBLUE, self.small_rect)
			
			self.handle_quit()
			self.handle_keys()
			self.handle_gamepad()

			pygame.display.update()				# necessary to update the display
			pygame.time.delay(50)				# pause for 50 milliseconds


	#-------------------------------------------------------------------------------
	def handle_quit(self):
		for event in pygame.event.get():	# loop through all pygame events
			if event.type == QUIT:  		# QUIT event occurs when click X on window bar
				pygame.quit()
				sys.exit()


	def handle_keys(self):
		keys_pressed = pygame.key.get_pressed()
		# ^ gets the state of all keyboard buttons - True means it is pressed down
		if keys_pressed[K_LEFT]:	self.small_rect = self.small_rect.move((-3, 0))
		if keys_pressed[K_RIGHT]:	self.small_rect = self.small_rect.move((+3, 0))
		if keys_pressed[K_UP]:		self.small_rect = self.small_rect.move(( 0,-3))
		if keys_pressed[K_DOWN]:	self.small_rect = self.small_rect.move(( 0,+3))

	def handle_gamepad(self):
		axis_0 = round(self.gamepad.get_axis(0))
		axis_1 = round(self.gamepad.get_axis(1))
		button_a = self.gamepad.get_button(1)
		
		if axis_0 == -1:	self.small_rect = self.small_rect.move((-3, 0))
		if axis_0 == +1:	self.small_rect = self.small_rect.move((+3, 0))
		
		if axis_1 == -1:	self.small_rect = self.small_rect.move(( 0,-3))
		if axis_1 == +1:	self.small_rect = self.small_rect.move(( 0,+3))

		if button_a:	self.small_rect = Rect((0, 0), (50, 50))

		# print('axis_0:{}  axis_1:{}  button_a:{}'.format(axis_0, axis_1, button_a))


#-------------------------------------------------------------------------------
if __name__ == '__main__':
	GameLoop()()
