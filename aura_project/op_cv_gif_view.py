import cv2
import numpy as np
import sys
import os
import threading
import time

display_fifo = 'DISPLAY_FIFO_DONT_TOUCH'
#new_el = True
#stopped=True
filen="sleeping.gif"
cha = False
no_display = False

def start_fifo():
	if not os.path.exists(display_fifo):
		os.mkfifo(display_fifo)
	os.chmod(display_fifo, 438)

def write_in_fifo(emo):
	f = open(display_fifo, "w")
	f.write(emo)
	f.close()

def main_logic():
	global filen
	global cha
	t = threading.Thread(target=show_gif)
	t.start()
	print('waiting')
	while True:
		fp = open(display_fifo, "r")
		ss = fp.readline()
		fp.close()
		ss = ss.replace('\n', '')
		ss = ss.replace(' ', '_')
		print(ss)
		if no_display:
			continue
		if not ss=="":
			filen=ss+'.gif'
			cha = True
# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
def show_gif():
	global filen
	global cha
	if no_display:
		return
	window_name = 'ffname'
	img = np.zeros(shape=(500,500,3)).astype('uint8')
	cv2.imshow(window_name, img)
	cv2.namedWindow(window_name,cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
	cv2.moveWindow(window_name, 390, 110)
	cv2.waitKey(1)
	while True:
		print(filen)
		cap = cv2.VideoCapture('gifs-500/'+filen)
 
		# Read until video is completed
		while(cap.isOpened()):
			if cha==True:
				cha=False
				break
			# Capture frame-by-frame
			ret, frame = cap.read()
			if ret == True:
				# Display the resulting frame
				cv2.imshow(window_name,frame)
		 
				# Press Q on keyboard to	exit
				if cv2.waitKey(25) & 0xFF == ord('q'):
					break
		 
			# Break the loop
			else: 
				break
	 
		# When everything done, release the video capture object
		cap.release()
	# Closes all the frames
	cv2.destroyAllWindows()
