import pygame

background_colour = "#202030" # IF THIS IS UPDATED, ALSO UPDATE THE VALUE IN SIXMONTHS.PY

def getBlock(blocktype, x, y):
	if blocktype == 'B':
		block = Block(x, y, True)
	elif blocktype == 'E':
		block = ExitBlock(x, y, True)
	elif blocktype == 'C':
		block = Block(x, y, False)
	elif blocktype == 'I':
		block = Block(x, y, True, background_colour) # If the colour is the background but we make it collidable, it becomes an invisible block!
	else:
		block = 'noblock'
		#block = Block(x, y, False, background_colour) # A block with the background colour which isn't collidable i.e. a background block.
	
	return block

class Level(object):
	def __init__(self, blocksList, textDetailsList, playerDetailsList):
		self.blocksList = blocksList
		self.textDetails = textDetailsList
		self.playerDetails = self.playerx, self.playery = playerDetailsList[0], playerDetailsList[1]
		
		
class Block(pygame.sprite.Sprite):
	def __init__(self, x, y, collidable=True, colour='#9F9FBF'):
		self.x, self.y = x, y
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((32, 32))
		self.image.convert()
		self.image.fill(pygame.Color(colour))
		self.rect = pygame.Rect(x, y, 32, 32)
		self.collidable = collidable

	def update(self):
		pass

class ExitBlock(Block):
	def __init__(self, x, y, collidable = True, colour='#800040'):
		Block.__init__(self, x, y, collidable, colour)
		
# A custom exception to let us know when a level is complete. 
class LevelComplete(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
		
# A custom exception to end the game.
class GameComplete(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)



class Player(pygame.sprite.Sprite):
	def __init__(self, x, y, colour='#DFDFDF', width=32, height=32, collidable=True):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface((width, height))
		self.image.convert()
		self.image.fill(pygame.Color(colour))

		self.rect = pygame.Rect(x, y, width, height)

		self.xvel = 0
		self.yvel = 0
		self.inAir = False
		self.collidable = collidable

	def update(self, up, down, left, right, objects):
		if up:
			#Only jump if on the ground.
			if not self.inAir:
				self.yvel -= 7
		if down:
			pass #This could be used for special moves!
		if left:
			self.xvel = -5
		if right:
			self.xvel = 5

		if self.inAir:
			#Only accelerate due to gravity if there's nothing to hold you up!
			self.yvel += 0.3
			#Set a maximum speed.
			if self.yvel > 30: self.yvel = 30
		if not(left or right):
			self.xvel = 0
		
		self.rect.left += self.xvel
		self.collide(self.xvel, 0, objects)

		self.inAir = True
		
		self.rect.top += self.yvel
		self.collide(0, self.yvel, objects)


	def collide(self, xvel, yvel, objects):
		for object_instance in objects:
			if pygame.sprite.collide_rect(self, object_instance) and object_instance.collidable:
				if isinstance(object_instance, ExitBlock):
					raise LevelComplete("Level Complete")
				if xvel > 0: 
					self.rect.right = object_instance.rect.left
				if xvel < 0: 
					self.rect.left = object_instance.rect.right
				if yvel > 0:
					self.rect.bottom = object_instance.rect.top
					self.inAir = False
					self.yvel = 0
				if yvel < 0: 
					self.rect.top = object_instance.rect.bottom
					self.yvel = 0
