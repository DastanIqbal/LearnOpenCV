import cv2
import numpy as np

DATA_PATH = "/Users/admin/Iqbal/Study/OpenCV/LearnOpenCV/src/res/opencv-courses/"

faceImage = cv2.imread(DATA_PATH + "images/musk.jpg", cv2.IMREAD_COLOR)
faceImage = np.float32(faceImage) / 255
# cv2.imshow("Face", faceImage)

sunglassImage = cv2.imread(DATA_PATH + "images/sunglass.png", -1)
sunglassImage = np.float32(sunglassImage) / 255
# cv2.imshow("Sunglass", sunglassImage)

sunglassImage = cv2.resize(sunglassImage, None, fx=0.5, fy=0.5)

sunglassH, sunglassW, channel = sunglassImage.shape
print(sunglassImage.shape)

sunglassBGR = sunglassImage[:, :, 0:3]
sunglassAlpha = sunglassImage[:, :, 3]

# cv2.imshow("Sunglass BGR", sunglassBGR)
# cv2.imshow("Sunglass Alpha", sunglassAlpha)

topLeft = 130
topRight = 130
bottomLeft = topLeft + sunglassH
bottomRight = topRight + sunglassW

faceWithSunglassNaive = faceImage.copy()

faceWithSunglassNaive[topLeft:bottomLeft, topRight:bottomRight] = sunglassBGR
# cv2.imshow("Face with Sunglass", faceWithSunglassNaive)
faceWithSunglassAirthmetic = faceImage.copy()

eyeRoI = faceWithSunglassAirthmetic[topLeft:bottomLeft, topRight:bottomRight]

sunglassMergedAlpha = cv2.merge((sunglassAlpha, sunglassAlpha, sunglassAlpha))

sunglassMasked = cv2.multiply(sunglassBGR, sunglassMergedAlpha)
eyeMasked = cv2.multiply(eyeRoI, (1 - sunglassMergedAlpha))

eyeRoIFinal = cv2.add(eyeMasked, sunglassMasked)

eyeMasked = cv2.multiply(eyeRoI, (1 + sunglassMasked))


faceWithSunglassAirthmetic[topLeft:bottomLeft, topRight:bottomRight] = eyeRoIFinal
cv2.imshow("Masked Sunglass", faceWithSunglassAirthmetic)

faceWithSunglassAirthmetic[topLeft:bottomLeft, topRight:bottomRight] = eyeMasked
cv2.imshow("Masked Sunglass Eye visibility", faceWithSunglassAirthmetic)

cv2.waitKey()
cv2.destroyAllWindows()
