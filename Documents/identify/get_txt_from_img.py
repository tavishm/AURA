print('importing...')
import io
import os
import cv2
import threading

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
print('imported successfully')

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate

cap = cv2.VideoCapture(0)

ret, frame = cap.read()
cv2.imwrite('resources/wakeupcat.jpg', frame)
def show(frame):
	cv2.imshow('frame',frame)
	cv2.waitKey()

t = threading.Thread(target=show,args=([frame]))
t.start()
file_name = os.path.abspath('resources/wakeupcat.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

print('Labels:')
for label in labels:
    print(label.description)
