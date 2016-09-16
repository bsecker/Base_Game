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
        self.print_frames = 0
        self.fps_timer = 0.0
        self.print_fps_frequency = 1000

    def go(self):
        """main loop"""
        while self.game_running:

            # Update
            self.event_loop()
            self.update()

            # Draw
            self.draw(self.screen)
            self.clock.tick(constants.FPS)
            pygame.display.update()

        pygame.quit()

    def update(self):
        state = getattr(self, self.game_state)
        state()

        self.levelmanager.update()

        for _i in self.levelmanager.level_objs:
            _i.update()

        elapsed_milliseconds = self.clock.get_time()
        #Print the fps that the game is running at.
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

    def draw(self, surface):
        surface.fill(constants.BG_COLOUR)

        for _i in self.levelmanager.level_objs:
            _i.draw(surface)

    def state_build(self):
        pass

    def state_fight(self):
        pass

    def state_menu(self):
        pass

if __name__ == '__main__':
    game = World()
    game.go()