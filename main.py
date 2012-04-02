#!/usr/bin/env python

import random
import pygame
from pygame.locals import *
from MapGenerator import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

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


class Main:
    """
    The Main PyMan Class - This class handles the main 
    initialization and creating of the Game.
    """
    
    def __init__(self, land, heights, width=1024, height=768):
        """Initialize"""
        """Initialize PyGame"""
        pygame.init()
        self.land = land
        self.heights = heights
        """Create the Screen"""
        self.screen = pygame.display.set_mode((width, height))
        self.width, self.height = width, height


    def set_full_screen(self):
        modes = pygame.display.list_modes(32)
        if modes:
            pygame.display.set_mode(modes[0], pygame.FULLSCREEN, 32)
        self.width, self.height = modes[0]        

    def main_loop(self):
        """This is the Main Loop of the Game"""

        img_resources = "./images/"
        img_sand = pygame.image.load(img_resources + "sand.png").convert()
        img_forest = pygame.image.load(img_resources + "forest.png").convert()
        img_grass = pygame.image.load(img_resources + "grass.png").convert()
        img_water = pygame.image.load(img_resources + "water.png").convert()

        self.img_blocks = { 0 : img_water,
                            1 : img_sand,
                            2 : img_grass,
                            3 : img_forest }

        self.texture_size = 16

        self.block_size_x = self.width / self.texture_size
        self.block_size_y = self.height / self.texture_size

        lsize = self.land.get_size() >> 2
        self.displs_x = abs(int(random.gauss(lsize, lsize)))
        self.displs_y = abs(int(random.gauss(lsize, lsize)))

        speed_x = self.block_size_x >> 2
        speed_y = self.block_size_y >> 2

        self.redraw()

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sys.exit()
                    if event.key == K_RIGHT:
                        self.displs_x += speed_x
                        self.displs_x %= self.land.get_size()
                    elif event.key == K_LEFT:
                        self.displs_x -= speed_x
                        self.displs_x %= self.land.get_size()
                    elif event.key == K_UP:
                        self.displs_y -= speed_y
                        self.displs_y %= self.land.get_size()
                    elif event.key == K_DOWN:
                        self.displs_y += speed_y
                        self.displs_y %= self.land.get_size()
                    self.redraw()
                
    def redraw(self):
        for x in range(self.block_size_x):
            for y in range(self.block_size_y):
                val = self.land.value((x+self.displs_x)%size,(y+self.displs_y)%size)
                img_block_id = self.get_block_type_id(val)
                lb = LandscapeBlock(self.screen,
                                    x*self.texture_size,
                                    y*self.texture_size,
                                    self.texture_size,
                                    self.texture_size,
                                    self.img_blocks[img_block_id])
                lb.draw(self.screen)
        pygame.display.flip()

    def get_block_type_id(self, val):
        for i in range(len(self.heights)-1):
            if self.heights[i] <= val <= self.heights[i+1]:
                return i        


if __name__ == "__main__":
    # the approximate size of the map you want (should be large than size of main screen)
    # I will try to think how to fix it later
    size = 1000
    # (change view) roughness, more biggest value will give more filled map
    roughness = 15.0
    # (change map ) you can think about seed as map number or id
    seed = 123123
    # 0.0 < sea < 0.44 < sand < 0.50 < ground < 0.85 < forest < 1
    heights = [0, 0.55, 0.60, 0.93, 1]

    land = DiamondSquare(size, roughness, seed, True)

    MainWindow = Main(land, heights)
    #MainWindow.set_full_screen()
    MainWindow.main_loop()
