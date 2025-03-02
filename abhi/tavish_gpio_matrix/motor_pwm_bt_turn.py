from keypress import get_key
from matrix_lite import gpio

for i in (0,1,2,3):
    gpio.setFunction(i, 'DIGITAL')
    gpio.setMode(i, "output")

while True:
    ss = get_key()
    if ss == 'down':
        print('Moving backward')
        gpio.setDigital(0,"ON")
        gpio.setDigital(1,"OFF")
        gpio.setDigital(2,"ON")
        gpio.setDigital(3,"OFF")

    elif ss == 'up':
        print('Moving forward')
        gpio.setDigital(0,"OFF")
        gpio.setDigital(1,"ON")
        gpio.setDigital(2,"OFF")
        gpio.setDigital(3,"ON")

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
        break
gpio.setDigital(0,"OFF")
gpio.setDigital(1,"OFF")
gpio.setDigital(2,"OFF")
gpio.setDigital(3,"OFF")

