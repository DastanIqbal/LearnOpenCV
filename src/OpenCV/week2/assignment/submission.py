import cv2

start = ()
end = ()

windowName = "Window"


def cropImage(start, end):
    crop = source.copy()
    image = crop[start[1]:end[1], start[0]:end[0]]
    cv2.imwrite("face.png", image)


def drawRectangle(action, x, y, flags, userdata):
    global start, end

    if action == cv2.EVENT_LBUTTONDOWN:
        start = (x, y)
        cv2.circle(source, start, 1, (255, 255, 0), 1, cv2.LINE_AA)

    if action == cv2.EVENT_LBUTTONUP:
        end = (x, y)
        cv2.rectangle(source, start, end, (255, 255, 0), 1, cv2.LINE_AA)
        cropImage(start, end)


source = cv2.imread("./images/sample.jpg", cv2.IMREAD_COLOR)
cv2.imshow(windowName, source)
cv2.namedWindow(windowName)
cv2.setMouseCallback(windowName, drawRectangle)

k = 0
while k != 27:
    cv2.imshow(windowName, source)
    cv2.putText(
        source,
        '''Choose top left corner, and drag,?''',
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )
    k = cv2.waitKey(25) & 0xFF

cv2.destroyAllWindows()
