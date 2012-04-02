
import pygame

class LandscapeBlock(pygame.sprite.Sprite):
    """
    Landscape Block sprite
    There are 4 types of it:
        Water < Sand < Grass < Forest
    """
    def __init__(self, parent, x, y, w, h, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.rect.w, self.rect.h = w, h
    
    def draw(self, parent):
        parent.blit(self.image, self.rect)