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
			return 'ls'
		if char == 'k':
			return 'rs'
		if char == 'c':
			raise Exception('Quit')
		checkControllers()

def gameLoop(game):
	while True:
		time.sleep(0.05)
		try:
			response = checkControllers()
		except Exception as state:
			break
		state = game.gameFrame(response)
		formattedState = str(state)
		if 'serve' in formattedState:
			served = False
			while not served:
				response = checkControllers()
				served = game.serveBall(state[0], response)

def startGame():
	game = Pong(80,24)
	game.setupGame()
	served = False
	while not served:
		response = checkControllers()
		served = game.serveBall(game.getServeSide(), response)
	gameLoop(game)


def main():
	startGame()

main()
