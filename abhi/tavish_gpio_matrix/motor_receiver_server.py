from keypress import get_key
from motor_omni_pwm import mpctrl, start_fifo, write_keypress_fifo, MOTOR_FIFO
import time, threading, os

start_fifo()
mpctrl.init()
tt = threading.Thread(name='motorpwmcontroller', target=mpctrl.run)
tt.start()

FS = 60
TS = 40
print('Running motor server')
while True:
	time.sleep(0.1)
	print('Waiting for command')
	fp = open(MOTOR_FIFO, "r")
	print('Opened FIFo channel')
	ss = fp.readline()
	fp.close()
	if len(ss.strip()) == 0: continue
	print('Received from FIFO:', ss)
	ss = ss.strip().split()[-1]
	print('Command to execute:', ss)
	if ss == 'down' or ss == 'back':
		print('Moving backward')
		mpctrl.set_all_dstate(-FS, -FS, -FS, -FS)
	elif ss == 'up' or ss == 'front':
		print('Moving forward')
		mpctrl.set_all_dstate(FS, FS, FS, FS)
	elif ss == 'right':
		print('Moving right')
		mpctrl.set_all_dstate(-TS, TS, -TS, TS)
	elif ss == 'left':
		print('Moving left')
		mpctrl.set_all_dstate(TS, -TS, TS, -TS)
	elif ss == 'stop':
		print('stopping')
		mpctrl.set_all_dstate(0, 0, 0, 0)
	elif ss == 'exit':
		print('Exiting')
		mpctrl.set_all_dstate(0, 0, 0, 0)
		break

mpctrl.stop()
tt.join()


