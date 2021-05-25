import cv2

"""
Segmentation Technique
Adaptive Thresholding
"""

img = cv2.imread("./../res/sudoku.png", cv2.IMREAD_GRAYSCALE)
cv2.imshow("Original", img)

# Simple Thresholding
ret, thresh_basic = cv2.threshold(img, 70, 255, cv2.THRESH_BINARY)
cv2.imshow("Basic Binary", thresh_basic)

thresh_adapt = cv2.adaptiveThreshold(
    img,
    255,  # Max value of pixel value
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    115,  # Neighbourhood parameters how far and what is the localization look like
    1  # Mean subtraction of the end result
)
cv2.imshow("Adaptive Threshold", thresh_adapt)

cv2.waitKey(0)
cv2.destroyAllWindows()
