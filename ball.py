from sprite import Sprite

Reset = u"\u001b[0m"

class Ball(Sprite):
	
	def __init__(self, color, width, height, parentWidth, parentHeight, direction):
		Sprite.__init__(self, color, width, height, direction)
		self.parentHeight = parentHeight
		self.parentWidth = parentWidth
		self.bouncePhysics = {
			'u' : 'd',
			'd' : 'u',
			'r' : 'l',
			'l' : 'r',
			'ru' : 'rd',
			'lu' : 'ld',
			'rd' : 'ru',
			'ld' : 'lu',
			''   : ''
		}
		self.noFlash = False

	def __str__(self):
		return str(" " * self.width)

	def setNoFlash(self, toggle):
		self.noFlash = toggle

	def prepareServe(self, x, y):
		if self.getYPos() != y:
			self.printToConsole(Reset, self.getXPos(), self.getYPos(), self, self.parentWidth, self.parentHeight)
			self.setXYPos(x, y)
			self.printToConsole(self.getColor(), self.getXPos(), self.getYPos(), self, self.parentWidth, self.parentHeight)

	def move(self, dir):
		self.dir = dir
		if len(dir) == 1:
			self.performMove(dir)
		else:
			self.performDiagMove(dir)

	def bounce(self, redirect = 1):
		self.noFlash = True
		if redirect <= 2:
			direction = {
			   0 : 'u',
			   1 : '',
			   2 : 'd',
			}
		else:
			direction = {
			   0 : 'u',
			   1 : 'u',
			   2 : '',
			   3 : 'd',
			   4 : 'd',
			}
		self.setDir(self.bouncePhysics[direction[redirect]] + self.bouncePhysics[self.getDir()[0]])

	def checkBoundary(self):
		# Specification requires no bounce 4 columns in from each horizontal boundary
		# Hit left wall
		if self.getXPos() == 0: 
			if 'u' in self.getDir():
				self.setDir('ru')
			elif 'd' in self.getDir():
				self.setDir('rd')
			else:
				self.setDir('r')
		# Hit right wall
		if self.getXPos() == self.parentWidth:
			if 'u' in self.getDir():
				self.setDir('lu')
			elif 'd' in self.getDir():
				self.setDir('ld')
			else:
				self.setDir('l')
		# Hit bottom wall
		if self.getYPos() == 0:
			if 'r' in self.getDir():
				self.setDir('ru')
			elif 'l' in self.getDir():
				self.setDir('lu')
			else:
				self.setDir('u')
		# Hit top wall
		if self.getYPos() == self.parentHeight:
			if 'r' in self.getDir():
				self.setDir('rd')
			elif 'l' in self.getDir():
				self.setDir('ld')
			else:
				self.setDir('d')
		self.move(self.dir)

	def render(self):
		if not self.noFlash: 
			self.printToConsole(Reset, self.getXPos(), self.getYPos(), self, self.parentWidth, self.parentHeight)
		self.noFlash = False
		self.checkBoundary()
		self.printToConsole(self.getColor(), self.getXPos(), self.getYPos(), self, self.parentWidth, self.parentHeight)
			
