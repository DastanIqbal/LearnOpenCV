import cv2

img = cv2.imread("./../res/faces.jpeg", cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

eyes_classifier = cv2.CascadeClassifier("haarcascade_eye.xml")

eyes = eyes_classifier.detectMultiScale(gray, scaleFactor=1.20, minNeighbors=20, minSize=(10, 10))
print(len(eyes))

for (x, y, w, h) in eyes:
    cx = (x + x + w) / 2
    cy = (y + y + h) / 2
    cv2.circle(img, (int(cx), int(cy)), int(w / 2), (255, 0, 255), 4)

cv2.imshow("Eyes", img)
cv2.waitKey(0)

cv2.destroyAllWindows()
