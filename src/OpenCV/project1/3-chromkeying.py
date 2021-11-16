# Enter your code here
import cv2 as cv
import numpy as np

width = 1280
height = 720
windowName = "ChromaKeying"
videoFile = "greenscreen-asteroid.mp4"

tolerance = 0
softness = 0
defringe = 50
isColorPicked = False
hsvColorValue = []


def fixSize(frame):
    return cv.resize(frame, dsize=(width, height), interpolation=cv.INTER_LINEAR)


bg = cv.imread('bg.jpg', cv.IMREAD_COLOR)
bg = fixSize(bg)

video = cv.VideoCapture(videoFile)

if not video.isOpened():
    print("Video Not available")
else:
    ret, frame = video.read()
    frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # frameWidth = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
    # frameHeight = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
    bg = fixSize(bg)
    frameHSV = fixSize(frameHSV)
    print("Video is available")
    # print(f"Frame {frameWidth}x{frameHeight} Background {bg.shape[1]}x{bg.shape[0]}")


def pickColor(action, x, y, flags, userdata):
    global isColorPicked
    global hsvColorValue
    if action == cv.EVENT_LBUTTONDOWN and isColorPicked == False:
        isColorPicked = True
        hsvColorValue = tuple(frameHSV[y, x, :])
        showFrame()
        print(f"PickedColor {hsvColorValue}")


def getTolerance(*args):
    global tolerance
    tolerance = cv.getTrackbarPos("Tolerance", windowName)
    showFrame()


def getSoftness(*args):
    global softness
    softness = cv.getTrackbarPos('Softness', windowName)
    showFrame()


def getDefringe(*args):
    global defringe
    defringe = cv.getTrackbarPos("Defringe", windowName)
    defringe = 2 * defringe - 100  # -100 to 100
    showFrame()


def showFrame():
    if isColorPicked:
        cv.imshow(windowName, processChromeKeying())


def processChromeKeying():
    global bg
    global tolerance
    global softness
    global defringe
    global frame
    global frameHSV
    global hsvColorValue

    # Step : Adjust Green Channel Defringe
    B, G, R = cv.split(frame)
    gMod = np.uint8(np.clip(np.int32(G) + np.ones_like(G, dtype="int32") * defringe, 0, 255))
    frameMod = cv.merge((B, gMod, R))

    # Step : find color range HSV Channel
    frameModHSV = cv.cvtColor(frameMod, cv.COLOR_BGR2HSV)

    H, S, V = cv.split(frameHSV)
    hMod, sMod, vMod = cv.split(frameModHSV)

    # Step : Adjust tolerance level in HSV
    lowerH = np.array(np.clip(hsvColorValue[0] - tolerance, 0, 180))
    upperH = np.array(np.clip(hsvColorValue[0] + tolerance, 0, 180))

    # Step : Create Mask
    mask = cv.inRange(hMod, lowerH, upperH)
    mask = 255 - mask

    # Step : Adjust Softness level, Gaussian Blur
    if softness == 0:
        maskBlur = mask
    else:
        maskBlur = cv.GaussianBlur(mask, (2 * softness + 1, 2 * softness + 1), 0, 0)
        maskBlur = np.uint8(np.round((maskBlur / 255.0) * (mask * 255.0) * 255))

    # Step : Apply Mask on Value Channel
    v = np.uint8(np.round((V / 255.0) * (maskBlur / 255.0) * 255))
    softFrame = cv.merge((H, S, v))
    softFrame = cv.cvtColor(softFrame, cv.COLOR_HSV2BGR)

    # Step : Crate Mask
    maskInv = np.ones_like(bg)
    maskInv[:, :, 0] = 255 - mask
    maskInv[:, :, 1] = 255 - mask
    maskInv[:, :, 2] = 255 - mask

    # Step : Apply Mask on Background
    bgFrame = np.uint8(np.round((bg / 255.0) * (maskInv / 255.0) * 255))

    # Step : Combine Frame and Background
    bgFrame = cv.add(softFrame, bgFrame)

    return bgFrame


cv.namedWindow(windowName)
cv.setMouseCallback(windowName, pickColor)
cv.createTrackbar("Tolerance", windowName, 0, 100, getTolerance)
cv.createTrackbar("Softness", windowName, 0, 100, getSoftness)
cv.createTrackbar("Defringe", windowName, 50, 100, getDefringe)

while True and video.isOpened():
    isClosed = 0
    video = cv.VideoCapture(videoFile)
    while video.isOpened():
        ret, frame = video.read()
        if ret:
            frame = fixSize(frame)
            frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            if isColorPicked:
                cv.imshow(windowName, processChromeKeying())
            else:
                cv.imshow(windowName, frame)
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
