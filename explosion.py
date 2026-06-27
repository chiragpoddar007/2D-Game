import pygame

class Explosion:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.radius = 5
        self.max_radius = 35
        self.growth_speed = 4
        self.finished = False

    def update(self):
        self.radius += self.growth_speed
        if self.radius >= self.max_radius:
            self.finished = True

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 150, 0), (self.x, self.y), self.radius)
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), self.radius // 2)