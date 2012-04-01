#!/usr/bin/env python

import random
import pygame
from pygame.color import THECOLORS
from pygame.locals import *
from MapGenerator import *

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
        """Set the window Size"""
        self.land = land
        self.heights = heights
        self.width = width
        self.height = height
        """Create the Screen"""
        self.screen = pygame.display.set_mode((self.width, self.height))

    def MainLoop(self):
        """This is the Main Loop of the Game"""

        self.colors = { 0 : THECOLORS["blue"],
                        1 : THECOLORS["yellow"],
                        2 : THECOLORS["black"],
                        3 : THECOLORS["green"] }
        self.block_size = 64
        self.block_size_x = self.width / self.block_size
        self.block_size_y = self.height / self.block_size

        lsize = self.land.getSize() >> 2
        self.displs_x = abs(int(random.gauss(lsize, lsize)))
        self.displs_y = abs(int(random.gauss(lsize, lsize)))

        speed = self.block_size / 4

        self.redraw()

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == KEYDOWN:
                    if (event.key == K_RIGHT):
                        self.displs_x += speed
                        self.displs_x %= self.land.getSize()
                    elif (event.key == K_LEFT):
                        self.displs_x -= speed
                        self.displs_x %= self.land.getSize()
                    elif (event.key == K_UP):
                        self.displs_y -= speed
                        self.displs_y %= self.land.getSize()
                    elif (event.key == K_DOWN):
                        self.displs_y += speed
                        self.displs_y %= self.land.getSize()
                    self.redraw()
                
    def redraw(self):
        for x in range(self.block_size):
            for y in range(self.block_size):
                val = self.land.value((x+self.displs_x)%size,(y+self.displs_y)%size)
                color_id = self.get_color_id(val)
                pygame.draw.rect( self.screen, self.colors[color_id], 
                                  (x*self.block_size_x, y*self.block_size_y, self.block_size_x, self.block_size_y))
        pygame.display.flip()

    def get_color_id(self, val):
        for i in range(len(self.heights)-1):
            if self.heights[i] <= val <= self.heights[i+1]:
                return i


if __name__ == "__main__":
    # the approximate size of the map you want (should be large than size of main screen)
    # I will try to think how to fix it later
    size = 1024
    # (change view) roughness, more biggest value will give more filled map
    roughness = 15.0
    # (change map ) you can think about seed as map number or id
    seed = 123123
    # 0.0 < sea < 0.44 < sand < 0.50 < ground < 0.85 < forest < 1
    heights = [0, 0.55, 0.60, 0.93, 1]

    land = DiamondSquare(size, roughness, seed, True)
    #grid = land.pregenerate()
    #size = land.getSize()
    #height_map = land.getHeightMap(heights)

    MainWindow = Main(land, heights)
    MainWindow.MainLoop()
