from ball import Ball
from paddle import Paddle
from score import Score
from net import Net
import sys, time 

UpCode = lambda n: (u"\u001b[" + str(n) + "A")
DownCode = lambda n: (u"\u001b[" + str(n) + "B")
RightCode = lambda n: (u"\u001b[" + str(n) + "C")
LeftCode = lambda n: (u"\u001b[" + str(n) + "D")

Red = u"\u001b[41m"
White = u"\u001b[47m"
Black = u"\u001b[40m"
Green = u"\u001b[42m"
Reset = u"\u001b[0m"

class Pong(object):

	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.top = height
		self.bottom = 0
		self.left = 0
		self.right = width

		self.ball = Ball(Red, 1, 1, self.width, self.height, 'ur')	
		self.leftPaddle = Paddle(White, 1, 3, self.width, self.height)
		self.rightPaddle = Paddle(White, 1, 3, self.width, self.height)

		self.leftScore = Score(White, 3, 5, self.width, self.height, 0)
		self.rightScore = Score(White, 3, 5, self.width, self.height, 0)
		self.net = Net(Green, 1, 2, self.width, self.height, 10)

		sys.stdout.flush()
		for i in range(0, self.height):
			sys.stdout.write('\n')
			i=+1

	def initPositions(self):
		self.leftPaddle.setXYPos(2, int(self.height / 2))
		self.rightPaddle.setXYPos(self.width - 2, int(self.height / 2))
		self.leftScore.setXYPos(int(self.width / 2) - 10, self.height - 8)
		self.rightScore.setXYPos(int(self.width / 2) + 10, self.height - 8)
		self.net.setXYPos(int(self.width / 2), 0)
		self.ball.setXYPos(10, int(self.height / 2) - 1)

	def incrementScore(self):
		# Hit left wall
		if self.ball.getXPos() == self.width: 
			self.leftScore.setScore(self.leftScore.getScore() + 1)
			self.leftScore.render()
			return 'left'
		# Hit right wall
		if self.ball.getXPos() == 0:
			self.rightScore.setScore(self.rightScore.getScore() + 1)
			self.rightScore.render()
			return 'right'
		return None

	def collision(self, a, b, extraX = 0, extraY = 0):
		# Subtract one to account for original position
		xA = a.getXPos() - extraX
		xAEnd = a.getXPos() + a.getWidth() - 1 + extraX
		xB = b.getXPos()
		xBEnd = b.getXPos() + b.getWidth() - 1
		yA = a.getYPos() - extraY
		yAEnd = a.getYPos() + a.getHeight() - 1 + extraY
		yB = b.getYPos()
		yBEnd = b.getYPos() + b.getHeight() - 1
		if (xA <= xB and xAEnd >= xBEnd) and (yA <= yB and yAEnd >= yBEnd):
			return True
		return False

	def initalRender(self):
		self.leftScore.render()
		self.rightScore.render()
		self.net.render()
		self.leftPaddle.render()
		self.rightPaddle.render()

	def runGame(self, state = 'run'):
		while True:
			time.sleep(0.05)
			self.ball.render()
			score = self.incrementScore()
			if score != None:
				raise Exception(score)
			if self.collision(self.leftPaddle, self.ball):
				self.ball.bounce()
				self.leftPaddle.render(self.ball.getXPos(), self.ball.getYPos())
			if self.collision(self.rightPaddle, self.ball):
				self.ball.bounce()
				self.rightPaddle.render(self.ball.getXPos(), self.ball.getYPos())
			if self.collision(self.leftScore, self.ball, 1, 1):
				self.leftScore.render(self.ball.getXPos(), self.ball.getYPos())
			if self.collision(self.rightScore, self.ball, 1, 1):
				self.rightScore.render(self.ball.getXPos(), self.ball.getYPos())
			if self.collision(self.net, self.ball, 0, self.height):
				self.ball.setNoFlash(True)
				self.net.render()
		
	def startGame(self):
		self.initPositions()
		self.initalRender()
		self.runGame()
		
		

			
			
				



	