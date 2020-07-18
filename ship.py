import pygame


class Ship:
    """
    * A class to manage the ship *
    """

    def __init__(self, ai_game):
        """
        * Initialize the ship and its starting position. *
        """
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship image and get its rectangle
        self.image = pygame.image.load("./images/ship.bmp")
        self.rect = self.image.get_rect()

        # Ship starts at the middle of the bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)

        # Movement Flags
        self.move_right = False
        self.move_left = False

    def update(self):
        """
        * Updates the position of the ship. *
        """
        if self.move_right:
            self.x += self.settings.ship_speed
        elif self.move_left:
            self.x -= self.settings.ship_speed

        # Update rect from self.x
        self.rect.x = self.x

    def blitme(self):
        """
        * Draw the ship at its current location. *
        """
        self.screen.blit(self.image, self.rect)
