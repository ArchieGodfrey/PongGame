from sprite import Sprite

Reset = u"\u001b[0m"

class Net(Sprite):
	
    def __init__(self, color, width, height, parentWidth, parentHeight, spacing):
        Sprite.__init__(self, color, width, height)
        self.parentHeight = parentHeight
        self.parentWidth = parentWidth
        self.spacing = spacing

    def __str__(self):
        return str(" " * self.width)

    def render(self, dir = None):
        for i in range(0, int(self.parentHeight / 2)):
            if i % 2 > 0:
                for j in range(0, self.getHeight()):
                    self.printToConsole(self.getColor(), self.getXPos(), self.getYPos() + j + (i * self.getHeight()), self, self.parentWidth, self.parentHeight)
