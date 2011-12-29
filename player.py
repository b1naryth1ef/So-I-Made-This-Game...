class Player():
	def __init__(self, name, char, pos=[3,3]):
		self.name = name
		self.char = char
		self.pos = pos
		self.realpos = lambda: [self.pos[0]-1, self.pos[1]-1]
		self.map = None
		self.levels = None
		self.ai = None

		self.movx = [0,0]
		self.movy = [0,0]

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