import random

import cv2
import numpy as np

"""
Canny Edge Detection (Overlap detection)
"""

img = cv2.imread("../../../../res/fuzzy.png", cv2.IMREAD_COLOR)
cv2.imshow("Original", img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3, 3), 0)

thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 205, 1) #  Inversing because the foreground of the image was white and we want to take out the objects which are going to be darker than this color
cv2.imshow("Binary", thresh)

contours, hirearchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(len(contours))

object = np.zeros([img.shape[0], img.shape[1], 3], 'uint8')

for c in contours:

    area = cv2.contourArea(c)
    perimeter = cv2.arcLength(c, True)

    if area > 1000:
        cv2.drawContours(object, [c], -1, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), -1)
        print("Area: {} Perimeter: {}".format(area, perimeter))

cv2.imshow("Contours", object)

cv2.waitKey(0)
cv2.destroyAllWindows()
