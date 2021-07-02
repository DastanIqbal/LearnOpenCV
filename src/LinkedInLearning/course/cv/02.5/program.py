import cv2
import numpy as np

image = cv2.imread("../../../../res/opencv.png", 1)
cv2.imshow("Original", image)

blur = cv2.GaussianBlur(image, (5, 55), 0)
cv2.imshow("Blur", blur)

# Diloation black to white
# Erosiaon white to black

kernel = np.ones((5, 5), 'uint8')

dilate = cv2.dilate(image, kernel, iterations=1)
erod = cv2.erode(image, kernel, iterations=1)

cv2.imshow("Dilate", dilate)
cv2.imshow("Erode", erod)

cv2.waitKey(0)
cv2.destroyAllWindows()
