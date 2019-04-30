from ball import Ball
from paddle import Paddle
from score import Score
from net import Net
import sys, time, random 

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
		self.serve = 'r' if random.randint(0,1) > 0 else 'l'

		self.ball = Ball(Red, 1, 1, self.width, self.height, self.serve)
		self.leftPaddle = Paddle(White, 1, 3, self.width, self.height)
		self.rightPaddle = Paddle(White, 1, 3, self.width, self.height)

		self.leftScore = Score(White, 3, 5, self.width, self.height, 0)
		self.rightScore = Score(White, 3, 5, self.width, self.height, 0)
		self.net = Net(Green, 1, 2, self.width, self.height)

		sys.stdout.flush()
		for i in range(0, self.height):
			sys.stdout.write('\n')
			i=+1

	def getServeSide(self):
		return self.serve

	def initPositions(self):
		self.leftPaddle.setXYPos(3, int(self.height / 2))
		self.rightPaddle.setXYPos(self.width - 3, int(self.height / 2))
		self.leftScore.setXYPos(int(self.width / 2) - 10, self.height - 8)
		self.rightScore.setXYPos(int(self.width / 2) + 10, self.height - 8)
		self.net.setXYPos(int(self.width / 2), 0)
		self.ball.setXYPos(int(self.width / 2), int(self.height / 2))

	def incrementScore(self):
		increment = False
		# Hit left wall
		if self.ball.getXPos() == self.width: 
			self.leftScore.setScore(self.leftScore.getScore() + 1)
			self.leftScore.render()
			increment = True
		# Hit right wall
		if self.ball.getXPos() == 0:
			self.rightScore.setScore(self.rightScore.getScore() + 1)
			self.rightScore.render()
			increment = True
		if increment:
			swap = True if (self.rightScore.getScore() + self.leftScore.getScore()) % 5 == 0 else False
			self.serve = 'r' if self.serve == 'l' and swap else 'l'
			return self.serve + 'serve'
		return None

	def serveBall(self, side, response):
		paddle = self.leftPaddle if side == 'l' else self.rightPaddle
		if 'l' in side and not 'r' in response:
			paddle = self.leftPaddle
		if 'r' in side and not 'l' in response:
			paddle = self.rightPaddle
		paddle.render(response[1])
		opposite = 'r' if side == 'l' else 'l'
		self.ball.setDir(opposite)
		offset = self.ball.getWidth() if paddle.getXPos() < int(self.width / 2) else (-self.ball.getWidth())
		self.ball.prepareServe(paddle.getXPos() + offset, paddle.getYPos() + int(paddle.getHeight() / 2))
		if 's' in response:
			return True
		return False

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
		self.net.initalRender()
		self.net.render()
		self.leftPaddle.render()
		self.rightPaddle.render()
		self.serveBall(self.serve, self.serve + ' ')

	def handleCollisions(self):
		# Collisions that require actions
		if self.collision(self.leftPaddle, self.ball):
			self.ball.bounce(self.leftPaddle.getYPos() - self.ball.getYPos())
			self.leftPaddle.render(None, self.ball.getXPos(), self.ball.getYPos())
		if self.collision(self.rightPaddle, self.ball):
			self.ball.bounce(self.rightPaddle.getYPos() - self.ball.getYPos())
			self.rightPaddle.render(None, self.ball.getXPos(), self.ball.getYPos())
		
		# Collisions that only require re-renders
		if self.collision(self.leftScore, self.ball, 1, 1):
			self.leftScore.render(self.ball.getXPos(), self.ball.getYPos())
		if self.collision(self.rightScore, self.ball, 1, 1):
			self.rightScore.render(self.ball.getXPos(), self.ball.getYPos())
		if self.collision(self.net, self.ball, 0, self.height):
			self.net.render(self.ball.getXPos(), self.ball.getYPos())

	def gameFrame(self, move = None):
		# Render ball before score to remove debounce errors on re-run of function
		self.ball.render()
		self.handleCollisions()
		if move != None and 'l' in move:
			self.leftPaddle.render(move[1])
		if move != None and 'r' in move:
			self.rightPaddle.render(move[1])
		score = self.incrementScore()
		if score != None:
			return score
			
	def setupGame(self):
		self.initPositions()
		self.initalRender()
		
		

			
			
				



	
