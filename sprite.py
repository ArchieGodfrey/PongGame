from serialPort import openPort
import sys, time 

UpCode = lambda n: (u"\u001b[" + str(n) + "A")
DownCode = lambda n: (u"\u001b[" + str(n) + "B")
RightCode = lambda n: (u"\u001b[" + str(n) + "C")
LeftCode = lambda n: (u"\u001b[" + str(n) + "D")

RightDownCode = lambda x, y: (u"\u001b[" + str(x) + "C\u001b[" + str(y) + "A")

Reset = u"\u001b[0m"

WriteToPort = False

class Sprite(object):

    def __init__(self, color, width, height, direction = None):
        self.height = height
        self.width = width
        self.color = color
        self.dir = direction
        self.xPos = 0
        self.yPos = 0

        if WriteToPort:
            self.serialPort = openPort()

    def getColor(self):
        return self.color

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def getXPos(self):
        return self.xPos

    def getYPos(self):
        return self.yPos
    
    def getDir(self):
        return self.dir

    def setXPos(self, coord):
        self.xPos = coord

    def setYPos(self, coord):
        self.yPos = coord

    def setXYPos(self, x, y):
        self.xPos = x
        self.yPos = y

    def setDir(self, dir):
        self.dir = dir

    def horizontalMove(self, dir):
        if dir == 'r':
            self.setXPos(self.xPos + self.width)
        else:
            self.setXPos(self.xPos - self.width)

    def verticalMove(self, dir):
        if dir == 'u':
            self.setYPos(self.yPos + self.height)
        else:
            self.setYPos(self.yPos - self.height)
    
    def performMove(self, dir):
        if dir == 'l' or dir == 'r':
            self.horizontalMove(dir)
        else:
            self.verticalMove(dir)

    def performDiagMove(self, dir):
        if 'l' in dir:
            if 'u' in dir:
                self.horizontalMove('l')
                self.verticalMove('u')
            else :
                self.horizontalMove('l')
                self.verticalMove('d')
        else:
            if 'u' in dir:
                self.horizontalMove('r')
                self.verticalMove('u')
            else :
                self.horizontalMove('r')
                self.verticalMove('d')

    def printToConsole(self, color, x, y, message, screenWidth, screenHeight):
	if WriteToPort:
		self.serialPort.write(str(color + RightCode(x) + UpCode(y) + str(message)) + DownCode(screenHeight) + LeftCode(screenWidth))
	else:	
		sys.stdout.write(color + RightCode(x) + UpCode(y) + str(message) + Reset)
		sys.stdout.write(DownCode(screenHeight) + LeftCode(screenWidth))
		sys.stdout.flush()

