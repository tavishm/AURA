print('importing...')
import cv2
import numpy as np
import sys
import os
sys.path.append('../../tavish_gpio_matrix/')
#from function_for_pwm_motor import move
from motor_omni_pwm import write_keypress_fifo
print('imported successfully')
## face cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')


## video capture
cap = cv2.VideoCapture(0)

while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()
#	frame = cv2.flip(frame, 0 )
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = frame[y:y+h, x:x+w]
		face_mid = x+(w/2)
		twid = frame.shape[1]
		nozone = 11
		lzones = 4
		rzones = 4
		mzones = 3
		zonewid = twid/nozone
		lzoneswid = zonewid*lzones
		rzoneswid = zonewid*(mzones+lzones)
		if face_mid > rzoneswid:
			write_keypress_fifo(' right ')
		elif face_mid < lzoneswid:
			write_keypress_fifo(' left ')
		else:
			if h>85:
				write_keypress_fifo(' back ')
			elif h<50:
				write_keypress_fifo(' front ')
			else:
				write_keypress_fifo(' stop ')
		print(face_mid, w,h)
	cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		write_keypress_fifo(' exit ')
		break
	face_mid = None
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
exit()
