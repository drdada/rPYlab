# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import pingLib
import blinkLib
import logging
import threading
logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='/var/log/mainLoop.log')

sleeptime=10 #in sec
hostPing ="192.168.1.1" # IP host to check

global ping1_flag
ping1_flag = 0

def pingTest():
	while True:
		try:
			resPing= pingLib.check_ping(hostPing)
		except:
			print("Ping command Failed !")
			logging.error('Ping command Failed !')
		if resPing == "1": #1=ok 0=Failed
			print("Ping ALERT")
			logging.info('Host %s is not reachable',hostPing)
		ping1_flag = resPing
		time.sleep(sleeptime)
	
def ledNotification():
	while True:
		print("On va vérifier les flag")
		print(ping1_flag)
		if ping1_flag == "1":
			print("J'ai recu un flag, on clignote")
			blinkLib.blink(2,2)
		time.sleep(5)

#Da Main loop
if __name__ == '__main__':
	try:
		print 'Press Ctrl-C to quit.'
		thread_pingTest = threading.Thread(name='pingTest', target=pingTest)
		thread_ledNotif = threading.Thread(name='ledNotification', target=ledNotification)
		
		thread_pingTest.start()
		print 'Thread pingstart ok'
		thread_ledNotif.start()
		print 'Thread ledNotif ok'

		thread_pingTest.join()
                thread_ledNotif.join()

	except KeyboardInterrupt:
		print("Bye")
	finally:
		GPIO.cleanup()
