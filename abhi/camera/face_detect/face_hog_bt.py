print('importing...')
import cv2
import numpy as np
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
	im = np.float32(gray) / 255
	# Calculate gradient
	gx = cv2.Sobel(im, cv2.CV_32F, 1, 0, ksize=1)
	gy = cv2.Sobel(im, cv2.CV_32F, 0, 1, ksize=1)
	mag, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)
	cv2.imshow('im', mag)
#	plt.show()

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
exit()
