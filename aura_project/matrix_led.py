import time, threading, copy
import zmq # Asynchronous messaging framework

from matrix_io.proto.malos.v1 import driver_pb2 # MATRIX Protocol Buffer driver library
from matrix_io.proto.malos.v1 import io_pb2 # MATRIX Protocol Buffer sensor library

import config
from config import States, Errors, ExitCode, LEDStatus, MUTE_MICROPHONE

STOP_RECORDING_LED_THREAD = False
STOP_PROCESSING_LED_THREAD = False

CurrentLEDImage = None

def connect_socket():
	context = zmq.Context()  # Define zmq socket
	socket = context.socket(zmq.PUSH)  # Create a Pusher socket
	socket.connect(
		'tcp://{0}:{1}'.format(config.MATRIX_IP, config.EVERLOOP_PORT)
	)  # Connect Pusher to configuration socket
	return socket


def refresh_led_state():
	global CurrentLEDImage
	socket = connect_socket()
	driver_config_proto = driver_pb2.DriverConfig()
	driver_config_proto.image.led.extend(adjust_brightness(copy.deepcopy(CurrentLEDImage)))  # Store the Everloop image in driver configuration
	socket.send(driver_config_proto.SerializeToString())  # Send driver configuration through ZMQ socket

def reset_LED_image():
	global CurrentLEDImage
	CurrentLEDImage=[black_px() for i in range(config.LED_COUNT)]

def adjust_brightness(leds):
	for l in leds:
		(l.red, l.green, l.blue)  = int(l.red*config.BRIGHTNESS), int(l.green*config.BRIGHTNESS), int(l.blue*config.BRIGHTNESS)
	return leds

def processing_px():
	l = io_pb2.LedValue()
	(l.red, l.green, l.blue)  = 255,0,255
	return l

def recording_px():
	l = io_pb2.LedValue()
	(l.red, l.green, l.blue)  = 0,0,255
	return l

def status_green_px():
	l = io_pb2.LedValue()
	(l.red, l.green, l.blue)  = 0,255,0
	return l

def status_red_px():
	l = io_pb2.LedValue()
	(l.red, l.green, l.blue)  = 255,0,0
	return l

def black_px():
	l = io_pb2.LedValue()
	(l.red, l.green, l.blue)  = 0,0,0
	return l

def init_led_state():
	reset_LED_image()
	refresh_led_state()

def update_status_signal():
	global CurrentLEDImage
	simg = []
	### ACTIVE OR INACTIVE: 0,G,G,0
	if (config.SimboState==States.ACTIVE or config.SimboState==States.INACTIVE):
		simg = [black_px(), status_green_px(), status_green_px(), black_px()]
	### ERROR-NOCONNECTION: 0,R,R,0
	if (config.SimboState==States.ERROR and Errors.NOCONNECTION in config.SimboError):
		simg = [black_px(), status_red_px(), status_red_px(), black_px()]

	for i in range(len(config.StatusLED)):
		CurrentLEDImage[config.StatusLED[i]] = simg[i]

def update_recording_signal(nth_led=0, reset=False):
	global CurrentLEDImage
	if reset:
		for i in config.RecordingLED:
			CurrentLEDImage[i] = black_px()
	else:
		for i in range(nth_led):
			CurrentLEDImage[ config.RecordingLED[i] ] = recording_px()
		for i in range(nth_led, len(config.RecordingLED)):
			CurrentLEDImage[ config.RecordingLED[i] ] = black_px()

def recording_trail_loop():
	""" Glow LEDs """
	global STOP_RECORDING_LED_THREAD

	led_times = (0.1, 0.2, 0.3, 0.42, 0.65, 1, 1.5, 2.5, 4, 6, 8, 10, 15, 20) 
	next_led_on = 0
	time_elapsed=0
	while not STOP_RECORDING_LED_THREAD:
		if next_led_on < len(led_times) and time_elapsed >= led_times[next_led_on]:
			update_recording_signal(nth_led=next_led_on+1)
			refresh_led_state()
			next_led_on += 1
		time.sleep(0.03)
		time_elapsed=time_elapsed+0.03

