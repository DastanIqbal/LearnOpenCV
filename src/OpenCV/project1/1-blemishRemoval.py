import cv2 as cv
import numpy as np

windowName = "Blemish Removal"

p = 15
best_gradient = 0

im = cv.imread("blemish.png")
cv.namedWindow(windowName)
img_copy = im.copy()
print(f"Shape {img_copy.shape}")


def findNeigbhours(x, y):
    print(f"pointx {x},{y}")
    return [
        # Center Region
        (x - p, x + p, y - p, y + p),
        # Left Region
        (x - p - 2 * p - 1, x - p - 1, y - p, y + p),
        # Top Left Region
        (x - p - 2 * p - 1, x - p - 1, y + p + 1, y + p + 2 * p),
        # Top Region
        (x - p, x + p, y + p, y + p + 2 * p),
        # Top Right Region
        (x + p + 1, x + p + 2 * p + 1, y + p + 1, y + p + 2 * p),
        # Right Region
        (x + p + 1, x + p + 2 * p + 1, y - p, y + p),
        # Bottom Right Region
        (x + p + 1, x + p + 2 * p, y - p - 2 * p, y - p - 1),
        # Bottom Region
        (x - p, x + p, y - p - 2 * p, y - p - 1),
        # Bottom Left Region
        (x - p - 2 * p - 1, x - p - 1, y - p - 2 * p, y - p - 1),
    ]


def findGradientMean(roi):
    print(f"roi {roi}")
    roi = img_copy[roi[0]:roi[1], roi[2]:roi[3]]
    # cv.imshow("Roi", roi)
    sobelX = cv.Sobel(roi, cv.CV_32F, 1, 0, ksize=-1)
    sobelY = cv.Sobel(roi, cv.CV_32F, 0, 1, ksize=-1)
    return np.mean(np.sqrt((np.square(sobelX) + np.square(sobelY))))


def removeBlemish(x, y):
    global img_copy, best_gradient
    neigbhours = findNeigbhours(y, x)
    print(f"Neighbours {neigbhours}")

    l, r, b, t = neigbhours[0]
    best_roi = [l, r, b, t]
    best_gradient = findGradientMean(best_roi)

    for l, r, b, t in neigbhours[1:]:
        gradient = findGradientMean([l, r, b, t])
        print(f"gradient {gradient}")
        if gradient < best_gradient:
            best_gradient = gradient
            best_roi = [l, r, b, t]
            print(f"Minimum gradient is {gradient}")

    if best_roi != neigbhours[0]:
        mask = np.ones(img_copy[best_roi[0]:best_roi[1], best_roi[2]:best_roi[3]].shape, dtype=np.uint8)
        mask = 255 * mask
        img_copy = cv.seamlessClone(
            img_copy[best_roi[0]:best_roi[1], best_roi[2]:best_roi[3]],
            img_copy,
            mask,
            (x, y),
            cv.NORMAL_CLONE
        )
        cv.imshow(windowName, img_copy)


def onMouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        removeBlemish(x, y)


cv.setMouseCallback(windowName, onMouse)

ch = 0
while ch != 27:
    cv.imshow(windowName, img_copy)
    ch = cv.waitKey()

cv.waitKey()
cv.destroyWindow()
