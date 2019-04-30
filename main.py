from pong import Pong
import sys, time, tty

ControllersConnected = False

def checkControllers():
	if ControllersConnected:
		return 's'
	else:
		tty.setraw(sys.stdin)
		char = sys.stdin.readline(1)
		if char == 'w':
			return 'lu'
		if char == 's':
			return 'ld'
		if char == 'o':
			return 'ru'
		if char == 'l':
			return 'rd'
		if char == 'd':
			return 's'
		if char == 'k':
			return 's'
		if char == 'c':
			raise Exception('Quit')
		pass

def gameLoop(game):
	while True:
		time.sleep(0.05)
		try:
			response = checkControllers()
		except Exception as state:
			break
		try:
			game.gameFrame(response)
		except Exception as state:
			formattedState = str(state)
			if formattedState == 'IncrementLeftScore':
				served = False
				while not served:
					response = checkControllers()
					served = game.serveBall('l', response)
			if formattedState == 'IncrementRightScore':
				served = False
				while not served:
					response = checkControllers()
					served = game.serveBall('r', response)
			pass

def startGame():
	game = Pong(80,24)
	game.setupGame()
	gameLoop(game)


def main():
	startGame()

main()
