#!/usr/bin/env python

import pygame
from pygame.locals import *
from MapGenerator import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class Main:
    """The Main PyMan Class - This class handles the main 
    initialization and creating of the Game."""
    
    def __init__(self, land, heights, width=1024,height=768):
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

        green = (0, 255, 0)
        blue = (0, 0, 255)
        black = (0, 0, 0)
        yellow = (150, 150, 0)

        self.colors = { 0 : blue,
                   1 : yellow,
                   2 : black,
                   3 : green }

        self.displs_x, self.displs_y = 0, 0
        self.block_size = 64
        self.block_size_x = self.width / self.block_size
        self.block_size_y = self.height / self.block_size
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
        for x in range(0,self.block_size):
            for y in range(0,self.block_size):
                val = self.land.value((x+self.displs_x)%size,(y+self.displs_y)%size)
                color_id = self.get_color_id(val)
                pygame.draw.rect( self.screen, self.colors[color_id], 
                                  (x*self.block_size_x, y*self.block_size_y, self.block_size_x, self.block_size_y))
        pygame.display.flip()

    def get_color_id(self, val):
        for i in range(len(self.heights)-1):
            if val >= self.heights[i] and val <= self.heights[i+1]:
                return i


if __name__ == "__main__":
    # the approximate size of the map you want (should be large than size of screen)
    size = 4000
    # (change view) roughness, more biggest value will give more filled map
    roughness = 65.0
    # (change map ) you can think about seed as map number or id
    seed = 1
    # 0.0 < sea < 0.44 < sand < 0.50 < ground < 0.85 < forest < 1
    heights = [0, 0.80, 0.85, 0.98, 1]

    land = DiamondSquare(size, roughness, seed, True)
    #grid = land.pregenerate()
    #size = land.getSize()
    #height_map = land.getHeightMap(heights)

    MainWindow = Main(land, heights)
    MainWindow.MainLoop()


