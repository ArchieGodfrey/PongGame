from serial import Serial
import RPi.GPIO as GPIO	
import sys, time  
import smbus	#I2C library 

#Screen
def openScreen():
	# Open Pi serial port, speed 9600 bits per second 
	serialPort = Serial("/dev/ttyAMA0", 9600) # Should not need, but just in case 
	if (serialPort.isOpen() == False): 
		serialPort.open() 
	return serialPort


#8 LEDS
def sendToLEDS(string):
	I2C_ADDR = 0x39		#I2C base address

	bus = smbus.SMBus(1)	#enable I2C bus
	try:
	    bus.write_byte( I2C_ADDR, string )

	except IOError:
	  print("lost connection to I2C device")

	except TypeError:
	  print("Invalid Type device")


#7 segment display
def sendToDisplay(num):
	conversion = {
		0: 0x20,
		1: 0xFC,
		2: 0x42,
		3: 0x48,
		4: 0x8C,
		5: 0x09,
		6: 0x01,
		7: 0x6C,
		8: 0x00,
		9: 0x0C,
	}
	I2C_ADDR = 0x38		#I2C base address

	bus = smbus.SMBus(1)	#enable I2C bus
	try:
	    bus.write_byte( I2C_ADDR, conversion[num] ) 

	except IOError:
	  print("lost connection to I2C device")

	except TypeError:
	  print("Invalid Type device")

class Adc():
    def __init__( self, pinI, pinO  ):
        self.count = 0
        self.RESET_PIN = pinO
        self.TEST_PIN = pinI

        GPIO.setwarnings(False) 	
        GPIO.setmode(GPIO.BCM) 		

        GPIO.setup(self.RESET_PIN, GPIO.OUT) 
        GPIO.output(self.RESET_PIN, False) 	

        GPIO.setup(self.TEST_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def update(self):
        self.count = -15 #Usually 0, added as temp low pass filter
        GPIO.output(self.RESET_PIN, True) 	
        time.sleep(0.001)
        GPIO.output(self.RESET_PIN, False) 

        while GPIO.input(self.TEST_PIN) == 0:
            self.count +=1	

        return self.count 

    def getOutput(self):
	sample = 250
	count = 0
	for i in range(sample):
		count = count + self.update() 
        return count/sample 
	


