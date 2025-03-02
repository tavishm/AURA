from matrix_lite import gpio

def move(ss):
	for i in (0,1,2,3):
		gpio.setFunction(i, 'DIGITAL')
		gpio.setMode(i, "output")
	if ss == 'front':
		print('Moving forward')
		gpio.setDigital(0,"OFF")
		gpio.setDigital(1,"ON")
		gpio.setDigital(2,"OFF")
		gpio.setDigital(3,"ON")

	elif ss == 'back':
		print('Moving backward')
		gpio.setDigital(0,"ON")
		gpio.setDigital(1,"OFF")
		gpio.setDigital(2,"ON")
		gpio.setDigital(3,"OFF")

	elif ss == 'right':
		print('Moving right')
		gpio.setDigital(0,"OFF")
		gpio.setDigital(1,"ON")
		gpio.setDigital(2,"OFF")
		gpio.setDigital(3,"OFF")

	elif ss == 'left':
		print('Moving left')
		gpio.setDigital(0,"OFF")
		gpio.setDigital(1,"OFF")
		gpio.setDigital(2,"OFF")
		gpio.setDigital(3,"ON")
	else:
		print('Exiting')
		gpio.setDigital(0,"OFF")
		gpio.setDigital(1,"OFF")
		gpio.setDigital(2,"OFF")
		gpio.setDigital(3,"OFF")

