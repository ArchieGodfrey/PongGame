from sprite import Sprite
import sys
Reset = u"\u001b[0m"
Black = u"\u001b[40m"

class Score(Sprite):
	
    def __init__(self, color, width, height, parentWidth, parentHeight, number):
        Sprite.__init__(self, color, width, height)
        self.number = number
        self.parentHeight = parentHeight
        self.parentWidth = parentWidth
        self.currentPixels = []

    def getScore(self):
        return self.number
    
    def setScore(self, number):
        self.number = number

    def addPixel(self, x, y):
        self.currentPixels.append([x, y])

    def checkPixel(self, x, y):
        for pixel in self.currentPixels:
            if pixel[0] == x and pixel[1] == y:
                return True
        return False

    def renderPixel(self, x, y):
        self.addPixel(self.getXPos() + x, self.getYPos() + y)
        self.printToConsole(self.getColor(), self.getXPos() + x, self.getYPos() + y, self, self.parentWidth, self.parentHeight)

    def zero(self):
        for i in range(0, self.height):
            self.renderPixel(0,i)
            self.renderPixel(self.width - 1,i)
        for i in range(1, self.width - 1):
            self.renderPixel(i,0)
            self.renderPixel(i, self.height - 1)
    
    def one(self):
        for i in range(0, self.height):
            self.renderPixel(self.width - 1,i)
    
    def two(self):
        for i in range(0, self.height):
            if i < int(self.height / 2):
                self.renderPixel(0,i)
            
        for i in range(0, self.width):
            self.renderPixel(i,0)
            self.renderPixel(i, int(self.height / 2))
            self.renderPixel(i, self.height - 1)
        
    
    def three(self):
        for i in range(0, self.height):
            self.renderPixel(self.width - 1,i)
        for i in range(0, self.width - 1):
            self.renderPixel(i,0)
            self.renderPixel(i, int(self.height / 2))
            self.renderPixel(i, self.height - 1)

    def four(self):
        for i in range(0, self.height):
            self.renderPixel(self.width - 1,i)
        for i in range(int(self.height / 2), self.height):
            self.renderPixel(0,i)
        for i in range(1, self.width - 1):
            self.renderPixel(i,int(self.height / 2))

    def five(self):
        for i in range(0, self.height):
            self.renderPixel(0,i) #Left column
            self.renderPixel(self.width - 1,i) # Right column
        for i in range(1, self.width - 1):
            self.renderPixel(i,0) #Bottom
	    self.renderPixel(i, int(self.height / 2)) #Middle
            self.renderPixel(i, self.height - 1) #Top

    def six(self):
        for i in range(0, self.height):
            if i < int(self.height / 2):
                self.renderPixel(0,i)
        for i in range(0, self.width):
            self.renderPixel(i,0)
            self.renderPixel(i, int(self.height / 2))
            self.renderPixel(i, self.height - 1)

    def seven(self):
        for i in range(0, self.height):
            self.renderPixel(self.width - 1,i) # Right column
        self.renderPixel(int(self.height / 2), self.height) #Middle
    
    def eight(self):
        for i in range(0, self.height):
            self.renderPixel(0,i)
            self.renderPixel(self.width - 1,i)
        for i in range(1, self.width - 1):
            self.renderPixel(i,0)
            self.renderPixel(i, int(self.height / 2))
            self.renderPixel(i, self.height - 1)

    def nine(self):
        for i in range(0, self.height):
            self.renderPixel(self.width - 1,i)
        for i in range(int(self.height / 2), self.height):
            self.renderPixel(0,i)
        for i in range(1, self.width - 1):
            self.renderPixel(i,int(self.height / 2))
            self.renderPixel(i, self.height - 1)

    def winner(self):
        self.renderPixel(0,int(self.height / 2))
	self.renderPixel(int(self.width / 2),0)
	self.renderPixel(self.width,int(self.height / 2))

    def clear(self):
        self.currentPixels = []
        for i in range(0, self.width):
            self.printToConsole(Black, self.getXPos() + i, self.getYPos(), self, self.parentWidth, self.parentHeight)
        for i in range(0, self.height):
            self.printToConsole(Black, self.getXPos(), self.getYPos() + i, self, self.parentWidth, self.parentHeight)

    def render(self, x = None, y = None):
        if (x != None and y != None):
            if self.checkPixel(x, y):
                self.printToConsole(self.getColor(), x, y, self, self.parentWidth, self.parentHeight)
	    else:
		self.printToConsole(Reset, x, y, self, self.parentWidth, self.parentHeight)
            return
        self.clear()
        options = {
           0 : self.zero,
           1 : self.one,
           2 : self.two,
           3 : self.three,
           4 : self.four,
           5 : self.five,
           6 : self.six,
           7 : self.seven,
           8 : self.eight,
           9 : self.nine,
	  10 : self.winner,
        }
        options[self.number]()

    def __str__(self):
        return " "
