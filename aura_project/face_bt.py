print('importing...')
import cv2
import numpy as np
import sys
import os
from motor_omni_pwm import write_keypress_fifo
print('imported successfully')
## face cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

vnozone = 20
vtzones = 4

hnozone = 20
hlzones = 5
hmzones = 10
skip_val = 5
## video capture
cap = cv2.VideoCapture(0)
nth = 0
stop_mode = False
flip_im = False
gray_im = False
while(True):
	nth+=1
	# Capture frame-by-frame
	ret, frame = cap.read()
	if nth%skip_val > 0:
		continue
	if flip_im: frame = cv2.flip(frame, 0 )
	if gray_im: gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	else: gray = frame

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	if len(faces) == 0 and not stop_mode:
		write_keypress_fifo(' stop ')
		stop_mode = True
	for (x,y,w,h) in faces[:1]:
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
		face_xmid = x+(w/2)
		face_ymid = y+(h/2)
		twid = frame.shape[1]
		zonewid = twid/hnozone
		lzoneswid = zonewid*hlzones
		rzoneswid = zonewid*(hmzones+hlzones)
		if face_xmid > rzoneswid:
			stop_mode = False
			write_keypress_fifo(' right ')
			print(' right ')
		elif face_xmid < lzoneswid:
			stop_mode = False
			write_keypress_fifo(' left ')
			print(' left ')
		else:
			imh = frame.shape[0]
			zoneheight = imh/vnozone
			topzone = zoneheight * vtzones
			
			if h>100:
				stop_mode = False
				write_keypress_fifo(' back ')
				print(' back ')
			elif h<85:
				stop_mode = False
				write_keypress_fifo(' front ')
				print(' front ')
			elif face_ymid < topzone:
				stop_mode = False
				write_keypress_fifo(' back ')
				print(' back ')
			elif not stop_mode:
				stop_mode = True
				write_keypress_fifo(' stop ')
				print(' stop ')
		print(face_xmid, w,h)
	face_xmid = None
	cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
exit()
