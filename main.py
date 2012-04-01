#!/usr/bin/env python

import pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class PyManMain:
    """The Main PyMan Class - This class handles the main 
    initialization and creating of the Game."""
    
    def __init__(self, land, width=1024,height=768):
        """Initialize"""
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        self.land = land
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
        self.block_size = 32
        self.block_size_x = self.width / self.block_size
        self.block_size_y = self.height / self.block_size
        speed = 10

        heights = [0, 0.60, 0.70, 0.95, 1]

        self.redraw()

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
        
                elif event.type == KEYDOWN:
                    if (event.key == K_RIGHT):
                        self.displs_x += speed
                        self.displs_x %= land.getSize()
                    elif (event.key == K_LEFT):
                        self.displs_x -= speed
                        self.displs_x %= land.getSize()
                    elif (event.key == K_UP):
                        self.displs_y -= speed
                        self.displs_y %= land.getSize()
                    elif (event.key == K_DOWN):
                        self.displs_y += speed
                        self.displs_y %= land.getSize()
                    
                    self.redraw()
                
    def redraw(self):
        for x in range(0,self.block_size):
            for y in range(0,self.block_size):
                pygame.draw.rect( self.screen, self.colors[self.land[x+self.displs_x][y+self.displs_y]], 
                                  (x*self.block_size_x, y*self.block_size_y, self.block_size_x, self.block_size_y))
            #print "x = {} y = {}".format(x+self.displs_x, y+self.displs_y)
        pygame.display.flip()


if __name__ == "__main__":
    # the approximate size of the map you want
    size = 500
    # (change view) roughness, more biggest value will give more filled map
    roughness = 35.0
    # (change map ) you can think about seed as map number or id
    seed = 234
    # 0.0 < sea < 0.44 < sand < 0.50 < ground < 0.85 < forest < 1
    heights = [0, 0.60, 0.70, 0.95, 1]

    land = DiamondSquare(size, roughness, seed, True)
    size = land.getSize()

    grid = land.pregenerate()
    height_map = land.getHeightMap(heights)

    MainWindow = PyManMain(height_map)
    MainWindow.MainLoop()

    #root = Tk()
    #ex = Example(root)

    #root.geometry("500x500+300+300")
    #root.mainloop()


