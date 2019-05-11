from serial import Serial
import CONSTANTS as C
import RPi.GPIO as GPIO	
import sys, time  
import smbus
from PyGlow import PyGlow

#Screen
def openScreen():
	serialPort = Serial(C.SERIAL_OUTPUT, C.SERIAL_RATE) 
	if (serialPort.isOpen() == False): 
		serialPort.open() 
	if C.HARDWARE_DEBUG:
		sys.stdout.write(C.LEFTCODE(1000) + C.UPCODE(0) + 'Serial Port Connected on : ' + str(C.SERIAL_OUTPUT))
		sys.stdout.write(C.DOWNCODE(C.TERMINAL_HEIGHT) + C.LEFTCODE(C.TERMINAL_WIDTH))
	return serialPort

def sendToSerial(port, message):
	port.write(message)
	if C.HARDWARE_DEBUG:
		sys.stdout.write(C.LEFTCODE(1000) + C.UPCODE(5) + 'Serial Port: ' )
		sys.stdout.write(C.DOWNCODE(C.TERMINAL_HEIGHT) + C.LEFTCODE(C.TERMINAL_WIDTH))

#8 LEDS
def offPiLEDS():
	for i in range(8):
		port = 2**i
		GPIO.output(C.PI_EIGHT_PORTS[port], 0) 	

def sendToLEDS(string):
	offPiLEDS()
	bus = smbus.SMBus(1)	
	try:
	    bus.write_byte( C.LEDS_OUTPUT, string )
	    GPIO.output(C.PI_EIGHT_PORTS[string], 1)
	    if C.HARDWARE_DEBUG:
		    sys.stdout.write(C.LEFTCODE(1000) + C.UPCODE(10) + '8 LEDs: ' + str(string))
		    sys.stdout.write(C.DOWNCODE(C.TERMINAL_HEIGHT) + C.LEFTCODE(C.TERMINAL_WIDTH))

	except IOError:
	  	sys.stdout.write(C.LEFTCODE(1000) + C.UPCODE(10) + '8 LEDs: ' + "lost connection to LEDS")
          	sys.stdout.write(C.DOWNCODE(C.TERMINAL_HEIGHT) + C.LEFTCODE(C.TERMINAL_WIDTH))

	except TypeError:
		sys.stdout.write(C.LEFTCODE(1000) + C.UPCODE(10) + '8 LEDs: ' + "Invalid Type for LEDS")
          	sys.stdout.write(C.DOWNCODE(C.TERMINAL_HEIGHT) + C.LEFTCODE(C.TERMINAL_WIDTH))

def setupPiLEDS():
	for i in range(8):
		port = 2**i
		GPIO.setup(C.PI_EIGHT_PORTS[port], GPIO.OUT) 



#7 segment display
def sendToDisplay(num):
	bus = smbus.SMBus(1)	
	try:			  
		bus.write_byte_data( C.SEGMENT_DISPLAY_OUTPUT, 0x01, num )
		if C.HARDWARE_DEBUG:
		    sys.stdout.write(C.LEFTCODE(1000) + C.UPCODE(15) + '7 Segment Display: ' + str(num))
		    sys.stdout.write(C.DOWNCODE(C.TERMINAL_HEIGHT) + C.LEFTCODE(C.TERMINAL_WIDTH))
	except IOError:
		sys.stdout.write(C.LEFTCODE(1000) + C.UPCODE(15) + '7 Segment Display: ' + "lost connection to 7 segment display")
		sys.stdout.write(C.DOWNCODE(C.TERMINAL_HEIGHT) + C.LEFTCODE(C.TERMINAL_WIDTH))

	except TypeError:
		sys.stdout.write(C.LEFTCODE(1000) + C.UPCODE(15) + '7 Segment Display: ' + "Invalid Type for 7 segment display")
		sys.stdout.write(C.DOWNCODE(C.TERMINAL_HEIGHT) + C.LEFTCODE(C.TERMINAL_WIDTH))

#Buzzer
def sendToBuzzer(freq):
	GPIO.setwarnings(False) 	
	GPIO.setmode(GPIO.BCM) 	

	GPIO.setup(C.BUZZER_OUTPUT, GPIO.OUT) 	
	PWM = GPIO.PWM(C.BUZZER_OUTPUT, freq)	#set freq 100Hz
	PWM.start(0)			

	for i in range(5,100,10):
	      PWM.ChangeDutyCycle(i)
	      time.sleep(0.1)
	for i in range(100,0,-5):
	      PWM.ChangeDutyCycle(i)


#PiGlow
def switchOffPiGlow():
	try:
		pyglow.color("white", 0)
		pyglow.color("blue", 0)
		pyglow.color("green", 0)
	except IOError:
		swicthOffPiGlow()

def pointGlow(side):
	pyglow = PyGlow()
	try:
		pyglow.color("white", 50)
		pyglow.color("blue", 50)
		pyglow.color("green", 50)
	except IOError:
		switchOffPiGlow
	time.sleep(1)
	try:
		pyglow.color("white", 0)
		pyglow.color("blue", 0)
		pyglow.color("green", 0)
	except IOError:
		switchOffPiGlow


