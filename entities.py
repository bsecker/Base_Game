import pygame
import constants

"""

TO DO:
replace sprites with dirty sprites!

"""

class BaseEntity:
    def __init__(self, x, y, width, height, colour):
        """for blocky style entities"""
        self.image = pygame.Surface(( width, height))
        self.image.fill(colour)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Block(BaseEntity):
    def __init__(self, colour, x, y):
        BaseEntity.__init__(self, x, y, constants.BLOCK_SIZE, constants.BLOCK_SIZE, colour)

class Wood(Block):
    def __init__(self, x, y):
        Block.__init__(self, constants.BROWN, x, y)

class Sail(Block):
    def __init__(self, x, y):
        Block.__init__(self, constants.WHITE, x, y)

class Sea(BaseEntity):
    """ the sea """
    def __init__(self):
        BaseEntity.__init__(self, 0, constants.SCREEN_HEIGHT - constants.SEA_HEIGHT, constants.SCREEN_WIDTH, constants.SEA_HEIGHT, constants.BLUE)

