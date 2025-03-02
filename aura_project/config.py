import time, enum

MATRIX_IP = '127.0.0.1'  # Local device ip
EVERLOOP_PORT = 20021  # Driver Base port
LED_COUNT = 18  # Amount of LEDs on MATRIX device
BRIGHTNESS = 0.02
StatusLED = (1,0,17,16) #### LED Numbers for status 
RecordingLED = (2,3,4,5,6,7,8,9,10,11,12,13,14,15)  ### LED Numbers used for recording

# Audio recording parameters
RATE = 32000
CHUNK = int(RATE / 10)  # 100ms

# Visual Feedback
RECORDING_LED_THREAD = None
PROCESSING_LED_THREAD = None
SPEAK_THREAD = None

###
MUTE_MICROPHONE = False
STOP_SPEAKING = False
I_AM_TALKING = False
PRE_PHRASE_WAKEWORD_FLAG = False

#### STT
MICROPHONE_STREAM_OBJ = None
STT_THREAD = None
STOP_STT_THREAD = False ### failsafe variable

class States(enum.Enum):
	INACTIVE = 1  #### Inactive mode without errors - Not listening. Waiting for start
	ACTIVE = 2	#### Active mode without errors - Listening to User
	ERROR = 3	 #### Reached error state - Either no internet or Others

### Whenever system comes out of state ensure that SimboState is set to INACTIVE and SimboError is reset

class Errors(enum.Enum):
	NOCONNECTION = 1  #### No internet

class Warnings(enum.Enum):
	NONE = 0
	NOBLUETOOTH = 1   #### Bluetooth device not connected

class ExitCode(enum.Enum):
	SUCCESS = 0   #### success
	FAIL = 1	  #### plain fail

class LEDStatus(enum.Enum):
	INIT = 1
	UPDATE_STATUS = 2
	EXIT = 3
	START_RECORDING = 4
	STOP_RECORDING = 5
	START_PROCESSING = 6
	STOP_PROCESSING = 7

SimboState = States.INACTIVE
SimboError = {}
SimboWarnings = {}

