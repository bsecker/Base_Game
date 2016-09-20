import pygame
import constants
import math
from random import randint
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

class Block(BaseEntity):
    def __init__(self, colour, x, y, block_list):
        BaseEntity.__init__(self, x, y, constants.BLOCK_SIZE, constants.BLOCK_SIZE, colour)
        self.block_list = block_list
        self.y_vel = 0
        self.solid = True
        self.health = 1
        self.alive = True
        self.cost = 1
        self.owner = 'player'

    def update(self):
        self.update_gravity()

        self.rect.y += self.y_vel

    def update_gravity(self):
        pass

class Wood(Block):
    def __init__(self, x, y, block_list):
        Block.__init__(self, constants.BROWN, x, y, block_list)
        self.entity_id = "wood"
        self.cost = 1

class ReinforcedWood(Block):
    def __init__(self, x, y, block_list):
        Block.__init__(self, constants.DARKBROWN, x, y, block_list)
        self.entity_id = "rewood"
        self.health = 3
        self.cost = 5

class Sail(Block):
    def __init__(self, x, y, block_list):
        Block.__init__(self, constants.WHITE, x, y, block_list)
        self.entity_id = "sail"
        self.cost = 1

class Sea(BaseEntity):
    """ the sea """
    def __init__(self):
        BaseEntity.__init__(self, 0, constants.SCREEN_HEIGHT - constants.SEA_HEIGHT, constants.SCREEN_WIDTH, constants.SEA_HEIGHT, constants.BLUE)
        self.entity_id = "sea"
        self.solid = False
        self.alive = True
        self.health = 1

class ProjectileLauncher(BaseEntity):
    def __init__(self, x, y, blocklist, spritefile):
        BaseEntity.__init__(self, x, y, spritefile = spritefile)
        self.entity_id = None
        self.solid = True
        self.block_list = blocklist
        self.cost = 0
        self.health = 3
        self.owner = 'player'

        self.can_fire = False
        self.reload_max = 100
        self.reload_time = 0

        self.fire_angle = -45
        self.fire_angle_varation = 25
        self.fire_speed = 10

    def update(self):
        if self.reload_time >= self.reload_max:
            #fire
            self.reload_time = 0
            self.fire()
        else:
            self.reload_time += 1

    def fire(self):
        proj = Projectile(self.rect.x, self.rect.y-10, self.block_list, self.fire_speed, self.fire_angle+randint(-self.fire_angle_varation,self.fire_angle_varation))
        self.block_list.add(proj)

class Catapult(ProjectileLauncher):
    def __init__(self, x, y, block_list, spritefile = 'spr_catapult'):
        ProjectileLauncher.__init__(self, x, y, block_list, spritefile)
        self.entity_id = 'catapult'
        self.cost = 20

class CatapultEnemy(Catapult):
    def __init__(self, x, y, block_list, spritefile = 'spr_catapult_left'):
        ProjectileLauncher.__init__(self, x, y, block_list, spritefile)
        self.entity_id = 'catapult'
        self.fire_angle = 225
        self.fire_angle_varation = 25
        self.fire_speed = 10

class Cannon(Catapult):
    def __init__(self, x, y, block_list, spritefile = 'spr_cannon'):
        ProjectileLauncher.__init__(self, x, y, block_list, spritefile)
        self.entity_id = 'cannon'
        self.reload_max = 50
        self.fire_angle = -10
        self.fire_angle_varation = 5
        self.fire_speed = 14
        self.cost = 30

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
        self.solid = False

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