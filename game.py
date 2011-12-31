import pygame, random, sys, time, pygcurse, thread
import inputr, reqs
from pygame.locals import *
from levels import level1, level2
from mapper import Map
from player import Player
from ai import AI
from items import Apple

GREEN = (0, 255, 0)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
ORANGE = (255,140,0)
BLUE = (0,0,255)

THREADS = []
MESSAGES = []
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
p1.map.pathRender()
p1.inv[1] = Apple()
updateRender = True #Update our Screen once

win.fill(bgcolor=BLACK)
win.putchars('Teh Game', 20, 3, fgcolor=WHITE)
win.putchars('[enter]', 21, 4, fgcolor=WHITE)
win.update()
inp.waitFor('enter')
reqs.startup()

def addMessage(msg, color=BLUE): MESSAGES.append((msg,color))

def screenLoop():
	global updateRender
	#p1.map.updateChar((10,10), "8") #This physically changes the map... Not really safe...
	p1.map.modifyChar((10,10), "8") #This puts a place holder onto the map. Much safer...
	updateRender = True	
 
def inventory():
	li = p1.niceInv()
	choice = reqs.selectionScreen(li, 'Inventory:', ORANGE, '[Enter] To select | [R] to dump | [Q] to exit', ORANGE, True)
	if choice[0] != None and choice[1] != None:
		if p1.inv[choice[0]].type == 'food':
			p1.eatObj(p1.inv[choice[0]])
	
def loop():
	global updateRender, FRAME
	global moveUp, moveDown, moveRight, moveLeft
	while True:
		if updateRender is True:
			_x = 0
			r = []
			p1.tick()
			updateRender = False
			render = p1.map.newNewRender()
			win.fill(bgcolor=BLACK)
			for line in render:
				_x+=1
				win.putchars(line, 1, _x, fgcolor=RED)
			for bot in p1.ai:
				if bot.alive is True and bot.map == p1.map.id:
					win.putchar(bot.char, bot.pos[0], bot.pos[1], fgcolor=bot.color)
			if p1.display is True: win.putchar(p1.char, p1.pos[0], p1.pos[1], fgcolor=GREEN)
			_x+=1
			win.putchars('Health', 1, _x, fgcolor=BLUE)
			win.putchars('%s' % (p1.niceHealth()), 7, _x, fgcolor=RED)
			for i in MESSAGES:
				_x+=1
				r = True
				win.putchars(i[0], 1, _x, fgcolor=i[1])
				win.putchars('[enter]', len(i[0])+2, _x, fgcolor=ORANGE)
				MESSAGES.remove(i)
			win.putchars('Pos: %s | Frame: %s' % (p1.pos, FRAME), 1, _x+2, fgcolor=ORANGE)
			win.update()
			if r is True: inp.waitFor('enter', 1)
			FRAME += 1
		inp.retrieve()
		if inp.value != ([], []):
			if 'q' in inp.value[0]: sys.exit()
			if 'w' in inp.value[0] and p1.moveUp() is True: updateRender = True					
			if 'a' in inp.value[0] and p1.moveLeft() is True: updateRender = True
			if 's' in inp.value[0] and p1.moveDown() is True: updateRender = True
			if 'd' in inp.value[0] and p1.moveRight() is True: updateRender = True
			if 'x' in inp.value[0]: THREADS.append(thread.start_new_thread(screenLoop, ()))
			if 'i' in inp.value[0]: inventory()
			
		if p1.ai != None and p1.ai != []:
			for i in p1.ai:
				if i.map == p1.map.id:
					if i.move() is True:
						updateRender = True
								
		time.sleep(.01)

loop()