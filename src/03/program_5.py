import cv2
import numpy as np

"""
Contour Object Detection
Find Area, Perimeter, Center and Curvature
"""

img = cv2.imread("./../res/detect_blob.png", cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
cv2.imshow("Binary", thresh)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
img2 = img.copy()
index = -1
thickness = 4
color = (255, 0, 255)

object = np.zeros([img.shape[0], img.shape[1], 3], 'uint8')

for c in contours:
    cv2.drawContours(object, [c], -1, color, -1)  # -1 fill the contour object with color

    area = cv2.contourArea(c)
    perimeter = cv2.arcLength(c, True)

    M = cv2.moments(c)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    cv2.circle(object, (cx, cy), 4, (0, 0, 255), -1)

    print("Area: {}, permeter: {}".format(area, perimeter))

cv2.imshow("Contours", object)

cv2.waitKey(0)
cv2.destroyAllWindows()
