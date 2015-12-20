import logging,os

def check_ping(hostname):
	response = os.system("ping -c 1 " + hostname)
	# and then check the response...
	if response == 0:
		#OK
        	pingstatus = "1"
	else:
		#Non-OK
		pingstatus = "0"

	return pingstatus
