import ports as Ports
import sys, time 
import CONSTANTS as C

class Sprite(object):

    def __init__(self, color, width, height, direction = None):
        self.height = height
        self.width = width
        self.color = color
        self.dir = direction
        self.xPos = 0
        self.yPos = 0

        if C.SERIAL_PORT_CONNECTED:
            self.serialPort = Ports.openScreen()

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
            self.setXPos(self.xPos + 1)
        else:
            self.setXPos(self.xPos - 1)

    def verticalMove(self, dir):
        if dir == 'u':
            self.setYPos(self.yPos + 1)
        else:
            self.setYPos(self.yPos - 1)
    
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
	if C.SERIAL_PORT_CONNECTED:
		Ports.sendToSerial(self.serialPort, str(C.RIGHTCODE(x) + C.UPCODE(y) + color + str(message)) + C.DOWNCODE(screenHeight) + C.LEFTCODE(screenWidth) + C.RESET)
	else:	
		sys.stdout.write(color + C.RIGHTCODE(x) + C.UPCODE(y) + str(message) + C.RESET)
		sys.stdout.write(C.DOWNCODE(screenHeight) + C.LEFTCODE(screenWidth))
		sys.stdout.flush()

