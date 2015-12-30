# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import pingLib
import blinkLib
import logging
import threading
import ConfigParser

## Log Config
logging.basicConfig(level=logging.DEBUG, #Change it for different log level (debug, info)
        format='%(asctime)s :: %(levelname)-8s :: %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='/var/log/mainLoop.log')

## Mail Config (see also mail.conf)
mailConfig = ConfigParser.ConfigParser()
mailConfig.readfp(open(r'mail.conf'))
userMail = mailConfig.get('mailSettings', 'user')
pwMail = mailConfig.get('mailSettings', 'password')

## Check Ping COnfig
pingSleeptime=10 #in sec for the check ping interval
hostPing ="192.168.1.1" # IP host to check

### END CONFIG

global ping1_flag
ping1_flag = 0
global gmail1_flag
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
		else:
			logging.debug('Host %s : OK',hostPing)
		ping1_flag = resPing
		time.sleep(pingSleeptime)
	logging.debug("Exiting PingTest Thread")
	
def ledNotification():
	global ping1_flag, gmail1_flag, threadOn
	logging.debug("Starting LedNotif Thread")
	time.sleep(6)
	while not threadOn:
		if ping1_flag == "0":
			logging.debug("Ping Flag received: Blinking !")
			blinkLib.blink(19,float(0.1))
		if ping1_flag == "1" and gmail1_flag > 0:
			logging.debug("Gmail flag received: Blinking")
			blinkLib.blink(gmail1_flag,2)
		time.sleep(10)
	logging.debug("Exiting PingTest Thread")

#TY to https://gist.github.com/vadviktor/3529647#file-gmail-py 
def gmail_connect(username,password):
  import imaplib,re
  i=imaplib.IMAP4_SSL('imap.gmail.com')
  try:
    i.login(username,password)
    x,y=i.status('INBOX','(MESSAGES UNSEEN)')
    messages=int(re.search('MESSAGES\s+(\d+)',y[0]).group(1))
    unseen=int(re.search('UNSEEN\s+(\d+)',y[0]).group(1))-2
    return (messages,unseen)
  except:
    return False,0

def gmail_check():
        global gmail1_flag, threadOn
	time.sleep(2)
        logging.debug("Starting Gmail_check Thread")
        while not threadOn:
                try:
			messages,unread = gmail_connect(userMail,pwMail)
                except:
                        print("Gmail Check command Failed !")
                        logging.error('Gmail check command Failed !')
                if unread == 0: 
                        logging.debug('Gmail Check: No new messages - Total: %i ',messages)
		else:
			logging.info('Gmail Check: %i new messages ! - Total: %i ',unread,messages)
                gmail1_flag = unread
                time.sleep(10)
        logging.debug("Exiting gmailCheck Thread")


#Da Main loop
if __name__ == '__main__':
	try:
		print("Press Ctrl-C to quit.")
		thread_pingTest = threading.Thread(name='pingTest', target=pingTest)
		thread_ledNotif = threading.Thread(name='ledNotification', target=ledNotification)
		thread_gmailNotif = threading.Thread(name='gmail_check', target=gmail_check)
		
		thread_pingTest.start() #start threads
		thread_ledNotif.start()
		thread_gmailNotif.start()

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
