import pygame
import constants
import math
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
        self.y_vel = 0
        self.solid = True

    def update(self):
        self.update_gravity()

        self.rect.y += self.y_vel

    def update_gravity(self):
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
        self.solid = False

class Catapult(BaseEntity):
    def __init__(self, x, y, block_list):
        BaseEntity.__init__(self, x, y, spritefile = 'spr_catapult')
        self.entity_id = 'catapult'
        self.solid = False
        self.block_list = block_list

        self.can_fire = False
        self.reload_max = 50
        self.reload_time = 0

    def update(self):
        if self.reload_time >= self.reload_max:
            #fire
            self.reload_time = 0
            # JUST MAKE SURE self.blocklist DOESNT CHANGE OR SOMETHING??!
            proj = Projectile(self.rect.x, self.rect.y, self.block_list, 10, -45)
            self.block_list.append(proj)
        else:
            self.reload_time += 1

class Cannon(BaseEntity):
    def __init__(self):
        pass

class Projectile(BaseEntity):
    def __init__(self, x, y, block_list, speed, direction):
        BaseEntity.__init__(self, x, y, spritefile = 'spr_projectile')
        self.block_list = block_list
        self.speed = speed
        self.direction = direction
        self.max_gravity = 10
        self.gravity_accel = .1
        self.alive = True
        self.entity_id = 'projectile'


        # convert angle to radians, then calculate x & y speeds
        self.angle = self.direction * math.pi/180
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed

    def update(self):
        # if outside screen, delete
        if self.rect.y > constants.SCREEN_HEIGHT:
            self.alive = False

        # delete in contact with water

        # move
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        # update gravity
        if self.y_vel <= self.max_gravity:
            self.y_vel += self.gravity_accel

