from pong import Pong
import ports as Ports
import sys, time, tty

ControllersConnected = True
adc = Ports.Adc( 10, 9 )

def convertToPos(data):
	if data > 15: #Update when changing filter
		#up	
		pos = data * (40 / 15)	
		return pos	
	else:
		#down
		pos = data * (40 / 15)
		return data

def checkControllers():
	if ControllersConnected:
		print(convertToPos(adc.getOutput()))
		return 'l' + str(convertToPos(adc.getOutput()))
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

def serve(game, side):
	served = False
	currentWait = 0
	count = 9
	Ports.sendToDisplay(count)
	while not served:
		if currentWait >= 1 and count  > 0:
			count = count - 1
			Ports.sendToDisplay(count)
			currentWait = 0
		currentWait = currentWait + 0.05
		response = checkControllers()
		if response != None:
			served = game.serveBall(side, side + response)
		if count == 0:
			served = game.serveBall(side, game.getServeSide() + 's')
		time.sleep(0.05)

def gameLoop(game):
	while True:
		time.sleep(0.05)
		try:
			response = checkControllers()
		except Exception as state:
			break
		state = game.gameFrame(response)
		formattedState = str(state)
		Ports.sendToLEDS(game.getBallBinPos())

		if 'super' in response:
			game.toggleSuper(response[0])	

		if 'serve' in formattedState:
			serve(game, state[0])

		if 'winner' in formattedState:
			game.displayWinner(state[0])

def startGame():
	game = Pong(80,24)
	game.setupGame()
	serve(game, game.getServeSide())
	gameLoop(game)


def main():
	startGame()

main()
