import pygame
import pygame.font
import sys


class Menu:
    """ A class that represents the main menu of the game. """

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.stats = ai_game.stats
        self.ai_game = ai_game

        # Font settings for scoring information.
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 35)

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

        self.controls_image = pygame.image.load("./images/controls.png")
        self.controls_image = pygame.transform.scale(
            self.controls_image, (1000, 300))
        self.controls_image_rect = self.controls_image.get_rect()

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

        # Controls Image
        self.controls_image_rect.bottom = self.screen_rect.bottom - 50
        self.controls_image_rect.centerx = self.screen_rect.centerx

        # Main Menu Music
        pygame.mixer.music.load('./sounds/Theme.wav')

        # High Score
        self.high_score = self.get_high_score()
        self.prep_high_score()

    def get_high_score(self):
        # Default high score.
        high_score = 0

        # Try to read the high score from a file.
        try:
            high_score_file = open("high_score.dat", "r")
            high_score = int(high_score_file.read())
            high_score_file.close()
        except FileNotFoundError:
            # First run, hence, no file, no high score.
            high_score = 0
        except IOError:
            # Error reading file, no high score.
            high_score = 0
        except ValueError:
            # There's a file there, but we don't understand the number.
            high_score = 0

        return high_score

    def prep_high_score(self):
        """ Turn the high score into a rendered image. """
        high_score = round(self.stats.high_score, -1)
        high_score_str = "HiScore - " + "{:,}".format(high_score)
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top + 20

    def main_menu(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.4)
        self.show_menu = True
        self.game_active = False
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background_image, [0, 0])
        self.screen.blit(self.logo, self.logo_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self._check_events()
        self._update_menu()
        self.screen.blit(self.controls_image, self.controls_image_rect)
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
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    if self.selected_index == 1:
                        pygame.mixer.music.fadeout(1500)
                        self.show_menu = False
                        self.game_active = True
                    else:
                        sys.exit()
