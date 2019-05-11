from sprite import Sprite

Reset = u"\u001b[0m"

class Paddle(Sprite):
	
    def __init__(self, color, width, height, parentWidth, parentHeight, direction = 'u'):
        Sprite.__init__(self, color, width, height, direction)
        self.parentHeight = parentHeight
        self.parentWidth = parentWidth

    def __str__(self):
        return str(" " * self.width)

    def setHeight(self, height):
        if height != self.height:
            self.height = height

    def move(self, pos):
        self.setYPos(int(pos))

    def render(self, dir = None, x = None, y = None):
        if (x != None and y != None):
            self.printToConsole(self.getColor(), x, y, self, self.parentWidth, self.parentHeight)
            return
	if dir != None and not 's' in dir and int(dir) != self.getYPos():
		for i in range(0, self.getHeight()):
		    self.printToConsole(Reset, self.getXPos(), self.getYPos() + i, self, self.parentWidth, self.parentHeight)
		self.move(dir)
		for i in range(0, self.getHeight()):
		    self.printToConsole(self.getColor(), self.getXPos(), self.getYPos() + i, self, self.parentWidth, self.parentHeight)
