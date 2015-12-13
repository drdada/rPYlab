import logging,os
logging.basicConfig(level=logging.DEBUG,
	format='%(asctime)s %(levelname)-8s %(message)s',
	datefmt='%a, %d %b %Y %H:%M:%S',
	filename='/var/log/pingTest.log')

def check_ping(hostname):
	response = os.system("ping -c 1 " + hostname)
	# and then check the response...
	if response == 0:
		#OK
        	pingstatus = "1"
	else:
		#Non-OK
		pingstatus = "0"
		logging.info('Host %s is not reachable',hostname)	

	return pingstatus
