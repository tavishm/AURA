import time
import zmq # Asynchronous messaging framework

from random import randint
from matrix_io.proto.malos.v1 import driver_pb2 # MATRIX Protocol Buffer driver library
from matrix_io.proto.malos.v1 import io_pb2 # MATRIX Protocol Buffer sensor library

MATRIX_IP = '127.0.0.1'  # Local device ip
EVERLOOP_PORT = 20021  # Driver Base port
LED_COUNT = 18  # Amount of LEDs on MATRIX device
STOP_THREAD = False


def connect_socket():
    context = zmq.Context()  # Define zmq socket
    socket = context.socket(zmq.PUSH)  # Create a Pusher socket
    socket.connect(
        'tcp://{0}:{1}'.format(MATRIX_IP, EVERLOOP_PORT)
    )  # Connect Pusher to configuration socket
    return socket


def glow_led(driver_config_proto, socket, everloop_image):
    driver_config_proto.image.led.extend(everloop_image)  # Store the Everloop image in driver configuration
    socket.send(driver_config_proto.SerializeToString())  # Send driver configuration through ZMQ socket


def blink_limited_signal(color, count):
    """ Glow LEDs """
    global LED_COUNT
    socket = connect_socket()

    for i in range(count * 2):
        driver_config_proto = driver_pb2.DriverConfig()
        image = []
        for led in range(LED_COUNT):
            ledValue = io_pb2.LedValue()
            if i % 2 == 0:
                if color == 'red':
                    ledValue.blue = 0
                    ledValue.red = 255
                    ledValue.green = 0
                elif color == 'green':
                    ledValue.blue = 0
                    ledValue.red = 0
                    ledValue.green = 255
                elif color == 'blue':
                    ledValue.blue = 255
                    ledValue.red = 0
                    ledValue.green = 0
            else:
                ledValue.blue = 0
                ledValue.red = 0
                ledValue.green = 0
            ledValue.white = 0
            image.append(ledValue)
        glow_led(driver_config_proto, socket, image)
        time.sleep(0.7)


def red_blink_signal():
    """ Glow LEDs """
    global LED_COUNT, STOP_THREAD
    socket = connect_socket()

    i = 0
    while not STOP_THREAD:
        driver_config_proto = driver_pb2.DriverConfig()
        image = []
        for led in range(LED_COUNT):
            ledValue = io_pb2.LedValue()
            if i % 2 == 0:
                ledValue.blue = 5
                ledValue.red = 240
                ledValue.green = 10
            else:
                ledValue.blue = 0
                ledValue.red = 0
                ledValue.green = 0
            ledValue.white = 0
            image.append(ledValue)
        i += 1
        glow_led(driver_config_proto, socket, image)
        time.sleep(0.7)


def green_blink_signal():
    """ Glow LEDs """
    global LED_COUNT, STOP_THREAD
    socket = connect_socket()

    i = 0
    while not STOP_THREAD:
        driver_config_proto = driver_pb2.DriverConfig()
        image = []
        for led in range(LED_COUNT):
            ledValue = io_pb2.LedValue()
            if i % 2 == 0:
                ledValue.blue = 10
                ledValue.red = 5
                ledValue.green = 240
            else:
                ledValue.blue = 0
                ledValue.red = 0
                ledValue.green = 0
            ledValue.white = 0
            image.append(ledValue)
        i += 1
        glow_led(driver_config_proto, socket, image)
        time.sleep(0.7)


def blue_circular_signal():
    """ Glow LEDs """
    global LED_COUNT, STOP_THREAD
    socket = connect_socket()

    i = 0
    while not STOP_THREAD:
        driver_config_proto = driver_pb2.DriverConfig()
        image = []
        for led in range(LED_COUNT):
            ledValue = io_pb2.LedValue()
            if((led + i) % LED_COUNT == 0):
                ledValue.blue = 255
                ledValue.red = 0
                ledValue.green = 0
            else:
                ledValue.blue = 0
                ledValue.red = 0
                ledValue.green = 0
            ledValue.white = 0
            image.append(ledValue)
        i += 1
        glow_led(driver_config_proto, socket, image)
        time.sleep(0.03)


def rgb_circular_signal():
    """ Glow LEDs """
    global LED_COUNT, STOP_THREAD
    socket = connect_socket()

    i = 0
    while not STOP_THREAD:
        driver_config_proto = driver_pb2.DriverConfig()  # Create a new driver config
        image = []  # Create an empty Everloop image
        for led in range(LED_COUNT):  # For each device LED
            ledValue = io_pb2.LedValue()  # Set individual LED value
            if((led + i) % LED_COUNT == 0):
                ledValue.blue = i % 151 # randint(0, 50)
                ledValue.red = (i + 1) % 151 # randint(0, 200)
                ledValue.green = (150 - (i + (i + 1))) % 151 # randint(0, 255)
            else:
                ledValue.blue = 0
                ledValue.red = 0
                ledValue.green = 0
            ledValue.white = 0
            image.append(ledValue)
        i += 1
        glow_led(driver_config_proto, socket, image)
        time.sleep(0.03)  # Wait before restarting loop


def glow_blue():
    """ Glow LEDs """
    global LED_COUNT
    socket = connect_socket()
    driver_config_proto = driver_pb2.DriverConfig()
    image = []
    for led in range(LED_COUNT):
        led_value = io_pb2.LedValue()
        led_value.blue = 100
        led_value.green = 0
        led_value.red = 0
        image.append(led_value)
    glow_led(driver_config_proto, socket, image)


def blue_white_signal():
    """ Glow LEDs """
    global LED_COUNT, STOP_THREAD
    socket = connect_socket()

    i = 0
    while not STOP_THREAD:
        driver_config_proto = driver_pb2.DriverConfig()
        image = []
        for led in range(LED_COUNT):
            led_value = io_pb2.LedValue()
            if((led + i) % LED_COUNT == 0):
                led_value.blue = 100
                led_value.green = 100
                led_value.red = 100
            else:
                led_value.blue = 100
                led_value.green = 0
                led_value.red = 0
            image.append(led_value)
        i += 1
        glow_led(driver_config_proto, socket, image)
        time.sleep(0.03)


def shut_down_signal(current_thread):
    """ Glow LEDs """
    global LED_COUNT, STOP_THREAD
    STOP_THREAD = True  # Stop the current threads glowing LEDs
    current_thread.join()  # Wait for thread to finish
    socket = connect_socket()
    driver_config_proto = driver_pb2.DriverConfig()
    image = []
    for led in range(LED_COUNT):
        ledValue = io_pb2.LedValue()
        ledValue.blue = 0
        ledValue.red = 0
        ledValue.green = 0
        ledValue.white = 0
        image.append(ledValue)
    glow_led(driver_config_proto, socket, image)
    STOP_THREAD = False  # Enable new threads to glow LEDs


if __name__ == '__main__':
    try:
        blink_limited_signal(color='green', count=1)
    except KeyboardInterrupt: # Avoid logging Everloop errors on user quiting
        print('Quit.')
