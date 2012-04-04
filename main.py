#!/usr/bin/env python

import random
import sprites
import land 
import sys

import pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

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

        self.load_resources()

        self.texture_size = 16

        self.block_size_x = self.width / self.texture_size
        self.block_size_y = self.height / self.texture_size

        lsize = self.land.get_size() >> 2

        """Get random x,y starting location"""
        self.displs_x = abs(int(random.gauss(lsize, lsize)))
        self.displs_y = abs(int(random.gauss(lsize, lsize)))

        self.redraw()

        while 1:
            self.process_events()

    def process_events(self):
        speed_x = self.block_size_x >> 2
        speed_y = self.block_size_y >> 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        key = pygame.key.get_pressed()

        if key[K_ESCAPE]:
            sys.exit()
        elif key[K_RIGHT]:
            self.displs_x += speed_x
            self.displs_x %= self.land.get_size()
        elif key[K_LEFT]:
            self.displs_x -= speed_x
            self.displs_x %= self.land.get_size()
        elif key[K_UP]:
            self.displs_y -= speed_y
            self.displs_y %= self.land.get_size()
        elif key[K_DOWN]:
            self.displs_y += speed_y
            self.displs_y %= self.land.get_size()
        
        mouse = pygame.mouse.get_pressed()

        self.redraw()

        '''Print debug inforation to the screen'''
        values = { 'x' : self.displs_x, 'y' : self.displs_y }
        font = pygame.font.Font(None, 30)
        text = font.render("x = %(x)d y = %(y)d" % values, True, (255, 255, 255), (0,0,0))
        self.screen.blit(text, (0,0))

        if mouse[0]:
            pos = pygame.mouse.get_pos()
            values = { 'x' : pos[0]/16 + self.displs_x, 'y' : pos[1]/16 + self.displs_y }
            font = pygame.font.Font(None, 30)
            text = font.render("Mouse click: x = %(x)d y = %(y)d" % values, True, (255, 255, 255), (0,0,0))
            self.screen.blit(text, (0,20))    
            
        pygame.display.flip()        

        '''------------------------------------'''

    def load_resources(self):
        img_resources = "./images/"
        img_sand = pygame.image.load(img_resources + "sand.png").convert()
        img_forest = pygame.image.load(img_resources + "forest.png").convert()
        img_grass = pygame.image.load(img_resources + "grass.png").convert()
        img_water = pygame.image.load(img_resources + "water.png").convert()

        self.img_blocks = { 0 : img_water,
                            1 : img_sand,
                            2 : img_grass,
                            3 : img_forest }        
                
    def redraw(self):
        for x in range(self.block_size_x):
            for y in range(self.block_size_y):
                val = self.land.value((x+self.displs_x)%land.get_size(),(y+self.displs_y)%land.get_size())
                lb = sprites.LandscapeBlock(self.screen,
                                            x*self.texture_size,
                                            y*self.texture_size,
                                            self.texture_size,
                                            self.texture_size,
                                            self.img_blocks[val])
                lb.draw(self.screen)

        #pygame.display.flip()


if __name__ == "__main__":
    # the approximate size of the map you want (should be large than size of main screen)
    # I will try to think how to fix it later
    size = 1000
    # (change view) roughness, more biggest value will give more filled map
    roughness = 15.0
    # (change map ) you can think about seed as map number or id
    land_id = 123123
    # 0.0 < sea < 0.44 < sand < 0.50 < ground < 0.85 < forest < 1
    heights = [0, 0.55, 0.60, 0.93, 1]

    land = land.Land(size, heights, land_id, roughness, True)

    MainWindow = Main(land, heights)
    MainWindow.set_full_screen()
    MainWindow.main_loop()