def update__signal(nth_led=0, reset=False):
	global CurrentLEDImage
	if reset:
		for i in config.RecordingLED:
			CurrentLEDImage[i] = black_px()
	else:
		for i in range(nth_led):
			CurrentLEDImage[ config.RecordingLED[i] ] = recording_px()
		for i in range(nth_led, len(config.RecordingLED)):
			CurrentLEDImage[ config.RecordingLED[i] ] = black_px()

def stop_recording_thread():
	global STOP_RECORDING_LED_THREAD
	if config.RECORDING_LED_THREAD != None:
		STOP_RECORDING_LED_THREAD = True
		if config.RECORDING_LED_THREAD.is_alive(): config.RECORDING_LED_THREAD.join()
		STOP_RECORDING_LED_THREAD = False  #### reset this to ensure that thread keep running if started again
		update_recording_signal(reset=True)
		refresh_led_state() ### refresh led image
		config.RECORDING_LED_THREAD = None

def start_recording_thread():
	global STOP_RECORDING_LED_THREAD
	stop_recording_thread()
	if config.RECORDING_LED_THREAD == None:
		### the below lines are done in if loop function stop_recording_thread
		STOP_RECORDING_LED_THREAD = False  #### reset this to ensure that thread keep running
		update_recording_signal(reset=True)
		refresh_led_state() ### refresh led image
	config.RECORDING_LED_THREAD = threading.Thread(name='LEDEvent', target=recording_trail_loop)
	config.RECORDING_LED_THREAD.start()

def processing_trail_loop():
	""" Glow LEDs """
	global STOP_PROCESSING_LED_THREAD

	next_led_on = 0
	time_elapsed=0
	nth = 0
	adder=1
	p = 0
	cflag = True
	while not STOP_PROCESSING_LED_THREAD:
		for i in config.RecordingLED: CurrentLEDImage[i] = black_px()
		for i in range(nth, nth+3):
			CurrentLEDImage[config.RecordingLED[i]] = processing_px()
		nth+=adder
		if nth>=len(config.RecordingLED)-3: adder=-1
		if nth==0: adder=1
		if nth==11 or nth == 0:cflag=not cflag
		if p>=6 and cflag==True:
			p-=1
		elif p>=6 and cflag==False:
			p+=1
		elif p<=6 and cflag==True:
			p+=1
		elif p<=6 and cflag==False:
			p-=1

		refresh_led_state()
		time.sleep(0.001*p*2)

def stop_processing_thread():
	global STOP_PROCESSING_LED_THREAD
	if config.PROCESSING_LED_THREAD != None:
		STOP_PROCESSING_LED_THREAD = True
		if config.PROCESSING_LED_THREAD.is_alive(): config.PROCESSING_LED_THREAD.join()
		STOP_PROCESSING_LED_THREAD = False  #### reset this to ensure that thread keep running if started again
		update_recording_signal(reset=True)
		refresh_led_state() ### refresh led image
		config.PROCESSING_LED_THREAD = None

def start_processing_thread():
	global STOP_PROCESSING_LED_THREAD
	stop_processing_thread()
	if config.PROCESSING_LED_THREAD == None:
		### the below lines are done in if loop function stop_processing_thread
		STOP_PROCESSING_LED_THREAD = False  #### reset this to ensure that thread keep running
		update_recording_signal(reset=True)
		refresh_led_state() ### refresh led image
	config.PROCESSING_LED_THREAD = threading.Thread(name='LEDEvent', target=processing_trail_loop)
	config.PROCESSING_LED_THREAD.start()

def change_led_state(state):
	if state==LEDStatus.INIT:
		reset_LED_image()
	if state==LEDStatus.UPDATE_STATUS:
		update_recording_signal(reset=True)
		update_status_signal()
	if state==LEDStatus.EXIT:
		reset_LED_image()
	if state==LEDStatus.START_RECORDING:
		reset_LED_image()
		update_status_signal()
		start_recording_thread()
	if state==LEDStatus.STOP_RECORDING:
		stop_recording_thread()
		update_status_signal()
	if state==LEDStatus.START_PROCESSING:
		reset_LED_image()
		update_status_signal()
		start_processing_thread()
	if state==LEDStatus.STOP_PROCESSING:
		stop_processing_thread()
		update_status_signal()

	refresh_led_state()

	

