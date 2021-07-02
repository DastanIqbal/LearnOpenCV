import cv2

"""
Canny Edge Detection (Overlap detection)
"""

img = cv2.imread("../../../../res/tomatoes.jpg", cv2.IMREAD_COLOR)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
res, thresh = cv2.threshold(hsv[:, :, 0], 25, 255, cv2.THRESH_BINARY_INV)
cv2.imshow("Thresh", thresh)

edges = cv2.Canny(img, 100, 70)
cv2.imshow("Canny", edges)

cv2.waitKey(0)
cv2.destroyAllWindows()
