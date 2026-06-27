import pygame
import settings

class Player:
    def __init__(self):
        self.image = pygame.image.load("assets//Image//player_ship.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(100,100))

        self.rect = self.image.get_rect()
        self.rect.center = (400,500)

        self.speed = settings.PLAYER_SPEED

        self.width = self.rect.width

    def move(self,screen_width,screen_height):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        elif keys[pygame.K_UP]:
            self.rect.x -= self.speed

        elif keys[pygame.K_DOWN]:
            self.rect.x += self.speed

        # Boundary limits
        if self.rect.left < 0:
            self.rect.left = 0
        
        elif self.rect.right > screen_width:
            self.rect.right = screen_width

        elif self.rect.top < 0:
            self.rect.top = 0

        elif self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

        # Boundaries
        self.rect.clamp_ip(pygame.Rect(0,0,screen_width,screen_height))

    def draw(self,screen):
        screen.blit(self.image,self.rect)