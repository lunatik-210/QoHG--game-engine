
from Tkinter import *
from MapGenerator import *

class Example(Frame):
    def __init__(self, parent, grid, h):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        self.grid = grid
        self.h = h
        
    def initUI(self):
        self.parent.title("Colors")        
        self.pack(fill=BOTH, expand=1)               
        canvas = Canvas(self)
        left = h / 5
        right = left + (h >> 6)
        tree  = left + (h >> 2)
        print "Rendering map..."
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                a = 2
                color = "Blue"
                if grid[x][y] > left and grid[x][y] < right:
                    color = "Yellow"
                if grid[x][y] >= right and grid[x][y] < tree:
                    color = "Black"
                if grid[x][y] >= tree:
                    color = "Green"
                canvas.create_rectangle(a*x, a*y, 2*a*x, 2*a*y, 
                    outline=color, fill=color)          
        canvas.pack(fill=BOTH, expand=1)
        print "Rendering map... - Done"

if __name__ == "__main__":
    dsize = 500
    h = 1000
    
    print "Building terrain..."
    grid, dsize = generate_map(dsize, h)
    print grid
    print "Building terrain... - Done", dsize, "*", dsize

    root = Tk()
    ex = Example(root, grid, h)
    root.geometry("1000x1000+300+300")
    root.mainloop()       




