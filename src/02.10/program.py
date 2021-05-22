import random

import cv2
import numpy as np

b = random.randint(0, 255)
g = random.randint(0, 255)
r = random.randint(0, 255)
color = (b, g, r)
radius = 3
pressed = False

canvas = np.ones([500, 500, 3], 'uint8') * 255


def click(event, x, y, flags, param):
    global canvas, pressed
    if event == cv2.EVENT_LBUTTONDOWN:
        pressed = True
        cv2.circle(canvas, (x, y), radius, color, -1)
    if event == cv2.EVENT_LBUTTONUP:
        pressed = False
    if event == cv2.EVENT_MOUSEMOVE and pressed == True:
        cv2.circle(canvas, (x, y), radius, color, -1)


cv2.namedWindow("Canvas")
cv2.setMouseCallback("Canvas", click)

while True:
    cv2.imshow("Canvas", canvas)

    ch = cv2.waitKey(1)
    if ch & 0xFF == ord('q'):
        break
    if ch & 0xFF == ord('c'):
        b = random.randint(0, 255)
        g = random.randint(0, 255)
        r = random.randint(0, 255)
        color = (b, g, r)

cv2.destroyAllWindows()
