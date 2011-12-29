import pygame, random, sys, time, pygcurse, thread
import inputr
from pygame.locals import *
from levels import level1, level2
from mapper import Map
from player import Player
from ai import AI

GREEN = (0, 255, 0)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
ORANGE = (255,140,0)
BLUE = (0,0,255)

THREADS = []
WINWIDTH = 50
WINHEIGHT = 25
TEXTCOLOR = WHITE
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 5
FRAME = 0

moveUp = False
moveDown = False
moveRight = False
moveLeft = False

win = pygcurse.PygcurseWindow(WINWIDTH, WINHEIGHT, fullscreen=False)
win.autoupdate = False
pygame.display.set_caption('So I made this game...')
inp = inputr.KeyboardInput()

p1 = Player('Joe', '@')
p1.levels = {
	'1': Map(1, level1.nice, level1.info, p1).genHitMap(),
	'2': Map(2, level2.nice, level2.info, p1).genHitMap()
}
p1.selectMap(1)
p1.ai = [AI('Joe', p1, color=BLUE, Map=1).spawn()]

updateRender = True #Update our Screen once

win.fill(bgcolor=BLACK)
win.putchars('Teh Game', 20, 3, fgcolor=WHITE)
win.putchars('[enter]', 21, 4, fgcolor=WHITE)
win.update()
inp.waitFor('enter')

def screenLoop():
	global updateRender
	#p1.map.updateChar((10,10), "8") #This physically changes the map... Not really safe...
	p1.map.modifyChar((10,10), "8") #This puts a place holder onto the map. Much safer...
	updateRender = True	

def loop():
	global updateRender, FRAME
	global moveUp, moveDown, moveRight, moveLeft
	while True:
		
		win.fill(bgcolor=BLACK)
		_x = 0
		if updateRender is True:
			updateRender = False
			render = p1.map.newNewRender()
			for line in render:
				_x+=1
				win.putchars(line, 1, _x, fgcolor=RED)
				win.putchar(p1.char, p1.pos[0], p1.pos[1], fgcolor=GREEN)
				for bot in p1.ai:
					if bot.alive is True and bot.map == p1.map.id:
						win.putchar(bot.char, bot.pos[0], bot.pos[1], fgcolor=bot.color)
			win.putchars('Pos: %s | Frame: %s' % (p1.pos, FRAME), 1, _x+2, fgcolor=ORANGE)
			win.update()
			if FRAME >= 1000000:
				print 'Reseting frame count; it\'s way too high!'
				FRAME = 0
			else:
				FRAME += 1
		inp.retrieve()
		if inp.value != ([], []):
			if 'q' in inp.value[0]: sys.exit()
			if 'w' in inp.value[0]: 
				if p1.moveUp() is True:
					updateRender = True
			if 'a' in inp.value[0]: 
				if p1.moveLeft() is True:
					updateRender = True
			if 's' in inp.value[0]: 
				if p1.moveDown() is True:
					updateRender = True
			if 'd' in inp.value[0]: 
				if p1.moveRight() is True:
					updateRender = True
			if 'x' in inp.value[0]: 
				THREADS.append(thread.start_new_thread(screenLoop, ()))
			
		if p1.ai != None and p1.ai != []:
			for i in p1.ai:
				if i.map == p1.map.id:
					if i.move() is True:
						updateRender = True
								
		time.sleep(.01)

loop()