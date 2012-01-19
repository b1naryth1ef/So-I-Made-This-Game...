import reqs, random, items, game, time
from colors import health, RED, ORANGE

class Player():
	def __init__(self, name, char, pos=[3,3]):
		import game
		self.name = name
		self.char = char
		self.pos = pos
		self.lastPos = pos
		self.health = [50,50]
		self.dead = False
		self.display = True
		self.poisoned = [False, 0, 0, 0] #Is poisoned and amount per tick, and duration, and last done
		self.realpos = lambda: [self.pos[0]-1, self.pos[1]-1]
		self.inv = items.BackPack()
		self.map = None
		self.levels = None
		self.ai = None
		self.mode = 1

		self.beforeCombat = [0, []] #MAP, POS
		self.weaponChoice = 0
		self.combatWith = None
		self.movx = [0,0]
		self.movy = [0,0]

		self.poisonTime = 0
		self.lastModified = []

	def displayInventory(self):
		li = self.niceInv()
		choice = reqs.selectionScreen(li, 'Inventory:', ORANGE, '[Enter] to select | [R] to dump | [Q] to exit', ORANGE, True)
		if choice[0] != None and choice[1] != None:
			if self.inv[choice[0]].type == 'food':
				self.eatObj(self.inv[choice[0]])
			elif self.inv[choice[0]].type == 'weapon' and self.mode == 0:
				self.weaponChoice = choice[0]
				#self.atkObj(self.inv[choice[0]])
		game.render()

	def getStatus(self):
		if self.poisoned[0] is True: return ['Poisoned!', health[1]]
		if self.health[0] > 40: return ['Great!', health[2]]
		elif self.health[0] > 30: return ['Good.', health[3]]
		elif self.health[0] > 20: return ['Okay.', health[4]]
		elif self.health[0] > 10: return ['Injured.', health[5]]
		elif self.health[0] > 0: return ['Almost Dead.', health[6]]

	def pickup(self, item): return self.inv.addItem(item)

	def useWeapon(self): #@DEV add an animation
		if self.mode == 0 and self.combatWith.alive is True:
			if self.weaponChoice == 0: pass #@DEV use knife/fists?
			else: self.atkObj(self.inv[self.weaponChoice])

	def attacked(self, amount):
		self.unheal(amount)
		game.MODIFY = 1

	def attackMode(self, bot):
		self.beforeCombat = [self.map.id, self.pos]
		self.selectMap(0)
		self.pos = self.map.startPos
		self.mode = 0 #Attack mode
		self.combatWith = bot

	def wonBattle(self): #@DEV add an animation
		self.selectMap(self.beforeCombat[0])
		self.pos = self.beforeCombat[1]
		self.mode = 1
		self.combatWith = None

	def newPickup(self, item): 
		i = items.itemz[item]()
		return (i, self.pickup(i))
	
	def niceHealth(self):
		if self.health[0] > 5:
			return '%s%s' % ('='*(int(round(self.health[0]))/5), ' '*abs((int(round(self.health[0]))-self.health[1])/5))
		else: return '=         '

	def tick(self):
		if self.poisoned[0] is True:
			if time.time() - self.poisonTime <= self.poisoned[2]:
				if time.time() - self.poisoned[3] > 1:
					self.unheal(self.poisoned[1])
					self.poisoned[3] = time.time()
			else:
				self.poisoned = [False, 0, 0, 0] #Reset poison

		if self.map.hitMap[tuple(self.realpos())][1] == 'PICKUP': #Idk why I put this here. Could just as easily been in the main loop...
			i = self.map.infoMap[tuple(self.realpos())]['pickup'][0]
			y = self.newPickup(i)
			if y[1] is False:
				game.MESSAGES.append(('Can\'t pickup %s, inventory full!' % y[0].name, game.BLUE, 4))
				self.moveBack()
				return None
			else:
				game.MESSAGES.append(('Picked up a %s' % (y[0].name), game.BLUE, 4))

			if self.map.infoMap[tuple(self.realpos())]['pickup'][1] is True:
				self.map.updateChar((tuple(self.pos)), ' ')
				self.map.hitMap[tuple(self.realpos())] = (True, 'AIR')
		
		if self.health[0] <= 0 and self.dead is False: self.die()

		for i in self.ai:
			if i.alive is True and i.map == self.map.id and self.pos == i.pos and self.mode == 1:
				i.attackPlayer()

	def niceInv(self):
		li = {}
		for i in self.inv.s:
			if self.inv.s[i] != None:
				li[i] = self.inv.s[i].name
		return li

	def die(self):
		self.health[0] = -1
		self.dead = True
		self.combatWith = None

	def unheal(self, amount):
		if self.health[0]-amount < 0: self.die()
		else: self.health[0]-=amount

	def heal(self, amount):
		if self.health[0]+amount > self.health[1]: self.health[0] = self.health[1]
		else: self.health[0]+=amount

	def eatObj(self, obj): #Action binded to eating
		if obj.type == 'food':
			dat = obj.use()
			self.heal(dat[0])
			self.unheal(dat[1])
			if dat[2] is True:
				self.poisoned[0] = True
				self.poisoned[1] = dat[4]
				self.poisoned[2] = dat[3]
				self.poisonTime = time.time()
			return True
		return False

	def useObj(self, obj): pass
	def atkObj(self, obj):
		if self.mode == 0:
			dam = obj.genDamage()
			self.combatWith.unheal(dam[0])
			self.unheal(dam[1])

	def moveUp(self): return self.move(y=-1)
	def moveDown(self): return self.move(y=1)
	def moveLeft(self): return self.move(x=-1)
	def moveRight(self): return self.move(x=1)

	def selectMap(self, map):
		self.map = self.levels[str(map)]
		game.GETNEWREND = True

	def aiPos(self, pos):
		if self.ai != [] and self.ai != None:
			ret = {}
			for i in self.ai:
				ret[tuple(i.pos)] = i
			return ret

	def moveBack(self): #Could just do x,y = y,x but w/e
		self.pos, self.lastPos = reqs.trade(self.pos, self.lastPos)

	def move(self, x=0, y=0):
		cPos = self.pos
		nPos = [self.pos[0]+x, self.pos[1]+y]
		cPos = (self.pos[0]+x-1, self.pos[1]+y-1)
		#self.pos = nPos

		if self.map.hitMap[cPos][0] == True: 
			if self.map.hitMap[cPos][1] == 'PORTAL':
				self.pos = list(self.map.infoMap[cPos]['portal'][2])
				self.lastmap = self.map.id
				self.map = self.levels[self.map.infoMap[cPos]['portal'][1]]
				return True
			self.lastPos = self.pos
			self.pos = nPos
			return True
		else:
			return False

	def hash(self): return (self.health[0], self.pos, self.inv)