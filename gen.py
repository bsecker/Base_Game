import entities
import pygame
import constants

class LevelManager:
	"""handles all the game logic and everything basically lol"""
	def __init__(self):
		self.level_objs = self.generate_world()
		self.block_state = 'block_wood'

	def generate_world(self):
		sea = entities.Sea()
		return [sea]

	def update(self):
		# get block state
		state = getattr(self, self.block_state)
		state()

		self.get_mouse()

	def get_mouse(self):
		#print 'mouse at', pygame.mouse.get_pos()

		_pos = list(pygame.mouse.get_pos())
		_pos[0] = _pos[0] // constants.BLOCK_SIZE * constants.BLOCK_SIZE
		_pos[1] = _pos[1] // constants.BLOCK_SIZE * constants.BLOCK_SIZE
		_buttons = pygame.mouse.get_pressed()

		if _buttons[0]:
			# generate new block
			self.create_block(self.current_block, _pos)
		elif _buttons[2]:
			self.delete_block(_pos)

	def create_block(self, block, pos):
		"""create block at pos"""

		# if pos is taken, dont do anything
		for _i in self.level_objs:
			if _i.rect.collidepoint(pos[0]+1, pos[1]+1):
				return

		_block = block(pos[0], pos[1], self.level_objs) 
		self.level_objs.append(_block)
		print self.level_objs

	def delete_block(self, pos):
		"""delete block at position. doesn't delete water"""
		for _i in self.level_objs:
			if _i.rect.collidepoint(pos[0]+1, pos[1]+1):
				if _i.entity_id != 'sea':
					self.level_objs.remove(_i)

	def block_wood(self):
		self.current_block = entities.Wood

	def block_rewood(self):
		self.current_block = entities.ReinforcedWood

	def block_catapult(self):
		self.current_block = entities.Catapult
