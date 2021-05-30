import cv2

img = cv2.imread("./../res/faces.jpeg", cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

faces = face_classifier.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5, minSize=(40, 40))
print(len(faces))

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)

cv2.imshow("Faces", img)
cv2.waitKey(0)

cv2.destroyAllWindows()
