import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """ A class to manage the bullets fired from the ship. """

    def __init__(self, ai_game):
        """ Create a bullet at the ship's current position """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        # Load bullet SFX and play the sound for every bullet created
        self.bullet_sound = pygame.mixer.Sound("./sounds/PewPew.wav")
        self.bullet_sound.play()
        # Load collision SFX
        self.boom_sound = pygame.mixer.Sound("./sounds/Die.wav")
        # Create a bullet at (0,0) and then set the correct position
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        self.rect.y -= 5

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

    def update(self):
        """ Move the bullet up the screen. """
        # Update the decimal position of the bullet.
        self.y -= self.settings.bullet_speed
        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """ Draw the bullet to the screen """
        pygame.draw.rect(self.screen, self.color, self.rect)
