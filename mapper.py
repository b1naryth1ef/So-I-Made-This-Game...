class Map():
	def __init__(self, ID, niceMap, infoMap, player=None):
		self.id = ID
		self.niceMap = niceMap
		self.infoMap = infoMap
		self.player = player

		self.modify = {}
	
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
						self.startPos = poss
				else:
					self.hitMap[poss] = self.infoMap[poss]['hitinfo']
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

	def modifyChar(self, pos, char):
		self.modify[tuple(pos)] = char
	
	def rend(self, lines):
		linz = []
		for y in lines:
			mlin = []
			for x in lines[y]:
				if [x,y] == self.player.pos:
					mlin.append(self.player.char)
				else:
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
				#p = self.player.aiPos([_x, _y])
				if [_x,_y] == self.player.pos: lines[_y][_x] = self.player.char
				#elif (_x,_y) in p.keys(): lines[_y][_x] = p[(_x,_y)].char
				elif (_x,_y) in self.modify.keys(): lines[_y][_x] = self.modify[(_x,_y)]
				else: lines[_y][_x] = char
		return self.rend(lines)

	def pathRender(self):
		op = []
		cl = []

		for i in self.hitMap:
			if self.hitMap[i][0] == True: op.append(i)
			else: cl.append(i)
		
		print op
		print '\n\n\n\n\n'
		print cl

	#lines[self.player.pos[1]][self.player.pos[0]] = self.player.char