class SoftwareController():
    def __init__( self, pinI, serveI, superI):
      	self.serve = False
	self.mega = False
        self.superCount = 0
        self.TEST_PIN = pinI

        GPIO.setwarnings(False) 	
        GPIO.setmode(GPIO.BCM) 		

	self.bus = smbus.SMBus(1) 

	#Serve button
	GPIO.setup(serveI, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(serveI, GPIO.RISING, callback=self.servePressed, bouncetime=250) 

	#Super button
	GPIO.setup(superI, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(superI, GPIO.RISING, callback=self.superPressed, bouncetime=250)  

    def getOutput(self):
	self.bus.write_byte( self.TEST_PIN, 16 ) 
	wrongOrder = self.bus.read_word_data( self.TEST_PIN, 0x00 )
	newOrder = (wrongOrder >> 8) | (wrongOrder << 8)
	newOrder = newOrder & 0x0FFF
	relative = int(newOrder / 126)
			
	sys.stdout.write(C.LEFTCODE(1000) + C.UPCODE(3) + 'Software controller response : ' + str(relative) + '    ')
	sys.stdout.write(C.DOWNCODE(C.TERMINAL_HEIGHT) + C.LEFTCODE(C.TERMINAL_WIDTH))
	return relative
	
    def servePressed(self, pin): 			
	self.serve = True
	sys.stdout.write(C.LEFTCODE(1000) + C.UPCODE(3) + 'Software controller response : ' + 'serve')
	sys.stdout.write(C.DOWNCODE(C.TERMINAL_HEIGHT) + C.LEFTCODE(C.TERMINAL_WIDTH))

    def superPressed(self, pin): 			
	self.mega = True
	sys.stdout.write(C.LEFTCODE(1000) + C.UPCODE(3) + 'Software controller response : ' + 'super')
	sys.stdout.write(C.DOWNCODE(C.TERMINAL_HEIGHT) + C.LEFTCODE(C.TERMINAL_WIDTH))

    def getResponse(self):
	if self.serve == True:
		self.serve = False
		return 'serve'
	if self.mega == True and self.superCount < 2:
		self.superCount = self.superCount + 1
		self.mega = False
		return 'super'
	return 'adc'








class HardwareController():
    def __init__( self, pinI, pinO, serveI, superI):
      	self.serve = False
	self.mega = False
	self.superCount = 0
	self.count = 0
        self.RESET_PIN = pinO
        self.TEST_PIN = pinI

        GPIO.setwarnings(False) 	
        GPIO.setmode(GPIO.BCM) 		

	#ADC
        GPIO.setup(self.RESET_PIN, GPIO.OUT) 
        GPIO.output(self.RESET_PIN, False) 	
        GPIO.setup(self.TEST_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	#Serve button
	GPIO.setup(serveI, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(serveI, GPIO.RISING, callback=self.servePressed, bouncetime=100) 

	#Super button
	GPIO.setup(superI, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(superI, GPIO.RISING, callback=self.superPressed, bouncetime=100) 

    def update(self):
        self.count = -13 #Usually 0, added as temp low pass filter
        GPIO.output(self.RESET_PIN, True) 	
        time.sleep(C.ADC_REFRESH_RATE)
        GPIO.output(self.RESET_PIN, False) 

        while GPIO.input(self.TEST_PIN) == 0:
            self.count +=1	

        return self.count 

    def getOutput(self):
	sample = 250
	count = 0
	for i in range(sample):
		count = count + self.update() 
	if C.HARDWARE_DEBUG:
		sys.stdout.write(C.LEFTCODE(1000) + C.UPCODE(19) + 'ADC: ' + str(count/sample))
		sys.stdout.write(C.DOWNCODE(C.TERMINAL_HEIGHT) + C.LEFTCODE(C.TERMINAL_WIDTH))
	sys.stdout.write(C.LEFTCODE(1000) + C.UPCODE(4) + 'Hardware controller response : ' + str(int(count/sample * 1.4)) + '    ')
	sys.stdout.write(C.DOWNCODE(C.TERMINAL_HEIGHT) + C.LEFTCODE(C.TERMINAL_WIDTH))
        return int((count/sample)*1.4) 

	
    def servePressed(self, pin): 			
	self.serve = True
	sys.stdout.write(C.LEFTCODE(1000) + C.UPCODE(4) + 'Hardware controller response : ' + 'serve')
	sys.stdout.write(C.DOWNCODE(C.TERMINAL_HEIGHT) + C.LEFTCODE(C.TERMINAL_WIDTH))

    def superPressed(self, pin): 			
	self.mega = True
	sys.stdout.write(C.LEFTCODE(1000) + C.UPCODE(4) + 'Hardware controller response : ' + 'super')
	sys.stdout.write(C.DOWNCODE(C.TERMINAL_HEIGHT) + C.LEFTCODE(C.TERMINAL_WIDTH))

    def getResponse(self):
	if self.serve == True:
		self.serve = False
		return 'serve'
	if self.mega == True and self.superCount < 2:
		self.superCount = self.superCount + 1
		self.mega = False
		return 'super'
	return 'adc'

	


