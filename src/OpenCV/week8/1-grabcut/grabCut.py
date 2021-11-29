# Convention of defining color in opencv is BGR
import cv2 as cv
import numpy as np
import sys

from dataPath import DATA_PATH

LIGHT_GREEN = [128, 255, 128]  # rectangle color
LIGHT_RED = [128, 128, 255]  # PR BG
BLUE = [255, 0, 0]  # rectangle color
RED = [0, 0, 255]  # PR BG
GREEN = [0, 255, 0]  # PR FG
BLACK = [0, 0, 0]  # sure BG
WHITE = [255, 255, 255]  # sure FG

# Creating Dictionary
DRAW_BG = {'color': RED, 'val': 0}
DRAW_FG = {'color': GREEN, 'val': 1}
DRAW_PR_FG = {'color': LIGHT_GREEN, 'val': 3}
DRAW_PR_BG = {'color': LIGHT_RED, 'val': 2}

# Setting up flags
rect = (0, 0, 1, 1)
drawing = False  # flag for drawing curves
rectangle = False  # flag for drawing rect
rect_over = False  # flag to check if rect drawn
rect_or_mask = 100  # flag for selecting rect or mask mode
value = DRAW_FG  # drawing initialized to FG
thickness = 3  # brush thickness
rect_not_done = True


def onmouse(event, x, y, flags, param):
    global img, img2, drawing, value, mask, rectangle, rect, rect_or_mask, ix, iy, rect_over, rect_not_done

    if event == cv.EVENT_LBUTTONDOWN and rect_not_done:
        rectangle = True
        ix, iy = x, y
    elif event == cv.EVENT_MOUSEMOVE:
        if rectangle:
            img = img2.copy()
            cv.rectangle(img, (ix, iy), (x, y), BLUE, 2)
            rect = (min(ix, x), min(iy, y), abs(ix - x), abs(iy - y))
            rect_or_mask = 0

    elif event == cv.EVENT_LBUTTONUP and rect_not_done:
        rectangle = False
        rect_not_done = False
        rect_over = True
        cv.rectangle(img, (ix, iy), (x, y), BLUE, 2)
        rect = (min(ix, x), min(iy, y), abs(ix - x), abs(iy - y))
        rect_or_mask = 0
        print(" Now press the key 'n' a few times until no further change \n")

    if event == cv.EVENT_LBUTTONDOWN:
        if not rect_over:
            print("first draw rectangle \n")
        else:
            drawing = True
            cv.circle(img, (x, y), thickness, value['color'], -1)
            cv.circle(mask, (x, y), thickness, value['val'], -1)

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:
            cv.circle(img, (x, y), thickness, value['color'], -1)
            cv.circle(mask, (x, y), thickness, value['val'], -1)

    elif event == cv.EVENT_LBUTTONUP:
        if drawing:
            drawing = False
            cv.circle(img, (x, y), thickness, value['color'], -1)
            cv.circle(mask, (x, y), thickness, value['val'], -1)


if __name__ == '__main__':
    print(__doc__)

    if len(sys.argv) == 2:
        filename = sys.argv[1]
        print("Loading Image \n")
    else:
        print("No input image given, so loading default image, DATA_PATH + /images/hillary_clinton.jpg")
        print("Correct Usage: python grabCut.py <filename> \n")
        filename = "/Users/admin/Iqbal/Study/OpenCV/LearnOpenCV/" + DATA_PATH + "images/hillary_clinton.jpg"

    print(filename)
    img = cv.imread(filename)
    img2 = img.copy()
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    output = np.zeros(img.shape, np.uint8)

    cv.namedWindow('output')
    cv.namedWindow('input')
    cv.setMouseCallback('input', onmouse)
    cv.moveWindow('input', img.shape[1] + 10, 90)

    print(" Instructions: \n")
    print(" Draw a rectangle around the object using right mouse button \n")

    while True:
        cv.imshow('output', output)
        cv.imshow('input', img)
        k = cv.waitKey(1)

        if k == 27:
            break
        elif k == ord('0'):
            print("Using Red color, > mark background regions with left mouse button \n")
            value = DRAW_BG
        elif k == ord('1'):
            print("Using Green color, > mark foreground regions with left mouse button \n")
            value = DRAW_FG
        elif k == ord('2'):
            print("Using Light Red color, > mark probable background regions with left mouse button \n")
            value = DRAW_PR_BG
        elif k == ord('3'):
            print("Using Light Green color, > mark probable foreground regions with left mouse button \n")
            value = DRAW_PR_FG

        elif k == ord('s'):
            bar = np.zeros((img.shape[0], 5, 3), np.uint8)
            res = np.hstack(img2, bar, img, bar, output)
            cv.imwrite('grabCut-output.png', res)
            print("Result saved as image \n")

        elif k == ord('r'):
            print("resetting \n")
            rect = (0, 0, 1, 1)
            drawing = False
            rectangle = False
            rect_or_mask = 100
            rect_over = False
            rect_not_done = True
            value = DRAW_FG
            img = img2.copy()
            mask = np.zeros(img.shape[:2], dtype=np.uint8)
            output = np.zeros(img.shape, np.uint8)
            print(__doc__)

        elif k == ord('n'):
            print(""" For finer touchups,  mark foreground and background after pressing keys 0-3
            and again press 'n' \n""")

            if rect_or_mask == 0:
                bgdmodel = np.zeros((1, 65), np.float64)
                fgdmodel = np.zeros((1, 65), np.float64)
                cv.grabCut(img2, mask, rect, bgdmodel, fgdmodel, 1, cv.GC_INIT_WITH_RECT)
                rect_or_mask = 1
            elif rect_or_mask == 1:
                bgdmodel = np.zeros((1, 65), np.float64)
                fgdmodel = np.zeros((1, 65), np.float64)
                cv.grabCut(img2, mask, rect, bgdmodel, fgdmodel, 1, cv.GC_INIT_WITH_MASK)

        mask2 = np.where((mask == 1) + (mask == 3), 255, 0).astype('uint8')
        output = cv.bitwise_and(img2, img2, mask=mask2)

    cv.destroyAllWindows()
