"""GUI Methods"""
import pygame
import constants

class BaseUIEntity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.entity_id = 'ui_obj'

class Wood(BaseUIEntity):
    def __init__(self, x, y):
        BaseUIEntity.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(constants.BROWN)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.entity_id = 'block_wood'


class ReinforcedWood(BaseUIEntity):
    def __init__(self, x, y):
        BaseUIEntity.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(constants.DARKBROWN)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.entity_id = 'block_rewood'


class Catapult(BaseUIEntity):
    def __init__(self, x, y):
        BaseUIEntity.__init__(self)
        self.image = pygame.image.load("resources/{0}.png".format("spr_catapult")).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.entity_id = 'block_catapult'

class Cannon(BaseUIEntity):
    def __init__(self, x, y):
        BaseUIEntity.__init__(self)
        self.image = pygame.image.load("resources/{0}.png".format("spr_cannon")).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.entity_id = 'block_cannon'
