
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(%d, %d)" % (self.x, self.y)

    def __eq__(self, pos):
        return ( self.x == pos.x and 
                 self.y == pos.y )

    def __repr__(self):
        return "(%d,%d)" % (self.x, self.y)

    def __add__(self, pos):
        return Position(self.x + pos.x, self.y + pos.y)

    def __sub__(self, pos):
        return Position(self.x - pos.x, self.y - pos.y)

    def __mod__(self, value):
        return Position(self.x % value, self.y % value)    

    def __div__(self, value):    
        return Position(self.x / value, self.y / value)    

    def left(self):
        return Position(self.x-1, self.y)

    def right(self):
        return Position(self.x+1, self.y)

    def bottom(self):
        return Position(self.x, self.y+1)

    def top(self):
        return Position(self.x, self.y-1)

    def lefttop(self):
        return Position(self.x-1, self.y-1)

    def righttop(self):
        return Position(self.x+1, self.y-1)

    def leftbottom(self):
        return Position(self.x-1, self.y+1)

    def rightbottom(self):
        return Position(self.x+1, self.y+1)

    def value(self):
        return (self.x, self.y)

    def get_neighbors(self):
        return (self.left(), self.top(), self.right(), self.bottom(),
                self.lefttop(), self.righttop(), self.leftbottom(), self.rightbottom())
        