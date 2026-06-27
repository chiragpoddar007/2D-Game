import pygame
import settings

class Button:
    def __init__(self,text,x,y, width, height, color):
        self.rect = pygame.Rect((x,y,width,height))
        self.base_color = color
        self.hover_color = settings.HOVER_COLOR
        self.text = text
        self.font = pygame.font.SysFont(None,40)

    def draw(self,screen):
        # pygame.draw.rect(screen, self.color,self.rect)
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect, border_radius = 12)
        else:
            pygame.draw.rect(screen, self.base_color, self.rect, border_radius = 12)

        text_surface = self.font.render(self.text,True,(255,255,255))
        text_rect = text_surface.get_rect(center = self.rect.center)
        screen.blit(text_surface,text_rect)

    def is_clicked(self,mouse_pos):
        return self.rect.collidepoint(mouse_pos)
        