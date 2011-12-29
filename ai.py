import time

class AI():
	def __init__(self, name, player, attack=1, health=5, Map=0, char='+', speed=1, color=(255,255,255)): 
		self.name = name
		self.player = player
		self.attack = attack
		self.health = [health, health]
		self.map = Map
		self.char = char
		self.color = color
		self.speed = speed

		self.alive = False
		self.pos = [10,10]

		self.lastmove = time.time()
	
	def spawn(self, pos=[10,10]):
		self.alive = True
		self.pos = pos
		return self

	def move(self):
		if time.time() - self.lastmove >= self.speed:
			self.lastmove = time.time()
			self.pos[0] += 1
			return True


class Pos():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.pos = lambda: [x,y]

def attackModel(botPos, goalPos): pass


def aStar(self, graph, current, end):
    openList = set()
    closedList = set()
    path = []

    def retracePath(c):
        path.insert(0,c)
        if c.parent == None:
            return
        retracePath(c.parent)

    openList.append(current)
    while len(openList) is not 0:
        current = min(openList, key=lambda inst:inst.H)
        if current == end:
            return retracePath(current)
        openList.remove(current)
        closedList.append(current)
        for tile in graph[current]:
            if tile not in closedList:
                tile.H = (abs(end.x-tile.x)+abs(end.y-tile.y))*10 
                if tile not in openList:
                    openList.append(tile)
                tile.parent = current
    return path