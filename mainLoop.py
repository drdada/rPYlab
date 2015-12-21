# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import pingLib
import blinkLib
import logging
import threading
logging.basicConfig(level=logging.DEBUG, #Change it for different log level (debug, info)
        format='%(asctime)s :: %(levelname)-8s :: %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='/var/log/mainLoop.log')

sleeptime=10 #in sec
hostPing ="192.168.1.1" # IP host to check

global ping1_flag
ping1_flag = 0
global threadOn #Flag to kill or not the threads
threadOn = False
logging.info("Starting Python Script Monitoring daemon")

def pingTest():
	global ping1_flag, threadOn
	logging.debug("Starting PingTest Thread")
	while not threadOn:
		try:
			resPing= pingLib.check_ping(hostPing)
		except:
			print("Ping command Failed !")
			logging.error('Ping command Failed !')
		if resPing == "0": #1=ok 0=Failed
			logging.info('Host %s is not reachable',hostPing)
		ping1_flag = resPing
		time.sleep(sleeptime)
	logging.debug("Exiting PingTest Thread")
	
def ledNotification():
	global ping1_flag, threadOn
	logging.debug("Starting LedNotif Thread")
	while not threadOn:
		print(ping1_flag)
		if ping1_flag == "0":
			logging.debug("Ping Flag received: Blinking !")
			blinkLib.blink(2,2)
		time.sleep(5)
	logging.debug("Exiting PingTest Thread")

#Da Main loop
if __name__ == '__main__':
	try:
		print("Press Ctrl-C to quit.")
		thread_pingTest = threading.Thread(name='pingTest', target=pingTest)
		thread_ledNotif = threading.Thread(name='ledNotification', target=ledNotification)
		
		thread_pingTest.start() #start threads
		thread_ledNotif.start()
		while True:		#Loop in order to wait for the ctrl-c
			time.sleep(1)        			
	except KeyboardInterrupt:
		logging.info("Ctrl-C received asking thread to stopping...")
		threadOn = True
	else:
		logging.warning("Main loop killed or something... Asking for kill remaining threads")
                threadOn = True
	finally:
		time.sleep(1) #Waiting for the threads
		logging.info("Exiting Python Script")
		GPIO.cleanup()
