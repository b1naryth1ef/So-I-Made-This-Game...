import random, time

class Entity():
	def __init__(self, Type, name):
		#General classifications
		self.type = Type
		self.name = name
		self.color = (255, 255, 255)
		self.char = '+'
		self.pos = [0, 0]
		self.speed = .3

		#Engine classifications
		self.slice = [None, 0] #Slice in the ENTITIES list (Second is which list, -1 is bad, 1 is good)
		self.map = None

		#Bools
		self.alive = False
		self.doTick = False
		self.spawned = False

	#Over-rides
	def spawn(self): pass
	def despawn(self): pass
	def action(self, hit): pass
	def tick(self): pass


class Projectile(Entity):
	def __init__(self, name, speed=0):
		global game
		import game
		Entity.__init__(self, 'projectile', name)
		self.lastMove = 0
		self.speed = speed
		self.velo = [0, 0]

	def spawn(self, pos, velo):
		self.velo = velo
		self.pos = pos
		self.alive, self.doTick, self.spawned = True, True, True
		self.slice = [game.addEntity(self, 1), 1]

	def despawn(self):
		self.alive, self.doTick = False, False
		self.slice = [game.moveEntity(self.slice[0], 1), -1]

	def action(self, hit):
		if hit.type == 'player': print 'HIT PLAYER' #Eventually fire player.hitByEnt() or smthing
		self.despawn()

	def tick(self):
		#print 'TICKING %s' % time.time()
		if self.pos[1] > len(game.p1.map.niceMap): return self.despawn()
		if self.pos[0] > len(game.p1.map.niceMap[self.pos[1]])+1 or self.pos[0] <= 0: return self.despawn()
		if time.time() - self.lastMove >= self.speed:
			self.pos = [i+self.velo[z] for z, i in enumerate(self.pos)] #Proud of this one
			return True

class Storage():
	def __init__(self, name, slots=5, Type=''):
		self.slots = slots
		self.name = name
		self.type = Type

		self.s = {}

		self.genStorage()

	def genStorage(self):
		for i in range(1,self.slots+1): #xrange is a waste here.
			self.s[i] = None

	def addItem(self, item):
		for x,y in enumerate(self.s.values()):
			pos = x+1
			if y == None:
				self.s[pos] = item
				return True
		return False
	
	def rmvItem(self, slot):
		del self.s[slot]
		return True

	def popItem(self, slot):
		ret = self.s[slot]
		del self.s[slot]
		return ret

	def iterate(self): return self.s

	def __setitem__(self, item, value):
		self.s[item] = value
	
	def __getitem__(self, item):
		return self.s[item]

class BackPack(Storage):
	def __init__(self):
		self.id = 4
		Storage.__init__(self, 'Back Pack', 5, 'inventory')

class Food():
	def __init__(self, name, health=0, unhealth=0, poison=False, poisonChance=0, poisonTime=60, poisonDamage=1):
		self.name = name
		self.type = 'food'
		self.health = health
		self.unhealth = unhealth
		self.poison = poison
		self.poisonChance = poisonChance
		self.poisonTime = poisonTime
		self.poisonDamage = poisonDamage
		self.alive = True

	def use(self):
		if self.poison is True and random.randint(1, self.poisonChance) == 1:
			return (self.health, self.unhealth, True, self.poisonTime, self.poisonDamage)
		else:
			return (self.health, self.unhealth, False, 0, 0)

class Weapon():
	def __init__(self, name, damage=0, damageModifier=0, knockback=0, knockbackModifier=0, effect=None, durability=0, value=5):
		self.name = name
		self.type = 'weapon'
		self.damage = damage
		self.damageModifier = damageModifier
		self.knockback = knockback
		self.knockbackModifier = knockbackModifier
		self.effect = effect
		self.durability = durability
		self.value = value
		self.alive = True

	def genDamage(self):
		damMod = self.damageModifier
		knkMod = self.knockbackModifier
		if self.damageModifier == 0:
			damMod = 1
		if self.knockbackModifier == 0:
			knkMod = 1
		return (self.damage*damMod, self.knockback*knkMod)

class Apple(Food):
	def __init__(self):
		self.id = 0
		Food.__init__(self, 'Apple', 3)

class BadApple(Food):
	def __init__(self):
		self.id = 5
		Food.__init__(self, 'Bad Apple', 3, 0, True, 10, 5, .5)

class WoodSword(Weapon):
	def __init__(self):
		self.id = 1
		Weapon.__init__(self, 'Wood Sword', 3, 0, 0, 0, None, 30, 5)

class IronSword(Weapon):
	def __init__(self):
		self.id = 2
		Weapon.__init__(self, 'Iron Sword', 5, 0, 0, 0, None, 50, 15)
		
class GoldPlatedSword(Weapon):
	def __init__(self):
		self.id = 3
		Weapon.__init__(self, 'Gold Plated Sword', 10, 0, 0, 0, None, 75, 55)

#class Projectile(Entity):
#	def __init__(self, name):
#		Entity.__init__(self, 'Projectile', name)

class Arrow(Projectile):
	def __init__(self):
		self.id = 0
		Projectile.__init__(self, 'Arrow', )

class WoodBow(Weapon):
	def __init__(self):
		self.id = 6
		Weapon.__init__(self, 'Wood Bow')

entityz = {
	0:Arrow
}

itemz = {
	0:Apple,
	1:WoodSword,
	2:IronSword,
	3:GoldPlatedSword,
	4:BackPack,
	5:BadApple,
	6:WoodBow
}