## Blink a LED Lib
import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'

GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(7, GPIO.OUT) ## Setup GPIO Pin 7 to OUT

def blink(numTimes,speed):
	for i in range(0,numTimes):## Run loop numTimes
		GPIO.output(7,True)## Switch on pin 7
		time.sleep(speed)## Wait
		GPIO.output(7,False)## Switch off pin 7
		time.sleep(speed)## Wait

## ex.: Blink(int(iterations),float(speed))
