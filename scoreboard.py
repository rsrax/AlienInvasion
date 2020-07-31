import pygame.font


class Scoreboard:
    """ A class to report scoring information. """

    def __init__(self, ai_game):
        """ Initialize scorekeeping attributes. """
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information.
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 35)

        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def prep_score(self):
        """ Turn the score into a rendered image. """
        rounded_score = round(self.stats.score, -1)
        score_str = "Score - " + "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color)

        # Display the score at the top of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """ Turn the high score into a rendered image. """
        high_score = round(self.stats.high_score, -1)
        high_score_str = "HiScore - " + "{:,}".format(high_score)
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """ Turn the level text into a rendered image. """
        level = self.stats.level
        level_str = "Level - " + str(level)
        self.level_image = self.font.render(level_str, True, self.text_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def check_high_score(self):
        """ Check to see if there's a new high score. """
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.save_high_score()
            self.prep_high_score()

    def show_score(self):
        """ Draw score to the screen. """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

    def save_high_score(self):
        try:
            # Write the file to disk
            high_score_file = open("high_score.dat", "w")
            high_score_file.write(str(self.stats.high_score))
            high_score_file.close()
        except IOError:
            # Hm, can't write it.
            pass
