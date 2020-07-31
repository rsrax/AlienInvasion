class GameStats:
    """ Track statistics for Alien Invasion. """

    def __init__(self, ai_game):
        """ Initialize statistics. """
        self.settings = ai_game.settings
        self.reset_stats()
        # Start Alien Invasion in Active state.
        self.game_active = False

        # High Score can't be reset.
        self.high_score = self.get_high_score()

    def reset_stats(self):
        """ Initialize statistics that can change during the game. """
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

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
