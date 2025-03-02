import sys
#sys.path.append('/home/pi/abhi/tavish_gpio_matrix')
#sys.path.append('/home/pi/nlp/')
from wrapper import speak_text
#from function_for_pwm_motor import write_keypress_fifo
from motor_omni_pwm import write_keypress_fifo
import config, re, requests, os
import threading 
from matrix_led import stop_recording_thread, start_recording_thread, change_led_state
import edit_conf_state

save_internet = True

def use_text_data(data, final):
	def speak(intentqq):
				change_led_state(config.LEDStatus.STOP_PROCESSING)
				change_led_state(config.LEDStatus.START_RECORDING)
				config.I_AM_TALKING = True
				if intentqq == "CMDPLAYSONG" or intentqq == "CMDPLAYNEWS":
					config.MUTE_MICROPHONE = False
				print(str(config.MUTE_MICROPHONE)+"\n\n mic state:")
				edit_conf_state.set_state(edit_conf_state.tell_set())
				os.system('omxplayer -o local op.mp3')
				if not intentqq == "CMDPLAYSONG" or intentqq == "CMDPLAYNEWS":
					config.MUTE_MICROPHONE = False
				edit_conf_state.set_state('listening')
				config.I_AM_TALKING = False
				os.system('rm op.mp3*')

	def stop_speak():
		config.MUTE_MICROPHONE = False
		config.I_AM_TALKING = False
		edit_conf_state.set_state('listening')
		os.system('pkill omxplayer')
	def tts(data):
		print(data)
		data = data.replace(' ','+')
		data = data.replace(',','')
		data = data.replace('.','')
		data = data.replace('!','')
		data = data.replace('?','')
		print(data)
		requests.get('http://mankash.co.in/matrix-server-bkd/tts_universal_bt.py?text='+data)
		print('http://mankash.co.in/matrix-server-bkd/tts_universal_bt.py?text='+data)
		os.system('wget http://mankash.co.in/matrix-server-bkd/op_bo.mp3')
		os.system('omxplayer -o local op_bo.mp3')
		os.system('rm op_bo.mp3')
	try:
		### data=data argument in request is having issues on web server and hence sending via params
				if final:
					print('Sentence - ', data)
				else:
					print('Part Of Sentence - ', data)
				f = ['front', 'forward', 'straight', 'up', 'friend','state']
				b = ['back', 'backward','backwards', 'behind', 'sack', 'lack', 'bag', 'hack', 'back', 'mac', 'lac', 'lak', 'rack', 'wreck']
				r = ['right', 'write', 'rite', 'riot', 'fight', 'light', 'might', 'sight', 'height', 'tight', 'white', 'kite', 'knight', 'diet']
				l = ['left', 'theft']
				e = ['exit', 'pause', 'stop', 'spot', 'faught', 'brought']
				au = ['aura', 'aur']
#			   w = ['aura', 'aur', 'or', 'sour', 'lora', 'laura', 'dora', 'kohra']
				data = data['phrase'].lower()
				if not final:
					for el in au:
						if el.lower() in data:
							config.PRE_PHRASE_WAKEWORD_FLAG = True
					for el in f:
						if el.lower() in data:
							print('front')
							write_keypress_fifo(' front ')
							edit_conf_state.set_state('driving')
					for el in b:
						if el.lower() in data:
							print('back')
							write_keypress_fifo(' back ')
							edit_conf_state.set_state('driving')
					for el in r:
						if el.lower() in data:
							print('right')
							write_keypress_fifo(' right ')
							edit_conf_state.set_state('driving')
					for el in l:
						if el.lower() in data:
							print('left')
							write_keypress_fifo(' left ')
							edit_conf_state.set_state('driving')
					for el in e:
						if el.lower() in data:
							if config.I_AM_TALKING:
								stop_speak()
								print('stopped')
							else:
								print('exit')
								write_keypress_fifo(' stop ')
				if final:
					for el in au:
						if el.lower() in data or config.PRE_PHRASE_WAKEWORD_FLAG == True:
							data = re.sub('[^A-Za-z0-9 \+]+', '', data).replace(' ', '+').replace('aura', '')
							if not data == '':
#								data = 'I+heard+nothing+except+my+name'
								print('called me? ')
								config.MUTE_MICROPHONE = True
								change_led_state(config.LEDStatus.STOP_RECORDING)
								change_led_state(config.LEDStatus.START_PROCESSING)
								edit_conf_state.set_state('working')
								if save_internet:
									speak_text(data.replace('+', ' '))
								else:
									requests.get('http://mankash.co.in/matrix-server-bkd/wrapper.py?text='+data)
									print('http://mankash.co.in/matrix-server-bkd/wrapper.py?text='+data)
									os.system('wget http://mankash.co.in/matrix-server-bkd/op.mp3')
								config.SPEAK_THREAD = threading.Thread(name="speakingthread", target=speak,args=(edit_conf_state.tell_set(),))
								config.SPEAK_THREAD.start()
								config.PRE_PHRASE_WAKEWORD_FLAG = False
	except Exception as e:
				config.SimboState = States.ERROR
				change_led_state(LEDStatus.UPDATE_STATUS)
				edit_conf_state.set_state('sleeping')
