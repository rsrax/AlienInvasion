import sys
import pygame


class AlienInvasion:
    """ 
    * Overall class to manage the game assets and behavior. *
    """

    def __init__(self):
        """ 
        * Initializes the game and creates game resources. *
        """
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
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

            # Refresh the screen frames, update display
            pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
