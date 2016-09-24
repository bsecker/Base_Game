"""main module for controlling game state etc."""
import gen
import constants
import pygame

class World:
    def __init__(self):
        self.game_state = "state_build"

        # Initialise Pygame
        pygame.init()
        screen_size = (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption(constants.WIN_CAPTION)

        self.levelmanager = gen.LevelManager()

        self.clock = pygame.time.Clock()
        self.game_running = True
        self.print_frames = 1
        self.fps_timer = 0.0
        self.print_fps_frequency = 1000

        self.text_font = pygame.font.SysFont("monospace", 20)

    def go(self):
        """main loop"""
        while self.game_running:

            # Update
            self.event_loop()
            self.update()

            # Draw
            self.draw(self.screen)
            self.clock.tick(constants.FPS)

        pygame.quit()

    def update(self):
        state = getattr(self, self.game_state)
        state()

        self.levelmanager.update()
        self.check_winloss()

        # add money over time
        self.levelmanager.money += 0.01

        for _object in self.levelmanager.level_objs.sprites():
            _object.update()

            if _object.alive == False:
                _object.kill()

            if _object.entity_id == 'projectile':
                # do projectile collisions
                cols = pygame.sprite.spritecollide(_object, self.levelmanager.level_objs, 0)
                for collision in cols:

                    # collision with sea
                    if collision.entity_id == 'sea':
                        _object.kill()
 
                    # collision with wood, catapults, cannons, etc
                    if collision.entity_id == 'wood' or collision.entity_id == 'rewood' or collision.entity_id == 'catapult' or collision.entity_id == 'cannon':
                        collision.health +=- 1
                        _object.kill()

                        # kill if less than zero
                        if collision.health <= 0:
                            collision.alive = False

                            # give money if enemy block
                            if collision.owner == 'enemy':
                                self.levelmanager.money += collision.cost

                                
        
        #Print the fps that the game is running at.
        elapsed_milliseconds = self.clock.get_time()
        if self.print_frames:
            self.fps_timer += elapsed_milliseconds
            if self.fps_timer > self.print_fps_frequency:
                print "FPS: ", self.clock.get_fps()
                self.fps_timer = 0.0

    def event_loop(self):
        """main event loop"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False

            if event.type == pygame.KEYDOWN:
                # Quit Game
                if event.key == pygame.K_ESCAPE:
                    self.game_running = False

                if event.key == pygame.K_1:
                    self.levelmanager.block_state = 'block_wood'

                if event.key == pygame.K_2:
                    self.levelmanager.block_state = 'block_rewood'

                if event.key == pygame.K_3:
                    self.levelmanager.block_state = 'block_catapult'

                if event.key == pygame.K_4:
                    self.levelmanager.block_state = 'block_cannon'

    def draw(self, surface):
        surface.blit(self.levelmanager.background, (0,0))

        self.rects = self.levelmanager.level_objs.draw(surface)
        self.levelmanager.draw_text(surface, self.text_font)

        pygame.display.update()

    def check_winloss(self):
        """check if the amount of blocks on each side is zero.
        player wins when the opposite side is completely annihilated"""
        if len(self.levelmanager.player_objs) == 0:
            print 'player loses'
            return True
        if len(self.levelmanager.enemy_objs) == 0:
            print 'player wins'
            return False

    def state_build(self):
        pass

    def state_fight(self):
        pass

    def state_menu(self):
        pass

if __name__ == '__main__':
    game = World()
    game.go()

