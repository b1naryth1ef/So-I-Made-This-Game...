import pygame
from pygame.locals import *
import sys, time


keymap = {
	K_RETURN: 'enter',
	K_DOWN: 'down',
	K_UP: 'up',
	K_LEFT: 'left',
	K_RIGHT: 'right',
	K_PAGEDOWN: 'pgdn',
	K_PAGEUP: 'pgup',
	K_q: 'q',
	K_w: 'w',
	K_a: 'a',
	K_s: 's',
	K_d: 'd',
	K_x: 'x'
}

class KeyboardInput(object):
	def __init__(self):
		pass
	def retrieve(self):
		keys_pressed = []
		keys_released = []
		other = []
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key in keymap:
					keys_pressed.append(keymap[event.key])
			elif event.type == pygame.KEYUP:
				if event.key in keymap:
					keys_released.append(keymap[event.key])
			elif event.type == pygame.QUIT:
				sys.exit() #Eventually we need to watch on this, and save shit before quitting
		self.value = (keys_pressed, keys_released)
		return self.value

	def waitFor(self, value, Type=0):
		if value in keymap.values():
			while True:
				time.sleep(.03)
				self.retrieve()
				if self.value != ([], []):
					if Type == 0:
						if value in self.value[0] or value in self.value[1]: return True
					elif Type == 1:
						if value in self.value[0]: return True
					elif Type == 2:
						if value in self.value[1]: return True
