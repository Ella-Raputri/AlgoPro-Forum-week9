import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf

def run_game():
    #initialize game
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #make the play button
    play_button = Button(ai_settings, screen, "Play")

    #instance to store game stats
    stats = GameStats(ai_settings)
    #instance to store scoreboard
    sb = Scoreboard(ai_settings, screen, stats)

    #make a ship 
    ship = Ship(ai_settings,screen)
    #make a group to store bullets
    bullets = Group()
    #make an alien 
    aliens = Group()

    #create a fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    #start main loop for game 
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
        
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()
