from keypress import get_key
from motor_omni_pwm import write_keypress_fifo
### motor_receiver_server can take down, up, right, left, stop, exit. All other will be ignored
while True:
	ss = get_key()
	#ss = input().rstrip()
	if ss == 'down' or ss == 'up' or ss == 'right' or ss == 'left' or ss == 'stop' or ss == 'exit':
		print('Sending valid command:', ss)
		write_keypress_fifo(' '+ss+' ')
	else:
		print('### Unknown command:', ss)
		print('stopping')
		break


