from sprite import Sprite
from ball import Ball
from paddle import Paddle
from score import Score
from net import Net
import CONSTANTS as C
import ports as Ports
import sys, time, random 

class Pong(object):

	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.top = height
		self.bottom = 0
		self.leftPaddleSuper = False
		self.rightPaddleSuper = False

		self.serve = 'r' if random.randint(0,1) > 0 else 'l'
		self.ball = Ball(C.RED, C.BALL_WIDTH, C.BALL_HEIGHT, self.width, self.height, self.serve)
		self.leftPaddle = Paddle(C.WHITE, C.PADDLE_WIDTH, C.PADDLE_HEIGHT, self.width, self.height)
		self.rightPaddle = Paddle(C.WHITE, C.PADDLE_WIDTH, C.PADDLE_HEIGHT, self.width, self.height)

		self.leftScore = Score(C.YELLOW, C.SCORE_WIDTH, C.SCORE_HEIGHT, self.width, self.height, 0)
		self.rightScore = Score(C.YELLOW, C.SCORE_WIDTH, C.SCORE_HEIGHT, self.width, self.height, 0)
		self.net = Net(C.GREEN, C.NET_WIDTH, C.NET_HEIGHT, self.width, self.height)

	def getServeSide(self):
		return self.serve

	def getBallBinPos(self):
		relative = int((self.ball.getXPos()) / 10)
		return 2**relative

	def displayWinner(self, side):
		message = "The winner is Left Side!" if side == 'l' else "The winner is Right Side!"
		text = Sprite(C.WHITE, 0, 0)
		text.printToConsole(text.getColor(), int(self.width / 2) - int(len(message) / 2), int(self.height / 2), message, self.width, self.height)

	def initPositions(self):
		self.leftPaddle.setXYPos(C.PADDLE_X, int(self.height / 2))
		self.rightPaddle.setXYPos(self.width - C.PADDLE_X, int(self.height / 2))
		self.leftScore.setXYPos(int(self.width / 2) - self.leftScore.getWidth() - C.LEFT_SCORE_X, self.height - 8)
		self.rightScore.setXYPos(int(self.width / 2) + self.rightScore.getWidth() + C.RIGHT_SCORE_X, self.height - 8)
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
			Ports.sendToBuzzer(1000)
			if self.leftScore.getScore() == 10:
				return 'lwinner'
			if self.rightScore.getScore() == 10:
				return 'rwinner'
			swap = True if (self.rightScore.getScore() + self.leftScore.getScore()) % 5 == 0 else False
			self.serve = 'r' if self.serve == 'l' and swap else 'l'
			return self.serve + 'serve'
		return None

	def toggleSuper(self, side):
		if side != None:
			paddle = self.leftPaddle if side == 'l' else self.rightPaddle
			toggle = self.leftPaddleSuper if side == 'l' else self.rightPaddleSuper
			toggle = 15 if toggle == 0 else (toggle - C.FRAME_RATE)
			paddle.setHeight(5) if toggle > 0 else paddle.setHeight(3)
		sys.stdout.write(C.LEFTCODE(1000) + C.UPCODE(18) + 'Left Super: ' + str(self.leftPaddleSuper))
		sys.stdout.write(C.LEFTCODE(1000) + C.UPCODE(19) + 'Right Super: ' + str(self.rightPaddleSuper))
		sys.stdout.write(C.DOWNCODE(C.TERMINAL_HEIGHT) + C.LEFTCODE(C.TERMINAL_WIDTH))

	def serveBall(self, side, response = None):
		paddle = self.leftPaddle if side == 'l' else self.rightPaddle
		if response != None:
			if 'l' in side and not 'r' in response:
				paddle.render(response[1:])
			if 'r' in side and not 'l' in response:
				paddle.render(response[1:])
		opposite = 'r' if side == 'l' else 'l'
		self.ball.setDir(opposite)
		offset = self.ball.getWidth() if paddle.getXPos() < int(self.width / 2) else (-self.ball.getWidth())
		self.ball.prepareServe(paddle.getXPos() + offset, paddle.getYPos() + int(paddle.getHeight() / 2))
		if response != None and 's' in response and side in response:
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
		self.serveBall(self.serve)

	def handleCollisions(self):
		debug = ''	
		sys.stdout.write(C.LEFTCODE(1000) + C.UPCODE(23) + '                                ')
		# Collisions that require actions
		if self.collision(self.leftPaddle, self.ball):
			self.ball.bounce(self.ball.getYPos() - self.leftPaddle.getYPos())
			self.leftPaddle.render(None, self.ball.getXPos(), self.ball.getYPos())
			debug=('Left paddle hit ball ')
		if self.collision(self.rightPaddle, self.ball):
			self.ball.bounce(self.ball.getYPos() - self.rightPaddle.getYPos())
			self.rightPaddle.render(None, self.ball.getXPos(), self.ball.getYPos())
			debug=('Right paddle hit ball')
		
		# Collisions that only require re-renders
		if self.collision(self.leftScore, self.ball):
			self.ball.setNoFlash(True)
			self.leftScore.render(self.ball.getXPos(), self.ball.getYPos())
			debug=('Left score with ball ')
		if self.collision(self.rightScore, self.ball):
			self.ball.setNoFlash(True)
			self.rightScore.render(self.ball.getXPos(), self.ball.getYPos())
			debug=('Right score with ball')
		if self.collision(self.net, self.ball, 0, self.height):
			self.ball.setNoFlash(True)
			self.net.render(self.ball.getXPos(), self.ball.getYPos())
			debug=('Ball crossed the net ')
			
		sys.stdout.write(C.LEFTCODE(1000) + C.UPCODE(23) + 'Collisions: ' + debug)
		sys.stdout.write(C.DOWNCODE(C.TERMINAL_HEIGHT) + C.LEFTCODE(C.TERMINAL_WIDTH))

	def gameFrame(self, leftMove = None, rightMove = None):
		# Render ball after collisions to remove debounce errors
		self.handleCollisions()
		self.ball.render()
		if self.leftPaddleSuper > 0:
			self.toggleSuper('l')
		if self.rightPaddleSuper > 0:
			self.toggleSuper('r')
		if leftMove != None:
			self.leftPaddle.render(leftMove[1:])
		if rightMove != None:
			self.rightPaddle.render(rightMove[1:])
		score = self.incrementScore()
		if score != None:
			return score
			
	def setupGame(self):
		self.initPositions()
		self.initalRender()
		
		

			
			
				



	
