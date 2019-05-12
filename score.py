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

    def renderNumber(self, draw):

        validPos = [
            'top', 'middle', 'bottom', 'left', 'center', 'right'
        ]

        convertPos = {
            'top' : 'v' + str(self.getHeight() - 1),
            'middle' : 'v' + str(int(self.getHeight() / 2)),
            'bottom': 'v0',
            'left': 'h0',
            'center': 'h' + str(int(self.getWidth() / 2)),
            'right': 'h' + str(self.getWidth() - 1),
        }
        
        def processInput(pos, path):
            index = draw.index(pos) + len(pos)
            val = draw[index:index + 2]
            if val != ' ' and val != '':
                return [convertPos[pos][0], int(val)]

        for pos in validPos:
            if pos in draw:
                start = int(convertPos[pos][1:])
                path = processInput(pos, draw)
                if path[1] > 0:
                    if 'v' in path[0]:
                        for i in range(path[1]):
                            self.renderPixel(i, start)
                    else:
                        for i in range(path[1]):
                            self.renderPixel(start, i)
                else:
                    if 'v' in path[0]:
                        for i in range(-path[1]):
                            self.renderPixel(i - path[1], start)
                    else:
                        for i in range(-path[1]):
                            self.renderPixel(start, i - path[1] + 1)

    def clear(self):
        self.currentPixels = []
        for i in range(0, self.width):
            for j in range(0, self.height):
                self.printToConsole(Black, self.getXPos() + i, self.getYPos() + j, self, self.parentWidth, self.parentHeight)
                
    def render(self, x = None, y = None):
        if (x != None and y != None):
            if self.checkPixel(x, y):
                self.printToConsole(self.getColor(), x, y, self, self.parentWidth, self.parentHeight)
            else:
                self.printToConsole(Reset, x, y, self, self.parentWidth, self.parentHeight)
            return
        self.clear()
        options = {
           0 : 'top3 left5 right5 bottom3',
           1 : 'top2 center5 bottom3',
           2 : 'top3 left3 right-2 bottom3 middle3',
           3 : 'top3 middle3 right5 bottom3',
           4 : 'left-2 middle3 right5',
           5 : 'top3 left-2 right3 bottom3 middle3',
           6 : 'top3 left5 right3 bottom3 middle3',
           7 : 'top3 left-2 right5',
           8 : 'top3 left5 right5 bottom3 middle3',
           9 : 'top3 left-2 right5 middle3',
	       10: 'center-2 left-2 right-2 middle3',
        }
        self.renderNumber(options[self.number])

    def __str__(self):
        return " "
