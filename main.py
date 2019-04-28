from pong import Pong
import sys, time

def gameLoop(game):
	while True:
		time.sleep(0.05)
		try:
			game.gameFrame()
		except Exception as state:
			gameLoop(game)



def startGame():
	game = Pong(80,24)
	game.setupGame()
	gameLoop(game)


def main():
	startGame()

main()
