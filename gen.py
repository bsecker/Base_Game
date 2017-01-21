import entities
import pygame
import constants
import random
import gui
import time


class LevelManager:
    """handles all the game logic and everything basically lol

    TODO: Fix interaction between world.py class and this class. Half the functionality seems split across modules. Annoying!
    """

    def __init__(self):
        self.level_objs, self.player_objs, self.enemy_objs = self.generate_world()
        self.block_state = 'block_wood'
        self.money = 5000

        self.background = self.set_background(constants.LIGHTBLUE)
        self.ui         = self.set_ui()
        self.enemy      = Enemy(self)


    def generate_world(self):
        objs = pygame.sprite.Group()
        player_objs = pygame.sprite.Group()
        enemy_objs = pygame.sprite.Group()

        # add sea
        sea = entities.Sea()
        objs.add(sea)

        # add starting block
        _height = constants.SCREEN_HEIGHT - constants.SEA_HEIGHT - constants.BLOCK_SIZE
        start_block = entities.Wood(constants.BLOCK_SIZE * 5, _height, objs)
        start_block.cost = 0
        objs.add(start_block)
        player_objs.add(start_block)

        return objs, player_objs, enemy_objs

    def set_ui(self):
        """generate UI for game"""
        self.ui_objs = pygame.sprite.Group()

        block = gui.Wood(0,0)
        self.ui_objs.add(block)

        rewood = gui.ReinforcedWood(constants.BLOCK_SIZE,0)
        self.ui_objs.add(rewood)

        cat = gui.Catapult(constants.BLOCK_SIZE*2,0)
        self.ui_objs.add(cat)

        can = gui.Cannon(constants.BLOCK_SIZE*3,0)
        self.ui_objs.add(can)

    def update(self):
        # get block state
        state = getattr(self, self.block_state)
        state()

        self.enemy.think()

        self.get_mouse()


    def get_mouse(self):
        # print 'mouse at', pygame.mouse.get_pos()

        _pos = list(pygame.mouse.get_pos())
        _pos[0] = _pos[0] // constants.BLOCK_SIZE * constants.BLOCK_SIZE
        _pos[1] = _pos[1] // constants.BLOCK_SIZE * constants.BLOCK_SIZE
        _buttons = pygame.mouse.get_pressed()

        # Left click
        if _buttons[0]:
            self.create_block(self.current_block, _pos)

        # Right click
        elif _buttons[2]:
            self.delete_block(_pos)

    def create_block(self, block, pos):
        """create block at pos"""
        can_build = 0

        # check if within boundaries
        if pos[0] >= constants.BUILD_CONSTRAINT:
            return

        # before placing a block, check if the player has pushed a UI element:
        for _i in self.ui_objs:
            if _i.rect.collidepoint(pos[0]+1,pos[1]+1):
                self.block_state = _i.entity_id

        # loop through all blocks and check if it can be placed there.
        for _i in self.level_objs:
            if _i.entity_id != 'sea':
                # if pos is taken, do nothing and cancel everything
                if _i.rect.collidepoint(pos[0] + 1, pos[1] + 1):
                    return

                if block == entities.Catapult or block == entities.Cannon:
                    # can only build blocks above existing
                    if _i.rect.collidepoint(pos[0] + 1, pos[1] + constants.BLOCK_SIZE + 1):
                        # can't build blocks on catapults or cannons
                        if _i.entity_id != 'catapult' and _i.entity_id != 'cannon':
                            can_build = 1  # down

                else:
                    # can only build blocks on top, left or right of existing blocks
                    if _i.rect.collidepoint(pos[0] + constants.BLOCK_SIZE + 1, pos[1] + 1):
                        can_build = 1  # left
                    if _i.rect.collidepoint(pos[0] - 1, pos[1] + 1):
                        can_build = 1  # right
                    if _i.rect.collidepoint(pos[0] + 1, pos[1] + constants.BLOCK_SIZE + 1):
                        can_build = 1  # down

        if can_build == 1:
            _block = block(pos[0], pos[1], self.level_objs)

            if self.money >= _block.cost:
                self.level_objs.add(_block)
                self.player_objs.add(_block)
                self.money += - _block.cost
                return

    def delete_block(self, pos):
        """delete block at position. doesn't delete water"""

        # only delete blocks left of limit
        if pos[0] <= constants.BUILD_CONSTRAINT:
            for _i in self.level_objs:
                if _i.rect.collidepoint(pos[0] + 1, pos[1] + 1):
                    if _i.entity_id != 'sea' and _i.entity_id != 'projectile':
                        _i.kill()
                        self.money += _i.cost / 2

    def block_wood(self):
        self.current_block = entities.Wood

    def block_rewood(self):
        self.current_block = entities.ReinforcedWood

    def block_catapult(self):
        self.current_block = entities.Catapult

    def block_cannon(self):
        self.current_block = entities.Cannon

    def draw_text(self, surface, font):
        label = font.render("Money: {0}".format(str(self.money)), 0, constants.TEXT_COLOUR, constants.BG_COLOUR)
        text_rect = label.get_rect()
        text_rect.topleft = (10, 20)

        surface.blit(label, text_rect)

    def draw_ui(self, surface):
        pass

    def set_background(self, colour):
        bg = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        bg = bg.convert()
        bg.fill(colour)
        return bg

    # def generate_enemy_ship(self, x, y, catapults, cannons, length):
    #     """generate an enemy ship"""
    #
    #     # generate base
    #     for i in range(length):
    #         self._add_enemy_block( entities.Wood ,x + (i * constants.BLOCK_SIZE), y)
    #
    #     # add second layer
    #     for i in range(length):
    #         block = entities.Wood(x + (i * constants.BLOCK_SIZE), y - constants.BLOCK_SIZE, self.level_objs)
    #         block.owner = 'enemy'
    #         if random.randint(0, 1) == 1:
    #             self.level_objs.add(block)
    #             self.enemy_objs.add(block)
    #
    #             if random.randint(0, 1) == 1:
    #                 block = entities.CatapultEnemy(x + (i * constants.BLOCK_SIZE), y - constants.BLOCK_SIZE * 2,
    #                                                self.level_objs)
    #                 block.owner = 'enemy'
    #                 self.level_objs.add(block)
    #                 self.enemy_objs.add(block)
    #


class Enemy:
    def __init__(self, level):
        self.level = level
        self.create_ship()
        self.money = 10
        self.starttime = time.time()
        self.a = 0




    def create_ship(self):
        start_x = constants.SCREEN_WIDTH / 4 * 3 - (8 * constants.BLOCK_SIZE)
        start_y = constants.SCREEN_HEIGHT - constants.SEA_HEIGHT - constants.BLOCK_SIZE
        length  = 20

        # create lowermost level
        for i in range(length):
            self._create_enemy_block( entities.Wood ,start_x + (i * constants.BLOCK_SIZE), start_y)


    def think(self):
        """create blocks and catapults etc. Handle logic and AI here. Called every 0.5s"""
        self.a += 1
        print self.a



    # Private Functions

    def _create_enemy_block(self, block, x, y):
        block = block(x, y, self.level.level_objs)
        block.owner = 'enemy'
        self.level.level_objs.add(block)
        self.level.enemy_objs.add(block)

