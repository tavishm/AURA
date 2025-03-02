import RPi.GPIO as GPIO
import time, keyboard
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.output(11, False)
GPIO.output(13, False)
val = 0
my_pwm = GPIO.PWM(11, 100)
while True:  # making a loop
	try:  # used try so that if user pressed other than the given key error will not be shown
		if keyboard.is_pressed(keyboard.KEY_UP):  # if key 'q' is pressed 
			print('pressed up')
			val += 5
			if (val > 100): val = 100
			my_pwm.start(val)
		elif keyboard.is_pressed(keyboard.KEY_DOWN):
			print('pressed down')
			val -= 5
			if (val < 0): val = 0
			my_pwm.start(val)
		elif keyboard.is_pressed('e'):
			print('pressed exit')
			break
	except Exception as e:
		print('Error..', e);
		pass

GPIO.cleanup()
