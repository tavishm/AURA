from keypress import get_key
from matrix_lite import gpio

for i in (11,13, 19, 21):
    gpio.setFunction(i, 'DIGITAL')
    gpio.setMode(i, "output")

while True:
    ss = get_key()
    if ss == 'down':
        print('Moving backward')
        gpio.setDigital(1,"ON")
        gpio.setDigital(1,"OFF")
        gpio.setDigital(1,"ON")
        gpio.setDigital(1,"OFF")

    if ss == 'up':
        print('Moving forward')
        gpio.setDigital(1,"OFF")
        gpio.setDigital(1,"ON")
        gpio.setDigital(1,"OFF")
        gpio.setDigital(1,"ON")

    if ss == 'left':
        print('Moving left')
        gpio.setDigital(1,"ON")
        gpio.setDigital(1,"OFF")
        gpio.setDigital(1,"OFF")
        gpio.setDigital(1,"OFF")

    if ss == 'right':
        print('Moving right')
        gpio.setDigital(1,"OFF")
        gpio.setDigital(1,"OFF")
        gpio.setDigital(1,"ON")
        gpio.setDigital(1,"OFF")
    else:
        print('Exiting')
        break
