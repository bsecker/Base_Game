import entities
import pygame
import constants

class LevelManager:
	"""handles all the game logic and everything basically lol"""
	def __init__(self):
		self.level_objs = self.generate_world()

	def generate_world(self):
		sea = entities.Sea()
		return [sea]

	def update(self):
		self.get_mouse()

	def get_mouse(self):
		#print 'mouse at', pygame.mouse.get_pos()

		_pos = list(pygame.mouse.get_pos())
		_pos[0] = _pos[0] // constants.BLOCK_SIZE * constants.BLOCK_SIZE
		_pos[1] = _pos[1] // constants.BLOCK_SIZE * constants.BLOCK_SIZE
		_buttons = pygame.mouse.get_pressed()

		if _buttons[0]:
			# generate new block
			self.create_block(entities.Wood, _pos)
		elif _buttons[2]:
			self.delete_block(_pos)

	def create_block(self, block, pos):
		"""create block at pos"""

		# if pos is taken, dont do anything
		for _i in self.level_objs:
			if _i.rect.collidepoint(pos[0]+1, pos[1]+1):
				return
			# if in water, don't do anything


		_block = block(pos[0], pos[1]) 
		self.level_objs.append(_block)
		print self.level_objs

	def delete_block(self, pos):
		"""delete block at position"""
		for _i in self.level_objs:
			if _i.rect.collidepoint(pos[0]+1, pos[1]+1):
				self.level_objs.remove(_i)


### TO DO FOR TOMORROW:
### FIX ACCIDENTALLY DELETING WATER
### FIX BUILDING INSIDE WATER