import picamera 
import time
import time
import os

camera = picamera.PiCamera()
while True:
    if os.path.exists('frames/frame.jpg'): 
        os.remove('frames/frame.jpg')
    camera.capture('frames/frame.jpg')
    time.sleep(2)
    os.system('pkill gpicview')
    viewer =  os.system('xdg-open frames/frame.jpg')
