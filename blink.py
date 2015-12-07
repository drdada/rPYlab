## Blink a LED TEST
import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'

GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(7, GPIO.OUT) ## Setup GPIO Pin 7 to OUT

##Define a function named Blink()
def Blink(numTimes,speed):
	for i in range(0,numTimes):## Run loop numTimes
		GPIO.output(7,True)## Switch on pin 7
		time.sleep(speed)## Wait
		GPIO.output(7,False)## Switch off pin 7
		time.sleep(speed)## Wait
	GPIO.cleanup()

## Ask user for total number of blinks and length of each blink
iterations = raw_input("Enter total number of times to blink: ")
speed = raw_input("Enter length of each blink(seconds): ")

## Start Blink() function. Convert user input from strings to numeric data types and pass to Blink() as parameters
Blink(int(iterations),float(speed))
