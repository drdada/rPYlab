import RPi.GPIO as GPIO
import time
import pingLib
import blinkLib

sleeptime=10 #in sec

def loop():
	resPing= pingLib.check_ping("192.168.1.1")
	if resPing == "1":
		blinkLib.blink(2,2)
	time.sleep(sleeptime)


#At the end
if __name__ == '__main__':
	try:
		print 'Press Ctrl-C to quit.'
		while True:
			loop()
	finally:
		GPIO.cleanup()
