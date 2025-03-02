from __future__ import division

import re, sys, os, json, time, requests, threading, socket, pyaudio, wave

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from six.moves import queue
from matrix_led import change_led_state
import config
from config import States, Errors, ExitCode, LEDStatus
import use_text
import signal
import edit_conf_state


class MicrophoneStream(object):
	"""Opens a recording stream as a generator yielding the audio chunks."""
	def __init__(self, rate, chunk):
		self._rate = rate
		self._chunk = chunk
		
		# Create a thread-safe buffer of audio data
		self._buff = queue.Queue()
		self.closed = True
		self._recfile = wave.open("audio_record.wav","w")
		self._recfile.setparams((1, 2, 48000, self._chunk, 'NONE', "not compressed"))

	def find_matrix_mic_device_index(self):
		### useful function when matrix mic is not default mic
		p = self._audio_interface
		numdevices = p.get_device_count()
		for i in range(0, numdevices):
			if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
				dn = p.get_device_info_by_host_api_device_index(0, i).get('name')
				if ('matrixio' in dn.lower()):
					return i
		return None

	def __enter__(self):
		self._audio_interface = pyaudio.PyAudio()
		device_index = self.find_matrix_mic_device_index()
		if device_index == None:
			config.logw('\n####ERROR: Unable to fetch matrix mic. using default. May not work.')
			device_index = self._audio_interface.get_default_input_device_info().get('index')
		self._audio_stream = self._audio_interface.open(
			format=pyaudio.paInt16,
			input_device_index=device_index,
			# The API currently only supports 1-channel (mono) audio
			# https://goo.gl/z757pE
			channels=1, rate=self._rate,
			input=True, frames_per_buffer=self._chunk,
			# Run the audio stream asynchronously to fill the buffer object.
			# This is necessary so that the input device's buffer doesn't
			# overflow while the calling thread makes network requests, etc.
			stream_callback=self._fill_buffer,
		)
		self.closed = False
		self.stop = True
		config.STOP_STT_THREAD = False
		
		return self

	def __exit__(self, type, value, traceback):
		self.close_stream()

	def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
		"""Continuously collect data from the audio stream, into the buffer."""
		if (config.STOP_STT_THREAD == False):
			self._buff.put(in_data)
			self._recfile.writeframes(in_data)
		return None, pyaudio.paContinue

	def close_stream(self):
		self._audio_stream.stop_stream()
		self._audio_stream.close()
		self.closed = True
		# Signal the generator to terminate so that the client's
		# streaming_recognize method will not block the process termination.
		self._buff.put(None)
		self._audio_interface.terminate()
		self._recfile.close()
		config.MICROPHONE_STREAM_OBJ = None

	def generator(self):
		while not self.closed:

			# Use a blocking get() to ensure there's at least one chunk of
			# data, and stop iteration if the chunk is None, indicating the
			# end of the audio stream.
				chunk = self._buff.get()
				if chunk is None:
					return
				data = [chunk]
				
				# Now consume whatever other data's still buffered.
				while True:
					try:
						chunk = self._buff.get(block=False)
						if chunk is None:
							return
						data.append(chunk)
					except queue.Empty:
						break
					
				if config.MUTE_MICROPHONE == True:
					yield b''.join([])
				else:
					yield b''.join(data)


	
def listen_print_loop(responses):
	print('It is Coming')
	# Display visual response
	num_chars_printed = 0
	for response in responses:
		if config.STOP_STT_THREAD == True: 
			### TODO: dangerous as  google thing will be charged heaving.. show visual panic signal
			print('STOP STT THREAD SIGNAL Received. Not processing response')
			continue
		if not response.results:
			continue

		# The `results` list is consecutive. For streaming, we only care about
		# the first result being considered, since once it's `is_final`, it
		# moves on to considering the next utterance.
		result = response.results[0]
		if not result.alternatives:
			continue

		# Display the transcription of the top alternative.
		transcript = result.alternatives[0].transcript

		# Display interim results, but with a carriage return at the end of the
		# line, so subsequent lines will overwrite them.
		#
		# If the previous result was longer than this one, we need to print
		# some extra spaces to overwrite the previous result
		overwrite_chars = ' ' * (num_chars_printed - len(transcript))

		sys.stdout.write(transcript + overwrite_chars + '\r')
		sys.stdout.flush()
		num_chars_printed = len(transcript)
		phrase = transcript + overwrite_chars
		phrase = phrase.strip() if phrase[-1] != '.' else phrase.strip()[:-1]
		data = { 'phrase': phrase }
		t = threading.Thread(name='url_req_sent', target=use_text.use_text_data, args=(data,result.is_final))
		t.start()
		t.join()
		print('DONE-1')
		# Exit recognition if any of the transcribed phrases could be
		# one of our keywords.
		if re.search(r'\b(exit|quit)\b', transcript, re.I):
			change_led_state(LEDStatus.STOP_RECORDING)
			edit_conf_state.set_state('sleeping')
			print('Exiting..')
			reset_stt_thread_vars()
			sys.exit(ExitCode.SUCCESS)
			break
			num_chars_printed = 0
		change_led_state(LEDStatus.START_RECORDING)
		edit_conf_state.set_state('listening')
		
		print('DONE-2')
	print('\nWaiting for input...')


