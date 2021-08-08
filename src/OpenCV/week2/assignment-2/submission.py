import cv2

windowName = "Resize Image"

trackbarValue = "Scale"
trackbarScaleValue = 1
scaleFactor = 1
maxScaleUp = 100

trackbarType = "Type: \n 0: Scale Up \n 1: Scale Down"
scaleType = 0
maxType = 1

image = cv2.imread("./images/truth.png")
cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)


def scaleImage(*args):
    global scaleType
    global scaleFactor
    global trackbarScaleValue

    trackbarScaleValue = args[0]

    if scaleType == 0:
        scaleFactor = 1 + trackbarScaleValue / 100.0
    else:
        scaleFactor = 1 - trackbarScaleValue / 100.0

    if scaleFactor == 0:
        scaleFactor = 1
    scaledImage = cv2.resize(image, None, fx=scaleFactor, fy=scaleFactor, interpolation=cv2.INTER_LINEAR)
    cv2.imshow(windowName, scaledImage)


def scaleTypeImage(*args):
    global scaleType
    global scaleFactor
    scaleType = args[0]
    if scaleType == 0:
        scaleFactor = 1 + trackbarScaleValue / 100.0
    else:
        scaleFactor = 1 - trackbarScaleValue / 100.0

    if scaleFactor == 0:
        scaleFactor = 1.0
    scaledImage = cv2.resize(image, None, fx=scaleFactor, fy=scaleFactor, interpolation=cv2.INTER_LINEAR)
    cv2.imshow(windowName, scaledImage)


cv2.createTrackbar(trackbarValue, windowName, scaleFactor, maxScaleUp, scaleImage)
cv2.createTrackbar(trackbarType, windowName, scaleType, maxType, scaleTypeImage)
cv2.imshow(windowName, image)

k = 0
while True:
    if k == 27 or k == ord('q'):
        break
    k = cv2.waitKey(50) & 0xFF

cv2.destroyAllWindows()
