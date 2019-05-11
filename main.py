from pong import Pong
import CONSTANTS as C
import ports as Ports
import sys, time, tty

leftController = Ports.HardwareController( C.ADC_INPUT, C.ADC_OUTPUT, C.SERVE_INPUT, C.SUPER_INPUT )
rightController = Ports.SoftwareController( C.SOFTWARE_ADC_INPUT, C.SOFTWARE_SERVE_INPUT, C.SOFTWARE_SUPER_INPUT )

def convertToPos(data):
	pos = C.TERMINAL_HEIGHT - data
	if pos < C.PADDLE_HEIGHT:
		return 0
	if pos > C.TERMINAL_HEIGHT - C.PADDLE_HEIGHT:
		return C.TERMINAL_HEIGHT - C.PADDLE_HEIGHT
	return pos

def checkControllers(game, side):
	controller = leftController if side == 'l' else rightController
	response = controller.getResponse()
	if 'serve' in response:
		return side + 'serve'
	elif 'super' in response:
		return side + 'super'
	else:
		return side + str(convertToPos(controller.getOutput()))

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
		currentWait = currentWait + C.HARDWARE_RATE
		leftResponse = checkControllers(game, 'l')
		rightResponse = checkControllers(game, 'r')
		if leftResponse != None and 'l' in side:
			served = game.serveBall(side, leftResponse)
		if ('serve' in leftResponse and 'l' in side):
			served = game.serveBall(side, 'l' + 'serve')
		if rightResponse != None and 'r' in side:
			served = game.serveBall(side, rightResponse)
		if ('serve' in rightResponse and 'r' in side):
			served = game.serveBall(side, 'r' + 'serve')
		if count == 0:
			served = game.serveBall(side, game.getServeSide() + 'serve')


def gameLoop(game):
	play = True
	while play:
		time.sleep(C.FRAME_SPEED)
		leftResponse = checkControllers(game, 'l')
		rightResponse = checkControllers(game, 'r')
		state = game.gameFrame(leftResponse, rightResponse)
		formattedState = str(state)
		Ports.sendToLEDS(game.getBallBinPos())
		
		if 'super' in leftResponse:
			game.toggleSuper('l')	
		if 'super' in rightResponse:
			game.toggleSuper('r')
		if 'serve' in formattedState:
			Ports.pointGlow(state[0])
			serve(game, state[0])

		if 'winner' in formattedState:
			game.displayWinner(state[0])
			play = False

def startGame():
	sys.stdout.flush()
	for i in range(0, C.TERMINAL_HEIGHT):
		sys.stdout.write('\n')
		i=+1
	game = Pong(C.TERMINAL_WIDTH, C.TERMINAL_HEIGHT)
	game.setupGame()
	Ports.setupPiLEDS()
	serve(game, game.getServeSide())
	gameLoop(game)


def main():
	startGame()

main()
