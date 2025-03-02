#!/usr/bin/python3.6

# [START speech_transcribe_streaming_mic]
from __future__ import division

import re
import sys
import os
import json
import requests
import threading
import socket
import pyaudio
import wave

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from six.moves import queue
from evdev import InputDevice, categorize, ecodes
from matrix_led import (
    glow_blue,
    green_blink_signal,
    blink_limited_signal,
    blue_white_signal,
    shut_down_signal
)
from bluetooth_connect import connect_bt


# Audio recording parameters
RATE = 48000
CHUNK = int(RATE / 10)  # 100ms
num = 0

# Visual Feedback
LED_THREAD = None


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

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            input_device_index=2,
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
        self.btpause = False
        
    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()
        self._recfile.close()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        if (self.btpause == False):
            self._buff.put(in_data)
            self._recfile.writeframes(in_data)
        return None, pyaudio.paContinue

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
                    
                yield b''.join(data)


def check_internet():
    try:
        host = socket.gethostbyname('www.google.com')
        s = socket.create_connection((host, 80))
        s.close()
        return True
    except:
        pass
    return False


def create_led_threads(target):
    global LED_THREAD
    LED_THREAD = threading.Thread(
        name='LEDEvent', target=target
    )
    LED_THREAD.start()


def fetch_uid():
    with open('/home/pi/uid.txt') as f:
        uid = int(f.read())
    return uid




def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """

    # Display visual response
    num_chars_printed = 0
    for response in responses:
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

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()
            num_chars_printed = len(transcript)
        else:
            print('Final')
            print(transcript + overwrite_chars)

            # Prepare json data as argument for the script
            phrase = transcript + overwrite_chars
            phrase = phrase.strip() if phrase[-1] != '.' else phrase.strip()[:-1]

            # s = json.dump(req.text)
            # open("out.json","w").write(s)


            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                break

            num_chars_printed = 0


def get_text_from_voice():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.

    # Visual feedback on device
    global LED_THREAD
    glow_blue()
    if not check_internet():
        print('No internet connection.\nShutting Down...')
        blink_limited_signal(color='red', count=2)

    language_code = 'en-IN'  # a BCP-47 language tag
    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        enable_automatic_punctuation=True
    )
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=False
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        microphone_requests = (
            types.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )
        responses = client.streaming_recognize(streaming_config, microphone_requests)
        
        # Now, put the transcription responses to use.
        print('printing the response')
        listen_print_loop(responses)
