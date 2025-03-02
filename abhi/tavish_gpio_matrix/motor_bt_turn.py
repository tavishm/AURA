from keypress import get_key
from matrix_lite import gpio
import time

motor_gpio = {}
motor_gpio["FR"] = (0, 1)
motor_gpio["FL"] = (6, 7)
motor_gpio["RR"] = (5, 4)
motor_gpio["RL"] = (3, 2)

for i in range(8):
	gpio.setFunction(i, 'DIGITAL')
	gpio.setMode(i, "output")

def move_mtr(mm, cmd):
	if cmd=="stop":
		gpio.setDigital(motor_gpio[mm][0], "OFF")
		gpio.setDigital(motor_gpio[mm][1], "OFF")
	elif cmd=="forward":
		gpio.setDigital(motor_gpio[mm][0], "ON")
		gpio.setDigital(motor_gpio[mm][1], "OFF")
	elif cmd=="reverse":
		gpio.setDigital(motor_gpio[mm][0], "OFF")
		gpio.setDigital(motor_gpio[mm][1], "ON")

def stop_all():
	move_mtr('FR', 'stop')
	move_mtr('FL', 'stop')
	move_mtr('RR', 'stop')
	move_mtr('RL', 'stop')
	time.sleep(0.5)

def move_all(cmd):
	stop_all()
	move_mtr('FR', cmd)
	move_mtr('FL', cmd)
	move_mtr('RR', cmd)
	move_mtr('RL', cmd)


while True:
	ss = get_key()
	if ss == 'down':
		print('Moving backward')
		move_all("reverse")
	elif ss == 'up':
		print('Moving forward')
		move_all("forward")
	elif ss == 'right':
		print('Moving right')
		stop_all()
		move_mtr("FR", "reverse")
		move_mtr("RR", "reverse")
		move_mtr("FL", "forward")
		move_mtr("RL", "forward")
	elif ss == 'left':
		print('Moving left')
		stop_all()
		move_mtr("FR", "forward")
		move_mtr("RR", "forward")
		move_mtr("FL", "reverse")
		move_mtr("RL", "reverse")
	else:
		print('stopping')
		stop_all()

stop_all()

