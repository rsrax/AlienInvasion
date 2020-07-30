import pygame


class Menu:
    """ A class that represents the main menu of the game. """

    def __init__(self, ai_game):
        self.logo = pygame.image.load(
            "./images/alien_invasion.png").convert_alpha()
        self.play_button = pygame.image.load(
            "./images/play.png").convert_alpha()
        self.play_button_selected = pygame.image.load(
            "./images/play.png").convert_alpha()
        self.exit_button = pygame.image.load(
            "./images/play.png").convert_alpha()
        self.exit_button_selected = pygame.image.load(
            "./images/play.png").convert_alpha()
