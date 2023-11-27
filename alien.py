import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_settings, screen):
        #initialize alien
        super(Alien, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        #load the alien image and set it rect attribute
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        #start each new alien at top left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #store alien exact position
        self.x = float(self.rect.x)
    
    def blitme(self):
        #draw alien
        self.screen.blit(self.image, self.rect)

    def update(self):
        #move alien to right
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True