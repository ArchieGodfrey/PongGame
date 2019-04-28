
import sys, time  

def openPort():
	# Open Pi serial port, speed 9600 bits per second 
	serialPort = Serial("/dev/ttyAMA0", 9600) # Should not need, but just in case 
	if (serialPort.isOpen() == False): 
		serialPort.open() 
	return serialPort

def send(string):
	serialPort = openPort()
	# Wait for character to be RX. Print ASCII value to Pi screen 
	# TX back RX character to remote terminal. If RX character is 
	# CR exit loop and close serial port. 
	#go = True 
	#while (go): 
		#input_string = serialPort.read() 
		#print "ASCII Value: " + str(ord(input_string)) 
		#serialPort.write(input_string) 
	serialPort.write(string)
		#if (ord(input_string) == 13): 
			#go = False

	serialPort.close() 
	
