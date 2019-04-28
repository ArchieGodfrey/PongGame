from sprite import Sprite
import sys

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
			'ur' : 'dr',
			'ul' : 'dl',
			'dr' : 'ur',
			'dl' : 'ul',
		}
		self.noFlash = False

	def __str__(self):
		return str(" " * self.width)

	def setNoFlash(self, toggle):
		self.noFlash = toggle

	def move(self, dir):
		self.dir = dir
		if len(dir) == 1:
			self.performMove(dir)
		else:
			self.performDiagMove(dir)

	def bounce(self):
		self.noFlash = True
		self.setDir(self.bouncePhysics[self.getDir()])

	def checkBoundary(self):
		# Specification requires no bounce 4 columns in from each horizontal boundary
		# Hit left wall
		if self.getXPos() == 0: 
			if 'u' in self.getDir():
				self.setDir('ur')
			elif 'd' in self.getDir():
				self.setDir('dr')
			else:
				self.setDir('r')
		# Hit right wall
		if self.getXPos() == self.parentWidth:
			if 'u' in self.getDir():
				self.setDir('ul')
			elif 'd' in self.getDir():
				self.setDir('dl')
			else:
				self.setDir('l')
		# Hit bottom wall
		if self.getYPos() == 0:
			if 'r' in self.getDir():
				self.setDir('ur')
			elif 'l' in self.getDir():
				self.setDir('ul')
			else:
				self.setDir('u')
		# Hit top wall
		if self.getYPos() == self.parentHeight:
			if 'r' in self.getDir():
				self.setDir('dr')
			elif 'l' in self.getDir():
				self.setDir('dl')
			else:
				self.setDir('d')
		self.move(self.dir)

	def render(self):
		if not self.noFlash: 
			self.printToConsole(Reset, self.getXPos(), self.getYPos(), self, self.parentWidth, self.parentHeight)
		self.noFlash = False
		self.checkBoundary()
		self.printToConsole(self.getColor(), self.getXPos(), self.getYPos(), self, self.parentWidth, self.parentHeight)
			
