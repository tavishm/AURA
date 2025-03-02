import RPi.GPIO as GPIO
red_pin = 6
green_pin = 6
blue_pin = 6
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(blue_pin, GPIO.OUT)
GPIO.output(red_pin, False)
GPIO.output(green_pin, False)
GPIO.output(blue_pin, False)
try:
		while True:
				UserInput = input()
				UserInput = str(UserInput)
				if UserInput == "red":
						GPIO.output(red_pin, True)
						GPIO.output(green_pin, False)
						GPIO.output(blue_pin, False)
				elif UserInput == "green":
						GPIO.output(red_pin, False)
						GPIO.output(green_pin, True)
						GPIO.output(blue_pin, False)
				elif UserInput == "blue":
					GPIO.output(red_pin, False)
					GPIO.output(green_pin, False)
					GPIO.output(blue_pin, True)
				else:
					print('Only red, green, and blue are valid colors.')



