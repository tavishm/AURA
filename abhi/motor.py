# importing
import RPi.GPIO as GPIO
from keypress import get_key
# setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(0, GPIO.OUT)
GPIO.setup(1, GPIO.OUT)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.output(0, False)
GPIO.output(1, False)
GPIO.output(2, False)
GPIO.output(3, False)

while True:
    ss = get_key()
#for backwards
    if ss == 'down':
        print('Moving backward')
        GPIO.output(0, True) #puts the gpio 0 ON
        GPIO.output(1, False) # puts the gpio 1 OFF 
        GPIO.output(2, True) # puts the gpio 2 ON
        GPIO.output(3, False)# puts the gpio 3 OFF
#for front
    elif ss == 'up':
        print('Moving forward')
        GPIO.output(0, False) # puts the gpio 0 OFF
		GPIO.output(1, True) # puts the gpio 1 ON
		GPIO.output(2, False) # puts the gpio 2 OFF
        GPIO.output(3, True) # puts the gpio 3 ON
#for left
    elif ss == 'left':
        print('Taking left')
        GPIO.output(0, True)# puts the gpio 1 ON
        GPIO.output(1, False)# puts the gpio 1 OFF
        GPIO.output(2, False)# puts the gpio 1 OFF
        GPIO.output(3, False)# puts the gpio 1 OFF
#for right
    elif ss == 'right':
        print('Taking right')
        GPIO.output(0, False)# puts the gpio 1 OFF
        GPIO.output(1, False)# puts the gpio 1 OFF
        GPIO.output(2, True)# puts the gpio 1 ON
        GPIO.output(3, False)# puts the gpio 1 OFF
#if any thing else
    else: 
        print('Exiting')
        break


GPIO.cleanup()
