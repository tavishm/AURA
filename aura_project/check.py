import cv2

import sys, os, time
import numpy as np


window_name = 'ffname'

img = cv2.imread('gifs-500/sleeping.jpg', cv2.IMREAD_COLOR)
#cv2.namedWindow(window_name, flags=cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.imshow(window_name, img)
cv2.moveWindow(window_name,300,300)
cv2.waitKey()

