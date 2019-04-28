from sprite import Sprite

Reset = u"\u001b[0m"

class Paddle(Sprite):
	
    def __init__(self, color, width, height, parentWidth, parentHeight, direction = 'u'):
        Sprite.__init__(self, color, width, height, direction)
        self.parentHeight = parentHeight
        self.parentWidth = parentWidth

    def __str__(self):
        return str(" " * self.width)

    def move(self, dir):
        if (self.getYPos() != 0 + int(self.height / 2)) and (self.getYPos() != self.parentHeight - int(self.height / 2)):
            self.dir = dir
            self.performMove(dir)

    def render(self, x = None, y = None):
        if (x != None and y != None):
            self.printToConsole(self.getColor(), x, y, self, self.parentWidth, self.parentHeight)
            return
        for i in range(0, self.getHeight()):
            self.printToConsole(Reset, self.getXPos(), self.getYPos() + i, self, self.parentWidth, self.parentHeight)
        if dir != None:
            self.move(dir)
        for i in range(0, self.getHeight()):
            self.printToConsole(self.getColor(), self.getXPos(), self.getYPos() + i, self, self.parentWidth, self.parentHeight)
