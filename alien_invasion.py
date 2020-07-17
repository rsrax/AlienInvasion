import sys
import pygame
from settings import Settings


class AlienInvasion:
    """ 
    * Overall class to manage the game assets and behavior. *
    """

    def __init__(self):
        """ 
        * Initializes the game and creates game resources. *
        """
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        """ 
        * Start the main loop for the game. *
        """
        while True:
            # Watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            # Redraw the screen after each pass.
            self.screen.fill(self.settings.bg_color)
            # Refresh the screen frames, update display
            pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
