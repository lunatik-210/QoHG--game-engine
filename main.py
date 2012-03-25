#!/usr/bin/env python

from Tkinter import *
from MapGenerator import *
import sys

class Example(Frame):
    def __init__(self, parent, size, hight_map, land):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        self.land = land
        self.size = size
        self.hight_map = hight_map
        
    def initUI(self):
        self.parent.title("Colors")        
        self.pack(fill=BOTH, expand=1)               
        canvas = Canvas(self)
        a = 5
        print "Rendering map..."
        for x in range(size):
            sys.stdout.write(".")
            sys.stdout.flush()
            for y in range(size):
                
                val = land.value(x,y)

                color = "Blue"
                if val > hight_map[0] and val < hight_map[1]:
                    color = "Yellow"
                if val >= hight_map[1] and val < hight_map[2]:
                    color = "Black"
                if val >= hight_map[2]:
                    color = "Green"
                canvas.create_rectangle(a*x, a*y, 2*a*x, 2*a*y, 
                    outline="Black", fill=color)          
        canvas.pack(fill=BOTH, expand=1)
        print ""
        print "Rendering map... - Done"

if __name__ == "__main__":
    # the approximate size of the map you want
    size = 100
    # roughness, live it as 10.0
    roughness = 10.0
    # map number
    seed = 232
    # 0.0 < blue < 0.44 < yellow < 0.50 < black < 0.85 < Green < 1
    hight_map = [0.44, 0.50, 0.85]


    land = DiamondSquare(size, roughness, seed)
    size = land.getSize()
            
    root = Tk()
    ex = Example(root, size, hight_map, land)
    root.geometry("500x500+300+300")
    root.mainloop()
     




