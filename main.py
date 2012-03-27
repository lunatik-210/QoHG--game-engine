#!/usr/bin/env python
  
from Tkinter import *
from MapGenerator import *

import pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        
    def initUI(self):

        self.parent.title("Colors")        
        self.pack(fill=BOTH, expand=1)               
        canvas = Canvas(self)
        a = 1
        print "Rendering map...", size, "x", size
        for x in range(size):
            for y in range(size):
                val = height_map[x][y]
                color = "Blue"
                if val == 1:
                    color = "Yellow"
                if val == 2:
                    color = "Black"
                if val == 3:
                    color = "Green"
                canvas.create_rectangle(a*x, a*y, 2*a*x, 2*a*y, 
                    outline=color, fill=color)          
        canvas.pack(fill=BOTH, expand=1)        
        print "Rendering map... - Done", size, "x", size

class PyManMain:
    """The Main PyMan Class - This class handles the main 
    initialization and creating of the Game."""
    
    def __init__(self, width=640,height=480):
        """Initialize"""
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        self.width = width
        self.height = height
        """Create the Screen"""
        self.screen = pygame.display.set_mode((self.width, self.height))

    def MainLoop(self):
        """This is the Main Loop of the Game"""
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()

if __name__ == "__main__":
    # the approximate size of the map you want
    size = 500
    # (change view) roughness, more biggest value will give more filled map
    roughness = 25.0
    # (change map ) you can think about seed as map number or id
    seed = 232345345
    # 0.0 < sea < 0.44 < sand < 0.50 < ground < 0.85 < forest < 1
    heights = [0, 0.60, 0.70, 0.95, 1]

    land = DiamondSquare(size, roughness, seed, True)
    size = land.getSize()

    #MainWindow = PyManMain()
    #MainWindow.MainLoop()
    grid = land.pregenerate()
    height_map = land.getHeightMap(heights)

    root = Tk()
    ex = Example(root)

    root.geometry("500x500+300+300")
    root.mainloop()


