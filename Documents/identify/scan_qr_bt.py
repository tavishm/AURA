print('importing...')
import numpy as np
import cv2
from pyzbar.pyzbar import decode
print('imported successfully')

cap = cv2.VideoCapture(0)

while(True):
	ret, frame = cap.read()
#	frame = cv2.flip(frame, 1)
	cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
#	cv2.imsave("horn.png")
	data = decode(frame)
	if not data == []:
		data = list(data)[0][0]
		print('\n\n\n\n\n\nDetecrted QR code, \n\n It is \n\n ',data,'\n\n\n\n\n')
		break
cap.release()
cv2.destroyAllWindows()
exit()
