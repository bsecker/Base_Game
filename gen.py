import entities
import pygame
import constants

class LevelManager:
	"""handles all the game logic and everything basically lol"""
	def __init__(self):
		self.level_objs = self.generate_world()
		self.block_state = 'block_wood'
		self.money = 100
		self.buildcost = 0

	def generate_world(self):
		objs = []

		# add sea
		sea = entities.Sea()
		objs.append(sea)

		# add starting block
		_height = constants.SCREEN_HEIGHT - constants.SEA_HEIGHT - constants.BLOCK_SIZE
		start_block = entities.Wood(constants.BLOCK_SIZE*5, _height, objs) 
		start_block.cost = 0
		objs.append(start_block)

		return objs

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

		# Left click
		if _buttons[0]:
			# generate new block
			if self.money >= self.buildcost:
				self.create_block(self.current_block, _pos, self.buildcost)

		# Right click
		elif _buttons[2]:
			self.delete_block(_pos)

	def create_block(self, block, pos, cost):
		"""create block at pos"""
		can_build = 0

		# check if within boundaries
		if pos[0] >= constants.BUILD_CONSTRAINT:
			return

		# loop through all blocks and check if it can be placed there.
		for _i in self.level_objs:
			if _i.entity_id != 'sea':
				# if pos is taken, do nothing and cancel everything
				if _i.rect.collidepoint(pos[0]+1, pos[1]+1):
					return

				if block != (entities.Catapult or entities.Cannon):
					# can only build blocks on top, left or right of existing blocks
					if _i.rect.collidepoint(pos[0]+constants.BLOCK_SIZE+1, pos[1]+1):
						can_build = 1 #left
					if _i.rect.collidepoint(pos[0]-1, pos[1]+1):
					 	can_build = 1 #right
					if _i.rect.collidepoint(pos[0]+1, pos[1]+constants.BLOCK_SIZE+1):
						can_build = 1 #down
				else:
					# can only build blocks on top of existing blocks
					if _i.rect.collidepoint(pos[0]+1, pos[1]+constants.BLOCK_SIZE+1):
						can_build = 1 #down

		if can_build == 1:
			_block = block(pos[0], pos[1], self.level_objs) 
			_block.cost = cost
			self.level_objs.append(_block)
			self.money +=- cost
			return
				
	def delete_block(self, pos):
		"""delete block at position. doesn't delete water"""
		for _i in self.level_objs:
			if _i.rect.collidepoint(pos[0]+1, pos[1]+1):
				if _i.entity_id != 'sea':
					self.level_objs.remove(_i)
					self.money += _i.cost

	def block_wood(self):
		self.current_block = entities.Wood
		self.buildcost = 1

	def block_rewood(self):
		self.current_block = entities.ReinforcedWood
		self.buildcost = 5

	def block_catapult(self):
		self.current_block = entities.Catapult
		self.buildcost = 20

	def draw(self, surface, font):
		label = font.render("Money: {0}".format(str(self.money)), 1, constants.TEXT_COLOUR)
		surface.blit(label, (10,10))
