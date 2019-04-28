from pong import Pong

def runGame(game):
	try:
		game.runGame()
	except Exception as state:
		runGame(game)

def startGame():
	game = Pong(80,24)
	try:
		game.startGame()
	except Exception as state:
		sys.stdout.write(str(state))
		runGame(game)


def main():
	startGame()

main()
