import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        #initialize ship and its starting position
        self.screen = screen
        self.ai_settings = ai_settings
        super(Ship, self).__init__()

        #load the ship image
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #start each new ship at bottom center of screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #store decimal valur for ship center
        self.center = float(self.rect.centerx)

        #movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        #update the ship moving position
        if self.moving_right and (self.rect.right < self.screen_rect.right):
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and (self.rect.left > 0):
            self.center -= self.ai_settings.ship_speed_factor
        
        self.rect.centerx = self.center

    def blitme(self):
        #draw the ship at current position
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        #center the ship
        self.center = self.screen_rect.centerx