import pygame
import constants

"""

TO DO:
replace sprites with dirty sprites!

"""

class BaseEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, width = None, height = None, colour = None, spritefile = None): #better way of writing this?
        """for blocky style entities"""
        pygame.sprite.Sprite.__init__(self)

        if spritefile:
            self.image = pygame.image.load("resources/{0}.png".format(spritefile)).convert_alpha()
        else:
            self.image = pygame.Surface(( width, height))
            self.image.fill(colour)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        
    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Block(BaseEntity):
    def __init__(self, colour, x, y, block_list):
        BaseEntity.__init__(self, x, y, constants.BLOCK_SIZE, constants.BLOCK_SIZE, colour)
        self.block_list = block_list
        self.gravity_speed = 2
        self.y_vel = 0

    def update(self):
        self.update_gravity()

        self.rect.y += self.y_vel

    def update_gravity(self):
        """ falls if there is nothing underneath it"""
        # collide with objects

        #check point directly below self
        pass

class Wood(Block):
    def __init__(self, x, y, block_list):
        Block.__init__(self, constants.BROWN, x, y, block_list)
        self.entity_id = "wood"

class ReinforcedWood(Block):
    def __init__(self, x, y, block_list):
        Block.__init__(self, constants.DARKBROWN, x, y, block_list)
        self.entity_id = "rewood"

class Sail(Block):
    def __init__(self, x, y, block_list):
        Block.__init__(self, constants.WHITE, x, y, block_list)
        self.entity_id = "sail"

class Sea(BaseEntity):
    """ the sea """
    def __init__(self):
        BaseEntity.__init__(self, 0, constants.SCREEN_HEIGHT - constants.SEA_HEIGHT, constants.SCREEN_WIDTH, constants.SEA_HEIGHT, constants.BLUE)
        self.entity_id = "sea"

class Catapult(BaseEntity):
    def __init__(self, x, y, block_list):
        BaseEntity.__init__(self, x, y, spritefile = 'spr_catapult')
        self.entity_id = 'catapult'
        
    