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
        if 'd' in dir or 'u' in dir:
            if (self.getYPos() > int(self.height / 2)) and not 'u' in dir:
                self.dir = dir
                self.performMove(dir)
            if (self.getYPos() < self.parentHeight - self.height) and not 'd' in dir:
                self.dir = dir
                self.performMove(dir)
	elif len(dir) > 1 and self.getYPos() - dir != 0:
		for i in range(self.getYPos(), int(dir[1:])):
			self.performMove(dir)
		if self.getYPos() - dir > 0:
			self.dir = 'u'
		else:
			self.dir = 'd'

    def render(self, dir = None, x = None, y = None):
        if (x != None and y != None):
            self.printToConsole(self.getColor(), x, y, self, self.parentWidth, self.parentHeight)
            return
        for i in range(0, self.getHeight()):
            self.printToConsole(Reset, self.getXPos(), self.getYPos() + i, self, self.parentWidth, self.parentHeight)
        if dir != None:
            self.move(dir)
        for i in range(0, self.getHeight()):
            self.printToConsole(self.getColor(), self.getXPos(), self.getYPos() + i, self, self.parentWidth, self.parentHeight)
