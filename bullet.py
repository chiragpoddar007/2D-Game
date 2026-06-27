import pygame
import settings

class Bullet:
    def __init__(self,x,y):
        self.image = pygame.image.load("assets//Image//bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(40,80))

        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        # Speed of the bullet
        self.speed = settings.BULLET_SPEED

    def move(self):
        self.rect.y -= self.speed # Move upward

    def draw(self,screen):
        screen.blit(self.image,(self.rect))