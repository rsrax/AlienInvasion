import sys
import pygame
from settings import Settings
from ship import Ship


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
        self.ship = Ship(self)

    def _check_events(self):
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """ 
        * Respond to keypresses. *
        """
        if event.key == pygame.K_RIGHT:
            self.ship.move_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.move_left = True

    def _check_keyup_events(self, event):
        """ 
        * Respond to key releases. *
        """
        if event.key == pygame.K_RIGHT:
            self.ship.move_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.move_left = False

    def _update_screen(self):
        # Redraw the screen after each pass.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        # Refresh the screen frames, update display
        pygame.display.flip()

    def run_game(self):
        """ 
        * Start the main loop for the game. *
        """
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
