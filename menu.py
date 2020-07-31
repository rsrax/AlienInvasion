import pygame
import sys


class Menu:
    """ A class that represents the main menu of the game. """

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.background_image = pygame.image.load(
            "./images/background.png").convert_alpha()
        self.logo = pygame.image.load(
            "./images/alien_invasion.png").convert_alpha()
        self.logo_rect = self.logo.get_rect()
        self.play_button = pygame.image.load(
            "./images/play.png").convert_alpha()
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_selected = pygame.image.load(
            "./images/play_selected.png").convert_alpha()
        self.play_button_selected_rect = self.play_button_selected.get_rect()
        self.exit_button = pygame.image.load(
            "./images/exit.png").convert_alpha()
        self.exit_button_rect = self.exit_button.get_rect()
        self.exit_button_selected = pygame.image.load(
            "./images/exit_selected.png").convert_alpha()
        self.exit_button_selected_rect = self.exit_button_selected.get_rect()
        self.selected_index = 1

        # Logo Positioning
        self.logo_rect.y = self.logo.get_height()
        self.logo_rect.centerx = self.screen.get_width()/2

        # Inactive Button Positioning
        self.play_button_rect.y = 2*self.logo.get_height() + \
            2*self.play_button.get_height()
        self.play_button_rect.centerx = self.screen.get_width()/2
        self.exit_button_rect.y = self.play_button_rect.y + \
            1.5*self.exit_button.get_height()
        self.exit_button_rect.centerx = self.screen.get_width()/2

        # Active Button Positioning
        self.play_button_selected_rect = self.play_button_rect
        self.exit_button_selected_rect = self.exit_button_rect

        # Main Menu Music
        pygame.mixer.music.load('./sounds/Theme.wav')

    def main_menu(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
        self.show_menu = True
        self.game_active = False
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background_image, [0, 0])
        self.screen.blit(self.logo, self.logo_rect)
        self._check_events()
        self._update_menu()
        pygame.display.flip()

    def _update_menu(self):
        if self.selected_index == 1:
            self.screen.blit(self.play_button_selected,
                             self.play_button_selected_rect)
            self.screen.blit(self.exit_button, self.exit_button_rect)
        else:
            self.screen.blit(self.play_button, self.play_button_rect)
            self.screen.blit(self.exit_button_selected,
                             self.exit_button_selected_rect)

    def _check_events(self):
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.selected_index == 1:
                        self.selected_index = 2
                    else:
                        self.selected_index = 1
                elif event.key == pygame.K_UP:
                    if self.selected_index == 1:
                        self.selected_index = 2
                    else:
                        self.selected_index = 1
                elif event.key == pygame.K_q:
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    if self.selected_index == 1:
                        pygame.mixer.music.fadeout(1500)
                        self.show_menu = False
                        self.game_active = True
                    else:
                        sys.exit()
