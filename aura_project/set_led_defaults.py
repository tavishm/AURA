import config
import time, threading, copy
import zmq # Asynchronous messaging framework

from matrix_io.proto.malos.v1 import driver_pb2 # MATRIX Protocol Buffer driver library
from matrix_io.proto.malos.v1 import io_pb2 # MATRIX Protocol Buffer sensor library

import config
from config import States, Errors, ExitCode, LEDStatus, MUTE_MICROPHONE


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

def adjust_brightness(leds):
	for l in leds:
		(l.red, l.green, l.blue)  = int(l.red*config.BRIGHTNESS), int(l.green*config.BRIGHTNESS), int(l.blue*config.BRIGHTNESS)
	return leds

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

def reset_LED_image():
	global CurrentLEDImage
	CurrentLEDImage=[black_px() for i in range(config.LED_COUNT)]

def set_default_status():
	reset_LED_image()
	simg = [status_green_px(), status_green_px(), status_green_px(), black_px()]
	for i in range(len(config.StatusLED)):
		CurrentLEDImage[config.StatusLED[i]] = simg[i]

	refresh_led_state()

### set default LED status
set_default_status()