def get_text_from_voice():
	# See http://g.co/cloud/speech/docs/languages
	# for a list of supported languages.
	print("I am in get_text_from_voice");

	if Errors.NOCONNECTION in config.SimboError:
		print('No internet connection.\nExiting speech capture thread...')
		change_led_state(LEDStatus.STOP_RECORDING)
		edit_conf_state.set_state('sleeping')
		reset_stt_thread_vars()
		sys.exit(ExitCode.SUCCESS)
	
	# Metadata
	metadata = {"microphone_distance":"MIDFIELD", "interaction_type":"VOICE_COMMAND", "original_media_type":"AUDIO", "recording_device_type":"OTHER_INDOOR_DEVICE", "audio_topic":"Aura, how are you?"}
	language_code = 'en-IN'  # a BCP-47 language tag
	client = speech.SpeechClient()
	grconfig = types.RecognitionConfig(
		encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
		sample_rate_hertz=config.RATE,
		language_code=language_code,
		enable_automatic_punctuation=False,
		speech_contexts=[speech.types.SpeechContext(
   		phrases=['move left', 'aura', 'aura, what are you doing?', 'stop', 'go right', 'front', 'back', 'aura, play me the news', 'aura, play me a good song', 'aura, I want to listen you sing', 'aura, I am feeling bored'])],
		max_alternatives=30,
		model='command_and_search',
		metadata=metadata
	)
	streaming_config = types.StreamingRecognitionConfig(
		config=grconfig,
		interim_results=True,
		single_utterance=False
	)

	with MicrophoneStream(config.RATE, config.CHUNK) as stream:
		config.MICROPHONE_STREAM_OBJ = stream
		audio_generator = stream.generator()
		#### microphone_requests is a generator object class 
		#### (kind of iterator class which will produce next on demand)
		microphone_requests = (
			types.StreamingRecognizeRequest(audio_content=content)
			for content in audio_generator
		)
		#### responses is an iterator or cursor (like mysql) which gives data as needed
		#### in nutshell: microphone produces serial data which is streamed to google which again produces serial data
		responses = client.streaming_recognize(streaming_config, microphone_requests)
		
		# Now, put the transcription responses to use.
		change_led_state(LEDStatus.START_RECORDING)
		edit_conf_state.set_state('listening')
		print('\nWaiting for input...')
		try:
			listen_print_loop(responses)
		except:
			sys.exit(ExitCode.FAIL)

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    stop_stt_thread()
    exit()

def reset_stt_thread_vars():
	config.STT_THREAD = None
	config.MICROPHONE_STREAM_OBJ = None
	config.STOP_STT_THREAD = False

def stop_stt_thread():
	if config.STT_THREAD != None:
		config.STOP_STT_THREAD = True
		if config.MICROPHONE_STREAM_OBJ!=None: config.MICROPHONE_STREAM_OBJ.close_stream()
		if config.STT_THREAD.is_alive(): config.STT_THREAD.join()
		config.STOP_STT_THREAD = False  #### reset this for future new threads
		config.STT_THREAD = None
	change_led_state(LEDStatus.STOP_RECORDING)
	edit_conf_state.set_state('sleeping')
	

def start_stt_thread():
	print("I am in start_stt_thread");
	stop_stt_thread()
	config.STOP_STT_THREAD = False  #### reset at start of the thread
	config.STT_THREAD = threading.Thread(name='STTEvent', target=get_text_from_voice)
	config.STT_THREAD.start()

signal.signal(signal.SIGINT, signal_handler)
forever = threading.Event()
sst_thread = threading.Thread(name='STTEvent', target=get_text_from_voice)
sst_thread.start()

