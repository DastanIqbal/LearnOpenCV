import cv2 as cv
import numpy as np

width = 640
height = 480
windowName = "ChromaKeying"
videoFile = "greenscreen-demo.mp4"

bg = cv.imread('bg.jpg', cv.IMREAD_COLOR)
bg = cv.resize(bg, (width, height))

video = cv.VideoCapture(videoFile)

if not video.isOpened():
    print("Video Not available")
else:
    frame = video.read()
    frameWidth = width  # int(video.get(cv.CAP_PROP_FRAME_WIDTH))
    frameHeight = height  # int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
    bg = cv.resize(bg, dsize=(frameWidth, frameHeight), interpolation=cv.INTER_LINEAR)
    print("Video is available")
    print(f"Frame {frameWidth}x{frameHeight} Background {bg.shape[1]}x{bg.shape[0]}")


def removeChromeKeying(frame):
    global bg
    greenMask = cv.inRange(frame, (0, 100, 0), (100, 255, 100))
    # greenMask = cv.GaussianBlur(greenMask, (3, 3), 10, 10)
    # frame[greenMask != 0] = [0, 0, 0]
    # bg[greenMask == 0] = [0, 0, 0]
    # merge = bg + frame
    # merge = cv.bitwise_and(frame,frame,mask= greenMask)
    return greenMask


def nothing(x):
    pass


cv.namedWindow('HSV')
cv.resizeWindow('HSV', 300, 300)

cv.createTrackbar('L – h', 'HSV', 0, 179, nothing)
cv.createTrackbar('U – h', 'HSV', 179, 179, nothing)

cv.createTrackbar('L – s', 'HSV', 0, 255, nothing)
cv.createTrackbar('U – s', 'HSV', 255, 255, nothing)

cv.createTrackbar('L – v', 'HSV', 0, 255, nothing)
cv.createTrackbar('U – v', 'HSV', 255, 255, nothing)
# cv.createTrackbar('S ROWS', 'panel', 0, 480, nothing)
# cv.createTrackbar('E ROWS', 'panel', 480, 480, nothing)
# cv.createTrackbar('S COL', 'panel', 0, 640, nothing)
# cv.createTrackbar('E COL', 'panel', 640, 640, nothing)
while True:
    isClosed = 0
    video = cv.VideoCapture(videoFile)
    while video.isOpened():
        ret, frame = video.read()
        if ret:
            # frame = removeChromeKeying(frame)
            frame = cv.resize(frame, (width, height))
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            l_h = cv.getTrackbarPos('L – h', 'HSV')
            l_s = cv.getTrackbarPos('L – s', 'HSV')
            l_v = cv.getTrackbarPos('L – v', 'HSV')
            U_h = cv.getTrackbarPos('U – h', 'HSV')
            U_s = cv.getTrackbarPos('U – s', 'HSV')
            U_v = cv.getTrackbarPos('U – v', 'HSV')

            # lower = np.array([l_h, l_s, l_v])
            # upper = np.array([U_h, U_s, U_v])
            # lower = np.array([44, 83, 0])
            # upper = np.array([74, 255, 255])
            lower = np.array([42, 138, 123])
            upper = np.array([179, 255, 255])
            mask = cv.inRange(hsv, lower, upper)
            # mask = cv.morphologyEx(mask, cv.MORPH_OPEN, (3, 3))
            res = cv.bitwise_and(frame, frame, mask=mask)
            f = frame - res
            green_screen = np.where(f == 0, bg, f)
            green_screen = cv.GaussianBlur(green_screen, (5, 5), 0, 0)

            cv.imshow(windowName, frame)
            cv.imshow("Mask", mask)
            # cv.imshow("Res", f)
            cv.imshow("Green Screen", green_screen)

            ch = cv.waitKey(25)
            if ch & 0xFF == ord('q'):
                isClosed = 1
                break
        else:
            break
    if isClosed:
        break

video.release()
cv.destroyAllWindows()
