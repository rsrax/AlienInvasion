import sys
import pygame
import ctypes
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from menu import Menu
from scoreboard import Scoreboard


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
        ctypes.windll.user32.SetProcessDPIAware()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.background_image = pygame.image.load(
            "./images/BG.png").convert()
        self.mainmenu = Menu(self)
        # Create an instance to store the game statistics
        # And create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        self.game_over_sound = pygame.mixer.Sound("./sounds/game_over.wav")
        self.level_lost_sound = pygame.mixer.Sound("./sounds/Lose.wav")

    def _create_fleet(self):
        """ Create the fleet of aliens """
        # Create an alien and find the number of aliens in a row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_aliens_x = available_space_x // (3*alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3*alien_height)-3*ship_height)
        number_rows = available_space_y // (3*alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # Create an alien and place it in the row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = 3 * alien_width + 3 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 3*alien.rect.height * row_number
        self.aliens.add(alien)

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
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

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
        self.screen.blit(self.background_image, [0, 0])
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Show the score.
        self.sb.show_score()

        # Refresh the screen frames, update display
        pygame.display.flip()

    def _update_aliens(self):
        """ 
            1. Check if the fleet is at an edge
            2. Update the position of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collision.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_alien_bottom()

    def _fire_bullet(self):
        """ Create a new bullet and add it to the bullets group """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """ Update position of the bullets and get rid of old bullets. """
        # Update bullet positions
        self.bullets.update()

        # Get rid of bullets that have disappeared from the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """ Respond to bullet-alien collisions """
        # Collision sound, DIE ALIEN!
        for bullet in self.bullets.sprites():
            for alien in self.aliens.sprites():
                if bullet.rect.colliderect(alien.rect):
                    bullet.boom_sound.play()
                    self.settings.alien_speed += 0.0025
        # Check for any bullets that have hit an alien
        # If so, get rid of the alien and the bullet
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _check_fleet_edges(self):
        """ Respond appropriately if any aliens have reached the edges """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """ Drop the entire fleet and change its direction """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """ Respond to the ship being hit by an alien. """

        if self.stats.ships_left > 0:
            # Decrement ships left.
            self.stats.ships_left -= 1

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Crash sound.
            pygame.mixer.Sound.play(self.level_lost_sound)

            # Pause.
            sleep(0.75)
        else:
            pygame.mixer.Sound.play(self.game_over_sound)
            sleep(4.5)
            self.stats.game_active = False

    def _check_alien_bottom(self):
        """ Check whether an alien has reached the bottom of the screen. """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def run_game(self):
        """ 
        * Start the main loop for the game. *
        """
        while True:
            if self.settings.show_menu:
                self.mainmenu.main_menu()
                self.settings.show_menu = self.mainmenu.show_menu
                self.stats.game_active = self.mainmenu.game_active
                if not self.settings.show_menu:
                    self.settings.initialize_dynamic_settings()
                    self.stats.reset_stats()
                    self.sb.prep_score()
                    self.sb.prep_level()

                    # Get rid of any remaining aliens and bullets.
                    self.aliens.empty()
                    self.bullets.empty()

                    # Create a new fleet and center the ship.
                    self._create_fleet()
                    self.ship.center_ship()
            else:
                self._check_events()
                if self.stats.game_active:
                    self.ship.update()
                    self._update_bullets()
                    self._update_aliens()
                else:
                    self.settings.show_menu = True
                    continue
                self._update_screen()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
