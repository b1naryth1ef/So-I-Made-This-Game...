import pygame, sys, os, pickle, time, pygcurse
import inputr, reqs
from pygame.locals import *
from levels import level1, level2, level0
from mapper import Map
from player import Player
from items import Projectile
from ai import AI
from items import Apple, BadApple, WoodSword
from colors import GREEN, BLACK, WHITE, RED, ORANGE, BLUE, health

EVENTS = {}
TICKS = {}
ENTITIES = {}
BAD_ENTITIES = {}
MESSAGES = []
WINWIDTH = 50 #@DEV Change for beta!
WINHEIGHT = 25 #@DEV Change for beta!
GETNEWREND = False
RENDER_FAIL = True
FRAME = 0
LASTRENDER = 0
LASTFRAME = 0
OLDHASH = None
MODIFY = 0
THROTTLE = .03 #Lower = worse performance

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
p1.selectMap(1)
p1.ai = [AI('Mr. Starting Bot', p1, color=BLUE, Map=1).spawn()]
p1.inv.addItem(BadApple())
p1.inv.addItem(WoodSword())

win.fill(bgcolor=BLACK)
win.putchars('Teh Game', 20, 3, fgcolor=WHITE)
win.putchars('[enter]', 21, 4, fgcolor=WHITE, update=True)
#win.update()
inp.waitFor('enter')
reqs.startup()

def addEntity(entity, li):
	global ENTITIES
	if li == -1: li = BAD_ENTITIES
	elif li == 1: li = ENTITIES
	if len(li.keys()) == 0: v = [0]
	else: v = li.keys()
	p = max(v)+1
	li[p] = entity
	return p

def removeEntity(sli, li):
	if li == 0: li = [BAD_ENTITIES, ENTITIES]
	elif li == 1: li = [ENTITIES]
	elif li == -1: li = [BAD_ENTITIES]
	for i in li: i.pop(sli)

def moveEntity(sli, from_li):
	if from_li == 1: li = ENTITIES
	elif from_li == -1: li = BAD_ENTITIES
	ent = li[sli]
	del li[sli]
	return addEntity(ent, from_li*-1)

def addMessage(msg, color=BLUE): MESSAGES.append((msg,color))

def addEvent(callback, duration): EVENTS[time.time()+duration] = callback #@DEV fix case where two events are made at the same time

def screenLoop():
	global updateRender
	#p1.map.updateChar((10,10), "8") #This physically changes the map... Not really safe...
	p1.map.modifyChar((10,10), "8") #This puts a place holder onto the map. Much safer...
	render()

def findSaves(home=os.getcwd()):
	print 'heyaaa!'
	if not os.path.exists(os.path.join(home, 'save_dir')):
		os.mkdir(os.path.join(home, 'save_dir'))
	if os.path.exists(os.path.join(home, 'save_dir', 'save_file.dat')): 
		return True
	else:
		return False

def loadSave():
	global p1, ENTITIES, TICKS
	with open(os.path.join(os.getcwd(), 'save_dir', 'save_file.dat'), 'r') as f:
		save = pickle.load(f)
		p1 = save['p1']
		TICKS = save['ticks']
		ENTITIES = save['ents']
		#print p1.ai[0].alive

def init(makeSave=False):
	global p1
	win.fill(bgcolor=BLACK)
	save = findSaves()
	print save
	if not save:
		win.putchars('No save file found! Press [enter] to create new game...', 1, 1)
		win.update()
		inp.waitFor('enter', 1)
		p1.name = reqs.ask('Player Name')
	else:
		loadSave()

rendery = p1.map.newNewRender()	

def saveAndQuit():
	global p1
	with open(os.path.join(os.getcwd(), 'save_dir', 'save_file.dat'), 'w') as f:
		print 'Saving!'
		pickle.dump({'p1':p1, 'ticks':TICKS, 'ents':ENTITIES}, f)
		sys.exit()

def testEnts(x, y):
	F = Projectile('Projectile', .3)
	F.spawn(p1.pos, [y, x])

def getNewRender():
	global rendery
	rendery = p1.map.newNewRender()	

