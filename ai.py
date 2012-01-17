import time
from modules import astar

class AI():
	def __init__(self, name, player, attack=1, health=5, Map=0, char='+', speed=.5, color=(255,255,255)): 
		self.name = name
		self.player = player
		self.attack = attack
		self.health = [health, health]
		self.map = Map
		self.char = char
		self.color = color
		self.speed = speed
		self.goal = 'player' #player/entity
		self.pathFindy = astar.AStar()

		self.alive = False
		self.pos = [10, 10]

		self.lastmove = time.time()
	
	def spawn(self, pos=[11,11]):
		self.alive = True
		self.pos = pos
		return self

	def attackPlayer(self): print 'Would attack player'
	def attackEntity(self): pass

	def move(self):
		if time.time() - self.lastmove >= self.speed:
			if self.goal is 'player':
				self.pathFindy.findPath(tuple(self.player.pos), tuple(self.pos), self.player.levels[str(self.map)].hitMap) 
				f = self.pathFindy.path
				if len(f) > 1: self.pos = list(f[1])
				else: self.attackPlayer()
				self.lastmove = time.time()
				return True
	
	def die(self):
		self.health[0] = 0
		self.alive = False

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