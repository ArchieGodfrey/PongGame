from pong import Pong
import sys, time, tty

ControllersConnected = True

def checkControllers():
	if ControllersConnected:
		return None
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
		if char == 'c':
			raise Exception('Quit')
		pass

def gameLoop(game):
	while True:
		time.sleep(0.05)
		try:
			move = checkControllers()
		except Exception as state:
			break
		try:
			game.gameFrame(move)
		except Exception as state:
			formattedState = str(state)
			if formattedState == 'IncrementLeftScore':
				sys.stdout.write(formattedState)
			pass

def startGame():
	game = Pong(80,24)
	game.setupGame()
	gameLoop(game)


def main():
	startGame()

main()
