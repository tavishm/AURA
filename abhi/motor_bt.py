import RPi.GPIO as GPIO
import time
from keypress import get_key
GPIO.setmode(GPIO.BOARD)
for i in (11, 13, 19, 21):
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, False)

GPIO.setmode(GPIO.BOARD)
for i in (11, 13, 19, 21):
    GPIO.setup(i, GPIO.OUT)
def reset_io():
    for i in (11, 13, 19, 21):
        GPIO.output(i, False)

reset_io()
val = 50
incr = 50
my_pwmr = GPIO.PWM(11, 10000000)
my_pwml= GPIO.PWM(19, 10000000)

### forward
while True:
    ss = get_key()
    if ss == 'up':
        print('Moving forward')
        GPIO.output(11, False)
        GPIO.output(13, True)
        GPIO.output(19, False)
        GPIO.output(21, True)
    elif ss == 'down':
        print('Moving backward')
        GPIO.output(11, True)
        GPIO.output(13, False)
        GPIO.output(19, True)
        GPIO.output(21, False)
    elif ss == 'left':
        print('Taking left')
        GPIO.output(11, False)
        GPIO.output(13, True)
        GPIO.output(19, False)
        GPIO.output(21, False)
    elif ss == 'right':
        print('Taking right')
        GPIO.output(11, False)
        GPIO.output(13, False)
        GPIO.output(19, False)
        GPIO.output(21, True)
    else: 
        print('Exiting')
        break


GPIO.cleanup()
