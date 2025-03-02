from matrix_lite import gpio
while True:
		for i in (0,1,2,3):
			gpio.setFunction(i, 'DIGITAL')
			gpio.setMode(i, "output")		
		def movement():
			if motion == 'front':
				print('moving front..')
				gpio.setDigital(0, "ON")
				gpio.setDigital(1, "OFF")
				gpio.setDigital(2, "ON")
				gpio.setDigital(3, "OFF")
			if motion == 'back':
				print('moving back....')
				gpio.setDigital(0, "OFF")
				gpio.setDigital(1, "ON")
				gpio.setDigital(2, "OFF")
				gpio.setDigital(3, "ON")
			if motion == 'right':
				print('moving right...')
				gpio.setDigital(0, "OFF")
				gpio.setDigital(1, "ON")
				gpio.setDigital(2, "OFF")
				gpio.setDigital(3, "OFF")
			if motion == 'left':
				print('moving left....')
				gpio.setDigital(0, "ON")
				gpio.setDigital(1, "OFF")
				gpio.setDigital(2, "ON")
				gpio.setDigital(3, "ON")
			else:
				print('exiting........')
				gpio.setDigital(0, "OFF")
				gpio.setDigital(1, "OFF")
				gpio.setDigital(2, "OFF")
				gpio.setDigital(3, "OFF")
