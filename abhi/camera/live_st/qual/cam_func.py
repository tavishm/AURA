print('importing...')
import numpy as np
import time
import cv2
print('imported successfully')

def cam_catch(fps=24, qual=(640,460)):
	cap = cv2.VideoCapture(0)

	while True:
		time.sleep(1/(fps+1))
		ret, frame = cap.read()
#		frame = cv2.flip(frame, 0 )
		if not qual==(640,460):
			frame = cv2.resize(frame, qual)
			frame = cv2.resize(frame, (640,460))
		frame = cv2.flip(frame, 1 )
		cv2.imshow('frame',frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()
