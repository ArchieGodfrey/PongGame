from sprite import Sprite

Reset = u"\u001b[0m"

class Net(Sprite):
	
    def __init__(self, color, width, height, parentWidth, parentHeight):
        Sprite.__init__(self, color, width, height)
        self.parentHeight = parentHeight
        self.parentWidth = parentWidth
        self.currentPixels = []

    def __str__(self):
        return str(" " * self.width)

    def checkPixel(self, x, y):
        for pixel in self.currentPixels:
            if pixel[0] == x and pixel[1] == y:
                return True
        return False

    def initalRender(self):
        xPos = self.getXPos()
        yPos = self.getYPos()
        for i in range(0, int(self.parentHeight / 2)):
            if i % 2 > 0:
                for j in range(0, self.getHeight()):
                    self.currentPixels.append([xPos, yPos + j + (i * self.getHeight())])

    def render(self, x = None, y = None):
        for pixel in self.currentPixels:
            if (x != None and y != None):
		    if self.checkPixel(x, y):
		        self.printToConsole(self.getColor(), x, y, self, self.parentWidth, self.parentHeight)
		    else:
			self.printToConsole(Reset, x, y, self, self.parentWidth, self.parentHeight)
            	    return
            self.printToConsole(self.getColor(), pixel[0], pixel[1], self, self.parentWidth, self.parentHeight)
