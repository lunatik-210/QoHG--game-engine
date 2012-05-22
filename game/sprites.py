
import pygame

class LandscapeBlock(pygame.sprite.Sprite):
    """
    Landscape Block sprite
    There are 4 types of it:
        Water < Sand < Grass < Forest
    """
    def __init__(self, parent, x, y, w, h, texture):
        self.texture = texture
        self.x, self.y = x, y
    
    def draw(self, parent):
        self.texture.draw(parent, (self.x, self.y))