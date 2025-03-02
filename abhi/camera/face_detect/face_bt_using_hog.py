import cv2
import numpy as np
gray = cv2.imread('images/face_detect_test.jpeg', 0)
im = np.float32(gray) / 255.0
# Calculate gradient 
gx = cv2.Sobel(im, cv2.CV_32F, 1, 0, ksize=1)
gy = cv2.Sobel(im, cv2.CV_32F, 0, 1, ksize=1)
mag, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)
cv2.imshow('im', mag)
plt.show()
