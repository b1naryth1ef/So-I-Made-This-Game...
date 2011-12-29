import reqs, random

class Player():
	def __init__(self, name, char, pos=[3,3]):
		self.name = name
		self.char = char
		self.pos = pos
		self.health = [50,50]
		self.poisoned = (False, 0, 0) #Is poisoned and amount per tick, and duration
		self.realpos = lambda: [self.pos[0]-1, self.pos[1]-1]
		self.inv = {
		1:None,
		2:None,
		3:None,
		4:None,
		5:None}
		self.map = None
		self.levels = None
		self.ai = None

		self.movx = [0,0]
		self.movy = [0,0]

		self.poisonTime = 0

	def tick(self):
		if self.poisoned[0] is True:
			if time.time() - self.poisonTime >= self.poisoned[2]:
				self.unheal(self.poisoned[1])
				self.poisonTime = time.time()

	def niceInv(self):
		li = {}
		for i in self.inv:
			if self.inv[i] != None:
				li[i] = self.inv[i].name
		return li

	def die(self):
		self.health[0] = 0
		print 'Deadz!'

	def unheal(self, amount):
		if self.health[0]-amount < self.health[1]:
			self.die()
		else:
			self.health[0]-=amount

	def heal(self, amount):
		if self.health[0]+amount > self.health[1]:
			self.health[0] = self.health[1]
		else:
			self.health[0]+=amount

	def eatObj(self, obj):
		if obj.type == 'food':
			self.heal(obj.health)
			self.unheal(obj.unhealth)
			if obj.poison is True and random.randint(obj.poisonChance, 100):
				pass

	def moveUp(self): return self.move(y=-1)
	def moveDown(self): return self.move(y=1)
	def moveLeft(self): return self.move(x=-1)
	def moveRight(self): return self.move(x=1)

	def selectMap(self, map):
		self.map = self.levels[str(map)]

	def aiPos(self, pos):
		if self.ai != [] and self.ai != None:
			ret = {}
			for i in self.ai:
				ret[tuple(i.pos)] = i
			return ret

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
			self.pos = nPos
			return True
		else:
			return False