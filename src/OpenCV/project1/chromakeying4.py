"""
Tolerance and Blur is good
"""
import cv2
import matplotlib
import numpy as np

# matplotlib.rcParams['figure.figsize'] = (5.0, 5.0)
matplotlib.rcParams['image.cmap'] = 'gray'

color = []
lower = np.array([0, 100, 0])
upper_default = np.array([29, 255, 69])  # np.array([0,0,0])
upper_new = np.copy(upper_default)
no_of_blurs = 0
no_of_blurs_new = 0
Max = 255
w, h = 4, 4
lbuttondown = False


def SelectColor(action, x, y, flags, userdata):
    global color, frame, lbuttondown
    if action == cv2.EVENT_LBUTTONDOWN:
        lbuttondown = True
        color = frame[y, x]
        print("color selected:", color)
        # frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),1)
        roi = frame[y:y + h, x:x + w]
        avg_roi_row = np.average(roi, axis=0)
        avg_roi = np.average(avg_roi_row, axis=0)
        print("avg_roi:", np.uint8(avg_roi))
        avg_roi = np.uint8(avg_roi)

        upper_default[0] = avg_roi[0] + 10
        upper_default[1] = avg_roi[1]
        upper_default[2] = avg_roi[2] + 10
        print("upper_default", upper_default)


def Tolerance(*args):
    global upper_new
    upper_new = upper_default + args[0]
    upper_new = np.clip(upper_new, 0, 255)
    print("upper_new:", upper_new)


def Blurring(*args):
    global no_of_blurs, no_of_blurs_new
    no_of_blurs_new = no_of_blurs + args[0]
    print("args:", args[0])


background_org = cv2.imread("space.jpeg")
cap = cv2.VideoCapture("greenscreen-asteroid.mp4")
# cap = cv2.VideoCapture("greenscreen-demo.mp4")

if not cap.isOpened():
    print("Error opening video stream or file")

cv2.namedWindow("Window")
cv2.setMouseCallback("Window", SelectColor)
cv2.createTrackbar("Tolerance", "Window", 0, 255, Tolerance)
cv2.createTrackbar("Blur", "Window", 0, 10, Blurring)

# Default resolutions of the frame are obtained.
# Convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# outmp4 = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'XVID'), 10, (frame_width, frame_height))

k = 0
while k != 27:

    if not lbuttondown:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 1)

    background_new = np.copy(background_org)

    ret, frame = cap.read()

    if ret:
        frame_copy = frame.copy()

        if not lbuttondown:
            cv2.imshow('Window', frame)
        else:
            mask = cv2.inRange(frame_copy, lower, upper_new)

            for i in range(no_of_blurs_new):
                mask = cv2.GaussianBlur(mask, (3, 3), 0, 0)

            frame_copy[mask != 0] = [0, 0, 0]

            background_new = cv2.resize(background_new, (frame.shape[1], frame.shape[0]))
            background_new[mask == 0] = [0, 0, 0]

            final = np.add(frame_copy, background_new)

            cv2.imshow('Window', final)

            # outmp4.write(final)

    else:
        print("cap.read failed")
        break

    # Press esc on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
# outmp4.release()
