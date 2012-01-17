import pygame, random, sys, os, time, pygcurse, thread
import inputr, reqs
from pygame.locals import *
from levels import level1, level2, level0
from mapper import Map
from player import Player
from ai import AI
from items import Apple, BadApple
from colors import GREEN, BLACK, WHITE, RED, ORANGE, BLUE, health

THREADS = []
MESSAGES = []
WINWIDTH = 50
WINHEIGHT = 25
TEXTCOLOR = WHITE
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 5
FRAME = 0
LASTRENDER = 0
OLDHASH = None

win = pygcurse.PygcurseWindow(WINWIDTH, WINHEIGHT, fullscreen=False)
win.autoupdate = False
pygame.display.set_caption('So I made this game...')
inp = inputr.KeyboardInput()

p1 = Player('Joe', '@')
p1.levels = {
	'0': Map(0, level0.nice, level0.info, p1).genHitMap(),
	'1': Map(1, level1.nice, level1.info, p1).genHitMap(),
	'2': Map(2, level2.nice, level2.info, p1).genHitMap()
}
p1.selectMap(0)
p1.ai = []#[AI('Joe', p1, color=BLUE, Map=1).spawn()]
p1.map.pathRender()
p1.inv[1] = BadApple()

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
	render()
 
def inventory():
	li = p1.niceInv()
	choice = reqs.selectionScreen(li, 'Inventory:', ORANGE, '[Enter] to select | [R] to dump | [Q] to exit', ORANGE, True)
	if choice[0] != None and choice[1] != None:
		if p1.inv[choice[0]].type == 'food':
			p1.eatObj(p1.inv[choice[0]])
	render()

def findSaves(home=os.getcwd()):
    """Find save files, and return a list of them"""
    fn = []
    try:
        for i in os.listdir(os.path.join(home, 'saves')):
            if i.endswith('.dat') and not i.startswith("_"):
                fn.append(os.path.join(home, 'saves', i))
        return fn
    except:
        os.mkdir(os.path.join(home, 'saves'))
        return findSaves()

def init():
	win.fill(bgcolor=BLACK)
	saves = findSaves()
	if len(saves) is 0:
		win.putchars('No save files found! Press [enter] to create new game...', 1, 1)
		win.update()
		inp.waitFor('enter', 1)
		reqs.ask('Name')
	else:
		nicelist = {}
		y = 0
		for i in saves:
			y+=1
			nicelist[y] = i.split('/')[-1:][0]
		nicelist[y+1] = '[New]'
		print reqs.selectionScreen(nicelist, 'Save Files:', ORANGE, '[Enter] to select | [R] to dump | [Q] to exit', ORANGE, True)
	
def render():
	global updateRender, FRAME
	_x = 0
	r = False
	p1.tick()
	updateRender = False
	render = p1.map.newNewRender()
	win.fill(bgcolor=BLACK)
	for line in render: #Render the main screen
		_x+=1
		win.putchars(line, 1, _x, fgcolor=RED)
	for line in p1.map.colorModify.values(): #Render any itmes in colorModify
		for item in line:
			char = p1.map.niceMap[item[1][1]-1][item[1][0]-1]
			win.putchar(char, item[1][0], item[1][1], fgcolor=item[0])
	if len(p1.ai) >=1:
		for bot in p1.ai:
			if bot.alive is True and bot.map == p1.map.id:
				win.putchar(bot.char, bot.pos[0], bot.pos[1], fgcolor=bot.color)
	if p1.display is True: win.putchar(p1.char, p1.pos[0], p1.pos[1], fgcolor=GREEN)
	sat = p1.getStatus()
	hel = p1.niceHealth()
	_x+=1
	win.putchars('Health: [', 1, _x, fgcolor=BLUE)
	win.putchars('%s' % (hel), 10, _x, fgcolor=sat[1])
	win.putchars('] (', len(hel)+10, _x, fgcolor=BLUE)
	win.putchars('%s' % p1.health[0], len(hel)+13, _x, fgcolor=sat[1])
	win.putchars(')', len(hel)+13+len(str(p1.health[0])), _x, fgcolor=BLUE)
	if p1.health[0] < 20 or p1.poisoned[0] is True:
		_x+=1
		win.putchars('Status: ', 1, _x, fgcolor=BLUE)
		win.putchars('%s' % (sat[0]), 9, _x, fgcolor=sat[1])
	if len(MESSAGES) >= 1:
		for i in MESSAGES:
			_x+=1
			r = True
			win.putchars(i[0], 1, _x, fgcolor=i[1])
			win.putchars('[enter]', len(i[0])+2, _x, fgcolor=ORANGE)
			MESSAGES.remove(i)
	win.putchars('Pos: %s | Frame: %s' % (p1.pos, FRAME), 1, _x+1, fgcolor=ORANGE)
	win.update()
	if r is True: inp.waitFor('enter', 1)
	FRAME += 1

def loop():
	global updateRender, FRAME, lastFrame, LASTRENDER, OLDHASH
	while True:
		if updateRender is True: render()
		inp.retrieve()
		if inp.value != ([], []):
			if 'q' in inp.value[0]: sys.exit()
			if 'w' in inp.value[0] and p1.moveUp() is True: updateRender = True					
			if 'a' in inp.value[0] and p1.moveLeft() is True: updateRender = True
			if 's' in inp.value[0] and p1.moveDown() is True: updateRender = True
			if 'd' in inp.value[0] and p1.moveRight() is True: updateRender = True
			if 'x' in inp.value[0]: p1.unheal(1) #various tests go here
			if 'i' in inp.value[0]: inventory()
			
		if time.time() - LASTRENDER >= 1:
			LASTRENDER = time.time()
			p1.tick()

		if p1.hash() != OLDHASH: #Check to see if we should update the render
			OLDHASH = p1.hash()
			updateRender = True

		if p1.ai != None and p1.ai != []:
			for i in p1.ai:
				if i.map == p1.map.id:
					if i.move() is True:
						updateRender = True
								
		time.sleep(.01)
init()
render()
loop()