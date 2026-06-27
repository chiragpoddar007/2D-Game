import pygame
import random
import settings

class Enemy:
    def __init__(self,screen_width):
        # Image
        self.image = pygame.image.load("assets/Image/enemy_ship.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(80,80))

        # Create rect from image
        self.rect = self.image.get_rect()

        # Random horizontal position
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = -self.rect.height # Start above the screen

        # Random speed
        self.speed = random.randint(settings.ENEMY_MIN_SPEED,
                                    settings.ENEMY_MAX_SPEED)
        
    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image,self.rect)