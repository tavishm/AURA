from matrix_lite import gpio

def move(iq, frequency=100, percentage=50):
	for i in (0,1,2,3):
		gpio.setFunction(i, 'PWM')
		gpio.setMode(i, "output")
	if iq == 'front':
		print('Moving forward')
		gpio.setPWM({"pin": 0,"percentage":0,"frequency":frequency})
		gpio.setPWM({"pin": 1,"percentage":percentage,"frequency":frequency})
		gpio.setPWM({"pin": 2,"percentage":0,"frequency":frequency})
		gpio.setPWM({"pin": 3,"percentage":percentage,"frequency":frequency})

	elif iq  == 'back':
		print('Moving backward')
		gpio.setPWM({"pin": 0,"percentage":percentage,"frequency":frequency})
		gpio.setPWM({"pin": 1,"percentage":0,"frequency":frequency})
		gpio.setPWM({"pin": 2,"percentage":percentage,"frequency":frequency})
		gpio.setPWM({"pin": 3,"percentage":0,"frequency":frequency})

	elif iq == 'right':
		print('Moving right')
		gpio.setPWM({"pin": 0,"percentage":0,"frequency":frequency})
		gpio.setPWM({"pin": 1,"percentage":percentage,"frequency":frequency})
		gpio.setPWM({"pin": 2,"percentage":0,"frequency":frequency})
		gpio.setPWM({"pin": 3,"percentage":0,"frequency":frequency})

	elif iq == 'left':
		print('Moving left')
		gpio.setPWM({"pin": 0,"percentage":0,"frequency":frequency})
		gpio.setPWM({"pin": 1,"percentage":0,"frequency":frequency})
		gpio.setPWM({"pin": 2,"percentage":0,"frequency":frequency})
		gpio.setPWM({"pin": 3,"percentage":percentage,"frequency":frequency})
	else:
		print('Exiting')
		gpio.setPWM({"pin": 0,"percentage":0,"frequency":frequency})
		gpio.setPWM({"pin": 1,"percentage":0,"frequency":frequency})
		gpio.setPWM({"pin": 2,"percentage":0,"frequency":frequency})
		gpio.setPWM({"pin": 3,"percentage":0,"frequency":frequency})

