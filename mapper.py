
class Map():
	def __init__(self, ID, niceMap, infoMap, player=None):
		from game import GETNEWREND
		self.id = ID
		self.niceMap = niceMap
		self.infoMap = infoMap
		self.player = player

		self.modify = {}
		self.colorModify = {}
	
	def genHitMap(self):
		self.hitMap = {}
		_y = 0
		for y in self.niceMap:
			_x = 0
			for x in self.niceMap[_y]:
				pos = self.niceMap[_y][_x]
				poss = (_x,_y)
				if poss not in self.infoMap.keys():
					if pos == '#': self.hitMap[poss] = (False, 'WALL')
					elif pos == ' ': self.hitMap[poss] = (True, 'AIR')
					elif pos == 'P': 
						self.niceMap[_y] = self.niceMap[_y].replace('P', ' ')
						self.hitMap[poss] = (True, 'AIR')
						self.startPos = [poss[0]+1, poss[1]+1]
						print poss
				else:
					self.hitMap[poss] = self.infoMap[poss]['hitinfo']
					if 'color' in self.infoMap[poss].keys():
						if _y in self.colorModify.keys():
							if self.colorModify[_y] == None:
								self.colorModify[_y] = []
							self.colorModify[_y].append((self.infoMap[poss]['color'], tuple(poss)))
						else:
							self.colorModify[_y] = [(self.infoMap[poss]['color'], tuple(poss))]
 				_x += 1
			_y += 1
		return self

	def updateChar(self, pos, char, hit=None):
		pos = tuple(pos)
		oldline = self.niceMap[pos[1]-1]
		newline = []
		_x = 0
		for i in oldline:
			_x += 1
			if _x == pos[0]:
				newline.append(char)
			else:
				newline.append(i)
		self.niceMap[pos[1]-1] = ''.join(newline)

		if hit != None: #Update hitmap (should be tuplez)
			self.hitMap[(pos[1]-1, pos[0]-1)] = hit
			#print self.hitMap[(pos[1]-1, pos[0]-1)]
		GETNEWREND = True

	def modifyChar(self, pos, char):
		self.modify[tuple(pos)] = char
		GETNEWREND = True

	def unmodifyChar(self, pos):
		if tuple(pos) in self.modify.keys():
			del self.modify[tuple(pos)]
		GETNEWREND = True

	def colorChar(self, pos, color):
		try:
			if len(self.colorModify) >= pos[1]:
				if self.colorModify[pos[1]] != None: self.colorModify[pos[1]].append((color, pos))
				else: self.colorModify[pos[1]] = [(color, pos)]
		except: pass

	def uncolorChar(self, pos): #@DEV Possible we should add better options for this? So we can color a colored char but not uncolor it when its uncolored? 
		try:
			self.colorModify[pos[1]] = []
		except: pass
	
	def rend(self, lines):
		linz = []
		for y in lines:
			mlin = []
			for x in lines[y]:
				# if [x,y] == self.player.pos:
				# 	mlin.append(self.player.char)
				# else:
				mlin.append(lines[y][x])
			linz.append(''.join(mlin))
		return linz

	def newNewRender(self):
		lines = {}
		_y = 0
		for line in self.niceMap:
			_y += 1
			lines[_y] = {}
			_x = 0
			for char in line:
				_x += 1
				#p = self.player.aiPos([_x, _y]) @DEV WHAT THE FUCK DOES THIS EVEN DO? 
				#if [_x,_y] == self.player.pos: lines[_y][_x] = self.player.char
				#elif (_x,_y) in p.keys(): lines[_y][_x] = p[(_x,_y)].char @DEV same here
				if (_x,_y) in self.modify.keys(): lines[_y][_x] = self.modify[(_x,_y)]
				else: lines[_y][_x] = char
		return self.rend(lines)

	#lines[self.player.pos[1]][self.player.pos[0]] = self.player.char

