from pong import Pong
import sys, time

def checkControllers():
	return None

def gameLoop(game):
	while True:
		time.sleep(0.05)
		move = checkControllers()
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
