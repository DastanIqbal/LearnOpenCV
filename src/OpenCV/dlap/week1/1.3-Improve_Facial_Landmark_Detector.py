import numpy as np
import cv2
import sys
import dlib
from dataPath import MODEL_PATH
from dataPath import DATA_PATH
from renderFace import renderFace

RESIZE_HEIGHT = 480
SKIP_FRAMES = 2
PREDICTOR_PATH = MODEL_PATH + "shape_predictor_68_face_landmarks.dat"

cap = cv2.VideoCapture(0)

if(cap.isOpened() is False):
    print("Unable to connect to camera")
    sys.exit()

fps = 30.0
ret, im = cap.read()

if ret == True:
    height = im.shape[0]
    # calculate resize scale
    RESIZE_SCALE = float(height)/RESIZE_HEIGHT
    size = im.shape[0:2]
else:
    print("Unable to read frame")
    sys.exit()


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)

t = cv2.getTickCount()
count = 0

while True:
    if count == 0:
        t= cv2.getTickCount()

    ret, im = cap.read()
    imDlib = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

    imSmall = cv2.resize(im, None, fx = 1/RESIZE_SCALE, fy = 1/RESIZE_SCALE, interpolation=cv2.INTER_LINEAR)
    imSmallDlib = cv2.cvtColor(imSmall, cv2.COLOR_BGR2RGB)


    # Skip frames

    if(count % SKIP_FRAMES == 0):
        faces = detector(imSmallDlib, 0)

    for face in faces:
        newRect = dlib.rectangle(
            int(face.left() * RESIZE_SCALE),
            int(face.top() * RESIZE_SCALE),
            int(face.right() * RESIZE_SCALE),
            int(face.bottom() * RESIZE_SCALE)
        )

        shape = predictor(imDlib, newRect)
        renderFace(im, shape)

    # Put fps at which we are processinf camera feed on frame
    cv2.putText(im, "{0:.2f}-fps".format(fps), (50, size[0]-50), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 255), 3)
    # Display it all on the screen
    cv2.imshow("Fast Facial Landmark Detection", im)
    # Wait for keypress
    key = cv2.waitKey(1) & 0xFF

    # Stop the program.
    if key == 27:
        sys.exit()
    
    count = count + 1

    if(count == 100):
        t = (cv2.getTickCount() - t)/cv2.getTickFrequency()
        fps = 100.0/t
        count = 0

cv2.destroyAllWindows()
cap.relase()