def render():
	global updateRender, FRAME, MODIFY, GETNEWREND, rendery, LASTFRAME, RENDER_FAIL
	if RENDER_FAIL and time.time() - LASTFRAME < THROTTLE:
		return False
	else:
		RENDER_FAIL = True
	if GETNEWREND is True:
		rendery = p1.map.newNewRender()	
		GETNEWREND = False
	_x = MODIFY
	MODIFY = 0
	r = False
	p1.tick()
	updateRender = False
	win.fill(bgcolor=BLACK)
	for line in rendery: #Render the main screen
		_x+=1
		win.putchars(line, 1, _x, fgcolor=RED)
	if len(p1.ai) >=1:
		for bot in p1.ai:
			if bot.alive is True and bot.map == p1.map.id:
				win.putchar(bot.char, bot.pos[0], bot.pos[1], fgcolor=bot.color)
	if len(ENTITIES.keys()) >= 1:
		for ent in ENTITIES.values():
			win.putchar(ent.char, ent.pos[0], ent.pos[1], fgcolor=ent.color)
	if p1.display is True: win.putchar(p1.char, p1.pos[0], p1.pos[1], fgcolor=GREEN)
	for line in p1.map.colorModify.values(): #Render any itmes in colorModify
		for item in line:
			char = p1.map.niceMap[item[1][1]-1][item[1][0]-1]
			win.putchar(char, item[1][0], item[1][1], fgcolor=item[0])
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
	LASTFRAME = time.time()
	if r is True: inp.waitFor('enter', 1)
	FRAME += 1

def loop():
	global updateRender, FRAME, lastFrame, LASTRENDER, OLDHASH, ENTITIES
	while True:
		ent_pos = {}
		if updateRender is True: render()
		inp.retrieve()
		if inp.value != ([], []):
			if 'q' in inp.value[0]: sys.exit()
			if 'w' in inp.value[0] and p1.moveUp() is True: updateRender = True					
			if 'a' in inp.value[0] and p1.moveLeft() is True: updateRender = True
			if 's' in inp.value[0] and p1.moveDown() is True: updateRender = True
			if 'd' in inp.value[0] and p1.moveRight() is True: updateRender = True
			if 'x' in inp.value[0]: saveAndQuit()#p1.useWeapon() #@NOTE this bind will change...
			if 'i' in inp.value[0]: p1.displayInventory()
			#ENTS!
			if 'up' in inp.value[0]: testEnts(-1, 0)
			elif 'down' in inp.value[0]: testEnts(1, 0)
			elif 'left' in inp.value[0]: testEnts(0, -1)
			elif 'right' in inp.value[0]: testEnts(0, 1)

			
		if time.time() - LASTRENDER >= 1: #Fire a tick
			LASTRENDER = time.time()
			p1.tick()

		if not p1.checkHash(OLDHASH): #Has the player object changed sense the last render?
			OLDHASH = p1.hash()
			updateRender = True

		if TICKS != {}:
			for i in TICKS:
				TICKS[i].tick()

		if p1.ai != None and p1.ai != []:
			for i in p1.ai:
				if i.map == p1.map.id and i.alive is True:
					if i.move() is True:
						updateRender = True
					if tuple(i.pos) in ent_pos:
						ent_pos[tuple(i.pos)].append(i)
					else:
						ent_pos[tuple(i.pos)] = [i]

		if ENTITIES != None and ENTITIES != {}:
			for ent in ENTITIES.values(): #HITCHECK ON PLAYER
				if ent.pos == p1.pos: ent.collide(p1)
				if tuple(ent.pos) in ent_pos.keys(): #HITCHECK ON OTHER BOTS
					for i in ent_pos[tuple(ent.pos)]:
						ent.collide(i)

			for ent in ENTITIES.values():
				if ent.doTick is True:
					if ent.tick() is True:
						updateRender = True
		
		if EVENTS != {} and len(EVENTS) != 0:
			for i in EVENTS.keys():
				if time.time() >= i:
					EVENTS[i]()
					del EVENTS[i]
								
		time.sleep(.01)
init()
render()
loop()