class Item():
	def __init__(self, name, Type, kind, durability):
		self.name = name
		self.type = Type
		self.kind = kind
		self.dura = durability
		self.value = 0

		self.canUse = False
		self.canEat = False
		self.canFight = False

		#Weapons
		self.damage = 0 #Damge to opponet
		self.knockback = 0 #Damage to user

		#Consumables
		self.health = 0
		self.unhealth = 0
		self.poison = False
		self.poisonChance = 0 #X in 100 chance of getting poisoned

		if Type == 'food':
			self.canEat = True
			self.value = 1 #1 Dollah!
			self.health = 3
			
class Food():
	def __init__(self, name, health=0, unhealth=0, poison=False, poisonChance=0):
		self.name = name
		self.type = 'food'
		self.health = health
		self.unhealth = unhealth
		self.poison = poison
		self.poisonChance = poisonChance
		self.alive = True

class Apple(Food):
	def __init__(self):
		Food.__init__(self, 'Apple', 3)
		
