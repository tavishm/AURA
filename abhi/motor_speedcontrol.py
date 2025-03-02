import RPi.GPIO as GPIO
import time
#import keyboard
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
while True:  # making a loop
    c = input('Up (u) | Down (j) | Exit (e): ')
    if c=='u':
        print('pressed up')
        val += incr
        if (val > 100): val = 100
        my_pwmr.start(val)
        my_pwml.start(val)
    elif c=='j':
        print('pressed down')
        val -= incr
        if (val < 0): val = 0
        my_pwmr.start(val)
        my_pwml.start(val)
    elif c=='e':
        print('pressed exit')
        break
        print('Speed: ', val)
    elif c=='r':
        print('pressed right')
        reset_io()
        my_pwmr.stop()
        my_pwml.stop()
        my_pwmr = GPIO.PWM(13, 10000000)
        my_pwml= GPIO.PWM(21, 10000000)
        pwm.start(0)
        pwm.starrt(100)
GPIO.cleanup()
